import psycopg2 as pg
from datetime import date
import tabulate as tbl
import questionary
from pyfiglet import Figlet
from rich.console import Console
from rich.align import Align
import os
from rich.prompt import Prompt
import time

#CONNECTION TO DATABASE
def connect():
    try:
        conn = pg.connect(
        host= "localhost",
        database= "SISTEM_MBG",
        user= "postgres",
        password = "12345",
        port= ""
        )
        return conn
    except Exception as e:
        print("Terjadi kesalahan:", e)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


console = Console()
f = Figlet(font='slant')
#DASHBOARD
def dashboard():
    ascii_art = f.renderText("SISTEM MBG")
    
    console.print(Align.center(f"[bold cyan]{ascii_art}[/bold cyan]"))
    

    console.print(Align.center("[italic white]— Verification & Monitoring Dashboard —[/italic white]"))
    console.print(Align.center("[dim]kelompok[/dim]\n"))

#LOGIN FUNCTION
def login():
    while True:
        judul = Figlet(font='slant').renderText("LOGIN")
        console.print(judul, style="bold cyan", justify="center")

        Username = Prompt.ask("[bold green]Username[/]").lower().strip()
        password = Prompt.ask("[bold green]Password[/]",password=True).strip()
     
        try:
            conn = connect()
            with conn.cursor() as cur: 
                check_akun = """SELECT id_akun, id_role FROM akun
                                WHERE user_name = %s AND password = %s"""
                cur.execute(check_akun, (Username, password))
                result = cur.fetchone()
                
                if result is None:
                    print("Login Gagal: Username atau Password salah.")
                    time.sleep(2)
                    clear()
                else:
                    result_id = result[0]
                    result_role = result[1]

                    user_actv = {
                        'id_akun': result_id,
                        'role': result_role,
                        'nama': None,
                        'id_asli': None 
                    }

                    if result_role == 1:
                        petani=("SELECT id_petani, nama_petani FROM petani WHERE id_akun = %s")
                        cur.execute(petani,(result_id,))
                        data_petani = cur.fetchone()
                        
                        if data_petani:
                            user_actv['id_asli'] = data_petani[0] 
                            user_actv['nama'] = data_petani[1]   
                            
                            menu_petani(user_actv)
                            return user_actv 
                        else:
                            print("Error: Data detail petani tidak ditemukan.")
                            break 
                    
                    elif result_role == 2: 
                        karyawan=("SELECT id_karyawan, nama_karyawan FROM karyawan WHERE id_akun = %s")
                        cur.execute(karyawan,(result_id,))
                        data_karyawan = cur.fetchone()
                        
                        if data_karyawan:
                            user_actv['id_asli'] = data_karyawan[0] 
                            user_actv['nama'] = data_karyawan[1]   
                            
                            menu_karyawan(user_actv)
                            return user_actv 
                        else:
                            print("Error: Data detail karyawan tidak ditemukan.")
                            break
                    elif result_role == 3: 
                        dapur=("SELECT id_dapur, nama_dapur FROM dapur_instansi WHERE id_akun = %s")
                        cur.execute(dapur,(result_id,))
                        data_dapur = cur.fetchone()
                        
                        if data_dapur:
                            user_actv['id_asli'] = data_dapur[0] 
                            user_actv['nama'] = data_dapur[1]   
                            
                            menu_dapur(user_actv)
                            return user_actv
                        
                    elif result_role == 4: 
                            admin=("SELECT id_admin, nama_admin FROM admin WHERE id_akun = %s")
                            cur.execute(admin,(result_id,))
                            data_admin = cur.fetchone()
                            
                            if data_admin:
                                user_actv['id_asli'] = data_admin[0] 
                                user_actv['nama'] = data_admin[1]   
                                
                                menu_admin(user_actv)
                                return user_actv 
                            else:
                                print("Error: Data detail admin tidak ditemukan.")
                                break
            if conn:
                conn.close()
                clear()

        except Exception as e:
            print("Terjadi kesalahan sistem:", e)
            return None 
        
#LOGOUT FUNCTION         
def logout(user_session):
    try:
        nama=user_session.get('nama','user')
        confirm = questionary.select(
            "Yakin mau keluar?",
            choices=[
                "1. Ya",
                "2. Tidak"
            ]
        ).ask()

        if confirm == "1. Ya":
            judul = [[f"SAMPAI JUMPA {nama}"]]
            print("\n" + tbl.tabulate(judul, tablefmt="fancy_grid"))
            time.sleep(1)
            clear()
            exit()
        elif confirm == "2. Tidak":
            judul = [["HOREEEE!!! GAJADI KELUAR"]]
            print("\n" + tbl.tabulate(judul, tablefmt="fancy_grid"))
            time.sleep(1)
            return
    
    except Exception as e:
        print("Terjadi kesalahan sistem:", e)
        return None 

#TAMBAH NUTRISI KALO MISAL NAMA TUMBUHAN GA ADA DI DATABASE
def add_nutrisi(nama_baru): 
    try:
        conn = connect()
        with conn.cursor() as cur:   
            print("Silakan tambahkan kategori nutrisi agar bisa disimpan.")
            print("\n--- PILIH KATEGORI NUTRISI ---")
            cur.execute("SELECT id_nutrisi, nama_nutrisi FROM jenis_nutrisi ORDER BY id_nutrisi")
            list_nutrisi = cur.fetchall()

            if not list_nutrisi:
                print("Pilih nutrisi yang ada")
                return None

            for n in list_nutrisi:
                print(f"[{n[0]}] {n[1]}")
            
            pilihan_nutrisi = input("Masukkan ID Nutrisi: ")

            query_tambah_nutrisi = """
                INSERT INTO tumbuhan (nama_tumbuhan, id_nutrisi)
                VALUES (%s, %s)
                RETURNING id_tumbuhan
            """
            cur.execute(query_tambah_nutrisi, (nama_baru, pilihan_nutrisi))
            
            id_baru = cur.fetchone()[0]
            conn.commit()
            print(f"Berhasil mendaftarkan '{nama_baru}'.")
            return id_baru
        
        if conn:
            conn.close()

    except Exception as e:
        print("Terjadi kesalahan sistem:", e)
        return None
#UPDATE FUNCTION
def update(id_petani):
    try:
        conn = connect()
        with conn.cursor() as cur:
            id_update = int(input("Masukkan ID yang mau di ubah: "))

            check_id = "SELECT id_tumbuhan FROM panen WHERE id_panen = %s AND id_petani = %s"
            cur.execute(check_id, (id_update, id_petani))

            find=cur.fetchone()
            if not find:
                print("ID tidak ditemukan atau hasil panen bukan milik anda")
                return

            try:
                qty_baru = int(input("Masukkan kuantitas baru: "))

            except ValueError:
                print("Kuantitas harus angka!")
                return

            update_qty = """UPDATE panen SET kuantitas = %s WHERE id_panen = %s"""
            cur.execute(update_qty, (qty_baru, id_update))

            conn.commit()
            print("Data berhasil diperbarui!")
        
    except Exception as e:
        print("Terjadi kesalahan:", e)

def show(id_petani,user_session):
    nama_petani=user_session['nama']
    try:
        conn = connect()
        with conn.cursor() as cur:
            judul = [[f"RIWAYAT PANEN: {nama_petani.upper()}"]]
            print("\n" + tbl.tabulate(judul, tablefmt="fancy_grid"))
            read_data="""SELECT pa.id_panen,p.nama_petani,t.nama_tumbuhan,pa.kuantitas,pa.tgl_panen
                from petani p join panen pa using(id_petani)
                JOIN tumbuhan t using(id_tumbuhan)
                WHERE p.id_petani = %s
                ORDER BY pa.id_panen"""
            cur.execute(read_data,(id_petani,))
            show=cur.fetchall()
            if not show:
                print("Anda belum memiliki data panen")
            else:
                header=["id panen","nama petani","nama tumbuhan","kuantitas (kg)","tanggal panen"]
                print(tbl.tabulate(show,headers=header,tablefmt="fancy_grid"))

                try:
                    pilihan = questionary.select(
                        "Masukkan pilihan kamu",
                        choices=[
                            "1. Update data",
                            "2. Kembali ke menu"
                            ]
                    ).ask()

                    if pilihan == "1. Update data":
                        update(id_petani)
                            
                    elif pilihan == "2. Kembali ke menu":
                        menu_petani(user_session)
                except ValueError:
                    print("ID harus berupa angka.")
                    return

        if conn:
            conn.close()


    except Exception as e:
        print("terjadi kesalahan: ",e)
        return None         
# ADD PANEN
def tambah_panen(id_petani):
    print("\n(Ketik 'stop' di nama tumbuhan jika sudah selesai)\n")

    conn = connect() 
    cur = conn.cursor()
    
    banyak = [] 

    try:
       
        while True:
            nama_tumbuhan = input(f"Item ke-{len(banyak)+1} Nama Tumbuhan: ").strip().lower()
            
            if nama_tumbuhan == 'stop':
                break
            cur.execute("SELECT id_tumbuhan FROM tumbuhan WHERE nama_tumbuhan ILIKE %s", (nama_tumbuhan,))
            hasil = cur.fetchone()

            if hasil:
                id_fix = hasil[0]
            else:
                print("Panen belum tertera, daftarkan nutrisi dulu")
                id_fix = add_nutrisi(nama_tumbuhan.title()) 
                
                if not id_fix: continue 

            try:
                qty = int(input("   Jumlah (Kg): "))
                banyak.append([id_fix, nama_tumbuhan, qty]) 
                print("Masuk keranjang.\n")
            except ValueError:
                print("Kuantitas harus angka!\n")

        if not banyak:
            print("Tidak ada yang disimpan.")
            return

        print(f"\nMenyimpan {len(banyak)} item ke database...")
        
        tgl = input("Tanggal (Enter untuk hari ini): ")
        if not tgl: 
            tgl = date.today()

        q_header = """
            INSERT INTO pengiriman_pk (id_petani, tgl_pengiriman, status_verifikasi) 
            VALUES (%s, %s, 'sedang dikirim')
            RETURNING id_pengiriman
        """
        cur.execute(q_header, (id_petani, tgl))
        
        
        id_pengiriman = cur.fetchone()[0]
        print(f"Membuat ID Pengiriman: {id_pengiriman}")

       
        for item in banyak:
        
            q_panen = """
                INSERT INTO panen (id_petani, id_tumbuhan, kuantitas, tgl_panen) 
                VALUES (%s, %s, %s, %s)
                RETURNING id_panen
            """
            cur.execute(q_panen, (id_petani, item[0], item[2], tgl))
            id_panen_baru = cur.fetchone()[0] 

            q_detail = """
                INSERT INTO detail_pengiriman_pk (id_pengiriman, id_panen, kuantitas) 
                VALUES (%s, %s, %s)
            """
            cur.execute(q_detail, (id_pengiriman, id_panen_baru, item[2]))

        
        conn.commit()
        print(f"SUKSES! Paket ID {id_pengiriman} berisi {len(banyak)} barang telah dikirim.")

    except Exception as e:
        conn.rollback() 
        print(f"Error Sistem: {e}")
    finally:
        conn.close()

#PETANI FUNCTION
def menu_petani(user_session):
    actv_id = user_session['id_asli']
    nama_petani = user_session['nama']

    while True:
        clear()
        print("\n") 
        pilihan = questionary.select(
            f"Selamat datang {nama_petani}, Silakan pilih menu:",
            choices=[
                "1. Input & Kirim Data Panen",
                "2. Lihat & Update Riwayat Panen",
                "3. Keluar (Logout)"
            ]
        ).ask()

        if pilihan == "1. Input & Kirim Data Panen":
            tambah_panen(actv_id)
            input("Tekan Enter untuk kembali...") 
            
        elif pilihan == "2. Lihat & Update Riwayat Panen":
            show(actv_id, user_session)
            input("Tekan Enter untuk kembali...")

        elif pilihan == "3. Keluar (Logout)":
            logout(user_session)
        
#VERIFIKASI OLEH KARYAWAN
def verifikasi_panen(id_karyawan):
    conn = connect()
    cur = conn.cursor()

    try:
        judul = [["VERIFIKASI PENGIRIMAN MASUK"]]
        print("\n" + tbl.tabulate(judul, tablefmt="fancy_grid"))

        q_pending = """
            SELECT p.id_pengiriman, pet.nama_petani, p.tgl_pengiriman, COUNT(dp.id_detail)
            FROM pengiriman_pk p
            JOIN petani pet USING(id_petani)
            JOIN detail_pengiriman_pk dp USING(id_pengiriman)
            WHERE p.status_verifikasi = 'sedang dikirim' 
            GROUP BY p.id_pengiriman, pet.nama_petani, p.tgl_pengiriman
            ORDER BY p.tgl_pengiriman ASC
        """
        cur.execute(q_pending)
        list_pending = cur.fetchall()

        if not list_pending:
            print("Tidak ada data pending.")
            return

        print(tbl.tabulate(list_pending, headers=["ID", "Petani", "Tanggal", "Jml Item"], tablefmt="fancy_grid"))

        try:
            pilih = int(input("\nPilih ID Pengiriman: "))
            print("[ENTER] untuk keluar")
        except ValueError: return
        if not pilih:
            return

        cur.execute("SELECT id_pengiriman FROM pengiriman_pk WHERE id_pengiriman = %s AND status_verifikasi = 'sedang dikirim'", (pilih,))
        if not cur.fetchone():
            print("ID tidak valid.")
            return

        print("\nLokasi Penyimpanan:")
     
        cur.execute("SELECT id_gudang, nama_gudang FROM gudang ORDER BY id_gudang")
        list_gudang = cur.fetchall()
        for g in list_gudang:
            print(f"{g[0]}. {g[1]}")
            
        try:
            pilih_gudang = int(input("Simpan ke Gudang mana? (Pilih ID): "))

            cur.execute("SELECT id_gudang FROM gudang WHERE id_gudang = %s", (pilih_gudang,))
            if not cur.fetchone():
                print("Gudang tidak ditemukan.")
                return
        except ValueError: return

        q_detail = """
            SELECT t.id_tumbuhan, t.nama_tumbuhan, dp.kuantitas
            FROM detail_pengiriman_pk dp 
            JOIN panen p USING(id_panen)
            JOIN tumbuhan t USING(id_tumbuhan)
            WHERE dp.id_pengiriman = %s
        """
        cur.execute(q_detail, (pilih,))
        isi_detail = cur.fetchall()

        confirm = input(f"Verifikasi? (y/n): ").lower()
        if confirm != 'y': return

        print("Sedang memproses...")
        ID_TRANSAKSI_MASUK = 1 
        tgl_hari_ini = date.today()
        time.sleep(1)

        for barang in isi_detail:
            id_tumb = barang[0]
            nama_brg = barang[1]
            qty_masuk = barang[2]
    
            q_dist = """
                INSERT INTO distribusi (tgl_distribusi, kuantitas, id_gudang, id_karyawan, id_tumbuhan, id_transaksi)
                VALUES (%s, %s, %s, %s, %s, %s)"""

            cur.execute(q_dist, (tgl_hari_ini, qty_masuk, pilih_gudang, id_karyawan, id_tumb, ID_TRANSAKSI_MASUK))
            print(f" {nama_brg}: Tercatat masuk di distribusi (+{qty_masuk} Kg)")

        cur.execute("UPDATE pengiriman_pk SET status_verifikasi = 'Diterima', id_karyawan = %s WHERE id_pengiriman = %s", (id_karyawan, pilih))
        
        conn.commit()
        print(f"SUKSES! Data tersimpan di Gudang ID {pilih_gudang}.")

    except Exception as e:
        conn.rollback()
        print(f"Error Sistem: {e}")
    finally:
        if conn: conn.close()

#CEK GUDANG
def show_gudang():
    conn = connect()
    with conn.cursor() as cur:
        query = """
            SELECT g.nama_gudang, t.nama_tumbuhan, 
            SUM(CASE WHEN d.id_transaksi = 1 THEN d.kuantitas ELSE -d.kuantitas END) as total_stok, 
            t.id_tumbuhan
            FROM distribusi d
            JOIN gudang g ON d.id_gudang = g.id_gudang
            JOIN tumbuhan t ON d.id_tumbuhan = t.id_tumbuhan
            GROUP BY g.nama_gudang, t.nama_tumbuhan, t.id_tumbuhan
            HAVING SUM(CASE WHEN d.id_transaksi = 1 THEN d.kuantitas ELSE -d.kuantitas END) > 0
            ORDER BY g.nama_gudang ASC, t.nama_tumbuhan ASC
        """
        cur.execute(query)
        show = cur.fetchall()
        
        if not show:
            print("Stok Gudang Kosong.")
            return False

        headers = ["Lokasi", "Nama Komoditas", "Total Stok (Kg)", "ID Barang"]
        print(tbl.tabulate(show, headers=headers, tablefmt="fancy_grid"))
        return True 
    
    if conn: conn.close()
def gudang():
    
    judul = [["STOK GUDANG"]]
    print("\n" + tbl.tabulate(judul, tablefmt="fancy_grid"))
    show_gudang()
            
    back()
    
def back():
    input("\nTekan Enter untuk kembali =>")

def show_instansi():
    conn = connect()
    with conn.cursor() as cur:
    
        cur.execute("SELECT id_dapur, nama_dapur FROM dapur_instansi")
        list_dapur = cur.fetchall()
        
        print("\nDaftar Dapur:")
        headers = ["id_dapur", "Nama Dapur"]
        print(tbl.tabulate(list_dapur, headers=headers, tablefmt="fancy_grid"))
        
        if not list_dapur:
            print("Anda belum memiliki data panen")

#KIRIM KE INSTANSI
def kirim_instansi(id_karyawan):
    conn = connect()
    cur = conn.cursor()

    try:
        judul = [["IRIM KE DAPUR INSTANSI"]]
        print("\n" + tbl.tabulate(judul, tablefmt="fancy_grid"))
        
        show_instansi()
        try:
            pilih_dapur = int(input("Kirim ke Dapur mana? (Pilih ID): "))
            print("[ENTER] untuk kembali")
        except ValueError: return

        keranjang = []
        show_gudang()
        print("\nMasukkan Barang (Ketik 'stop' untuk selesai):")
        
        while True:
            nama_tumbuhan = input(f"Item ke-{len(keranjang)+1} Nama: ").lower().strip()
            if nama_tumbuhan == 'stop': break

            cur.execute("SELECT id_tumbuhan FROM tumbuhan WHERE nama_tumbuhan ILIKE %s", (nama_tumbuhan,))
            res = cur.fetchone()
            if not res:
                print("Barang tidak ditemukan.")
                continue
            
            id_tumb = res[0]
            
            try:
                qty = int(input("Jumlah (Kg): "))
                
                q_cek_stok = """
                    SELECT SUM(CASE WHEN id_transaksi = 1 THEN kuantitas ELSE -kuantitas END)
                    FROM distribusi WHERE id_tumbuhan = %s
                """
                cur.execute(q_cek_stok, (id_tumb,))
                sisa_stok = cur.fetchone()[0] or 0 
                
                if sisa_stok < qty:
                    print(f"Stok tidak cukup! Sisa stok gudang: {sisa_stok} Kg")
                    continue
                
                print("Ambil dari Gudang mana?")
                print("1. Gudang A")
                print("2. Gudang B")
                gudang_sumber = int(input("Pilih (1/2): "))
                
                keranjang.append({
                    'id': id_tumb, 
                    'nama': nama_tumbuhan, 
                    'qty': qty,
                    'gudang': gudang_sumber
                })
                print("Masuk keranjang.")
                
            except ValueError:
                print("Input salah.")

        if not keranjang: return

        tgl_hari_ini = date.today()
        ID_TRANSAKSI_KELUAR = 2 
        
        q_header = """
            INSERT INTO pengiriman_ki (tgl_pegiriman, status_verifikasi, id_dapur)
            VALUES (%s, 'sedang dikirim', %s)
            RETURNING id_pengiriman
        """
        cur.execute(q_header, (tgl_hari_ini, pilih_dapur))
        id_kirim_baru = cur.fetchone()[0]

        for item in keranjang:
    
            q_detail = """
                INSERT INTO detail_pengiriman_ki (kuantitas, id_karyawan, id_pengiriman, id_tumbuhan)
                VALUES (%s, %s, %s, %s)
            """
            cur.execute(q_detail, (item['qty'], id_karyawan, id_kirim_baru, item['id']))
        
            q_dist = """
                INSERT INTO distribusi (tgl_distribusi, kuantitas, id_gudang, id_karyawan, id_tumbuhan, id_transaksi)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(q_dist, (tgl_hari_ini, item['qty'], item['gudang'], id_karyawan, item['id'], ID_TRANSAKSI_KELUAR))

        conn.commit()
        print(f"SUKSES! Pengiriman ID {id_kirim_baru} sedang dikirim ke Dapur.")
        print("(Stok gudang otomatis berkurang)")

    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        conn.close()

    
def menu_karyawan(user_session):
    actv_id = user_session['id_asli']
    nama_karyawan=user_session['nama']
    
    while True:
        clear()
        pilihan = questionary.select(
            f"Selamat datang {nama_karyawan}, Silakan pilih menu:",
            choices=[
                "1. Verifikasi Hasil Panen",
                "2. Lihat Stok di Gudang",
                "3. Kirim Ke Dapur Instansi",
                "4. Keluar"
            ]
        ).ask()
        if pilihan == "1. Verifikasi Hasil Panen":
            verifikasi_panen(actv_id)
        elif pilihan == "2. Lihat Stok di Gudang":
            gudang()
        elif pilihan == "3. Kirim Ke Dapur Instansi":
            kirim_instansi(actv_id)
        elif pilihan == "4. Keluar":
            logout(user_session)

def lihat_pengiriman_dapur(id_dapur):
    conn = connect()
    cur = conn.cursor()

    try:
        q_paket="""
            SELECT pk.id_pengiriman, pk.tgl_pegiriman, COUNT(dp.id_detail) as jumlah_jenis_barang
            FROM pengiriman_ki pk
            JOIN detail_pengiriman_ki dp USING(id_pengiriman)
            WHERE pk.id_dapur = %s AND pk.status_verifikasi = 'sedang dikirim'
            GROUP BY pk.id_pengiriman, pk.tgl_pegiriman
            ORDER BY pk.tgl_pegiriman ASC
        """
        cur.execute(q_paket, (id_dapur,))
        
        list_pengiriman = cur.fetchall()
        
        if not list_pengiriman:
            print("Tidak ada pengiriman baru.")
            input("Tekan Enter untuk kembali...")
            return

        headers = ["ID Paket", "Tanggal Kirim", "Jml Item"]
        print(tbl.tabulate(list_pengiriman, headers=headers, tablefmt="fancy_grid"))
        
        print("\nLihat isi paket?")
        print("(Masukkan ID atau tekan Enter untuk batal)")
        
        try:
            input_str = input("Pilih ID: ")
            if not input_str: return # Jika Enter doang, kembali
            pilih_paket = int(input_str)
        except ValueError: 
            print("Input harus angka!")
            input("Enter...")
            return

        # Cek apakah ID ada di list yang ditampilkan tadi
        cek_valid = [x for x in list_pengiriman if x[0] == pilih_paket]
        if not cek_valid:
            print("ID tidak ditemukan di daftar.")
            input("Enter...")
            return
        
        q_detail = """
            SELECT t.nama_tumbuhan, dp.kuantitas
            FROM detail_pengiriman_ki dp
            JOIN tumbuhan t USING(id_tumbuhan)
            WHERE dp.id_pengiriman = %s
        """
        cur.execute(q_detail, (pilih_paket,))
        isi_paket = cur.fetchall()
        
        print(f"\nIsi Paket ID {pilih_paket}:")
        print(tbl.tabulate(isi_paket, headers=["Nama Barang", "Qty (Kg)"], tablefmt="simple"))
            
        input("\nTekan Enter untuk kembali ke menu...")

    except Exception as e:
        print("Error:", e)
        input("Enter...")
    finally:
        if conn: conn.close()
        
def verifikasi_dapur(id_dapur):
    conn = connect()
    cur = conn.cursor()
    try:
        judul = [["BARANG MASUK"]]
        print("\n" + tbl.tabulate(judul, tablefmt="fancy_grid"))
   
        q_pending = """
            SELECT pk.id_pengiriman, pk.tgl_pegiriman, COUNT(dp.id_detail) 
            FROM pengiriman_ki pk
            JOIN detail_pengiriman_ki dp USING(id_pengiriman)
            WHERE pk.id_dapur = %s AND pk.status_verifikasi = 'sedang dikirim'
            GROUP BY pk.id_pengiriman, pk.tgl_pegiriman
        """
        cur.execute(q_pending, (id_dapur,))
        data = cur.fetchall()
        
        if not data:
            print("Tidak ada kiriman baru.")
            return
            
        print(tbl.tabulate(data, headers=["ID Kirim", "Tanggal", "Jml Item"], tablefmt="fancy_grid"))
        
      
        pilih = input("Masukkan ID Pengiriman untuk diterima: ").strip()
        if not pilih: 
            return
        try:
            pilih=int(pilih)
        except ValueError:
            return  
                   

        cur.execute("""
            SELECT t.nama_tumbuhan, dp.kuantitas 
            FROM detail_pengiriman_ki dp
            JOIN tumbuhan t USING(id_tumbuhan)
            WHERE dp.id_pengiriman = %s
        """, (pilih,))
        items = cur.fetchall()
        print(tbl.tabulate(items, headers=["Barang", "Qty"], tablefmt="fancy_grid"))
        
        if input("Terima barang ini? (y/n): ").lower() == 'y':
           
            cur.execute("UPDATE pengiriman_ki SET status_verifikasi = 'Diterima' WHERE id_pengiriman = %s", (pilih,))
            conn.commit()
            print("Barang diterima!")
        else:
            return
            
    except Exception as e:
        print("Error:", e)
    finally: conn.close()

def menu_dapur(user_session):
    clear()
    
    actv_id = user_session['id_asli'] 
    nama_dapur = user_session['nama']

    while True:
        pilihan = questionary.select(
            f"Selamat datang {nama_dapur}, Silakan pilih menu:",
            choices=[
                "1. Lihat pengiriman",
                "2. Verifikasi pengiriman",
                "3. Logout"
                ]
            ).ask()
        
        if pilihan == "1. Lihat pengiriman":
            clear()
            lihat_pengiriman_dapur(actv_id)
        elif pilihan == "2. Verifikasi pengiriman":
            clear()
            verifikasi_dapur(actv_id)
        elif pilihan == "3. Logout":
            clear()
            logout(user_session)
            break

def show_user():
    conn = connect()
    cur = conn.cursor()

    try:
        judul = [["DAFTAR USER"]]
        print("\n" + tbl.tabulate(judul, tablefmt="fancy_grid"))

        query = """
            SELECT a.id_akun, a.user_name,a.password, r.nama_role,
                COALESCE(p.nama_petani, k.nama_karyawan, d.nama_dapur, '-') as nama_asli, a.no_hp, a.alamat
            FROM akun a
            JOIN roles r USING (id_role)
            LEFT JOIN petani p USING(id_akun)
            LEFT JOIN karyawan k USING(id_akun)
            LEFT JOIN dapur_instansi d USING(id_akun)
            ORDER BY a.id_akun ASC
        """
        
        cur.execute(query)
        data = cur.fetchall()

        if not data:
            print("Belum ada data user.")
        else:
            headers = ["ID", "Username","Password", "Role", "Nama Asli", "No HP", "Alamat"]
            print(tbl.tabulate(data, headers=headers, tablefmt="fancy_grid",maxcolwidths=[None, None, None, None, 20, None, 30]))
        pilihan = questionary.select(
            f"Silakan pilih menu:",
            choices=[
                "1. Tambah data user",
                "2. Update data",
                "3. Hapus data",
                "4. Kembali"
            ]
        ).ask()
        if pilihan == "1. Tambah data user":
            tambah_user()
        elif pilihan == "2. Update data":
            update_user()

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        if conn: conn.close()
        clear()

def tambah_user():
    conn = connect()
    cur = conn.cursor()

    try:
        print("\n==== TAMBAH USER BARU ====")

        cur.execute("SELECT id_role, nama_role FROM roles ORDER BY id_role limit 3")
        roles = cur.fetchall()
    
        pilih_role = [f"{r[0]}. {r[1]}" for r in roles]
        
        pilihan = questionary.select(
            "Pilih Role:",
            choices=pilih_role
        ).ask()
        if pilihan is None:
            print("kembali ke menu")
            return
    
        id_role_pilih = int(pilihan.split(".")[0])
        nama_role = pilihan.split(". ")[1].lower()

        print(f"\n--- Input Data {nama_role.title()} ---")
        username = input("Username : ").strip()
      
        cur.execute("SELECT id_akun FROM akun WHERE user_name = %s", (username,))
        if cur.fetchone():
            print("Username sudah dipakai! Gunakan yang lain.")
            input("Tekan Enter...")
            return

        password = input("Password : ").strip()
        no_hp    = input("No HP    : ").strip()
        nama_asli= input("Nama Asli: ").strip()
        alamat   = input("Alamat   : ").strip()

        if input("\nSimpan data? (y/n): ").lower() != 'y': return

        q_akun = """
            INSERT INTO akun (user_name, password, no_hp, alamat, id_role)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_akun
        """
        cur.execute(q_akun, (username, password, no_hp, alamat, id_role_pilih))
        id_akun_baru = cur.fetchone()[0]

        if 'petani' in nama_role:
            cur.execute("""
                INSERT INTO petani (nama_petani, alamat, id_akun)
                VALUES (%s, %s, %s)
            """, (nama_asli, alamat, id_akun_baru))

        elif 'karyawan' in nama_role:
            cur.execute("""
                INSERT INTO karyawan (nama_karyawan, alamat, id_akun)
                VALUES (%s, %s, %s)
            """, (nama_asli, alamat, id_akun_baru))
            
        elif 'dapur instansi' in nama_role:
            cur.execute("""
                INSERT INTO dapur_instansi (nama_dapur, id_akun)
                VALUES (%s, %s)
            """, (nama_asli, id_akun_baru))
        
        conn.commit()
        print(f"\nSUKSES! User '{nama_asli}' ({nama_role}) berhasil ditambahkan.")

    except Exception as e:
        conn.rollback()
        print(f"Error Sistem: {e}")
    finally:
        if conn: conn.close()
        input("\nTekan Enter untuk kembali...")
def update_user():
    conn = connect()
    cur = conn.cursor()

    try:
        print("\n==== UPDATE DATA USER ====")
        
        id_target = int(input("Masukkan ID Akun yang mau diubah: "))

        query_cek = "SELECT id_akun, id_role FROM akun WHERE id_akun = %s"
        cur.execute(query_cek, (id_target,))
        result = cur.fetchone()

        if not result:
            print("ID Akun tidak ditemukan.")
            return
        
        role_target = result[1]

        print("\n--- Masukkan Data Baru ---")
        new_username = input("Username Baru : ").strip()
        new_password = input("Password Baru : ").strip()
        new_nama     = input("Nama Baru     : ").strip()
        new_hp       = input("No HP Baru    : ").strip()
        new_alamat   = input("Alamat Baru   : ").strip()

        if input("\nSimpan perubahan? (y/n): ").lower() != 'y': return

        q_update_akun = """
            UPDATE akun 
            SET user_name = %s, password = %s, no_hp = %s, alamat = %s 
            WHERE id_akun = %s
        """
        cur.execute(q_update_akun, (new_username, new_password, new_hp, new_alamat, id_target))

        if role_target == 1:
            cur.execute("UPDATE petani SET nama_petani = %s WHERE id_akun = %s", (new_nama, id_target))
            
        elif role_target == 2:
            cur.execute("UPDATE karyawan SET nama_karyawan = %s WHERE id_akun = %s", (new_nama, id_target))
            
        elif role_target == 3: 
            cur.execute("UPDATE dapur_instansi SET nama_dapur = %s WHERE id_akun = %s", (new_nama, id_target))

        conn.commit()
        print("Data berhasil diperbarui!")

    except Exception as e:
        conn.rollback()
        print(f"Terjadi kesalahan: {e}")
    finally:
        if conn: conn.close()
        input("\nTekan Enter untuk kembali...")


def history_petani_karyawan():
    conn = connect()
    cur = conn.cursor()
    try:

        bulan = int(input("Masukkan angka bulan (1-12): "))
    
        if bulan < 1 or bulan > 12:
                print("bulan harus 1-12.")
                return

        query = """
        SELECT p.tgl_pengiriman, pet.nama_petani, kar.nama_karyawan, t.nama_tumbuhan, dp.kuantitas, p.status_verifikasi
                FROM pengiriman_pk p
                JOIN detail_pengiriman_pk dp USING(id_pengiriman)
                JOIN petani pet USING(id_petani)
                LEFT JOIN karyawan kar USING(id_karyawan)
                JOIN panen pa ON dp.id_panen = pa.id_panen
                JOIN tumbuhan t ON pa.id_tumbuhan = t.id_tumbuhan
                WHERE EXTRACT(MONTH FROM p.tgl_pengiriman) = %s
                ORDER BY p.tgl_pengiriman ASC
        """

        cur.execute(query, (bulan,))
        data = cur.fetchall()
        
        if not data:
            print("Tidak ada data pengiriman untuk bulan tersebut.")
            return
        
        headers = ["Petani", "Karyawan (ACC)", "Barang", "Qty (Kg)","Tanggal", "Status"]
        print(tbl.tabulate(data, headers=headers, tablefmt="fancy_grid"))
    
    except Exception as e:
        print("terjadi kesalahan",e)
    finally:
        if conn:
            conn.close()

def history_karyawan_dapur():
    conn = connect()
    cur = conn.cursor()

    try:
        bulan = int(input("Masukkan angka bulan (1-12): "))

        if bulan < 1 or bulan > 12:
            print("Bulan harus 1-12.")
            return

        query = """
        SELECT pk.tgl_pegiriman, 
               kar.nama_karyawan, 
               dpur.nama_dapur, 
               t.nama_tumbuhan, 
               dp.kuantitas, 
               pk.status_verifikasi
        FROM pengiriman_ki pk
        JOIN detail_pengiriman_ki dp USING(id_pengiriman)
        JOIN karyawan kar USING(id_karyawan)
        JOIN dapur_instansi dpur USING(id_dapur)
        JOIN tumbuhan t USING(id_tumbuhan)
        WHERE EXTRACT(MONTH FROM pk.tgl_pegiriman) = %s
        ORDER BY pk.tgl_pegiriman ASC
        """

        cur.execute(query, (bulan,))
        data = cur.fetchall()

        if not data:
            print("Tidak ada data pengiriman KD untuk bulan tersebut.")
            return

        headers = ["Tanggal", "Karyawan", "Dapur", "Barang", "Qty (Kg)", "Status"]
        print(tbl.tabulate(data, headers=headers, tablefmt="fancy_grid"))
        print()

    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        if conn:
            conn.close()


def menu_admin(user_session):

    # actv_id = user_session['id_asli']
    nama_admin=user_session['nama']

    while True:
     
        pilihan = questionary.select(
            f"Selamat datang {nama_admin}, Silakan pilih menu:",
            choices=[
                "1. Lihat data user",
                "2. Lihat pengiriman petani to karyawan",
                "3. Lihat pengiriman karyawan to instansi",
                "4. Keluar"
            ]
        ).ask()

<<<<<<< HEAD
        if pilihan == "1. Tambah data user":
            clear()
            tambah_user()

=======
        if pilihan == "1. Lihat data user":
            show_user()
>>>>>>> da4b977d5ae86f0e5e55eff39e3da3e34047091e
        elif pilihan == "2. Lihat pengiriman petani to karyawan":
            clear()
            history_petani_karyawan()
            input("Tekan Enter untuk kembali...")
            
        elif pilihan ==  "3. Lihat pengiriman karyawan to instansi":
            clear()
            history_karyawan_dapur()
            input("Tekan Enter untuk kembali...")

        elif pilihan == "4. Keluar":
            clear()
            logout(user_session)
        else:
            print("Pilihan tidak valid!")


dashboard()
login()