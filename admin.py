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

 



def history_petani_ke_karyawan():
    conn = connect()
    cur = conn.cursor()

    bulan = input("Masukkan bulan (1-12): ")

    query = """
    SELECT p.nama_petani, k.nama_karyawan, t.jenis_tumbuhan, peng.tanggal_pengiriman
    FROM pengiriman_petani_karyawan peng
    JOIN petani p ON peng.id_petani = p.id_petani
    JOIN karyawan k ON peng.id_karyawan = k.id_karyawan
    JOIN tumbuhan t ON peng.id_tumbuhan = t.id_tumbuhan
    WHERE EXTRACT(MONTH FROM peng.tanggal_pengiriman) = %s
    ORDER BY peng.tanggal_pengiriman ASC;
    """

    cur.execute(query, (bulan,))
    data = cur.fetchall()

    print("\n=== History Pengiriman Petani → Karyawan ===")
    for d in data:
        print(f"Petani: {d[0]} | Karyawan: {d[1]} | Tumbuhan: {d[2]} | Tanggal: {d[3]}")



def history_karyawan_ke_instansi():
    conn = connect()
    cur = conn.cursor()

    bulan = input("Masukkan bulan (1-12): ")

    query = """
    SELECT k.nama_karyawan, i.nama_instansi, g.jenis_tumbuhan, peng.tanggal_pengiriman
    FROM pengiriman_karyawan_instansi peng
    JOIN karyawan k ON peng.id_karyawan = k.id_karyawan
    JOIN instansi i ON peng.id_instansi = i.id_instansi
    JOIN tumbuhan g ON peng.id_tumbuhan = g.id_tumbuhan
    WHERE EXTRACT(MONTH FROM peng.tanggal_pengiriman) = %s
    ORDER BY peng.tanggal_pengiriman ASC;
    """

    cur.execute(query, (bulan,))
    data = cur.fetchall()

    print("\n=== History Pengiriman Karyawan → Instansi ===")
    for d in data:
        print(f"Karyawan: {d[0]} | Instansi: {d[1]} | Tumbuhan: {d[2]} | Tanggal: {d[3]}")

