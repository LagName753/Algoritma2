import csv
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def linear_search(data, keyword):
    result = []
    for item in data:
        if keyword in str(item).lower():
            result.append(item)
    return result

def insertion_sort_desc(data, kolom):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j][kolom] < key[kolom]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data

def load_users():
    users_list = []
    with open('./Database/users.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users_list.append(row)
    return users_list

def save_users(users_list):
    with open('./Database/users.csv', mode='w', newline='') as file:
        fieldnames = ['user_id', 'nama', 'alamat', 'no_telepon', 'username', 'tanggal_lahir', 'passcode', 'role']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users_list)

def aUsers():
    while True:
        clear_screen()
        print("===== Kelola Users (Admin) =====")
        print("1. Lihat Daftar Users")
        print("2. Tambah User")
        print("3. Edit User")
        print("4. Hapus User")
        print("5. Ubah Role User")
        print("6. Kembali")
        
        choice = input("Pilih menu: ")
        users_list = load_users()
        
        if choice == '1':
            while True:
                clear_screen()
                print("===== Lihat Data =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Linear Search)")
                print("3. Urutkan Data Menurun (Insertion Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                sub = input("Pilih opsi: ")

                if sub == '1':
                    for item in users_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif sub == '2':
                    keyword = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(users_list, keyword)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif sub == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in users_list[0]:
                        hasil = insertion_sort_desc(users_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif sub == '4':
                    keyword = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(users_list, keyword)
                    if hasil and kolom in hasil[0]:
                        hasil = insertion_sort_desc(hasil, kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid atau tidak ada hasil.")
                    input("\nTekan Enter untuk kembali...")

                elif sub == '5':
                    break
        
        elif choice == '2':
            clear_screen()
            print("Tambah User Baru:")
            user_id = input("ID User: ")
            nama = input("Nama: ")
            alamat = input("Alamat: ")
            no_telepon = input("No. Telepon: ")
            username = input("Username: ")
            tanggal_lahir = input("Tanggal Lahir (YYYY-MM-DD): ")
            passcode = input("Passcode: ")
            role = input("Role (admin/karyawan): ").lower()
            if role not in ['admin', 'karyawan']:
                print("Role harus 'admin' atau 'karyawan'")
                input("Tekan Enter untuk kembali")
                continue
            
            users_list.append({
                'user_id': user_id,
                'nama': nama,
                'alamat': alamat,
                'no_telepon': no_telepon,
                'username': username,
                'tanggal_lahir': tanggal_lahir,
                'passcode': passcode,
                'role': role
            })
            save_users(users_list)
            print("User berhasil ditambahkan")
            input("Tekan Enter untuk kembali")

        elif choice == '3':
            clear_screen()
            print("Edit User")
            user_id_input = input("Masukkan User ID yang akan diedit: ")
            found = False
            for user in users_list:
                if user['user_id'] == user_id_input:
                    found = True
                    print(f"Data saat ini: Nama: {user['nama']}, Alamat: {user['alamat']}, Telp: {user['no_telepon']}, Username: {user['username']}, Lahir: {user['tanggal_lahir']}, Role: {user['role']}")
                    new_nama = input("Nama baru (kosongkan jika tidak diubah): ")
                    new_alamat = input("Alamat baru (kosongkan jika tidak diubah): ")
                    new_telp = input("No. Telepon baru (kosongkan jika tidak diubah): ")
                    new_username = input("Username baru (kosongkan jika tidak diubah): ")
                    new_lahir = input("Tanggal Lahir baru (YYYY-MM-DD) (kosongkan jika tidak diubah): ")
                    new_passcode = input("Passcode baru (kosongkan jika tidak diubah): ")
                    new_role = input("Role baru (admin/karyawan) (kosongkan jika tidak diubah): ")
                    
                    if new_nama:
                        user['nama'] = new_nama
                    if new_alamat:
                        user['alamat'] = new_alamat
                    if new_telp:
                        user['no_telepon'] = new_telp
                    if new_username:
                        user['username'] = new_username
                    if new_lahir:
                        user['tanggal_lahir'] = new_lahir
                    if new_passcode:
                        user['passcode'] = new_passcode
                    if new_role:
                        user['role'] = new_role
                    
                    save_users(users_list)
                    print("User berhasil diupdate.")
                    break
            if not found:
                print("User dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif choice == '4':
            clear_screen()
            print("Hapus User")
            user_id_input = input("Masukkan User ID yang akan dihapus: ")
            found = False
            for i, user in enumerate(users_list):
                if user['user_id'] == user_id_input:
                    found = True
                    confirm = input(f"Yakin menghapus user ID {user_id_input}? (y/n): ").lower()
                    if confirm == 'y':
                        del users_list[i]
                        save_users(users_list)
                        print("User berhasil dihapus.")
                    break
            if not found:
                print("User dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif choice == '5':
            clear_screen()
            print("Ubah Role User")
            user_id_input = input("Masukkan User ID: ")
            found = False
            for user in users_list:
                if user['user_id'] == user_id_input:
                    found = True
                    print(f"Role saat ini: {user['role']}")
                    new_role = input("Masukkan role baru (admin/karyawan): ")
                    if new_role in ['admin', 'karyawan']:
                        user['role'] = new_role
                        save_users(users_list)
                        print("Role user berhasil diubah.")
                    else:
                        print("Role tidak valid. Gunakan 'admin' atau 'karyawan'.")
                    break
            if not found:
                print("User dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")
        
        elif choice == '6':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kUsers():
    while True:
        clear_screen()
        print("===== Users (Karyawan) =====")
        print("1. Lihat Daftar Users")
        print("2. Tambah User")
        print("3. Kembali")
        
        choice = input("Pilih menu: ")
        users_list = load_users()
        
        if choice == '1':
            while True:
                clear_screen()
                print("===== Lihat Data =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Linear Search)")
                print("3. Urutkan Data Menurun (Insertion Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                sub = input("Pilih opsi: ")

                if sub == '1':
                    for item in users_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif sub == '2':
                    keyword = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(users_list, keyword)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif sub == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in users_list[0]:
                        hasil = insertion_sort_desc(users_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif sub == '4':
                    keyword = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(users_list, keyword)
                    if hasil and kolom in hasil[0]:
                        hasil = insertion_sort_desc(hasil, kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid atau tidak ada hasil.")
                    input("\nTekan Enter untuk kembali...")

                elif sub == '5':
                    break
        
        elif choice == '2':
            clear_screen()
            print("Tambah User Baru:")
            user_id = input("ID User: ")
            nama = input("Nama: ")
            alamat = input("Alamat: ")
            no_telepon = input("No. Telepon: ")
            username = input("Username: ")
            tanggal_lahir = input("Tanggal Lahir (YYYY-MM-DD): ")
            passcode = input("Passcode: ")
            role = input("Role (admin/karyawan): ").lower()
            if role not in ['admin', 'karyawan']:
                print("Role harus 'admin' atau 'karyawan'")
                input("Tekan Enter untuk kembali")
                continue
            
            users_list.append({
                'user_id': user_id,
                'nama': nama,
                'alamat': alamat,
                'no_telepon': no_telepon,
                'username': username,
                'tanggal_lahir': tanggal_lahir,
                'passcode': passcode,
                'role': role
            })
            save_users(users_list)
            print("User berhasil ditambahkan")
            input("Tekan Enter untuk kembali")

        elif choice == '3':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")
