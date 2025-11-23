#UPDATE FUNCTION
def update_panen(id_petani,user_session):
    nama_petani=user_session['nama']
    try:
        conn = connect()
        with conn.cursor() as cur:
            print(f"==== RIWAYAT PANEN  {nama_petani}")
            read_data="""SELECT p.id_petani,p.nama_petani,t.nama_tumbuhan,pa.kuantitas,pa.tgl_panen
                from petani p join panen pa using(id_petani)
                JOIN tumbuhan t using(id_tumbuhan)
                WHERE p.id_petani = %s
                ORDER BY pa.tgl_panen"""
            cur.execute(read_data,(id_petani,))
    except Exception as e:
        print("terjadi kesalahan: ",e)
        return None