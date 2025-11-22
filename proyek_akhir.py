import psycopg2 as pg

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
                            
                            print(f"Selamat datang Petani {user_actv['nama']}")
                            print("Mau ngapain hari ini? ")
                            menu_petani()
                            return user_actv 
                        else:
                            print("Error: Data detail petani tidak ditemukan.")
                            break 
                    
                    elif result_role == 2: 
                         print("Login sebagai Karyawan")
                         break

        except Exception as e:
            print("Terjadi kesalahan sistem:", e)
            return None 
        
        finally:
            if conn:
                conn.close()  
def menu_petani(): 
    # actv_id=user_session['id_asli']
    # nama_petani=user_session['nama']

    while True:
        print("==== HALAMAN PETANI ====")
        print("1. Input Hasil Panen Baru")
        print("2. Lihat & Update Riwayat Panen")
        print("3. Keluar (Logout)")

        pilihan=input("pilih 1/2/3")

        if pilihan == '1':
            print("coba dulu")
        



print("======== AYo LOGIN DULU ============")
login()

