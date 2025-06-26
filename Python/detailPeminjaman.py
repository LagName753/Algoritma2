import csv
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_detail_peminjaman():
    detail_list = []
    with open('./Database/detail_peminjaman.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            detail_list.append(row)
    return detail_list

def linear_search(data, kunci):
    hasil = []
    for item in data:
        if kunci in str(item).lower():
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

def save_detail_peminjaman(detail_list):
    with open('./Database/detail_peminjaman.csv', mode='w', newline='') as file:
        fieldnames = ['detail_id', 'peminjaman_id', 'buku_id', 'status_peminjaman']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(detail_list)

def aDetailPeminjaman():
    while True:
        clear_screen()
        print("===== Kelola Detail Peminjaman (Admin) =====")
        print("1. Lihat Detail Peminjaman")
        print("2. Tambah Detail Peminjaman")
        print("3. Edit Detail Peminjaman")
        print("4. Hapus Detail Peminjaman")
        print("5. Ubah Status Peminjaman")
        print("6. Kembali")
        
        pilihan = input("Pilih menu: ")
        detail_list = load_detail_peminjaman()
        
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
                    for item in detail_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kunci = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(detail_list, kunci)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in detail_list[0]:
                        hasil = insertion_sort_desc(detail_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kunci = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(detail_list, kunci)
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
            print("Tambah Detail Peminjaman Baru:")
            detail_id = input("Detail ID: ")
            peminjaman_id = input("Peminjaman ID: ")
            buku_id = input("Buku ID: ")
            status_peminjaman = input("Status Peminjaman (dipinjam/dikembalikan/terlambat): ")
            
            detail_list.append({
                'detail_id': detail_id,
                'peminjaman_id': peminjaman_id,
                'buku_id': buku_id,
                'status_peminjaman': status_peminjaman
            })
            save_detail_peminjaman(detail_list)
            print("Detail Peminjaman berhasil ditambahkan")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '3':
            clear_screen()
            print("Edit Detail Peminjaman")
            detail_id = input("Masukkan Detail ID yang akan diedit: ")
            target = False
            for detail in detail_list:
                if detail['detail_id'] == detail_id:
                    target = True
                    print(f"Data saat ini: Peminjaman ID: {detail['peminjaman_id']}, Buku ID: {detail['buku_id']}, Status: {detail['status_peminjaman']}")
                    new_peminjaman_id = input("Peminjaman ID baru (kosongkan jika tidak diubah): ")
                    new_buku_id = input("Buku ID baru (kosongkan jika tidak diubah): ")
                    status = input("Status baru (kosongkan jika tidak diubah): ")
                    
                    if new_peminjaman_id:
                        detail['peminjaman_id'] = new_peminjaman_id
                    if new_buku_id:
                        detail['buku_id'] = new_buku_id
                    if status:
                        detail['status_peminjaman'] = status
                    
                    save_detail_peminjaman(detail_list)
                    print("Detail Peminjaman berhasil diupdate.")
                    break
            if not target:
                print("Detail dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Detail Peminjaman")
            detail_id = input("Masukkan Detail ID yang akan dihapus: ")
            target = False
            for i, detail in enumerate(detail_list):
                if detail['detail_id'] == detail_id:
                    target = True
                    confirm = input(f"Yakin menghapus detail ID {detail_id}? (y/n): ").lower()
                    if confirm == 'y':
                        del detail_list[i]
                        save_detail_peminjaman(detail_list)
                        print("Detail Peminjaman berhasil dihapus.")
                    break
            if not target:
                print("Detail dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5':
            clear_screen()
            print("Ubah Status Peminjaman")
            detail_id = input("Masukkan Detail ID: ")
            target = False
            for detail in detail_list:
                if detail['detail_id'] == detail_id:
                    target = True
                    print(f"Status saat ini: {detail['status_peminjaman']}")
                    status = input("Masukkan status baru (dipinjam/dikembalikan/terlambat): ")
                    if status in ['dipinjam', 'dikembalikan', 'terlambat']:
                        detail['status_peminjaman'] = status
                        save_detail_peminjaman(detail_list)
                        print("Status berhasil diubah.")
                    else:
                        print("Status tidak valid.")
                    break
            if not target:
                print("Detail dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '6':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan...")

def kDetailPeminjaman():
    while True:
        clear_screen()
        print("===== Detail Peminjaman (Karyawan) =====")
        print("1. Lihat Detail Peminjaman")
        print("2. Tambah Detail Peminjaman")
        print("3. Kembali")
        
        pilihan = input("Pilih menu: ")
        detail_list = load_detail_peminjaman()
        
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
                    for item in detail_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kunci = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(detail_list, kunci)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in detail_list[0]:
                        hasil = insertion_sort_desc(detail_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kunci = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(detail_list, kunci)
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
            print("Tambah Detail Peminjaman Baru:")
            detail_id = input("Detail ID: ")
            peminjaman_id = input("Peminjaman ID: ")
            buku_id = input("Buku ID: ")
            status_peminjaman = input("Status Peminjaman (dipinjam/dikembalikan/terlambat): ")
            
            detail_list.append({
                'detail_id': detail_id,
                'peminjaman_id': peminjaman_id,
                'buku_id': buku_id,
                'status_peminjaman': status_peminjaman
            })
            save_detail_peminjaman(detail_list)
            print("Detail Peminjaman berhasil ditambahkan")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")
            