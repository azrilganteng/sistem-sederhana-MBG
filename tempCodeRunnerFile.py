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
    print("halaman admin")
    

def login():
    while True:
        print("halaman login")
        Username= input("masukkan username: ")
        password= input("masukkan password: ")

        conn=connect()
    
        try:
            with conn.cursor() as cur:
                query = "SELECT * FROM login WHERE user_name = user_name AND password = password"
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

login()

