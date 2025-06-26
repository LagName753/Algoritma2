import csv
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_genre():
    genre_list = []
    with open('./Database/genre.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            genre_list.append(row)
    return genre_list

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

def save_genre(genre_list):
    with open('./Database/genre.csv', mode='w', newline='') as file:
        fieldnames = ['genre_id', 'nama_genre']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(genre_list)

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
                print("===== Lihat Data =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Linear Search)")
                print("3. Urutkan Data Menurun (Insertion Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in genre_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kunci = input("Masukkan kata kunci: ").lower()
                    hasil = linear_search(genre_list, kunci)
                    for item in hasil:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk sorting: ")
                    if kolom in genre_list[0]:
                        hasil = insertion_sort_desc(genre_list.copy(), kolom)
                        for item in hasil:
                            print(item)
                    else:
                        print("Kolom tidak valid.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kunci = input("Masukkan kata kunci: ").lower()
                    kolom = input("Kolom untuk sorting: ")
                    hasil = linear_search(genre_list, kunci)
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
            print("Tambah Genre Baru:")
            genre_id = input("ID Genre: ")
            nama_genre = input("Nama Genre: ")
            
            genre_list.append({
                'genre_id': genre_id,
                'nama_genre': nama_genre
            })
            save_genre(genre_list)
            print("Genre berhasil ditambahkan")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '5':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kGenre():
    while True:
        clear_screen()
        print("===== Lihat Data =====")
        print("1. Lihat Semua Data")
        print("2. Cari Data (Linear Search)")
        print("3. Urutkan Data Menurun (Insertion Sort)")
        print("4. Cari + Urutkan")
        print("5. Kembali")
        pilihan2 = input("Pilih opsi: ")
        genre_list = load_genre()

        if pilihan2 == '1':
            for item in genre_list:
                print(item)
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '2':
            kunci = input("Masukkan kata kunci: ").lower()
            hasil = linear_search(genre_list, kunci)
            for item in hasil:
                print(item)
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '3':
            kolom = input("Kolom untuk sorting: ")
            if kolom in genre_list[0]:
                hasil = insertion_sort_desc(genre_list.copy(), kolom)
                for item in hasil:
                    print(item)
            else:
                print("Kolom tidak valid.")
            input("\nTekan Enter untuk kembali...")

        elif pilihan2 == '4':
            kunci = input("Masukkan kata kunci: ").lower()
            kolom = input("Kolom untuk sorting: ")
            hasil = linear_search(genre_list, kunci)
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
