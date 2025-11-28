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

 

def verifikasi_penerimaan_dapur(id_dapur):
    conn = connect()
    cur = conn.cursor()
    try:
        print("\n--- BARANG MASUK (PENDING) ---")
   
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
        
        try:
            pilih = int(input("Masukkan ID Pengiriman untuk diterima: "))
        except: return

        cur.execute("""
            SELECT t.nama_tumbuhan, dp.kuantitas 
            FROM detail_pengiriman_ki dp
            JOIN tumbuhan t USING(id_tumbuhan)
            WHERE dp.id_pengiriman = %s
        """, (pilih,))
        items = cur.fetchall()
        print(tbl.tabulate(items, headers=["Barang", "Qty"], tablefmt="simple"))
        
        if input("Terima barang ini? (y/n): ").lower() == 'y':
           
            cur.execute("UPDATE pengiriman_ki SET status_verifikasi = 'Diterima' WHERE id_pengiriman = %s", (pilih,))
            conn.commit()
            print("Barang diterima!")
            
    except Exception as e:
        print("Error:", e)
    finally: conn.close()

def lihat_history_dapur(id_dapur):
    conn = connect()
    cur = conn.cursor()
    try:
        print("\n--- RIWAYAT PENERIMAAN ---")
        q_hist = """
            SELECT pk.tgl_pegiriman, t.nama_tumbuhan, dp.kuantitas, pk.status_verifikasi
            FROM pengiriman_ki pk
            JOIN detail_pengiriman_ki dp USING(id_pengiriman)
            JOIN tumbuhan t USING(id_tumbuhan)
            WHERE pk.id_dapur = %s AND pk.status_verifikasi = 'Diterima'
            ORDER BY pk.tgl_pegiriman DESC
        """
        cur.execute(q_hist, (id_dapur,))
        data = cur.fetchall()
        
        if not data:
            print("Belum ada riwayat.")
        else:
            print(tbl.tabulate(data, headers=["Tanggal", "Barang", "Qty", "Status"], tablefmt="fancy_grid"))
            input("Enter kembali...")
    finally: conn.close()