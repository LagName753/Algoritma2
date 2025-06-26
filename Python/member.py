import csv
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_member():
    member_list = []
    with open('./Database/member.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            member_list.append(row)
    return member_list

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

def save_member(member_list):
    with open('./Database/member.csv', mode='w', newline='') as file:
        fieldnames = ['member_id', 'nama', 'alamat', 'no_telepon', 'username', 'tanggal_lahir', 'passcode', 'status_keanggotaan']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(member_list)

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
                print("===== Lihat Data =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Linear Search)")
                print("3. Urutkan Data Menurun (Insertion Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in member_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kunci = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(member_list, kunci)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in member_list[0]:
                        hasil = insertion_sort_desc(member_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kunci = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(member_list, kunci)
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
            print("Tambah Member Baru:")
            member_id = input("ID Member: ")
            nama = input("Nama: ")
            alamat = input("Alamat: ")
            no_telepon = input("No. Telepon: ")
            username = input("Username: ")
            tanggal_lahir = input("Tanggal Lahir (YYYY-MM-DD): ")
            passcode = input("Passcode: ")
            status_keanggotaan = "aktif"
            
            member_list.append({
                'member_id': member_id,
                'nama': nama,
                'alamat': alamat,
                'no_telepon': no_telepon,
                'username': username,
                'tanggal_lahir': tanggal_lahir,
                'passcode': passcode,
                'status_keanggotaan': status_keanggotaan
            })
            save_member(member_list)
            print("Member berhasil ditambahkan")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3': 
            clear_screen()
            print("Edit Member")
            member_id = input("Masukkan Member ID yang akan diedit: ")
            target = False
            for member in member_list:
                if member['member_id'] == member_id:
                    target = True
                    print(f"Data saat ini: Nama: {member['nama']}, Alamat: {member['alamat']}, Telp: {member['no_telepon']}, Username: {member['username']}, Lahir: {member['tanggal_lahir']}")
                    new_nama = input("Nama baru (kosongkan jika tidak diubah): ")
                    new_alamat = input("Alamat baru (kosongkan jika tidak diubah): ")
                    new_telp = input("No. Telepon baru (kosongkan jika tidak diubah): ")
                    new_username = input("Username baru (kosongkan jika tidak diubah): ")
                    new_lahir = input("Tanggal Lahir baru (YYYY-MM-DD) (kosongkan jika tidak diubah): ")
                    new_passcode = input("Passcode baru (kosongkan jika tidak diubah): ")
                    
                    if new_nama:
                        member['nama'] = new_nama
                    if new_alamat:
                        member['alamat'] = new_alamat
                    if new_telp:
                        member['no_telepon'] = new_telp
                    if new_username:
                        member['username'] = new_username
                    if new_lahir:
                        member['tanggal_lahir'] = new_lahir
                    if new_passcode:
                        member['passcode'] = new_passcode
                    
                    save_member(member_list)
                    print("Member berhasil diupdate.")
                    break
            if not target:
                print("Member dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Member")
            member_id = input("Masukkan Member ID yang akan dihapus: ")
            target = False
            for i, member in enumerate(member_list):
                if member['member_id'] == member_id:
                    target = True
                    konfirmasi = input(f"Yakin menghapus member ID {member_id}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        del member_list[i]
                        save_member(member_list)
                        print("Member berhasil dihapus.")
                    break
            if not target:
                print("Member dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5': 
            clear_screen()
            print("Ubah Status Keanggotaan")
            member_id = input("Masukkan Member ID: ")
            target = False
            for member in member_list:
                if member['member_id'] == member_id:
                    target = True
                    print(f"Status saat ini: {member['status_keanggotaan']}")
                    new_status = input("Masukkan status baru (aktif/tidak aktif): ").lower()
                    if new_status in ['aktif', 'tidak aktif']:
                        member['status_keanggotaan'] = new_status
                        save_member(member_list)
                        print("Status keanggotaan berhasil diubah.")
                    else:
                        print("Status tidak valid. Gunakan 'aktif' atau 'tidak aktif'.")
                    break
            if not target:
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
                print("===== Lihat Data =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Linear Search)")
                print("3. Urutkan Data Menurun (Insertion Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in member_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kunci = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(member_list, kunci)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in member_list[0]:
                        hasil = insertion_sort_desc(member_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kunci = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(member_list, kunci)
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
            print("Tambah Member Baru:")
            member_id = input("ID Member: ")
            nama = input("Nama: ")
            alamat = input("Alamat: ")
            no_telepon = input("No. Telepon: ")
            username = input("Username: ")
            tanggal_lahir = input("Tanggal Lahir (YYYY-MM-DD): ")
            passcode = input("Passcode: ")
            status_keanggotaan = "aktif"
            
            member_list.append({
                'member_id': member_id,
                'nama': nama,
                'alamat': alamat,
                'no_telepon': no_telepon,
                'username': username,
                'tanggal_lahir': tanggal_lahir,
                'passcode': passcode,
                'status_keanggotaan': status_keanggotaan
            })
            save_member(member_list)
            print("Member berhasil ditambahkan")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '3':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")
