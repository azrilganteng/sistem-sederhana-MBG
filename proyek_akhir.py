import psycopg2 as pg
from datetime import date
import tabulate as tbl
import questionary


#CONNECTION TO DATABASE
def connect():
    try:
        conn = pg.connect(
        host= "localhost",
        database= "SISTEM_MBG",
        user= "postgres",
        password = "12345678",
        port= ""
        )
        return conn
    except Exception as e:
        print("Terjadi kesalahan:", e)

#LOGIN FUNCTION
def login():
    while True:
        print("\n--- HALAMAN LOGIN ---")
        Username = input("masukkan username: ")
        password = input("masukkan password: ")
     
        try:
            conn = connect()
            with conn.cursor() as cur: 
                check_akun = """SELECT id_akun, id_role FROM akun
                                WHERE user_name = %s AND password = %s"""
                cur.execute(check_akun, (Username, password))
                result = cur.fetchone()
                
                if result is None:
                    print("Login Gagal: Username atau Password salah.")
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
            if conn:
                conn.close()

        except Exception as e:
            print("Terjadi kesalahan sistem:", e)
            return None 
#LOGOUT FUNCTION         
def logout(user_session):
    try:
        nama=user_session.get('nama','user')
        confirm=input("Yakin mau keluar? [Y/N]").lower().strip()
        if confirm == 'y':
            print(f"Sampai jumpa kembali, {nama}!")
            exit()
        else:
            print(" YAUDAH GAUSAH LOGOUT ")
        
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
            print(f"==== RIWAYAT PANEN  {nama_petani}")
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
                print("History Panen anda")
                header=["id panen","nama petani","nama tumbuhan","kuantitas (kg)","tanggal panen"]
                print(tbl.tabulate(show,headers=header,tablefmt="fancy_grid"))
                try:
                    print("1. update data")
                    print("2. kembali")
                    try:
                        input_update = input("Masukan pilihan kamu: ").strip()

                        if input_update == '1':
                            update(id_petani)
                            
                        elif input_update == '2':
                            menu_petani(user_session)
                    except ValueError:
                        print("ID harus berupa angka.")
                        return

                except Exception as e:
                    print("Terjadi kesalahan:", e)

        if conn:
            conn.close()


    except Exception as e:
        print("terjadi kesalahan: ",e)
        return None         
# ADD PANEN
def tambah_panen(id_petani):
    print("(Ketik 'stop' di nama tumbuhan jika sudah selesai)\n")

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
        print(f"-> Membuat ID Pengiriman: {id_pengiriman}")

       
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
            break 
#VERIFIKASI OLEH KARYAWAN
def verifikasi_panen(id_karyawan):
    conn=connect()
    with conn.cursor() as cur:
        try:
            print("\n==== VERIFIKASI PENGIRIMAN MASUK ====")
            q_pending = """SELECT p.id_pengiriman, pet.nama_petani, p.tgl_pengiriman, COUNT(dp.id_detail) as jumlah_item
            FROM pengiriman_pk p
            JOIN petani pet USING(id_petani)
            JOIN detail_pengiriman_pk dp USING(id_pengiriman)
            WHERE p.status_verifikasi = 'sedang dikirim' 
            GROUP BY p.id_pengiriman, pet.nama_petani, p.tgl_pengiriman
            ORDER BY p.tgl_pengiriman ASC"""
            cur.execute(q_pending)
            list_pending=cur.fetchall()

            if not list_pending :
                print("Tidak ada data yang perlu diverifikasi")
                return
            header=["No pengiriman","nama petani","tgl pengiriman","jumlah item"]
            print(tbl.tabulate(list_pending,headers=header,tablefmt="fancy_grid"))

            try:
                pilih=int(input("Pilih ID yang mau diverifikasi: "))
                cur.execute("select id_pengiriman from pengiriman_pk where id_pengiriman =%s AND status_verifikasi = 'sedang dikirim'",(pilih,))
                if not cur.fetchone():
                    print(f"ID {pilih} sudah diverifikasi")

                    handling_eror=input()
                    if handling_eror:
                        return

                q_detail_pk="""select t.id_tumbuhan, t.nama_tumbuhan,dp.kuantitas
                from detail_pengiriman_pk dp join panen p using(id_panen)
                join tumbuhan t using(id_tumbuhan)
                where dp.id_pengiriman=%s"""
                cur.execute(q_detail_pk,(pilih,))
                isi_detail=cur.fetchall()
                if not isi_detail:
                    print("Tidak ada detail pengiriman ditemukan.")
                else:
                    print("\nDetail Pengiriman:")
                    header = ["ID Tumbuhan", "Nama Barang", "Qty (Kg)"]
                    print(tbl.tabulate(isi_detail,headers=header,tablefmt="simple"))
                    confirm = input("\nVerifikasi dan masukkan ke Gudang? (y/n): ").lower()
                    if confirm != 'y':
                        print("Verifikasi dibatalkan.")
                        return
                    else:
                        transaksi_masuk=1
                        tgl=date.today()

                        for barang in isi_detail:
                            id_tumb = barang[0]
                            qty_masuk = barang[2]
                            id_gudang_target = None
                            cur.execute("SELECT id_gudang, stok FROM gudang WHERE id_tumubuhan = %s", (id_tumb,))
                            data_gudang = cur.fetchone()

                            if data_gudang:
                                id_gudang_target = data_gudang[0]
                                cur.execute("UPDATE gudang SET stok = stok + %s WHERE id_gudang = %s", (qty_masuk, id_gudang_target))
                            else:
                                cur.execute("""
                                INSERT INTO gudang (id_tumubuhan, stok) VALUES (%s, %s) 
                                RETURNING id_gudang
                            """, (id_tumb, qty_masuk))
                            id_gudang_target = cur.fetchone()[0]
                            q_distribusi = """INSERT INTO distribusi (tgl_distribusi, kuantitas, id_transaksi, id_gudang, id_karyawan)
                                    VALUES (%s, %s, %s, %s, %s)"""
                            cur.execute(q_distribusi,(tgl, qty_masuk, transaksi_masuk, id_gudang_target, id_karyawan))
                            cur.execute("""UPDATE pengiriman_pk SET status_verifikasi = 'Diterima', id_karyawan = %s 
                                WHERE id_pengiriman = %s""", (id_karyawan, pilih))
                            print(f"SUKSES! Pengiriman ID {pilih} telah diverifikasi.")
                            print("Transaksi tercatat di tabel Distribusi.")

                            conn.commit()
            except ValueError:
                print("input harus angka")
                return
            if conn:
                conn.close()
        except Exception as e:
            print(f"Error Sistem: {e}")
#CEK GUDANG
def gudang(id_karyawan,user_session):
    conn = connect()
    with conn.cursor() as cur:
        try:
            show_gudang="""SELECT t.id_tumbuhan, t.nama_tumbuhan, g.stok, pe.tgl_pengiriman
            FROM gudang g
            JOIN tumbuhan t ON g.id_tumubuhan = t.id_tumbuhan
            join panen p using (id_tumbuhan)
            join detail_pengiriman_pk dp using (id_panen)
            join pengiriman_pk pe using (id_pengiriman) 
            order by pe.tgl_pengiriman ASC"""
            cur.execute(show_gudang)
            show=cur.fetchall()
            if not show:
                print("Belum ada data di gudang")
                return
            headers = ["ID Barang", "Nama Komoditas", "Stok Tersedia (Kg)","tgl dikirim"]
            print(tbl.tabulate(show, headers=headers, tablefmt="fancy_grid"))
            print("Tekan enter untuk kembali ke menu")
            if input():
                return
                
        except Exception as e:
            print("Terjadi kesalahan",e)
    if conn:
        conn.close()
#KIRIM KE INSTANSI
def kirim_instansi():
    conn = connect() 
    cur = conn.cursor()

    
def menu_karyawan(user_session):
    actv_id = user_session['id_asli']
    nama_karyawan=user_session['nama']
    

    while True:
        pilihan = questionary.select(
            f"Selamat datang {nama_karyawan}, Silakan pilih menu:",
            choices=[
                "1. Verifikasi Hasil Panen",
                "2. Lihat Stok di Gudang",
                "3. Kirim Ke Dapur Instansi",
                "4. Kaluar"
            ]
        ).ask()
        if pilihan == "1. Verifikasi Hasil Panen":
            verifikasi_panen(actv_id)
        elif pilihan == "2. Lihat Stok di Gudang":
            gudang(actv_id,user_session)
        elif pilihan == "3. Kirim Ke Dapur Instansi":
            kirim_instansi(actv_id)
        elif pilihan == "4. Kaluar":
            logout(user_session)
            break
    
def admin():
    print("==== Halaman Admin ====")
    print("1. Tambah data petani baru")
    print("2. Tambah data karyawan baru")
    print("3. Tambah data instansi baru")

    pilihan=input("========= Mau ngapain nih? =========")

    if pilihan == "1":
        print("====== Tambah data petani baru =======")
        try:
            nama=input("masukkan nama petani baru: ")
            almt=input("masukkan alamat petani: ")
            tlpn=input("masukkan nomer telpon petani: ")
            usr=input("masukkan username login petani: ")
            pw=input("masukkan password login petani: ")

            conn=con.connect()
            with conn.cursor() as cur:
                query = "INSERT INTO petani(nama_petani,alamat,no_telpon,user_name,password)" \
                "VALUES (%s, %s, %s, %s, %s)"
                cur.execute(query,(nama,almt,tlpn,usr,pw))
            conn.commit()
            print("Data petani Berhasil ditambah")

        except Exception as e:
            print("Terjadi kesalahan:", e)
            
    elif pilihan == "2":
        print("====== Tambah data karyawan baru =======")
        try:
            nama=input("masukkan nama karyawan baru: ")
            almt=input("masukkan alamat karyawan: ")
            tlpn=input("masukkan nomer telpon karyawan: ")
            usr=input("masukkan username login karyawan: ")
            pw=input("masukkan password login karyawan: ")

            conn=con.connect()
            with conn.cursor() as cur:
                query = "INSERT INTO karyawan(nama_karyawan,alamat,no_telpon,user_name,password)" \
                "VALUES (%s, %s, %s, %s, %s)"
                cur.execute(query,(nama,almt,tlpn,usr,pw))
            conn.commit()
            print("Data karyawan Berhasil ditambah")

        except Exception as e:
            print("Terjadi kesalahan:", e)


print("======== AYO LOGIN DULU ============")
login()