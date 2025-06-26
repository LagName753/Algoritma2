import csv
import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_pengunjung():
    pengunjung_list = []
    try:
        with open('./Database/pengunjung.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['jumlah_pinjam_saat_ini'] = int(row.get('jumlah_pinjam_saat_ini', 0))
                pengunjung_list.append(row)
    except FileNotFoundError:
        print("File pengunjung.csv tidak ditemukan. Membuat file baru.")
        save_pengunjung([])
    return pengunjung_list

def save_pengunjung(pengunjung_list):
    fieldnames = ['pengunjung_id', 'nama', 'asal_instansi', 'tujuan_kunjungan', 'waktu_masuk', 'waktu_keluar', 'jumlah_pinjam_saat_ini']
    with open('./Database/pengunjung.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pengunjung_list)

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

def aPengunjung():
    while True:
        clear_screen()
        print("===== Kelola Pengunjung (Admin) =====")
        print("1. Lihat Daftar Pengunjung")
        print("2. Tambah Pengunjung")
        print("3. Edit Pengunjung")
        print("4. Hapus Pengunjung")
        print("5. Catat Keberangkatan")
        print("6. Kembali")
        
        pilihan = input("Pilih menu: ")
        pengunjung_list = load_pengunjung()
        
        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data Pengunjung =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in pengunjung_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., pengunjung_id, nama, asal_instansi): ").strip()
                    if not kolom_cari or kolom_cari not in pengunjung_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()
                    
                    pengunjung_list_sorted = merge_sort_desc(pengunjung_list.copy(), kolom_cari)
                    hasil = binary_search(pengunjung_list_sorted, kolom_cari, keyword)
                    
                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., nama, waktu_masuk, jumlah_pinjam_saat_ini): ").strip()
                    if not kolom or kolom not in pengunjung_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    hasil_sort = merge_sort_desc(pengunjung_list.copy(), kolom)
                    
                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., pengunjung_id, nama): ").strip()
                    if not kolom_cari or kolom_cari not in pengunjung_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., nama, jumlah_pinjam_saat_ini): ").strip()
                    if not kolom_urut or kolom_urut not in pengunjung_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(pengunjung_list.copy(), kolom_cari)
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
            print("Tambah Pengunjung Baru:")
            pengunjung_id = input("ID Pengunjung: ")
            if any(p['pengunjung_id'] == pengunjung_id for p in pengunjung_list):
                print("ID Pengunjung sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            nama = input("Nama: ")
            asal_instansi = input("Asal Instansi: ")
            tujuan_kunjungan = input("Tujuan Kunjungan: ")
            waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            pengunjung_list.append({
                'pengunjung_id': pengunjung_id,
                'nama': nama,
                'asal_instansi': asal_instansi,
                'tujuan_kunjungan': tujuan_kunjungan,
                'waktu_masuk': waktu_masuk,
                'waktu_keluar': "",
                'jumlah_pinjam_saat_ini': 0
            })
            save_pengunjung(pengunjung_list)
            print("Pengunjung berhasil dicatat")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3':
            clear_screen()
            print("Edit Pengunjung")
            pengunjung_id = input("Masukkan Pengunjung ID yang akan diedit: ")
            target_pengunjung = None
            for pengunjung in pengunjung_list:
                if pengunjung['pengunjung_id'] == pengunjung_id:
                    target_pengunjung = pengunjung
                    break
            
            if target_pengunjung:
                print(f"Data saat ini: Nama: {target_pengunjung['nama']}, Asal Instansi: {target_pengunjung['asal_instansi']}, Tujuan: {target_pengunjung['tujuan_kunjungan']}, Jumlah Pinjam: {target_pengunjung['jumlah_pinjam_saat_ini']}")
                
                new_nama = input("Nama baru (kosongkan jika tidak diubah): ")
                new_asal = input("Asal Instansi baru (kosongkan jika tidak diubah): ")
                new_tujuan = input("Tujuan Kunjungan baru (kosongkan jika tidak diubah): ")
                
                if new_nama:
                    target_pengunjung['nama'] = new_nama
                if new_asal:
                    target_pengunjung['asal_instansi'] = new_asal
                if new_tujuan:
                    target_pengunjung['tujuan_kunjungan'] = new_tujuan

                save_pengunjung(pengunjung_list)
                print("Pengunjung berhasil diupdate.")
            else:
                print("Pengunjung dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Pengunjung")
            pengunjung_id = input("Masukkan Pengunjung ID yang akan dihapus: ")
            original_len = len(pengunjung_list)
            pengunjung_list = [p for p in pengunjung_list if p['pengunjung_id'] != pengunjung_id]
            
            if len(pengunjung_list) < original_len:
                save_pengunjung(pengunjung_list)
                print("Pengunjung berhasil dihapus.")
            else:
                print("Pengunjung dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5': 
            clear_screen()
            print("Catat Keberangkatan Pengunjung")
            pengunjung_id = input("Masukkan Pengunjung ID: ")
            target_pengunjung = None
            for pengunjung in pengunjung_list:
                if pengunjung['pengunjung_id'] == pengunjung_id:
                    target_pengunjung = pengunjung
                    break
            
            if target_pengunjung:
                if not target_pengunjung['waktu_keluar']:
                    target_pengunjung['waktu_keluar'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_pengunjung(pengunjung_list)
                    print("Keberangkatan berhasil dicatat.")
                else:
                    print("Pengunjung ini sudah dicatat keberangkatannya.")
            else:
                print("Pengunjung dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '6':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kPengunjung():
    while True:
        clear_screen()
        print("===== Pengunjung (Karyawan) =====")
        print("1. Lihat Daftar Pengunjung")
        print("2. Tambah Pengunjung")
        print("3. Catat Keberangkatan")
        print("4. Kembali")
        
        pilihan = input("Pilih menu: ")
        pengunjung_list = load_pengunjung()
        
        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data Pengunjung =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in pengunjung_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., pengunjung_id, nama, asal_instansi): ").strip()
                    if not kolom_cari or kolom_cari not in pengunjung_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()
                    
                    pengunjung_list_sorted = merge_sort_desc(pengunjung_list.copy(), kolom_cari)
                    hasil = binary_search(pengunjung_list_sorted, kolom_cari, keyword)
                    
                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., nama, waktu_masuk, jumlah_pinjam_saat_ini): ").strip()
                    if not kolom or kolom not in pengunjung_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    hasil_sort = merge_sort_desc(pengunjung_list.copy(), kolom)
                    
                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., pengunjung_id, nama): ").strip()
                    if not kolom_cari or kolom_cari not in pengunjung_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., nama, jumlah_pinjam_saat_ini): ").strip()
                    if not kolom_urut or kolom_urut not in pengunjung_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(pengunjung_list.copy(), kolom_cari)
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
            print("Tambah Pengunjung Baru:")
            pengunjung_id = input("ID Pengunjung: ")
            if any(p['pengunjung_id'] == pengunjung_id for p in pengunjung_list):
                print("ID Pengunjung sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            nama = input("Nama: ")
            asal_instansi = input("Asal Instansi: ")
            tujuan_kunjungan = input("Tujuan Kunjungan: ")
            waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            pengunjung_list.append({
                'pengunjung_id': pengunjung_id,
                'nama': nama,
                'asal_instansi': asal_instansi,
                'tujuan_kunjungan': tujuan_kunjungan,
                'waktu_masuk': waktu_masuk,
                'waktu_keluar': "",
                'jumlah_pinjam_saat_ini': 0
            })
            save_pengunjung(pengunjung_list)
            print("Pengunjung berhasil dicatat")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3': 
            clear_screen()
            print("Catat Keberangkatan Pengunjung")
            pengunjung_id = input("Masukkan Pengunjung ID: ")
            target_pengunjung = None
            for pengunjung in pengunjung_list:
                if pengunjung['pengunjung_id'] == pengunjung_id:
                    target_pengunjung = pengunjung
                    break
            
            if target_pengunjung:
                if not target_pengunjung['waktu_keluar']:
                    target_pengunjung['waktu_keluar'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_pengunjung(pengunjung_list)
                    print("Keberangkatan berhasil dicatat.")
                else:
                    print("Pengunjung ini sudah dicatat keberangkatannya.")
            else:
                print("Pengunjung dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '4':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")