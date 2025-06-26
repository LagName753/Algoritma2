import csv
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_detail_peminjaman():
    detail_list = []
    try:
        with open('./Database/detail_peminjaman.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                detail_list.append(row)
    except FileNotFoundError:
        print("File detail_peminjaman.csv tidak ditemukan. Membuat file baru.")
        save_detail_peminjaman([])
    return detail_list

def save_detail_peminjaman(detail_list):
    fieldnames = ['detail_id', 'peminjaman_id', 'buku_id', 'status_peminjaman']
    with open('./Database/detail_peminjaman.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(detail_list)

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
                print("===== Lihat Data Detail Peminjaman =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in detail_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., detail_id, peminjaman_id, buku_id, status_peminjaman): ").strip()
                    if not kolom_cari or kolom_cari not in detail_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    detail_list_sorted = merge_sort_desc(detail_list.copy(), kolom_cari)
                    hasil = binary_search(detail_list_sorted, kolom_cari, keyword)

                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., detail_id, peminjaman_id, buku_id, status_peminjaman): ").strip()
                    if not kolom or kolom not in detail_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    hasil_sort = merge_sort_desc(detail_list.copy(), kolom)

                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., detail_id, peminjaman_id): ").strip()
                    if not kolom_cari or kolom_cari not in detail_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., detail_id, buku_id): ").strip()
                    if not kolom_urut or kolom_urut not in detail_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(detail_list.copy(), kolom_cari)
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
            print("Tambah Detail Peminjaman Baru:")
            detail_id = input("Detail ID: ")
            if any(d['detail_id'] == detail_id for d in detail_list):
                print("ID Detail Peminjaman sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            peminjaman_id = input("Peminjaman ID: ")
            buku_id = input("Buku ID: ")
            status_peminjaman = input("Status Peminjaman (terpinjam/selesai/terlambat): ").lower()
            while status_peminjaman not in ['terpinjam', 'selesai', 'terlambat']:
                print("Status tidak valid. Gunakan 'terpinjam', 'selesai', atau 'terlambat'.")
                status_peminjaman = input("Status Peminjaman (terpinjam/selesai/terlambat): ").lower()

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
            target_detail = None
            for detail in detail_list:
                if detail['detail_id'] == detail_id:
                    target_detail = detail
                    break

            if target_detail:
                print(f"Data saat ini: Peminjaman ID: {target_detail['peminjaman_id']}, Buku ID: {target_detail['buku_id']}, Status: {target_detail['status_peminjaman']}")

                new_peminjaman_id = input("Peminjaman ID baru (kosongkan jika tidak diubah): ")
                new_buku_id = input("Buku ID baru (kosongkan jika tidak diubah): ")
                new_status = input("Status baru (terpinjam/selesai/terlambat) (kosongkan jika tidak diubah): ").lower()
                while new_status and new_status not in ['terpinjam', 'selesai', 'terlambat']:
                    print("Status tidak valid. Gunakan 'terpinjam', 'selesai', atau 'terlambat'.")
                    new_status = input("Status baru (terpinjam/selesai/terlambat) (kosongkan jika tidak diubah): ").lower()

                if new_peminjaman_id:
                    target_detail['peminjaman_id'] = new_peminjaman_id
                if new_buku_id:
                    target_detail['buku_id'] = new_buku_id
                if new_status:
                    target_detail['status_peminjaman'] = new_status

                save_detail_peminjaman(detail_list)
                print("Detail Peminjaman berhasil diupdate.")
            else:
                print("Detail dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Detail Peminjaman")
            detail_id = input("Masukkan Detail ID yang akan dihapus: ")

            found = False
            for i, detail in enumerate(detail_list):
                if detail['detail_id'] == detail_id:
                    found = True
                    konfirmasi = input(f"Yakin menghapus detail ID {detail_id}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        del detail_list[i]
                        save_detail_peminjaman(detail_list)
                        print("Detail Peminjaman berhasil dihapus.")
                    else:
                        print("Penghapusan dibatalkan.")
                    break

            if not found:
                print("Detail dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5':
            clear_screen()
            print("Ubah Status Peminjaman Detail")
            detail_id = input("Masukkan Detail ID: ")
            target_detail = None
            for detail in detail_list:
                if detail['detail_id'] == detail_id:
                    target_detail = detail
                    break

            if target_detail:
                print(f"Status saat ini: {target_detail['status_peminjaman']}")
                new_status = input("Masukkan status baru (terpinjam/selesai/terlambat): ").lower()
                if new_status in ['terpinjam', 'selesai', 'terlambat']:
                    target_detail['status_peminjaman'] = new_status
                    save_detail_peminjaman(detail_list)
                    print("Status detail peminjaman berhasil diubah.")
                else:
                    print("Status tidak valid. Gunakan 'terpinjam', 'selesai', atau 'terlambat'.")
            else:
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
                print("===== Lihat Data Detail Peminjaman =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in detail_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., detail_id, peminjaman_id, buku_id, status_peminjaman): ").strip()
                    if not kolom_cari or kolom_cari not in detail_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    detail_list_sorted = merge_sort_desc(detail_list.copy(), kolom_cari)
                    hasil = binary_search(detail_list_sorted, kolom_cari, keyword)

                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., detail_id, peminjaman_id, buku_id, status_peminjaman): ").strip()
                    if not kolom or kolom not in detail_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    hasil_sort = merge_sort_desc(detail_list.copy(), kolom)

                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., detail_id, peminjaman_id): ").strip()
                    if not kolom_cari or kolom_cari not in detail_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., detail_id, buku_id): ").strip()
                    if not kolom_urut or kolom_urut not in detail_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(detail_list.copy(), kolom_cari)
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
            print("Tambah Detail Peminjaman Baru:")
            detail_id = input("Detail ID: ")
            if any(d['detail_id'] == detail_id for d in detail_list):
                print("ID Detail Peminjaman sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            peminjaman_id = input("Peminjaman ID: ")
            buku_id = input("Buku ID: ")
            status_peminjaman = input("Status Peminjaman (terpinjam/selesai/terlambat): ").lower()
            while status_peminjaman not in ['terpinjam', 'selesai', 'terlambat']:
                print("Status tidak valid. Gunakan 'terpinjam', 'selesai', atau 'terlambat'.")
                status_peminjaman = input("Status Peminjaman (terpinjam/selesai/terlambat): ").lower()

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