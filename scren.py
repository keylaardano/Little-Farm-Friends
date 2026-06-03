import pygame
import math
import os
import sys
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)


class AssetManager:
    def __init__(self):
        self.base_dir = BASE_DIR

    def get_path(self, filename):
        possible_paths = [
            os.path.join(self.base_dir, "scren", filename),
            os.path.join(self.base_dir, filename),
        ]

        for path in possible_paths:
            if os.path.isfile(path):
                print("Asset ditemukan:", path)
                return path

        print("FILE TIDAK DITEMUKAN:", filename)
        pygame.quit()
        sys.exit()

    def load_image(self, filename, alpha=False):
        path = self.get_path(filename)

        if alpha:
            return pygame.image.load(path).convert_alpha()

        return pygame.image.load(path).convert()


class ImageHelper:
    @staticmethod
    def trim_alpha(image):
        rect = image.get_bounding_rect()
        return image.subsurface(rect).copy()

    @staticmethod
    def scale_by_width(image, target_width):
        w, h = image.get_size()
        ratio = target_width / w
        return pygame.transform.smoothscale(image, (int(w * ratio), int(h * ratio)))

    @staticmethod
    def draw_shadow(surface, image, center, offset=(0, 8)):
        shadow = image.copy()
        shadow.fill((0, 0, 0, 90), special_flags=pygame.BLEND_RGBA_MULT)
        rect = shadow.get_rect(center=(center[0] + offset[0], center[1] + offset[1]))
        surface.blit(shadow, rect)


class Leaf:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.x = random.randint(-100, self.width + 100)
        self.y = random.randint(-self.height, -20)
        self.speed = random.uniform(1.2, 2.8)
        self.size = random.randint(8, 16)
        self.angle = random.uniform(0, 360)
        self.swing = random.uniform(0.02, 0.05)
        self.color = random.choice([
            (90, 160, 65),
            (120, 180, 70),
            (210, 155, 60),
            (170, 110, 45)
        ])

    def update(self):
        self.y += self.speed
        self.x += math.sin(self.y * self.swing) * 1.4
        self.angle += 2

        if self.y > self.height + 30:
            self.reset()

    def draw(self, screen):
        leaf_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

        pygame.draw.ellipse(
            leaf_surface,
            self.color,
            (4, 2, self.size, self.size // 2)
        )

        pygame.draw.line(
            leaf_surface,
            (70, 100, 40),
            (4, self.size // 2),
            (4 + self.size, self.size // 2),
            2
        )

        rotated = pygame.transform.rotate(leaf_surface, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect)


class Button:
    def __init__(self, image, center):
        self.original_image = image
        self.center = center
        self.rect = self.original_image.get_rect(center=self.center)

    def draw(self, screen, mouse_pos, timer):
        scale = 1 + math.sin(timer * 0.08) * 0.012

        if self.rect.collidepoint(mouse_pos):
            scale = 1.08

        image = pygame.transform.rotozoom(self.original_image, 0, scale)
        self.rect = image.get_rect(center=self.center)

        ImageHelper.draw_shadow(screen, image, self.center, offset=(0, 5))
        screen.blit(image, self.rect)

    def is_clicked(self, mouse_pos, clicked):
        return clicked and self.rect.collidepoint(mouse_pos)


class WelcomeScreen:
    def __init__(self, app):
        self.app = app
        self.timer = 0
        self.dark_timer = 0
        self.leaves = [Leaf(self.app.WIDTH, self.app.HEIGHT) for _ in range(18)]

        self.start_button = Button(
            self.app.menu_img,
            (self.app.WIDTH // 2, 540)
        )

    def run(self):
        while True:
            self.app.clock.tick(self.app.FPS)
            self.timer += 1
            self.dark_timer += 1

            mouse_pos = pygame.mouse.get_pos()
            clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.quit_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True

            self.app.screen.blit(self.app.background, (0, 0))

            for leaf in self.leaves:
                leaf.update()
                leaf.draw(self.app.screen)

            logo_scale = 1 + math.sin(self.timer * 0.06) * 0.018
            logo_y = 270 + math.sin(self.timer * 0.035) * 5
            logo = pygame.transform.rotozoom(self.app.logo_img, 0, logo_scale)

            logo_center = (self.app.WIDTH // 2, logo_y)
            ImageHelper.draw_shadow(self.app.screen, logo, logo_center, offset=(0, 10))
            self.app.screen.blit(logo, logo.get_rect(center=logo_center))

            self.start_button.draw(self.app.screen, mouse_pos, self.timer)

            if self.start_button.is_clicked(mouse_pos, clicked) and self.dark_timer >= 20:
                return

            pygame.display.update()


class LoadingScreen:
    def __init__(self, app):
        self.app = app
        self.progress = 0
        self.timer = 0
        self.leaves = [Leaf(self.app.WIDTH, self.app.HEIGHT) for _ in range(10)]

    def draw_loading_view(self, complete=False):
        self.app.screen.blit(self.app.background, (0, 0))

        for leaf in self.leaves:
            leaf.update()
            leaf.draw(self.app.screen)

        logo = ImageHelper.scale_by_width(self.app.logo_img, 600)
        logo_center = (self.app.WIDTH // 2, 260)
        ImageHelper.draw_shadow(self.app.screen, logo, logo_center)
        self.app.screen.blit(logo, logo.get_rect(center=logo_center))

        if complete:
            text = self.app.font.render("Complete!", True, self.app.DARK_BROWN)
        else:
            dots = "." * ((self.timer // 20) % 4)
            text = self.app.font.render("Loading" + dots, True, self.app.DARK_BROWN)

        self.app.screen.blit(text, text.get_rect(center=(self.app.WIDTH // 2, 480)))

        bar_x, bar_y, bar_w, bar_h = 350, 530, 580, 34

        pygame.draw.rect(
            self.app.screen,
            self.app.CREAM,
            (bar_x, bar_y, bar_w, bar_h),
            border_radius=20
        )

        pygame.draw.rect(
            self.app.screen,
            self.app.GREEN,
            (bar_x, bar_y, int(bar_w * self.progress / 100), bar_h),
            border_radius=20
        )

        pygame.draw.rect(
            self.app.screen,
            self.app.BROWN,
            (bar_x, bar_y, bar_w, bar_h),
            4,
            border_radius=20
        )

        percent = self.app.small_font.render(
            f"{int(self.progress)}%",
            True,
            self.app.DARK_BROWN
        )
        self.app.screen.blit(percent, percent.get_rect(center=(self.app.WIDTH // 2, 600)))

    def transition_to_next_screen(self):
        fade = pygame.Surface((self.app.WIDTH, self.app.HEIGHT))
        fade.fill((0, 0, 0))

        self.progress = 100

        for alpha in range(0, 256, 6):
            self.draw_loading_view(complete=True)

            fade.set_alpha(alpha)
            self.app.screen.blit(fade, (0, 0))

            pygame.display.update()
            self.app.clock.tick(self.app.FPS)

    def run(self):
        while True:
            self.app.clock.tick(self.app.FPS)

            if self.progress < 100:
                self.progress += 0.35
            else:
                self.progress = 100

            self.timer += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.quit_game()

            self.draw_loading_view()
            pygame.display.update()

            if self.progress >= 100:
                pygame.time.delay(500)
                self.transition_to_next_screen()
                return


class Game:
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60

    BROWN = (92, 55, 25)
    DARK_BROWN = (65, 38, 18)
    CREAM = (255, 239, 190)
    GREEN = (94, 180, 85)

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Little Farm Friends")
        self.clock = pygame.time.Clock()

        self.assets = AssetManager()

        self.font = pygame.font.SysFont("comicsansms", 30, bold=True)
        self.small_font = pygame.font.SysFont("comicsansms", 24, bold=True)

        self.background = self.assets.load_image("background.png")
        self.background = pygame.transform.smoothscale(
            self.background,
            (self.WIDTH, self.HEIGHT)
        )

        self.logo_img = self.assets.load_image("logo.png", alpha=True)
        self.logo_img = ImageHelper.trim_alpha(self.logo_img)
        self.logo_img = ImageHelper.scale_by_width(self.logo_img, 600)

        self.menu_img = self.assets.load_image("menu.png", alpha=True)
        self.menu_img = ImageHelper.trim_alpha(self.menu_img)
        self.menu_img = ImageHelper.scale_by_width(self.menu_img, 170)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self, lanjut_ke_main_loop=True):
        WelcomeScreen(self).run()
        LoadingScreen(self).run()

if __name__ == "__main__":
    game = Game()
    game.run()