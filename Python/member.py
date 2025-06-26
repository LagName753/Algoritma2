import csv
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_member():
    member_list = []
    try:
        with open('./Database/member.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['jumlah_pinjam_saat_ini'] = int(row.get('jumlah_pinjam_saat_ini', 0))
                member_list.append(row)
    except FileNotFoundError:
        print("File member.csv tidak ditemukan. Membuat file baru.")
        save_member([])
    return member_list

def save_member(member_list):
    fieldnames = ['member_id', 'nama', 'alamat', 'no_telepon', 'email', 'tanggal_lahir', 'passcode', 'status_keanggotaan', 'jumlah_pinjam_saat_ini']
    with open('./Database/member.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(member_list)

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

def aMember():
    while True:
        clear_screen()
        print("===== Kelola Member (Admin) =====")
        print("1. Lihat Daftar Member")
        print("2. Tambah Member")
        print("3. Edit Member")
        print("4. Hapus Member")
        print("5. Ubah Status Keanggotaan")
        print("6. Kembali")
        
        pilihan = input("Pilih menu: ")
        member_list = load_member()
        
        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data Member =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in member_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., member_id, nama, email): ").strip()
                    if not kolom_cari or kolom_cari not in member_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()
                    
                    member_list_sorted = merge_sort_desc(member_list.copy(), kolom_cari)
                    hasil = binary_search(member_list_sorted, kolom_cari, keyword)
                    
                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., nama, tanggal_lahir, jumlah_pinjam_saat_ini): ").strip()
                    if not kolom or kolom not in member_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    hasil_sort = merge_sort_desc(member_list.copy(), kolom)
                    
                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., member_id, nama): ").strip()
                    if not kolom_cari or kolom_cari not in member_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., nama, jumlah_pinjam_saat_ini): ").strip()
                    if not kolom_urut or kolom_urut not in member_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(member_list.copy(), kolom_cari)
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
            print("Tambah Member Baru:")
            member_id = input("ID Member: ")
            if any(m['member_id'] == member_id for m in member_list):
                print("ID Member sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            nama = input("Nama: ")
            alamat = input("Alamat: ")
            no_telepon = input("No. Telepon: ")
            email = input("Email: ")
            tanggal_lahir = input("Tanggal Lahir (YYYY-MM-DD): ")
            passcode = input("Passcode: ")
            status_keanggotaan = "aktif" 

            member_list.append({
                'member_id': member_id,
                'nama': nama,
                'alamat': alamat,
                'no_telepon': no_telepon,
                'email': email,
                'tanggal_lahir': tanggal_lahir,
                'passcode': passcode,
                'status_keanggotaan': status_keanggotaan,
                'jumlah_pinjam_saat_ini': 0
            })
            save_member(member_list)
            print("Member berhasil ditambahkan")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3': 
            clear_screen()
            print("Edit Member")
            member_id = input("Masukkan Member ID yang akan diedit: ")
            target_member = None
            for member in member_list:
                if member['member_id'] == member_id:
                    target_member = member
                    break
            
            if target_member:
                print(f"Data saat ini: Nama: {target_member['nama']}, Alamat: {target_member['alamat']}, Telp: {target_member['no_telepon']}, Email: {target_member['email']}, Lahir: {target_member['tanggal_lahir']}, Status Keanggotaan: {target_member['status_keanggotaan']}, Jumlah Pinjam: {target_member['jumlah_pinjam_saat_ini']}")
                
                new_nama = input("Nama baru (kosongkan jika tidak diubah): ")
                new_alamat = input("Alamat baru (kosongkan jika tidak diubah): ")
                new_telp = input("No. Telepon baru (kosongkan jika tidak diubah): ")
                new_email = input("Email baru (kosongkan jika tidak diubah): ")
                new_lahir = input("Tanggal Lahir baru (YYYY-MM-DD) (kosongkan jika tidak diubah): ")
                new_passcode = input("Passcode baru (kosongkan jika tidak diubah): ")
                new_status = input("Status Keanggotaan baru (aktif/tidak aktif) (kosongkan jika tidak diubah): ").lower()
                while new_status and new_status not in ['aktif', 'tidak aktif']:
                    print("Status keanggotaan tidak valid. Gunakan 'aktif' atau 'tidak aktif'.")
                    new_status = input("Status Keanggotaan baru (aktif/tidak aktif) (kosongkan jika tidak diubah): ").lower()
                
                if new_nama:
                    target_member['nama'] = new_nama
                if new_alamat:
                    target_member['alamat'] = new_alamat
                if new_telp:
                    target_member['no_telepon'] = new_telp
                if new_email:
                    target_member['email'] = new_email
                if new_lahir:
                    target_member['tanggal_lahir'] = new_lahir
                if new_passcode:
                    target_member['passcode'] = new_passcode
                if new_status:
                    target_member['status_keanggotaan'] = new_status

                save_member(member_list)
                print("Member berhasil diupdate.")
            else:
                print("Member dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Member")
            member_id = input("Masukkan Member ID yang akan dihapus: ")
            original_len = len(member_list)
            member_list = [m for m in member_list if m['member_id'] != member_id]
            
            if len(member_list) < original_len:
                save_member(member_list)
                print("Member berhasil dihapus.")
            else:
                print("Member dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5': 
            clear_screen()
            print("Ubah Status Keanggotaan")
            member_id = input("Masukkan Member ID: ")
            target_member = None
            for member in member_list:
                if member['member_id'] == member_id:
                    target_member = member
                    break
            
            if target_member:
                print(f"Status saat ini: {target_member['status_keanggotaan']}")
                new_status = input("Masukkan status baru (aktif/tidak aktif): ").lower()
                if new_status in ['aktif', 'tidak aktif']:
                    target_member['status_keanggotaan'] = new_status
                    save_member(member_list)
                    print("Status keanggotaan berhasil diubah.")
                else:
                    print("Status tidak valid. Gunakan 'aktif' atau 'tidak aktif'.")
            else:
                print("Member dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '6':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kMember():
    while True:
        clear_screen()
        print("===== Member (Karyawan) =====")
        print("1. Lihat Daftar Member")
        print("2. Tambah Member")
        print("3. Kembali")
        
        pilihan = input("Pilih menu: ")
        member_list = load_member()
        
        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data Member =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in member_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., member_id, nama, email): ").strip()
                    if not kolom_cari or kolom_cari not in member_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()
                    
                    member_list_sorted = merge_sort_desc(member_list.copy(), kolom_cari)
                    hasil = binary_search(member_list_sorted, kolom_cari, keyword)
                    
                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., nama, tanggal_lahir, jumlah_pinjam_saat_ini): ").strip()
                    if not kolom or kolom not in member_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    hasil_sort = merge_sort_desc(member_list.copy(), kolom)
                    
                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., member_id, nama): ").strip()
                    if not kolom_cari or kolom_cari not in member_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., nama, jumlah_pinjam_saat_ini): ").strip()
                    if not kolom_urut or kolom_urut not in member_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(member_list.copy(), kolom_cari)
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
            print("Tambah Member Baru:")
            member_id = input("ID Member: ")
            if any(m['member_id'] == member_id for m in member_list):
                print("ID Member sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            nama = input("Nama: ")
            alamat = input("Alamat: ")
            no_telepon = input("No. Telepon: ")
            email = input("Email: ")
            tanggal_lahir = input("Tanggal Lahir (YYYY-MM-DD): ")
            passcode = input("Passcode: ")
            status_keanggotaan = "aktif"

            member_list.append({
                'member_id': member_id,
                'nama': nama,
                'alamat': alamat,
                'no_telepon': no_telepon,
                'email': email,
                'tanggal_lahir': tanggal_lahir,
                'passcode': passcode,
                'status_keanggotaan': status_keanggotaan,
                'jumlah_pinjam_saat_ini': 0
            })
            save_member(member_list)
            print("Member berhasil ditambahkan")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '3':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")