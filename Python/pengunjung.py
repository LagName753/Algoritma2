import csv
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_pengunjung():
    pengunjung_list = []
    with open('./Database/pengunjung.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pengunjung_list.append(row)
    return pengunjung_list

def linear_search(data, keyword):
    hasil = []
    for item in data:
        if keyword in str(item).lower():
            hasil.append(item)
    return hasil

def insertion_sort_desc(data, kolom):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j][kolom] < key[kolom]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data

def save_pengunjung(pengunjung_list):
    with open('./Database/pengunjung.csv', mode='w', newline='') as file:
        fieldnames = ['pengunjung_id', 'nama', 'asal_instansi', 'tujuan_kunjungan', 'waktu_masuk', 'waktu_keluar']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pengunjung_list)

def aPengunjung():
    while True:
        clear_screen()
        print("===== Kelola Pengunjung (Admin) =====")
        print("1. Lihat Daftar Pengunjung")
        print("2. Tambah Pengunjung")
        print("3. Edit Pengunjung")
        print("4. Hapus Pengunjung")
        print("5. Catat Keberangkatan")
        print("6. Kembali")
        
        pilihan = input("Pilih menu: ")
        pengunjung_list = load_pengunjung()
        
        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Linear Search)")
                print("3. Urutkan Data Menurun (Insertion Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in pengunjung_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    keyword = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(pengunjung_list, keyword)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in pengunjung_list[0]:
                        hasil = insertion_sort_desc(pengunjung_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    keyword = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(pengunjung_list, keyword)
                    if hasil and kolom in hasil[0]:
                        hasil = insertion_sort_desc(hasil, kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid atau tidak ada hasil.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '5':
                    break
        
        elif pilihan == '2':
            clear_screen()
            print("Tambah Pengunjung Baru:")
            pengunjung_id = input("ID Pengunjung: ")
            nama = input("Nama: ")
            asal_instansi = input("Asal Instansi: ")
            tujuan_kunjungan = input("Tujuan Kunjungan: ")
            waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            pengunjung_list.append({
                'pengunjung_id': pengunjung_id,
                'nama': nama,
                'asal_instansi': asal_instansi,
                'tujuan_kunjungan': tujuan_kunjungan,
                'waktu_masuk': waktu_masuk,
                'waktu_keluar': ""
            })
            save_pengunjung(pengunjung_list)
            print("Pengunjung berhasil dicatat")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3':
            clear_screen()
            print("Edit Pengunjung")
            pengunjung_id = input("Masukkan Pengunjung ID yang akan diedit: ")
            dtarget = False
            for pengunjung in pengunjung_list:
                if pengunjung['pengunjung_id'] == pengunjung_id:
                    dtarget = True
                    print(f"Data saat ini: Nama: {pengunjung['nama']}, Asal Instansi: {pengunjung['asal_instansi']}, Tujuan: {pengunjung['tujuan_kunjungan']}")
                    new_nama = input("Nama baru (kosongkan jika tidak diubah): ")
                    new_asal = input("Asal Instansi baru (kosongkan jika tidak diubah): ")
                    new_tujuan = input("Tujuan Kunjungan baru (kosongkan jika tidak diubah): ")
                    
                    if new_nama:
                        pengunjung['nama'] = new_nama
                    if new_asal:
                        pengunjung['asal_instansi'] = new_asal
                    if new_tujuan:
                        pengunjung['tujuan_kunjungan'] = new_tujuan
                    
                    save_pengunjung(pengunjung_list)
                    print("Pengunjung berhasil diupdate.")
                    break
            if not dtarget:
                print("Pengunjung dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Pengunjung")
            pengunjung_id = input("Masukkan Pengunjung ID yang akan dihapus: ")
            dtarget = False
            for i, pengunjung in enumerate(pengunjung_list):
                if pengunjung['pengunjung_id'] == pengunjung_id:
                    dtarget = True
                    confirm = input(f"Yakin menghapus pengunjung ID {pengunjung_id}? (y/n): ").lower()
                    if confirm == 'y':
                        del pengunjung_list[i]
                        save_pengunjung(pengunjung_list)
                        print("Pengunjung berhasil dihapus.")
                    break
            if not dtarget:
                print("Pengunjung dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5': 
            clear_screen()
            print("Catat Keberangkatan Pengunjung")
            pengunjung_id = input("Masukkan Pengunjung ID: ")
            dtarget = False
            for pengunjung in pengunjung_list:
                if pengunjung['pengunjung_id'] == pengunjung_id:
                    dtarget = True
                    if not pengunjung['waktu_keluar']:
                        pengunjung['waktu_keluar'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_pengunjung(pengunjung_list)
                        print("Keberangkatan berhasil dicatat.")
                    else:
                        print("Pengunjung ini sudah dicatat keberangkatannya.")
                    break
            if not dtarget:
                print("Pengunjung dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '6':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kPengunjung():
    while True:
        clear_screen()
        print("===== Pengunjung (Karyawan) =====")
        print("1. Lihat Daftar Pengunjung")
        print("2. Tambah Pengunjung")
        print("3. Catat Keberangkatan")
        print("4. Kembali")
        
        pilihan = input("Pilih menu: ")
        pengunjung_list = load_pengunjung()
        
        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Linear Search)")
                print("3. Urutkan Data Menurun (Insertion Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in pengunjung_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    keyword = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(pengunjung_list, keyword)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in pengunjung_list[0]:
                        hasil = insertion_sort_desc(pengunjung_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    keyword = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(pengunjung_list, keyword)
                    if hasil and kolom in hasil[0]:
                        hasil = insertion_sort_desc(hasil, kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid atau tidak ada hasil.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '5':
                    break
        
        elif pilihan == '2':
            clear_screen()
            print("Tambah Pengunjung Baru:")
            pengunjung_id = input("ID Pengunjung: ")
            nama = input("Nama: ")
            asal_instansi = input("Asal Instansi: ")
            tujuan_kunjungan = input("Tujuan Kunjungan: ")
            waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            pengunjung_list.append({
                'pengunjung_id': pengunjung_id,
                'nama': nama,
                'asal_instansi': asal_instansi,
                'tujuan_kunjungan': tujuan_kunjungan,
                'waktu_masuk': waktu_masuk,
                'waktu_keluar': ""
            })
            save_pengunjung(pengunjung_list)
            print("Pengunjung berhasil dicatat")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '4':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")
