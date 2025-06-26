import csv
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_buku():
    buku_list = []
    with open('./Database/buku.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            buku_list.append(row)
    return buku_list

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

def save_buku(buku_list):
    with open('./Database/buku.csv', mode='w', newline='') as file:
        fieldnames = ['buku_id', 'judul_buku', 'isbn', 'tahun_terbit', 'penerbit', 'genre_id', 'status_buku']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(buku_list)

def aMenu():
    while True:
        clear_screen()
        print("===== Kelola Buku (Admin) =====")
        print("1. Lihat Daftar Buku")
        print("2. Tambah Buku")
        print("3. Edit Buku")
        print("4. Hapus Buku")
        print("5. Ubah Status Buku")
        print("6. Cari Buku")
        print("7. Kembali")
        
        pilihan = input("Pilih menu: ")
        buku_list = load_buku()
        
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
                    for item in buku_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    keyword = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(buku_list, keyword)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in buku_list[0]:
                        hasil = insertion_sort_desc(buku_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    keyword = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(buku_list, keyword)
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
            print("Tambah Buku Baru:")
            buku_id = input("ID Buku: ")
            judul_buku = input("Judul Buku: ")
            isbn = input("ISBN: ")
            tahun_terbit = input("Tahun Terbit: ")
            penerbit = input("Penerbit: ")
            genre_id = input("Genre ID: ")
            status_buku = input("Status Buku (ada/tidak ada): ")
            
            buku_list.append({
                'buku_id': buku_id,
                'judul_buku': judul_buku,
                'isbn': isbn,
                'tahun_terbit': tahun_terbit,
                'penerbit': penerbit,
                'genre_id': genre_id,
                'status_buku': status_buku
            })
            save_buku(buku_list)
            print("Buku berhasil ditambahkan")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3':
            clear_screen()
            print("Edit Buku")
            buku_id = input("Masukkan Buku ID yang akan diedit: ")
            target = False
            for buku in buku_list:
                if buku['buku_id'] == buku_id:
                    target = True
                    print(f"Data saat ini: Judul: {buku['judul_buku']}, ISBN: {buku['isbn']}, Tahun: {buku['tahun_terbit']}, Penerbit: {buku['penerbit']}, Genre ID: {buku['genre_id']}, Status: {buku['status_buku']}")
                    new_judul = input("Judul baru (kosongkan jika tidak diubah): ")
                    new_isbn = input("ISBN baru (kosongkan jika tidak diubah): ")
                    new_tahun = input("Tahun Terbit baru (kosongkan jika tidak diubah): ")
                    new_penerbit = input("Penerbit baru (kosongkan jika tidak diubah): ")
                    new_genre = input("Genre ID baru (kosongkan jika tidak diubah): ")
                    status = input("Status baru (ada/tidak ada) (kosongkan jika tidak diubah): ")
                    
                    if new_judul:
                        buku['judul_buku'] = new_judul
                    if new_isbn:
                        buku['isbn'] = new_isbn
                    if new_tahun:
                        buku['tahun_terbit'] = new_tahun
                    if new_penerbit:
                        buku['penerbit'] = new_penerbit
                    if new_genre:
                        buku['genre_id'] = new_genre
                    if status:
                        buku['status_buku'] = status
                    
                    save_buku(buku_list)
                    print("Buku berhasil diupdate.")
                    break
            if not target:
                print("Buku dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Buku")
            buku_id = input("Masukkan Buku ID yang akan dihapus: ")
            target = False
            for i, buku in enumerate(buku_list):
                if buku['buku_id'] == buku_id:
                    target = True
                    konfirmasi = input(f"Yakin menghapus buku ID {buku_id}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        del buku_list[i]
                        save_buku(buku_list)
                        print("Buku berhasil dihapus.")
                    break
            if not target:
                print("Buku dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5':
            clear_screen()
            print("Ubah Status Buku")
            buku_id = input("Masukkan Buku ID: ")
            target = False
            for buku in buku_list:
                if buku['buku_id'] == buku_id:
                    target = True
                    print(f"Status saat ini: {buku['status_buku']}")
                    status = input("Masukkan status baru (ada/tidak ada): ").lower()
                    if status in ['ada', 'tidak ada']:
                        buku['status_buku'] = status
                        save_buku(buku_list)
                        print("Status buku berhasil diubah.")
                    else:
                        print("Status tidak valid. Gunakan 'ada' atau 'tidak ada'.")
                    break
            if not target:
                print("Buku dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '6':
            clear_screen()
            keyword = input("Masukkan kata kunci pencarian (judul/ISBN/penerbit): ").lower()
            hasil2 = []
            for buku in buku_list:
                if (keyword in buku['judul_buku'].lower() or 
                    keyword in buku['isbn'].lower() or 
                    keyword in buku['penerbit'].lower()):
                    hasil2.append(buku)
            
            if hasil2:
                print("Hasil Pencarian:")
                for buku in hasil2:
                    print(f"ID: {buku['buku_id']}, Judul: {buku['judul_buku']}, ISBN: {buku['isbn']}, Tahun: {buku['tahun_terbit']}, Penerbit: {buku['penerbit']}, Genre ID: {buku['genre_id']}, Status: {buku['status_buku']}")
            else:
                print("Tidak ditemukan buku dengan kata kunci tersebut.")
            input("\nTekan Enter untuk kembali")
        
        elif pilihan == '7':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kMenu():
    while True:
        clear_screen()
        print("===== Lihat Data =====")
        print("1. Lihat Semua Data")
        print("2. Cari Data (Linear Search)")
        print("3. Urutkan Data Menurun (Insertion Sort)")
        print("4. Cari + Urutkan")
        print("5. Kembali")
        pilihan2 = input("Pilih opsi: ")
        buku_list = load_buku()

        if pilihan2 == '1':
            for item in buku_list:
                print(item)
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '2':
            keyword = input("Masukkan kata kunci: ").lower()
            hasil = linear_search(buku_list, keyword)
            for item in hasil:
                print(item)
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '3':
            kolom = input("Kolom untuk sorting: ")
            if kolom in buku_list[0]:
                hasil = insertion_sort_desc(buku_list.copy(), kolom)
                for item in hasil:
                    print(item)
            else:
                print("Kolom tidak valid.")
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '4':
            keyword = input("Masukkan kata kunci: ").lower()
            kolom = input("Kolom untuk sorting: ")
            hasil = linear_search(buku_list, keyword)
            if hasil and kolom in hasil[0]:
                hasil = insertion_sort_desc(hasil, kolom)
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
            