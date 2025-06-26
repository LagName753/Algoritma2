import csv
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_denda():
    denda_list = []
    with open('./Database/denda.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            denda_list.append(row)
    return denda_list

def linear_search(data, kunci):
    hasil = []
    for item in data:
        if kunci in str(item).lower():
            hasil.append(item)
    return hasil

def insertion_sort(data, kolom):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j][kolom] < key[kolom]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data

def save_denda(denda_list):
    with open('./Database/denda.csv', mode='w', newline='') as file:
        fieldnames = ['denda_id', 'jumlah_denda', 'tanggal_denda', 'status_denda', 'member_id', 'detail_id']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(denda_list)

def aDenda():
    while True:
        clear_screen()
        print("===== Kelola Denda (Admin) =====")
        print("1. Lihat Daftar Denda")
        print("2. Tambah Denda")
        print("3. Edit Denda")
        print("4. Hapus Denda")
        print("5. Ubah Status Denda")
        print("6. Kembali")
        
        pilihan = input("Pilih menu: ")
        denda_list = load_denda()
        
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
                    for item in denda_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kunci = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(denda_list, kunci)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in denda_list[0]:
                        hasil = insertion_sort(denda_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kunci = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(denda_list, kunci)
                    if hasil and kolom in hasil[0]:
                        hasil = insertion_sort(hasil, kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid atau tidak ada hasil.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '5':
                    break
        
        elif pilihan == '2':
            clear_screen()
            print("Tambah Denda Baru:")
            denda_id = input("ID Denda: ")
            jumlah_denda = input("Jumlah Denda: ")
            tanggal_denda = datetime.now().strftime("%Y-%m-%d")
            status_denda = "belum dibayar"
            member_id = input("Member ID: ")
            detail_id = input("Detail ID: ")
            
            denda_list.append({
                'denda_id': denda_id,
                'jumlah_denda': jumlah_denda,
                'tanggal_denda': tanggal_denda,
                'status_denda': status_denda,
                'member_id': member_id,
                'detail_id': detail_id
            })
            save_denda(denda_list)
            print("Denda berhasil ditambahkan")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '3':
            clear_screen()
            print("Edit Denda")
            denda_id = input("Masukkan ID Denda yang akan diedit: ")
            target = False
            for denda in denda_list:
                if denda['denda_id'] == denda_id:
                    target = True
                    print(f"Data saat ini: Jumlah: Rp{denda['jumlah_denda']}, Status: {denda['status_denda']}, Member ID: {denda['member_id']}, Detail ID: {denda['detail_id']}")
                    new_jumlah = input("Jumlah Denda baru (kosongkan jika tidak diubah): ")
                    new_status = input("Status baru (kosongkan jika tidak diubah): ")
                    new_member_id = input("Member ID baru (kosongkan jika tidak diubah): ")
                    new_detail_id = input("Detail ID baru (kosongkan jika tidak diubah): ")
                    
                    if new_jumlah:
                        denda['jumlah_denda'] = new_jumlah
                    if new_status:
                        denda['status_denda'] = new_status
                    if new_member_id:
                        denda['member_id'] = new_member_id
                    if new_detail_id:
                        denda['detail_id'] = new_detail_id
                    
                    save_denda(denda_list)
                    print("Denda berhasil diupdate.")
                    break
            if not target:
                print("Denda dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Denda")
            denda_id = input("Masukkan ID Denda yang akan dihapus: ")
            target = False
            for i, denda in enumerate(denda_list):
                if denda['denda_id'] == denda_id:
                    target = True
                    confirm = input(f"Yakin menghapus denda ID {denda_id}? (y/n): ").lower()
                    if confirm == 'y':
                        del denda_list[i]
                        save_denda(denda_list)
                        print("Denda berhasil dihapus.")
                    break
            if not target:
                print("Denda dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5':
            clear_screen()
            print("Ubah Status Denda")
            denda_id = input("Masukkan ID Denda: ")
            target = False
            for denda in denda_list:
                if denda['denda_id'] == denda_id:
                    target = True
                    print(f"Status saat ini: {denda['status_denda']}")
                    new_status = input("Masukkan status baru (lunas/belum dibayar): ").lower()
                    if new_status in ['lunas', 'belum dibayar']:
                        denda['status_denda'] = new_status
                        save_denda(denda_list)
                        print("Status denda berhasil diubah.")
                    else:
                        print("Status tidak valid. Gunakan 'lunas' atau 'belum dibayar'.")
                    break
            if not target:
                print("Denda dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '6':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kDenda():
    while True:
        clear_screen()
        print("===== Lihat Data =====")
        print("1. Lihat Semua Data")
        print("2. Cari Data (Linear Search)")
        print("3. Urutkan Data Menurun (Insertion Sort)")
        print("4. Cari + Urutkan")
        print("5. Kembali")
        pilihan2 = input("Pilih opsi: ")
        denda_list = load_denda()

        if pilihan2 == '1':
            for item in denda_list:
                print(item)
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '2':
            kunci = input("Masukkan kata kunci: ").lower()
            hasil = linear_search(denda_list, kunci)
            for item in hasil:
                print(item)
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '3':
            kolom = input("Kolom untuk sorting: ")
            if kolom in denda_list[0]:
                hasil = insertion_sort(denda_list.copy(), kolom)
                for item in hasil:
                    print(item)
            else:
                print("Kolom tidak valid.")
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '4':
            kunci = input("Masukkan kata kunci: ").lower()
            kolom = input("Kolom untuk sorting: ")
            hasil = linear_search(denda_list, kunci)
            if hasil and kolom in hasil[0]:
                hasil = insertion_sort(hasil, kolom)
                for item in hasil:
                    print(item)
            else:
                print("Kolom tidak valid atau tidak ada hasil.")
                input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '5':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")
