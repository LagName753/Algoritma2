import csv
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_denda():
    denda_list = []
    try:
        with open('./Database/denda.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                denda_list.append(row)
    except FileNotFoundError:
        print("File denda.csv tidak ditemukan. Membuat file baru.")
        save_denda([])
    return denda_list

def save_denda(denda_list):
    fieldnames = ['denda_id', 'jumlah_denda', 'tanggal_denda', 'status_denda', 'member_id', 'detail_id']
    with open('./Database/denda.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(denda_list)

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
            val_left = float(left[left_idx][kolom])
            val_right = float(right[right_idx][kolom])
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
            if key_column == 'jumlah_denda':
                if float(current_item_value) == float(target_value):
                    left = mid
                    while left >= 0 and float(data[left][key_column]) == float(target_value):
                        found_items.append(data[left])
                        left -= 1
                    right = mid + 1
                    while right < len(data) and float(data[right][key_column]) == float(target_value):
                        found_items.append(data[right])
                        right += 1
                    return list({frozenset(d.items()) for d in found_items})
                elif float(current_item_value) < float(target_value):
                    low = mid + 1
                else:
                    high = mid - 1
            else:
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
                print("===== Lihat Data Denda =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in denda_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., denda_id, jumlah_denda, member_id, status_denda): ").strip()
                    if not kolom_cari or kolom_cari not in denda_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    denda_list_sorted = merge_sort_desc(denda_list.copy(), kolom_cari)
                    hasil = binary_search(denda_list_sorted, kolom_cari, keyword)

                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., jumlah_denda, tanggal_denda, status_denda): ").strip()
                    if not kolom or kolom not in denda_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    hasil_sort = merge_sort_desc(denda_list.copy(), kolom)

                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., denda_id, member_id): ").strip()
                    if not kolom_cari or kolom_cari not in denda_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., jumlah_denda, tanggal_denda): ").strip()
                    if not kolom_urut or kolom_urut not in denda_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(denda_list.copy(), kolom_cari)
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
            print("Tambah Denda Baru:")
            denda_id = input("ID Denda: ")
            if any(d['denda_id'] == denda_id for d in denda_list):
                print("ID Denda sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            jumlah_denda = input("Jumlah Denda: ")
            try:
                jumlah_denda = float(jumlah_denda)
                if jumlah_denda < 0:
                    raise ValueError
            except ValueError:
                print("Jumlah denda tidak valid. Masukkan angka non-negatif.")
                input("Tekan Enter untuk kembali")
                continue

            tanggal_denda = datetime.now().strftime("%Y-%m-%d")
            status_denda = "belum dibayar"
            member_id = input("Member ID: ")
            detail_id = input("Detail ID (opsional): ")

            denda_list.append({
                'denda_id': denda_id,
                'jumlah_denda': str(jumlah_denda),
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
            target_denda = None
            for denda in denda_list:
                if denda['denda_id'] == denda_id:
                    target_denda = denda
                    break

            if target_denda:
                print(f"Data saat ini: Jumlah: Rp{target_denda['jumlah_denda']}, Status: {target_denda['status_denda']}, Member ID: {target_denda['member_id']}, Detail ID: {target_denda['detail_id']}")

                new_jumlah = input("Jumlah Denda baru (kosongkan jika tidak diubah): ")
                if new_jumlah:
                    try:
                        new_jumlah = float(new_jumlah)
                        if new_jumlah < 0:
                            raise ValueError
                        target_denda['jumlah_denda'] = str(new_jumlah)
                    except ValueError:
                        print("Jumlah denda tidak valid. Masukkan angka non-negatif.")
                        input("Tekan Enter untuk kembali")
                        continue

                new_status = input("Status baru (lunas/belum dibayar) (kosongkan jika tidak diubah): ").lower()
                while new_status and new_status not in ['lunas', 'belum dibayar']:
                    print("Status tidak valid. Gunakan 'lunas' atau 'belum dibayar'.")
                    new_status = input("Status baru (lunas/belum dibayar) (kosongkan jika tidak diubah): ").lower()

                new_member_id = input("Member ID baru (kosongkan jika tidak diubah): ")
                new_detail_id = input("Detail ID baru (kosongkan jika tidak diubah): ")

                if new_status:
                    target_denda['status_denda'] = new_status
                if new_member_id:
                    target_denda['member_id'] = new_member_id
                if new_detail_id:
                    target_denda['detail_id'] = new_detail_id

                save_denda(denda_list)
                print("Denda berhasil diupdate.")
            else:
                print("Denda dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Denda")
            denda_id = input("Masukkan ID Denda yang akan dihapus: ")

            found = False
            for i, denda in enumerate(denda_list):
                if denda['denda_id'] == denda_id:
                    found = True
                    konfirmasi = input(f"Yakin menghapus denda ID {denda_id}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        del denda_list[i]
                        save_denda(denda_list)
                        print("Denda berhasil dihapus.")
                    else:
                        print("Penghapusan dibatalkan.")
                    break

            if not found:
                print("Denda dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5':
            clear_screen()
            print("Ubah Status Denda")
            denda_id = input("Masukkan ID Denda: ")
            target_denda = None
            for denda in denda_list:
                if denda['denda_id'] == denda_id:
                    target_denda = denda
                    break

            if target_denda:
                print(f"Status saat ini: {target_denda['status_denda']}")
                new_status = input("Masukkan status baru (lunas/belum dibayar): ").lower()
                if new_status in ['lunas', 'belum dibayar']:
                    target_denda['status_denda'] = new_status
                    save_denda(denda_list)
                    print("Status denda berhasil diubah.")
                else:
                    print("Status tidak valid. Gunakan 'lunas' atau 'belum dibayar'.")
            else:
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
        print("===== Denda (Karyawan) =====")
        print("1. Lihat Daftar Denda")
        print("2. Kembali")

        pilihan = input("Pilih menu: ")
        denda_list = load_denda()

        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data Denda =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in denda_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., denda_id, jumlah_denda, member_id, status_denda): ").strip()
                    if not kolom_cari or kolom_cari not in denda_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    denda_list_sorted = merge_sort_desc(denda_list.copy(), kolom_cari)
                    hasil = binary_search(denda_list_sorted, kolom_cari, keyword)

                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., jumlah_denda, tanggal_denda, status_denda): ").strip()
                    if not kolom or kolom not in denda_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    hasil_sort = merge_sort_desc(denda_list.copy(), kolom)

                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., denda_id, member_id): ").strip()
                    if not kolom_cari or kolom_cari not in denda_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., jumlah_denda, tanggal_denda): ").strip()
                    if not kolom_urut or kolom_urut not in denda_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(denda_list.copy(), kolom_cari)
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