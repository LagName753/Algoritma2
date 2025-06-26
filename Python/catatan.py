import csv
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_catatan():
    catatan_list = []
    try:
        with open('./Database/catatan.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                catatan_list.append(row)
    except FileNotFoundError:
        print("File catatan.csv tidak ditemukan. Membuat file baru.")
        save_catatan([])
    return catatan_list

def save_catatan(catatan_list):
    fieldnames = ['catatan_id', 'user_id', 'tanggal_pembuatan', 'detail_catatan', 'status']
    with open('./Database/catatan.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(catatan_list)

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
                print("===== Lihat Data Catatan =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in catatan_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., catatan_id, detail_catatan, status): ").strip()
                    if not kolom_cari or kolom_cari not in catatan_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()
                    
                    catatan_list_sorted = merge_sort_desc(catatan_list.copy(), kolom_cari)
                    hasil = binary_search(catatan_list_sorted, kolom_cari, keyword)
                    
                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., catatan_id, tanggal_pembuatan, status): ").strip()
                    if not kolom or kolom not in catatan_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    hasil_sort = merge_sort_desc(catatan_list.copy(), kolom)
                    
                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., catatan_id, detail_catatan): ").strip()
                    if not kolom_cari or kolom_cari not in catatan_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., catatan_id, tanggal_pembuatan): ").strip()
                    if not kolom_urut or kolom_urut not in catatan_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(catatan_list.copy(), kolom_cari)
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
            print("Tambah Catatan Baru:")
            catatan_id = input("ID Catatan: ")
            if any(c['catatan_id'] == catatan_id for c in catatan_list):
                print("ID Catatan sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            user_id = input("User ID: ")
            detail_catatan = input("Detail Catatan: ")
            tanggal_pembuatan = datetime.now().strftime("%Y-%m-%d")
            status = input("Status (selamanya/belum selesai/sudah selesai): ").lower()
            while status not in ['selamanya', 'belum selesai', 'sudah selesai']:
                print("Status tidak valid. Gunakan 'selamanya', 'belum selesai', atau 'sudah selesai'.")
                status = input("Status (selamanya/belum selesai/sudah selesai): ").lower()
            
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
            target_catatan = None
            for catatan in catatan_list:
                if catatan['catatan_id'] == catatan_id:
                    target_catatan = catatan
                    break
            
            if target_catatan:
                print(f"Data saat ini: Detail: {target_catatan['detail_catatan']}, Status: {target_catatan['status']}")
                new_detail = input("Detail Catatan baru (kosongkan jika tidak diubah): ")
                new_status = input("Status baru (selamanya/belum selesai/sudah selesai) (kosongkan jika tidak diubah): ").lower()
                while new_status and new_status not in ['selamanya', 'belum selesai', 'sudah selesai']:
                    print("Status tidak valid. Gunakan 'selamanya', 'belum selesai', atau 'sudah selesai'.")
                    new_status = input("Status baru (selamanya/belum selesai/sudah selesai) (kosongkan jika tidak diubah): ").lower()
                
                if new_detail:
                    target_catatan['detail_catatan'] = new_detail
                if new_status:
                    target_catatan['status'] = new_status
                
                save_catatan(catatan_list)
                print("Catatan berhasil diupdate.")
            else:
                print("Catatan dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Catatan")
            catatan_id = input("Masukkan Catatan ID yang akan dihapus: ")
            
            found = False
            for i, c in enumerate(catatan_list):
                if c['catatan_id'] == catatan_id:
                    found = True
                    konfirmasi = input(f"Yakin menghapus catatan ID {catatan_id}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        del catatan_list[i]
                        save_catatan(catatan_list)
                        print("Catatan berhasil dihapus.")
                    else:
                        print("Penghapusan dibatalkan.")
                    break

            if not found:
                print("Catatan dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5':
            clear_screen()
            print("Ubah Status Catatan")
            catatan_id = input("Masukkan Catatan ID: ")
            target_catatan = None
            for catatan in catatan_list:
                if catatan['catatan_id'] == catatan_id:
                    target_catatan = catatan
                    break
            
            if target_catatan:
                print(f"Status saat ini: {target_catatan['status']}")
                new_status = input("Masukkan status baru (selamanya/belum selesai/sudah selesai): ").lower()
                if new_status in ['selamanya', 'belum selesai', 'sudah selesai']:
                    target_catatan['status'] = new_status
                    save_catatan(catatan_list)
                    print("Status catatan berhasil diubah.")
                else:
                    print("Status tidak valid.")
            else:
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
                print("===== Lihat Data Catatan =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in catatan_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., catatan_id, detail_catatan, status): ").strip()
                    if not kolom_cari or kolom_cari not in catatan_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()
                    
                    catatan_list_sorted = merge_sort_desc(catatan_list.copy(), kolom_cari)
                    hasil = binary_search(catatan_list_sorted, kolom_cari, keyword)
                    
                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., catatan_id, tanggal_pembuatan, status): ").strip()
                    if not kolom or kolom not in catatan_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    hasil_sort = merge_sort_desc(catatan_list.copy(), kolom)
                    
                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., catatan_id, detail_catatan): ").strip()
                    if not kolom_cari or kolom_cari not in catatan_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., catatan_id, tanggal_pembuatan): ").strip()
                    if not kolom_urut or kolom_urut not in catatan_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(catatan_list.copy(), kolom_cari)
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
            print("Tambah Catatan Baru:")
            catatan_id = input("ID Catatan: ")
            if any(c['catatan_id'] == catatan_id for c in catatan_list):
                print("ID Catatan sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            user_id = input("User ID: ")
            detail_catatan = input("Detail Catatan: ")
            tanggal_pembuatan = datetime.now().strftime("%Y-%m-%d")
            status = input("Status (selamanya/belum selesai/sudah selesai): ").lower()
            while status not in ['selamanya', 'belum selesai', 'sudah selesai']:
                print("Status tidak valid. Gunakan 'selamanya', 'belum selesai', atau 'sudah selesai'.")
                status = input("Status (selamanya/belum selesai/sudah selesai): ").lower()
            
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