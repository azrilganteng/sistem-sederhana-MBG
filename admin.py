import psycopg2 as pg
import connection as con

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

 



