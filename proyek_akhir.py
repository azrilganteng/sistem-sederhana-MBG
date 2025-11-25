import psycopg2 as pg
from datetime import date
import tabulate as tbl


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
                         print("Login sebagai Karyawan")
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
    try:
        conn = connect()
        with conn.cursor() as cur:
            input_tumbuhan = input("masukkan nama tumbuhan: ").lower().strip()
            srch_by_name = """select id_tumbuhan,nama_tumbuhan from tumbuhan where nama_tumbuhan ilike %s"""
            cur.execute(srch_by_name, (input_tumbuhan,))
            result = cur.fetchone()
            id_tumbuhan_fix = None

            if result:
                id_tumbuhan_fix = result[0]
                print(f"Data ditemukan: {result[1]} (ID: {id_tumbuhan_fix})")
            else:
                id_tumbuhan_fix=add_nutrisi(input_tumbuhan)

            kuantitas = int(input("Kuantitas barang: "))
            tgl = input("Tanggal panen (yyyy-mm-dd) [Tekan enter]: ")
            
            if not tgl:
                tgl = date.today()

            add_data = """INSERT INTO panen (id_petani, id_tumbuhan, kuantitas, tgl_panen) VALUES (%s, %s, %s, %s)"""
            cur.execute(add_data, (id_petani, id_tumbuhan_fix, kuantitas, tgl))
            conn.commit()
            print("Data berhasil disimpan")

        if conn:
            conn.close()

    except Exception as e:
        print("Terjadi kesalahan sistem:", e)
        return None
#PETANI FUNCTION
def menu_petani(user_session):

    actv_id=user_session['id_asli']
    nama_petani=user_session['nama']

    while True:
        print(f"selamat datang {nama_petani}")
        print("==== HALAMAN PETANI ====")
        print("1. Input Hasil Panen Baru")
        print("2. Lihat & Update Riwayat Panen")
        print("3. Keluar (Logout)")

        pilihan=input("pilih 1/2/3")

        if pilihan == '1':
            tambah_panen(actv_id)
        elif pilihan == '2':
            show(actv_id,user_session)#beta version 
        elif pilihan == '3':
            logout(user_session)
        
print("======== AYO LOGIN DULU ============")
login()

