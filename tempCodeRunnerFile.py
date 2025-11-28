
# # def menu_dapur(user_session):
#     id_dapur = user_session['id_asli'] 
#     nama_dapur = user_session['nama']
    
#     while True:
#         print(f"\n==== DASHBOARD DAPUR: {nama_dapur} ====")
#         print("1. Verifikasi Penerimaan Barang")
#         print("2. Lihat Riwayat Penerimaan")
#         print("3. Logout")
        
#         pilihan = input("Pilih: ")
        
#         if pilihan == '1':
#             verifikasi_penerimaan_dapur(id_dapur)
#         elif pilihan == '2':
#             lihat_history_dapur(id_dapur)
#         elif pilihan == '3':
#             logout(user_session)