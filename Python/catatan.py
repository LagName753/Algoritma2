import csv
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_catatan():
    catatan_list = []
    with open('./Database/catatan.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            catatan_list.append(row)
    return catatan_list

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

def save_catatan(catatan_list):
    with open('./Database/catatan.csv', mode='w', newline='') as file:
        fieldnames = ['catatan_id', 'user_id', 'tanggal_pembuatan', 'detail_catatan', 'status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(catatan_list)

def aCatatan():
    while True:
        clear_screen()
        print("===== Kelola Catatan (Admin) =====")
        print("1. Lihat Daftar Catatan")
        print("2. Tambah Catatan")
        print("3. Edit Catatan")
        print("4. Hapus Catatan")
        print("5. Ubah Status Catatan")
        print("6. Kembali")
        
        pilihan = input("Pilih menu: ")
        catatan_list = load_catatan()
        
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
                    for item in catatan_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    keyword = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(catatan_list, keyword)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in catatan_list[0]:
                        hasil = insertion_sort_desc(catatan_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    keyword = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(catatan_list, keyword)
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
            print("Tambah Catatan Baru:")
            catatan_id = input("ID Catatan: ")
            user_id = input("User ID: ")
            detail_catatan = input("Detail Catatan: ")
            tanggal_pembuatan = datetime.now().strftime("%Y-%m-%d")
            status = input("Status (selamanya/belum selesai/sudah selesai): ")
            
            catatan_list.append({
                'catatan_id': catatan_id,
                'user_id': user_id,
                'tanggal_pembuatan': tanggal_pembuatan,
                'detail_catatan': detail_catatan,
                'status': status
            })
            save_catatan(catatan_list)
            print("Catatan berhasil ditambahkan")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3':
            clear_screen()
            print("Edit Catatan")
            catatan_id = input("Masukkan Catatan ID yang akan diedit: ")
            target = False
            for catatan in catatan_list:
                if catatan['catatan_id'] == catatan_id:
                    target = True
                    print(f"Data saat ini: Detail: {catatan['detail_catatan']}, Status: {catatan['status']}")
                    new_detail = input("Detail Catatan baru (kosongkan jika tidak diubah): ")
                    new_status = input("Status baru (selamanya/belum selesai/sudah selesai) (kosongkan jika tidak diubah): ")
                    
                    if new_detail:
                        catatan['detail_catatan'] = new_detail
                    if new_status:
                        catatan['status'] = new_status
                    
                    save_catatan(catatan_list)
                    print("Catatan berhasil diupdate.")
                    break
            if not target:
                print("Catatan dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Catatan")
            catatan_id = input("Masukkan Catatan ID yang akan dihapus: ")
            target = False
            for i, catatan in enumerate(catatan_list):
                if catatan['catatan_id'] == catatan_id:
                    target = True
                    confirm = input(f"Yakin menghapus catatan ID {catatan_id}? (y/n): ").lower()
                    if confirm == 'y':
                        del catatan_list[i]
                        save_catatan(catatan_list)
                        print("Catatan berhasil dihapus.")
                    break
            if not target:
                print("Catatan dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5':
            clear_screen()
            print("Ubah Status Catatan")
            catatan_id = input("Masukkan Catatan ID: ")
            target = False
            for catatan in catatan_list:
                if catatan['catatan_id'] == catatan_id:
                    target = True
                    print(f"Status saat ini: {catatan['status']}")
                    new_status = input("Masukkan status baru (selamanya/belum selesai/sudah selesai): ")
                    if new_status in ['selamanya', 'belum selesai', 'sudah selesai']:
                        catatan['status'] = new_status
                        save_catatan(catatan_list)
                        print("Status catatan berhasil diubah.")
                    else:
                        print("Status tidak valid.")
                    break
            if not target:
                print("Catatan dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '6':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kCatatan():
    while True:
        clear_screen()
        print("===== Catatan (Karyawan) =====")
        print("1. Lihat Daftar Catatan")
        print("2. Tambah Catatan")
        print("3. Kembali")
        
        pilihan = input("Pilih menu: ")
        catatan_list = load_catatan()
        
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
                    for item in catatan_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    keyword = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(catatan_list, keyword)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in catatan_list[0]:
                        hasil = insertion_sort_desc(catatan_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    keyword = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(catatan_list, keyword)
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
            print("Tambah Catatan Baru:")
            catatan_id = input("ID Catatan: ")
            user_id = input("User ID: ")
            detail_catatan = input("Detail Catatan: ")
            tanggal_pembuatan = datetime.now().strftime("%Y-%m-%d")
            status = input("Status (selamanya/belum selesai/sudah selesai): ")
            
            catatan_list.append({
                'catatan_id': catatan_id,
                'user_id': user_id,
                'tanggal_pembuatan': tanggal_pembuatan,
                'detail_catatan': detail_catatan,
                'status': status
            })
            save_catatan(catatan_list)
            print("Catatan berhasil ditambahkan")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '3':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")
            