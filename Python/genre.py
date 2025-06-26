import csv
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_genre():
    genre_list = []
    try:
        with open('./Database/genre.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                genre_list.append(row)
    except FileNotFoundError:
        print("File genre.csv tidak ditemukan. Membuat file baru.")
        save_genre([])
    return genre_list

def save_genre(genre_list):
    fieldnames = ['genre_id', 'nama_genre']
    with open('./Database/genre.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(genre_list)

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


def aGenre():
    while True:
        clear_screen()
        print("===== Kelola Genre (Admin) =====")
        print("1. Lihat Daftar Genre")
        print("2. Tambah Genre")
        print("3. Edit Genre")
        print("4. Hapus Genre")
        print("5. Kembali")

        pilihan = input("Pilih menu: ")
        genre_list = load_genre()

        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data Genre =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in genre_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., genre_id, nama_genre): ").strip()
                    if not kolom_cari or kolom_cari not in genre_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    genre_list_sorted = merge_sort_desc(genre_list.copy(), kolom_cari)
                    hasil = binary_search(genre_list_sorted, kolom_cari, keyword)

                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., genre_id, nama_genre): ").strip()
                    if not kolom or kolom not in genre_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    hasil_sort = merge_sort_desc(genre_list.copy(), kolom)

                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., genre_id, nama_genre): ").strip()
                    if not kolom_cari or kolom_cari not in genre_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., genre_id, nama_genre): ").strip()
                    if not kolom_urut or kolom_urut not in genre_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(genre_list.copy(), kolom_cari)
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
            print("Tambah Genre Baru:")
            genre_id = input("ID Genre: ")
            if any(g['genre_id'] == genre_id for g in genre_list):
                print("ID Genre sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            nama_genre = input("Nama Genre: ")

            genre_list.append({
                'genre_id': genre_id,
                'nama_genre': nama_genre
            })
            save_genre(genre_list)
            print("Genre berhasil ditambahkan")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3':
            clear_screen()
            print("Edit Genre")
            genre_id = input("Masukkan ID Genre yang akan diedit: ")
            target_genre = None
            for genre in genre_list:
                if genre['genre_id'] == genre_id:
                    target_genre = genre
                    break

            if target_genre:
                print(f"Data saat ini: Nama: {target_genre['nama_genre']}")
                new_nama = input("Nama Genre baru (kosongkan jika tidak diubah): ")

                if new_nama:
                    target_genre['nama_genre'] = new_nama

                save_genre(genre_list)
                print("Genre berhasil diupdate.")
            else:
                print("Genre dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Genre")
            genre_id = input("Masukkan ID Genre yang akan dihapus: ")

            found = False
            for i, genre in enumerate(genre_list):
                if genre['genre_id'] == genre_id:
                    found = True
                    konfirmasi = input(f"Yakin menghapus genre ID {genre_id}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        del genre_list[i]
                        save_genre(genre_list)
                        print("Genre berhasil dihapus.")
                    else:
                        print("Penghapusan dibatalkan.")
                    break

            if not found:
                print("Genre dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5':
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kGenre():
    while True:
        clear_screen()
        print("===== Genre (Karyawan) =====")
        print("1. Lihat Daftar Genre")
        print("2. Kembali")

        pilihan = input("Pilih menu: ")
        genre_list = load_genre()

        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data Genre =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in genre_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., genre_id, nama_genre): ").strip()
                    if not kolom_cari or kolom_cari not in genre_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    genre_list_sorted = merge_sort_desc(genre_list.copy(), kolom_cari)
                    hasil = binary_search(genre_list_sorted, kolom_cari, keyword)

                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., genre_id, nama_genre): ").strip()
                    if not kolom or kolom not in genre_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    hasil_sort = merge_sort_desc(genre_list.copy(), kolom)

                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., genre_id, nama_genre): ").strip()
                    if not kolom_cari or kolom_cari not in genre_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., genre_id, nama_genre): ").strip()
                    if not kolom_urut or kolom_urut not in genre_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(genre_list.copy(), kolom_cari)
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
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")