import pygame

from map_loader import MapLoader
from camera import Camera
from audio_manager import AudioManager
from player import Player
from chicken import Chicken
from cow import Cow
from menu_bar import MenuBar
from inventory import Inventory
from plant import PlantSystem
from planting import PlantingSystem
from coin import Coin
from sell_box import SellBox
from enemy import spawn_enemy_around_plants
from level_system import LevelSystem
from unlock_area import UnlockAreaSystem
from level_progress import LevelProgressSystem


class GameController:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.FPS = 60

        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Little Farm Friends")

        self.clock = pygame.time.Clock()
        self.running = True

        self.audio = AudioManager()
        self.audio.play_background(volume=0.5)

        self.game_map = MapLoader(
            "Tileset/tile/Tiled/Tilemaps/Beginning Fields.tmx"
        )

        self.plant_system = PlantSystem(
            "Tileset/Soil.png",
            self.game_map.tile_width,
            self.game_map.tile_height
        )

        self.planting_system = PlantingSystem(
            self.game_map.tile_width,
            self.game_map.tile_height
        )

        self.camera = self.create_camera()

        self.player = Player(
            520,
            230,
            self.game_map.used_width,
            self.game_map.used_height
        )

        self.level_system = LevelSystem()

        self.unlock_area_system = UnlockAreaSystem(
            self.game_map,
            self.level_system
        )

        self.font_level = pygame.font.SysFont(None, 28)
        self.font_message = pygame.font.SysFont(None, 24)

        self.level_message = ""
        self.level_message_timer = 0
        self.MESSAGE_DURATION = 35

        self.menu_bar = MenuBar(
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT,
            self.level_system
        )

        self.inventory = Inventory(
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT
        )

        self.coin = Coin(starting_amount=50)

        self.level_progress = LevelProgressSystem(
            self.level_system,
            self.coin
        )

        self.sell_box = SellBox(
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT
        )

        self.daftar_ayam = self.create_chickens()
        self.daftar_sapi = self.create_cows()

        self.feed_prices = {
            "Chicken Feed": 15,
            "Cows Feed": 25
        }

        self.enemies = []
        self.ENEMY_GIF_PATH = "enemy/1.gif"
        self.pending_enemy_spawns = []
        self.ENEMY_SPAWN_DELAY = 20000

        player_x, player_y = self.player.get_position()
        self.camera.center_on(player_x, player_y)

    def create_camera(self):
        base_zoom = max(
            self.SCREEN_WIDTH / self.game_map.used_width,
            self.SCREEN_HEIGHT / self.game_map.used_height
        )

        start_zoom = max(1.65, base_zoom)

        return Camera(
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT,
            self.game_map.used_width,
            self.game_map.used_height,
            start_zoom
        )

    def create_chickens(self):
        ayam_1 = Chicken(
            x=850,
            y=260,
            min_x=780,
            max_x=930,
            min_y=200,
            max_y=320
        )

        ayam_2 = Chicken(
            x=810,
            y=230,
            min_x=780,
            max_x=930,
            min_y=200,
            max_y=320
        )

        ayam_3 = Chicken(
            x=890,
            y=280,
            min_x=780,
            max_x=930,
            min_y=200,
            max_y=320
        )

        return [ayam_1, ayam_2, ayam_3]

    def create_cows(self):
        sapi_1 = Cow(
            x=850,
            y=500,
            min_x=780,
            max_x=930,
            min_y=450,
            max_y=550
        )

        sapi_2 = Cow(
            x=890,
            y=470,
            min_x=780,
            max_x=930,
            min_y=450,
            max_y=550
        )

        return [sapi_1, sapi_2]

    def show_message(self, text):
        self.level_message = text
        self.level_message_timer = self.MESSAGE_DURATION

    def get_active_animals(self):
        active_animals = []

        if self.level_system.is_feature_unlocked("chicken"):
            active_animals.extend(self.daftar_ayam)

        if self.level_system.is_feature_unlocked("cow"):
            active_animals.extend(self.daftar_sapi)

        return active_animals

    def get_active_enemy_objects(self):
        if not self.level_system.is_feature_unlocked("enemy"):
            return []

        return self.enemies

    def draw_game_object(self, game_object):
        game_object.draw(self.screen, self.camera)

    def update_game_object(self, game_object):
        game_object.update(self.game_map)

    def run(self):
        while self.running:
            self.screen.fill((144, 213, 118))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.FPS)

        self.audio.stop_music()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.camera.handle_event(event, pygame)

            self.handle_ui_events(event)
            self.handle_keyboard_events(event)
            self.handle_mouse_events(event)

    def handle_ui_events(self, event):
        self.menu_bar.handle_event(event)

        menu_message = self.menu_bar.consume_message()

        if menu_message:
            self.show_message(menu_message)

        self.inventory.handle_event(event)
        self.sell_box.handle_event(event, self.inventory, self.coin)

    def handle_keyboard_events(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
            self.handle_action_key()

    def handle_action_key(self):
        active_item = self.menu_bar.get_selected_item_name()

        if active_item == "Weapon":
            self.handle_weapon_attack()
        else:
            self.handle_animal_interaction(active_item)

    def handle_weapon_attack(self):
        if not self.level_system.is_feature_unlocked("weapon"):
            self.show_message("Weapon unlocks at Level 3")
            return

        berhasil_serang = self.player.attack()

        if not berhasil_serang:
            return

        attack_rect = self.player.get_attack_rect()
        player_center_x, player_center_y = self.player.get_center()

        target_enemy = None
        jarak_terdekat = float("inf")

        for enemy in self.enemies:
            if attack_rect.colliderect(enemy.rect):
                dx = enemy.rect.centerx - player_center_x
                dy = enemy.rect.centery - player_center_y
                jarak = (dx * dx + dy * dy) ** 0.5

                if jarak < jarak_terdekat:
                    jarak_terdekat = jarak
                    target_enemy = enemy

        if target_enemy:
            mati = target_enemy.take_damage(
                self.player.get_attack_damage()
            )

            if mati:
                self.enemies.remove(target_enemy)
                self.coin.add(2)
                self.show_message("Enemy defeated! Coin +2")

    def handle_animal_interaction(self, active_item):
        active_animals = self.get_active_animals()

        if active_item is None:
            return

        target_animals = []

        for hewan in active_animals:
            jarak = self.player.distance_to(hewan.x, hewan.y)

            if jarak >= 250:
                continue


            if hewan.status == "READY":
                self.player.interact_with_animal(
                    hewan,
                    active_item,
                    self.inventory,
                    self.coin
                )
                continue


            if hewan.status == "DIGESTING":
                continue

            if hewan.status == "HUNGRY":
                if active_item == "Chicken Feed" and isinstance(hewan, Chicken):
                    target_animals.append(hewan)

                elif active_item == "Cows Feed" and isinstance(hewan, Cow):
                    target_animals.append(hewan)

        if len(target_animals) == 0:
            return

        price = self.feed_prices[active_item]
        total_price = price * len(target_animals)

        if self.coin.amount < total_price:
            self.show_message("Not enough coins.")
            return

        self.coin.amount -= total_price

        for hewan in target_animals:
            self.player.interact_with_animal(
                hewan,
                active_item,
                self.inventory,
                self.coin
            )

    def handle_mouse_events(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button != 1:
            return

        mouse_pos = event.pos

        if self.is_click_on_ui(mouse_pos):
            return

        blocked, lock_message = self.unlock_area_system.is_click_blocked(
            mouse_pos,
            self.camera
        )

        if blocked:
            self.show_message(lock_message)
            return

        self.handle_map_click(mouse_pos)

    def is_click_on_ui(self, mouse_pos):
        klik_menu_button = self.menu_bar.button_rect.collidepoint(mouse_pos)
        klik_inventory_button = self.inventory.button_rect.collidepoint(mouse_pos)
        klik_sell_button = self.sell_box.button_rect.collidepoint(mouse_pos)

        klik_inventory_panel = self.inventory.is_open
        klik_sell_panel = self.sell_box.is_open

        klik_menu_panel = False

        if self.menu_bar.is_open:
            panel_rect = pygame.Rect(
                self.menu_bar.panel_x,
                self.menu_bar.current_panel_y,
                self.menu_bar.panel_width,
                self.menu_bar.panel_height
            )

            klik_menu_panel = panel_rect.collidepoint(mouse_pos)

        return (
            klik_menu_button
            or klik_inventory_button
            or klik_sell_button
            or klik_inventory_panel
            or klik_sell_panel
            or klik_menu_panel
        )

    def handle_map_click(self, mouse_pos):
        selected_item = self.menu_bar.get_selected_item_name()

        self.plant_system.handle_click(
            mouse_pos,
            self.camera,
            selected_item
        )

        berhasil_tanam = self.planting_system.handle_click(
            mouse_pos,
            self.camera,
            selected_item,
            self.plant_system.tilled_tiles,
            self.inventory,
            self.coin
        )

        if berhasil_tanam:
            if self.level_system.is_feature_unlocked("enemy"):
                self.pending_enemy_spawns.append(
                    pygame.time.get_ticks()
                )

    def update(self):
        self.update_player()
        self.update_animals()
        self.update_enemies()
        self.update_enemy_spawn()
        self.update_camera()
        self.update_ui()
        self.update_level_progress()
        self.update_message_timer()

    def update_player(self):
        self.player.set_current_tool(
            self.menu_bar.get_selected_item_name()
        )

        old_player_x, old_player_y = self.player.get_position()
        old_player_rect = self.player.get_rect_copy()

        self.update_game_object(self.player)

        blocked, lock_message = self.unlock_area_system.is_rect_blocked(
            self.player.get_rect()
        )

        if blocked:
            self.player.restore_position(
                old_player_x,
                old_player_y,
                old_player_rect
            )
            self.show_message(lock_message)

    def update_animals(self):
        active_animals = self.get_active_animals()

        for hewan in active_animals:
            hewan.update(self.game_map)

    def update_enemies(self):
        for enemy in self.get_active_enemy_objects():
            self.update_game_object(enemy)

    def update_enemy_spawn(self):
        current_time = pygame.time.get_ticks()

        for spawn_time in self.pending_enemy_spawns[:]:
            if current_time - spawn_time >= self.ENEMY_SPAWN_DELAY:
                enemy_baru = spawn_enemy_around_plants(
                    self.planting_system.get_all_crop_tiles(),
                    self.game_map.tile_width,
                    self.ENEMY_GIF_PATH
                )

                if enemy_baru:
                    self.enemies.append(enemy_baru)

                self.pending_enemy_spawns.remove(spawn_time)

    def update_camera(self):
        self.camera.update(pygame)

        if self.player.is_player_moving():
            player_x, player_y = self.player.get_position()
            self.camera.center_on(player_x, player_y)

    def update_ui(self):
        self.menu_bar.update()
        self.inventory.update()
        self.sell_box.update()
        self.planting_system.update()

    def update_level_progress(self):
        progress_message = self.level_progress.check_level_progress()

        if progress_message:
            self.show_message(progress_message)

    def update_message_timer(self):
        if self.level_message_timer > 0:
            self.level_message_timer -= 1

    def draw(self):
        self.game_map.draw(self.screen, self.camera)

        self.unlock_area_system.draw(self.screen, self.camera)

        self.plant_system.draw(self.screen, self.camera)
        self.planting_system.draw(self.screen, self.camera)

        for enemy in self.get_active_enemy_objects():
            self.draw_game_object(enemy)

        for hewan in self.get_active_animals():
            hewan.draw(self.screen, self.camera)

        self.draw_game_object(self.player)

        self.coin.draw(self.screen)
        self.menu_bar.draw(self.screen)
        self.inventory.draw(self.screen)
        self.sell_box.draw(self.screen, self.inventory)

        self.draw_level_indicator()
        self.draw_message_popup()

    def draw_level_indicator(self):
        level_bg = pygame.Rect(20, 72, 165, 62)

        pygame.draw.rect(
            self.screen,
            (60, 120, 60),
            level_bg,
            border_radius=12
        )

        level_text = self.font_level.render(
            f"Level {self.level_system.get_level()}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            level_text,
            (
                level_bg.x + 18,
                level_bg.y + 8
            )
        )

        target_coin = self.level_progress.get_current_target_coin()

        if target_coin is None:
            target_label = "Max Level"
        else:
            target_label = f"Target: {self.coin.amount}/{target_coin}"

        target_text = self.font_message.render(
            target_label,
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            target_text,
            (
                level_bg.x + 18,
                level_bg.y + 34
            )
        )

    def draw_message_popup(self):
        if self.level_message_timer <= 0:
            return

        if self.level_message == "":
            return

        message_surface = self.font_message.render(
            self.level_message,
            True,
            (60, 60, 60)
        )

        message_rect = message_surface.get_rect()

        popup_rect = pygame.Rect(
            self.SCREEN_WIDTH // 2 - message_rect.width // 2 - 25,
            25,
            message_rect.width + 50,
            45
        )

        pygame.draw.rect(
            self.screen,
            (255, 255, 240),
            popup_rect,
            border_radius=14
        )

        pygame.draw.rect(
            self.screen,
            (120, 180, 100),
            popup_rect,
            3,
            border_radius=14
        )

        self.screen.blit(
            message_surface,
            (
                popup_rect.centerx - message_rect.width // 2,
                popup_rect.centery - message_rect.height // 2
            )
        )