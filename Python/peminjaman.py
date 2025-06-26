import csv
import os
from datetime import datetime, timedelta

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_peminjaman():
    peminjaman_list = []
    with open('./Database/peminjaman.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            peminjaman_list.append(row)
    return peminjaman_list

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

def save_peminjaman(peminjaman_list):
    with open('./Database/peminjaman.csv', mode='w', newline='') as file:
        fieldnames = ['peminjaman_id', 'tanggal_peminjaman', 'tenggat_pengembalian', 
                     'tanggal_pengembalian', 'harga_peminjaman', 'member_id', 'user_id']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(peminjaman_list)

def aPeminjaman():
    while True:
        clear_screen()
        print("===== Kelola Peminjaman (Admin) =====")
        print("1. Lihat Daftar Peminjaman")
        print("2. Tambah Peminjaman")
        print("3. Edit Peminjaman")
        print("4. Hapus Peminjaman")
        print("5. Proses Pengembalian")
        print("6. Kembali")
        
        pilihan = input("Pilih menu: ")
        peminjaman_list = load_peminjaman()
        
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
                    for item in peminjaman_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    keyword = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(peminjaman_list, keyword)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in peminjaman_list[0]:
                        hasil = insertion_sort_desc(peminjaman_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    keyword = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(peminjaman_list, keyword)
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
            print("Tambah Peminjaman Baru:")
            peminjaman_id = input("ID Peminjaman: ")
            member_id = input("Member ID: ")
            user_id = input("User ID: ")
            tanggal_peminjaman = datetime.now().strftime("%Y-%m-%d")
            tenggat_pengembalian = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            harga_peminjaman = 5000
            
            peminjaman_list.append({
                'peminjaman_id': peminjaman_id,
                'tanggal_peminjaman': tanggal_peminjaman,
                'tenggat_pengembalian': tenggat_pengembalian,
                'tanggal_pengembalian': "",
                'harga_peminjaman': harga_peminjaman,
                'member_id': member_id,
                'user_id': user_id
            })
            save_peminjaman(peminjaman_list)
            print("Peminjaman berhasil ditambahkan")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3':
            clear_screen()
            print("Edit Peminjaman")
            peminjaman_id = input("Masukkan Peminjaman ID yang akan diedit: ")
            target = False
            for peminjaman in peminjaman_list:
                if peminjaman['peminjaman_id'] == peminjaman_id:
                    target = True
                    print(f"Data saat ini: Member ID: {peminjaman['member_id']}, User ID: {peminjaman['user_id']}, Tenggat: {peminjaman['tenggat_pengembalian']}")
                    new_member_id = input("Member ID baru (kosongkan jika tidak diubah): ")
                    new_user_id = input("User ID baru (kosongkan jika tidak diubah): ")
                    new_tenggat = input("Tenggat Pengembalian baru (YYYY-MM-DD) (kosongkan jika tidak diubah): ")
                    
                    if new_member_id:
                        peminjaman['member_id'] = new_member_id
                    if new_user_id:
                        peminjaman['user_id'] = new_user_id
                    if new_tenggat:
                        peminjaman['tenggat_pengembalian'] = new_tenggat
                    
                    save_peminjaman(peminjaman_list)
                    print("Peminjaman berhasil diupdate.")
                    break
            if not target:
                print("Peminjaman dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Peminjaman")
            peminjaman_id = input("Masukkan Peminjaman ID yang akan dihapus: ")
            target = False
            for i, peminjaman in enumerate(peminjaman_list):
                if peminjaman['peminjaman_id'] == peminjaman_id:
                    target = True
                    confirm = input(f"Yakin menghapus peminjaman ID {peminjaman_id}? (y/n): ").lower()
                    if confirm == 'y':
                        del peminjaman_list[i]
                        save_peminjaman(peminjaman_list)
                        print("Peminjaman berhasil dihapus.")
                    break
            if not target:
                print("Peminjaman dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        
        elif pilihan == '5':
            clear_screen()
            print("Proses Pengembalian Sederhana")
            peminjaman_id = input("Masukkan ID Peminjaman: ")
            tanggal_pengembalian = input("Masukkan Tanggal Pengembalian (YYYY-MM-DD): ")
            target = False

            for peminjaman in peminjaman_list:
                if peminjaman['peminjaman_id'] == peminjaman_id:
                    target = True
                    peminjaman['tanggal_pengembalian'] = tanggal_pengembalian
                    save_peminjaman(peminjaman_list)
                    print("Tanggal pengembalian berhasil dicatat.")
                    break

            if not target:
                print("Peminjaman dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        
        elif pilihan == '6':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kPeminjaman():
    while True:
        clear_screen()
        print("===== Peminjaman (Karyawan) =====")
        print("1. Lihat Daftar Peminjaman")
        print("2. Tambah Peminjaman")
        print("3. Proses Pengembalian")
        print("4. Kembali")
        
        pilihan = input("Pilih menu: ")
        peminjaman_list = load_peminjaman()
        
        if pilihan == '1':
            clear_screen()
            print("Daftar Peminjaman:")
            for peminjaman in peminjaman_list:
                print(f"ID: {peminjaman['peminjaman_id']}, Tanggal Pinjam: {peminjaman['tanggal_peminjaman']}, Tenggat: {peminjaman['tenggat_pengembalian']}, Pengembalian: {peminjaman['tanggal_pengembalian'] or '-'}, Harga: Rp{peminjaman['harga_peminjaman']}, Member ID: {peminjaman['member_id']}, User ID: {peminjaman['user_id']}")
            input("\nTekan Enter untuk kembali")
        
        elif pilihan == '2':
            clear_screen()
            print("Tambah Peminjaman Baru:")
            peminjaman_id = input("ID Peminjaman: ")
            member_id = input("Member ID: ")
            user_id = input("User ID: ")
            tanggal_peminjaman = datetime.now().strftime("%Y-%m-%d")
            tenggat_pengembalian = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            harga_peminjaman = 5000
            
            peminjaman_list.append({
                'peminjaman_id': peminjaman_id,
                'tanggal_peminjaman': tanggal_peminjaman,
                'tenggat_pengembalian': tenggat_pengembalian,
                'tanggal_pengembalian': "",
                'harga_peminjaman': harga_peminjaman,
                'member_id': member_id,
                'user_id': user_id
            })
            save_peminjaman(peminjaman_list)
            print("Peminjaman berhasil ditambahkan")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '4':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")
            