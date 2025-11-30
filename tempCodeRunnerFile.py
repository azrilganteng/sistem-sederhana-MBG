 pilihan = questionary.select(
            f"Selamat datang {nama_petani}, Silakan pilih menu:",
            choices=[
                "1. Input & Kirim Data Panen",
                "2. Lihat & Update Riwayat Panen",
                "3. Keluar (Logout)"
            ]
        ).ask()