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

            conn=connect()
            with conn.cursor() as cur:
                query = "INSERT INTO petani(nama_petani,alamat,no_hp,user_name,password)" \
                "VALUES (%s, %s, %s, %s, %s)"
                cur.execute(query,(nama,almt,tlpn,usr,pw))
            conn.commit()
            print("Data petani Berhasil ditambah")

        except Exception as e:
            print("Terjadi kesalahan:", e)
       
def login():
    while True:
        print("halaman login")
        Username= input("masukkan username: ")
        password= input("masukkan password: ")

        
        try:
            conn=connect()
            with conn.cursor() as cur:
                query = "SELECT * FROM admin WHERE user_name = %s AND password = %s"
                cur.execute(query,(Username,password))

                result = cur.fetchone()
                if result:
                    admin()
                    break
                else:
                    print("username atau password salah")
        except Exception as e:
            print("Terjadi kesalahan:", e)

            conn.close()
print("======== AYo LOGIN DULU ============")
login()

