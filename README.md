# Little-Farm-Friends
Anggota kelompok:
1. Ajeng Salma Arifa (25051204030)
2. Keyla Putri Nanjalita Ardano (25051204083)
3. Syafilla Fitri Faradilla (25051204176)

Deskripsi project:
Little Farm Friends adalah game simulasi pertanian 2D yang dikembangkan menggunakan Python dan Pygame dengan menerapkan konsep Object-Oriented Programming (OOP). Dalam permainan ini, pemain mengelola lahan pertanian dengan menanam, merawat, dan memanen tanaman untuk memperoleh koin dan meningkatkan level. Seiring perkembangan level, berbagai fitur baru akan terbuka, seperti perluasan lahan, jenis tanaman baru, kemunculan hama yang dapat dikalahkan menggunakan senjata, serta sistem peternakan ayam dan sapi yang menghasilkan telur dan susu. Melalui sistem progresi level tersebut, pemain dapat mengembangkan kebun sederhana menjadi area pertanian yang lebih lengkap dalam suasana permainan yang ringan dan santai. 

Fitur Utama:
1. Player Movement
Pemain dapat menggerakkan karakter untuk menjelajahi area farm.
2. Farming System
Pemain dapat mencangkul tanah, menanam tanaman, menunggu tanaman tumbuh, lalu memanennya.
3. Inventory System
Hasil panen dan hasil ternak akan tersimpan di inventory.
4. Sell Basket
Pemain dapat memilih item dari inventory untuk dijual dan mendapatkan coin.
5. Coin System
Coin digunakan untuk membeli bibit, memberi makan hewan, dan bertambah saat menjual item.
6. Animal System
Pemain dapat memberi makan ayam dan sapi, lalu mengambil hasil ternak seperti telur dan susu.
7. Enemy System
Enemy dapat muncul di sekitar tanaman dan bisa dikalahkan menggunakan weapon.
8. Level System
Beberapa fitur dan area akan terbuka sesuai perkembangan level pemain.

Cara Menjalankan Project:
1. Jalankan file main.py untuk memulai permainan.
2. Setelah game dijalankan, pemain akan masuk ke halaman Welcome Screen.
3. Klik tombol Start menggunakan pointer (mouse) untuk memulai permainan.
4. Setelah itu akan muncul Loading Screen yang menampilkan proses pemuatan aset permainan.
5. Setelah loading selesai, pemain akan masuk ke area permainan utama (Gameplay Level 1).
6. Gunakan tombol panah (← ↑ ↓ →) untuk menggerakkan karakter.
7. Gunakan tombol W, A, S, dan D untuk menggeser posisi map atau camera.
8. Gunakan pointer (mouse) untuk melakukan zoom in dan zoom out pada map.
9. Pilih Shovel pada menu bar menggunakan pointer (mouse), kemudian klik area lahan untuk mengolah tanah.
10. Pilih bibit tanaman pada menu bar menggunakan pointer (mouse), kemudian klik lahan yang telah diolah untuk menanam tanaman.
11. Tunggu hingga tanaman tumbuh dan siap dipanen.
12. Klik tanaman yang sudah matang menggunakan pointer (mouse) untuk memanen hasil pertanian.
13. Hasil panen akan otomatis masuk ke dalam Inventory.
14. Klik tombol Inventory menggunakan pointer (mouse) untuk melihat item yang dimiliki.
15. Pilih dan klik item yang ingin dijual menggunakan pointer (mouse), kemudian tentukan jumlah item yang akan dijual. 
16. Klik tombol Sell menggunakan pointer (mouse) untuk menjual hasil panen dan memperoleh Coin.
17. Kumpulkan Coin hingga mencapai target level yang ditentukan.
18. Setelah target Coin tercapai, pemain akan naik ke Level 2 dan membuka lahan serta tanaman baru.
19. Lanjutkan aktivitas farming untuk memperoleh lebih banyak Coin.
20. Setelah mencapai Level 3, fitur Enemy dan Weapon akan terbuka.
21. Gunakan lahan baru untuk memperluas area pertanian dan meningkatkan produksi tanaman.
22. Lakukan aktivitas farming seperti menanam, merawat, memanen, dan menjual hasil panen.
23. Enemy akan muncul di sekitar area pertanian.
24. Pilih Weapon pada menu bar menggunakan pointer (mouse).
25. Dekati enemy kemudian tekan SPACE untuk menyerang enemy menggunakan weapon.
26. Enemy yang berhasil dikalahkan akan memberikan tambahan Coin.
27. Pada level ini pemain juga dapat membuka fitur Chicken.
28. Pilih Chicken Feed menggunakan pointer (mouse), kemudian tekan ENTER di dekat ayam untuk memberi makan.
29. Setelah diberi makan, ayam akan menghasilkan Egg. Pilih Chicken Feed menggunakan pointer (mouse), kemudian tekan ENTER di dekat ayam yang telah menghasilkan 30. Egg untuk mengambil hasil produksi tersebut dan menyimpannya ke dalam Inventory.
31. Setelah mencapai Level 4, fitur Cow dan Cows Feed akan terbuka.
32. Pilih Cows Feed menggunakan pointer (mouse), kemudian tekan ENTER di dekat sapi untuk memberi makan.
33. Setelah diberi makan, sapi akan menghasilkan Milk. Pilih Cows Feed menggunakan pointer (mouse), kemudian tekan ENTER di dekat sapi yang 

Penjelasan Implementasi Object Oriented Programming (OOP):
A. Pewarisan (Inheritance)
Pewarisan digunakan untuk menghemat penulisan kode dengan menurunkan sifat (atribut) dan perilaku (metode) dari kelas induk (superclass) ke anak (subclass).
  - Animal (Superclass)
Pada file animal.py, class Animal dirancang sebagai kelas dasar untuk entitas hewan ternak. Class ini mewarisi modul ABC (Abstract Base Class) dan sudah mendefinisikan berbagai logika kompleks seperti animasi berjalan, pergerakan acak (random wander), status lapar (status = “HUNGRY”), batas area jalan, dan pembuatan ikon gelembung (bubble icon) untuk status pakan.
  - Subclass Hewan
Class turunan (seperti Chicken dan Cow) tidak perlu lagi menulis ulang seluruh logika pergerakan dan render animasi tersebut. Mereka hanya mewarisi sifat dari Animal dan cukup mendefinisikan atribut uniknya saja (seperti waktu produksi dan hasil panen telur/susu). 

	B. Abstraksi
Abstraksi digunakan untuk menyembunyikan kerumitan logika sistem ke dalam fungsi atau class yang berdiri sendiri, sehingga class utama atau sistem lain dapat menggunakannya dengan mudah. 
  - Abstraksi Metode Wajib
Di dalam animal.py class Animal menggunakan dekorator @abstractmethod pada fungsi produce(self). Ini menciptakan kontrak wajib bagi class turunannya untuk mengimplementasikan method produce() mereka sendiri, sementara sistem utama tidak perlu tahu bagaimana cara detail setiap hewan memproduksi barangnya.
  - Abstraksi Logika Spawning
Pada enemy.py, fungsi spawn_enemy_around_plants() menyembunyikan logika perhitungan matematika yang rumit untuk mengacak posisi spawn musuh di sisi luar area tanaman. 
  - Abstraksi Sistem Game
Di dalam game.py, kerumitan fitur dipisah menjadi sistem independen (misal: UnlockAreaSystem dan LevelProgressSystem). Class utama GameController berinteraksi dengan sistem ini secara abstrak, contohnya hanya dengan memanggil self.level_progress.check_level_progress().

	C. Polimorfisme (Polymorphism)
Polimorfisme memungkinkan method dengan nama yang sama persis dieksekusi dengan cara (perilaku) yang berbeda tergantung pada class yang memanggilnya. 
  - Method Overriding
	Di dalam proyek ini, entitas seperti Player, Enemy, dan Animal sama-sama mengimplementasikan fungsi dengan nama serupa, yaitu update(self, game_map) dan draw(self, screen, camera), namun dengan isi logika yang sangat berbeda:
Player.update() memproses input keyboard dari pemain dan membatasi pergerakan di layar.
Enemy.update() memproses pertambahan frame index untuk menjalankan animasi secara otomatis.
Animal.update() memproses waktu pencernaan dan menggerakkan AI hewan ternak.
  - Dynamic Binding
	Implementasi yang seragam ini memungkinkan game loop di GameController memanggil perintah secara dinamis, seperti self.update_game_object(obj) untuk semua tipe objek tanpa memerlukan banyak percabangan if-else.

	D. Enkapsulasi(Encapsulation)
Enkapsulasi diterapkan secara ketat untuk menyembunyikan detail dan melindungi data internal objek agar tidak dimodifikasi secara langsung dari luar class. 
  - Protected Attributes
	Pada class Player, seluruh atribut krusial dibungkus menggunakan awalan underscore (seperti self._x, self._speed, dan self._is_attacking). Ini menandakan variabel tersebut bersifat privat atau dilindungi. 
  - State Management
	Pada class Animal, status internal seperti self.status, self.feed_time, dan self.produce_duration tidak diubah langsung dari luar. Perubahan status dari "HUNGRY" menjadi "DIGESTING" atau "READY" dikelola secara internal melalui pemanggilan method feed() dan harvest().
Penggunaan Getter dan Setter
Untuk mengakses data penting Player dari luar class, digunakan dekorator @property bawaan Python (contoh: @property def is_moving(self)) atau menggunakan method getter/setter seperti get_position(). Hal ini mencegah terjadinya bug akibat perubahan koordinat karakter dari sistem eksternal secara sembarangan.


