import csv
import os
import math

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_buku():
    buku_list = []
    try:
        with open('./Database/buku.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['jumlah_peminjaman'] = int(row.get('jumlah_peminjaman', 0))
                row['posisi_lantai'] = int(row.get('posisi_lantai', 0))
                row['posisi_rak'] = row.get('posisi_rak', '')
                row['posisi_nomor'] = int(row.get('posisi_nomor', 0))
                row['bobot'] = int(row.get('bobot', 1))
                buku_list.append(row)
    except FileNotFoundError:
        print("File buku.csv tidak ditemukan. Membuat file baru.")
        save_buku([])
    return buku_list

def save_buku(buku_list):
    fieldnames = ['buku_id', 'judul_buku', 'isbn', 'tahun_terbit', 'penerbit', 'genre_id', 
                  'status_buku', 'jumlah_peminjaman', 'posisi_lantai', 'posisi_rak', 'posisi_nomor', 'bobot']
    with open('./Database/buku.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(buku_list)

def merge_sort_desc(data, kolom):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left_half = data[:mid]
    right_half = data[mid:]

    left_half = merge_sort_desc(left_half, kolom)
    right_half = merge_sort_desc(right_half, kolom)

    return merge(left_half, right_half, kolom)

def merge(left, right, kolom):
    merged = []
    left_idx = 0
    right_idx = 0

    while left_idx < len(left) and right_idx < len(right):
        try:
            val_left = int(left[left_idx][kolom])
            val_right = int(right[right_idx][kolom])
            if val_left >= val_right:
                merged.append(left[left_idx])
                left_idx += 1
            else:
                merged.append(right[right_idx])
                right_idx += 1
        except ValueError:
            if str(left[left_idx][kolom]) >= str(right[right_idx][kolom]):
                merged.append(left[left_idx])
                left_idx += 1
            else:
                merged.append(right[right_idx])
                right_idx += 1

    while left_idx < len(left):
        merged.append(left[left_idx])
        left_idx += 1

    while right_idx < len(right):
        merged.append(right[right_idx])
        right_idx += 1

    return merged

def binary_search(data, key_column, target_value):

    low = 0
    high = len(data) - 1
    found_items = []

    while low <= high:
        mid = (low + high) // 2
        current_item_value = data[mid][key_column]

        try:
            if int(current_item_value) == int(target_value):
                left = mid
                while left >= 0 and int(data[left][key_column]) == int(target_value):
                    found_items.append(data[left])
                    left -= 1
                right = mid + 1
                while right < len(data) and int(data[right][key_column]) == int(target_value):
                    found_items.append(data[right])
                    right += 1
                return list({frozenset(d.items()) for d in found_items})
            elif int(current_item_value) < int(target_value):
                low = mid + 1
            else:
                high = mid - 1
        except ValueError:
            if str(current_item_value).lower() == str(target_value).lower():
                left = mid
                while left >= 0 and str(data[left][key_column]).lower() == str(target_value).lower():
                    found_items.append(data[left])
                    left -= 1
                right = mid + 1
                while right < len(data) and str(data[right][key_column]).lower() == str(target_value).lower():
                    found_items.append(data[right])
                    right += 1
                return list({frozenset(d.items()) for d in found_items})
            elif str(current_item_value).lower() < str(target_value).lower():
                low = mid + 1
            else:
                high = mid - 1
    return found_items

def calculate_books_weight(selected_book_ids, all_buku_list):
    total_weight = 0
    for buku_id in selected_book_ids:
        for buku in all_buku_list:
            if buku['buku_id'] == buku_id:
                total_weight += buku['bobot']
                break
    return total_weight

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
                print("===== Lihat Data Buku =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in buku_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., buku_id, judul_buku, penerbit): ").strip()
                    if not kolom_cari or kolom_cari not in buku_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    buku_list_sorted = merge_sort_desc(buku_list.copy(), kolom_cari)

                    hasil = binary_search(buku_list_sorted, kolom_cari, keyword)

                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., jumlah_peminjaman, judul_buku, tahun_terbit): ").strip()
                    if not kolom or kolom not in buku_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    hasil_sort = merge_sort_desc(buku_list.copy(), kolom)

                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., buku_id, judul_buku): ").strip()
                    if not kolom_cari or kolom_cari not in buku_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., jumlah_peminjaman, judul_buku): ").strip()
                    if not kolom_urut or kolom_urut not in buku_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(buku_list.copy(), kolom_cari)

                    hasil_pencarian = binary_search(data_sorted_for_search, kolom_cari, keyword)

                    if hasil_pencarian:
                        hasil_terurut = merge_sort_desc(hasil_pencarian, kolom_urut)
                        print("\nHasil Pencarian dan Pengurutan:")
                        for item in hasil_terurut:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '5':
                    break

        elif pilihan == '2':
            clear_screen()
            print("Tambah Buku Baru:")
            buku_id = input("ID Buku: ")
            if any(b['buku_id'] == buku_id for b in buku_list):
                print("ID Buku sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            judul_buku = input("Judul Buku: ")
            isbn = input("ISBN: ")
            tahun_terbit = input("Tahun Terbit: ")
            penerbit = input("Penerbit: ")
            genre_id = input("Genre ID: ")
            status_buku = input("Status Buku (ada/tidak ada): ").lower()
            while status_buku not in ['ada', 'tidak ada']:
                print("Status buku tidak valid. Gunakan 'ada' atau 'tidak ada'.")
                status_buku = input("Status Buku (ada/tidak ada): ").lower()

            jumlah_peminjaman = 0
            posisi_lantai = input("Posisi Lantai (1/2): ")
            while posisi_lantai not in ['1', '2']:
                print("Lantai tidak valid. Gunakan '1' atau '2'.")
                posisi_lantai = input("Posisi Lantai (1/2): ")

            posisi_rak = input("Posisi Rak (A-T): ").upper()
            while not ('A' <= posisi_rak <= 'T' and len(posisi_rak) == 1):
                print("Rak tidak valid. Gunakan huruf A sampai T.")
                posisi_rak = input("Posisi Rak (A-T): ").upper()

            posisi_nomor = input("Posisi Nomor (1-50): ")
            try:
                posisi_nomor = int(posisi_nomor)
                if not (1 <= posisi_nomor <= 50):
                    raise ValueError
            except ValueError:
                print("Nomor rak tidak valid. Gunakan angka 1 sampai 50.")
                input("Tekan Enter untuk kembali")
                continue

            jumlah_halaman = input("Jumlah Halaman Buku: ")
            try:
                jumlah_halaman = int(jumlah_halaman)
            except ValueError:
                print("Jumlah halaman tidak valid. Masukkan angka.")
                input("Tekan Enter untuk kembali")
                continue

            bobot = math.ceil(jumlah_halaman / 200) if jumlah_halaman > 0 else 1 

            buku_list.append({
                'buku_id': buku_id,
                'judul_buku': judul_buku,
                'isbn': isbn,
                'tahun_terbit': tahun_terbit,
                'penerbit': penerbit,
                'genre_id': genre_id,
                'status_buku': status_buku,
                'jumlah_peminjaman': jumlah_peminjaman,
                'posisi_lantai': posisi_lantai,
                'posisi_rak': posisi_rak,
                'posisi_nomor': posisi_nomor,
                'bobot': bobot
            })
            save_buku(buku_list)
            print("Buku berhasil ditambahkan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3':
            clear_screen()
            print("Edit Buku")
            buku_id = input("Masukkan Buku ID yang akan diedit: ")
            target_buku = None
            for buku in buku_list:
                if buku['buku_id'] == buku_id:
                    target_buku = buku
                    break

            if target_buku:
                print(f"Data saat ini: Judul: {target_buku['judul_buku']}, ISBN: {target_buku['isbn']}, Tahun: {target_buku['tahun_terbit']}, Penerbit: {target_buku['penerbit']}, Genre ID: {target_buku['genre_id']}, Status: {target_buku['status_buku']}, Jumlah Pinjam: {target_buku['jumlah_peminjaman']}, Posisi: L{target_buku['posisi_lantai']} RAK-{target_buku['posisi_rak']} NO-{target_buku['posisi_nomor']}, Bobot: {target_buku['bobot']}")

                new_judul = input("Judul baru (kosongkan jika tidak diubah): ")
                new_isbn = input("ISBN baru (kosongkan jika tidak diubah): ")
                new_tahun = input("Tahun Terbit baru (kosongkan jika tidak diubah): ")
                new_penerbit = input("Penerbit baru (kosongkan jika tidak diubah): ")
                new_genre = input("Genre ID baru (kosongkan jika tidak diubah): ")
                status = input("Status baru (ada/tidak ada) (kosongkan jika tidak diubah): ").lower()
                while status and status not in ['ada', 'tidak ada']:
                    print("Status buku tidak valid. Gunakan 'ada' atau 'tidak ada'.")
                    status = input("Status baru (ada/tidak ada) (kosongkan jika tidak diubah): ").lower()
                new_posisi_lantai = input("Posisi Lantai baru (1/2, kosongkan jika tidak diubah): ")
                while new_posisi_lantai and new_posisi_lantai not in ['1', '2']:
                    print("Lantai tidak valid. Gunakan '1' atau '2'.")
                    new_posisi_lantai = input("Posisi Lantai baru (1/2, kosongkan jika tidak diubah): ")

                new_posisi_rak = input("Posisi Rak baru (A-T, kosongkan jika tidak diubah): ").upper()
                while new_posisi_rak and not ('A' <= new_posisi_rak <= 'T' and len(new_posisi_rak) == 1):
                    print("Rak tidak valid. Gunakan huruf A sampai T.")
                    new_posisi_rak = input("Posisi Rak baru (A-T, kosongkan jika tidak diubah): ").upper()

                new_posisi_nomor = input("Posisi Nomor baru (1-50, kosongkan jika tidak diubah): ")
                if new_posisi_nomor:
                    try:
                        new_posisi_nomor = int(new_posisi_nomor)
                        if not (1 <= new_posisi_nomor <= 50):
                            raise ValueError
                    except ValueError:
                        print("Nomor rak tidak valid. Masukkan angka 1 sampai 50.")
                        input("Tekan Enter untuk kembali")
                        continue

                new_jumlah_halaman = input("Jumlah Halaman baru (kosongkan jika tidak diubah): ")
                if new_jumlah_halaman:
                    try:
                        new_jumlah_halaman = int(new_jumlah_halaman)
                    except ValueError:
                        print("Jumlah halaman tidak valid. Masukkan angka.")
                        input("Tekan Enter untuk kembali")
                        continue
                    target_buku['bobot'] = math.ceil(new_jumlah_halaman / 200) if new_jumlah_halaman > 0 else 1


                if new_judul:
                    target_buku['judul_buku'] = new_judul
                if new_isbn:
                    target_buku['isbn'] = new_isbn
                if new_tahun:
                    target_buku['tahun_terbit'] = new_tahun
                if new_penerbit:
                    target_buku['penerbit'] = new_penerbit
                if new_genre:
                    target_buku['genre_id'] = new_genre
                if status:
                    target_buku['status_buku'] = status
                if new_posisi_lantai:
                    target_buku['posisi_lantai'] = new_posisi_lantai
                if new_posisi_rak:
                    target_buku['posisi_rak'] = new_posisi_rak
                if new_posisi_nomor:
                    target_buku['posisi_nomor'] = new_posisi_nomor

                save_buku(buku_list)
                print("Buku berhasil diupdate.")
            else:
                print("Buku dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Buku")
            buku_id = input("Masukkan Buku ID yang akan dihapus: ")
            original_len = len(buku_list)
            buku_list = [buku for buku in buku_list if buku['buku_id'] != buku_id]

            if len(buku_list) < original_len:
                save_buku(buku_list)
                print("Buku berhasil dihapus.")
            else:
                print("Buku dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5':
            clear_screen()
            print("Ubah Status Buku")
            buku_id = input("Masukkan Buku ID: ")
            target_buku = None
            for buku in buku_list:
                if buku['buku_id'] == buku_id:
                    target_buku = buku
                    break

            if target_buku:
                print(f"Status saat ini: {target_buku['status_buku']}")
                status = input("Masukkan status baru (ada/tidak ada): ").lower()
                if status in ['ada', 'tidak ada']:
                    target_buku['status_buku'] = status
                    save_buku(buku_list)
                    print("Status buku berhasil diubah.")
                else:
                    print("Status tidak valid. Gunakan 'ada' atau 'tidak ada'.")
            else:
                print("Buku dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '6':
            clear_screen()
            print("===== Cari Buku (Binary Search) =====")
            kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., buku_id, judul_buku, penerbit): ").strip()
            if not kolom_cari or kolom_cari not in buku_list[0]:
                print("Kolom tidak valid atau kosong.")
                input("\nTekan Enter untuk kembali...")
                continue

            keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

            buku_list_sorted = merge_sort_desc(buku_list.copy(), kolom_cari)

            hasil = binary_search(buku_list_sorted, kolom_cari, keyword)

            if hasil:
                print("\nHasil Pencarian:")
                for item in hasil:
                    print(item)
            else:
                print("Data tidak ditemukan.")
            input("\nTekan Enter untuk kembali...")

        elif pilihan == '7':
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kMenu():
    while True:
        clear_screen()
        print("===== Lihat Data Buku (Karyawan) =====")
        print("1. Lihat Semua Data")
        print("2. Cari Data (Binary Search)")
        print("3. Urutkan Data Menurun (Merge Sort)")
        print("4. Cari + Urutkan")
        print("5. Kembali")
        pilihan2 = input("Pilih opsi: ")
        buku_list = load_buku()

        if pilihan2 == '1':
            for item in buku_list:
                print(item)
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '2':
            kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., buku_id, judul_buku, penerbit): ").strip()
            if not kolom_cari or kolom_cari not in buku_list[0]:
                print("Kolom tidak valid atau kosong.")
                input("\nTekan Enter untuk kembali...")
                continue

            keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

            buku_list_sorted = merge_sort_desc(buku_list.copy(), kolom_cari)

            hasil = binary_search(buku_list_sorted, kolom_cari, keyword)

            if hasil:
                print("\nHasil Pencarian:")
                for item in hasil:
                    print(item)
            else:
                print("Data tidak ditemukan.")
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '3':
            kolom = input("Kolom untuk pengurutan menurun (e.g., jumlah_peminjaman, judul_buku, tahun_terbit): ").strip()
            if not kolom or kolom not in buku_list[0]:
                print("Kolom tidak valid atau kosong.")
                input("\nTekan Enter untuk kembali...")
                continue

            hasil_sort = merge_sort_desc(buku_list.copy(), kolom)

            print("\nHasil Urut Menurun:")
            for item in hasil_sort:
                print(item)
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '4':
            kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., buku_id, judul_buku): ").strip()
            if not kolom_cari or kolom_cari not in buku_list[0]:
                print("Kolom pencarian tidak valid atau kosong.")
                input("\nTekan Enter untuk kembali...")
                continue

            keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

            kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., jumlah_peminjaman, judul_buku): ").strip()
            if not kolom_urut or kolom_urut not in buku_list[0]:
                print("Kolom pengurutan tidak valid atau kosong.")
                input("\nTekan Enter untuk kembali...")
                continue

            data_sorted_for_search = merge_sort_desc(buku_list.copy(), kolom_cari)
            hasil_pencarian = binary_search(data_sorted_for_search, kolom_cari, keyword)

            if hasil_pencarian:
                hasil_terurut = merge_sort_desc(hasil_pencarian, kolom_urut)
                print("\nHasil Pencarian dan Pengurutan:")
                for item in hasil_terurut:
                    print(item)
            else:
                print("Data tidak ditemukan.")
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '5':
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")
            