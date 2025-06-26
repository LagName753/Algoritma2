import denda
import detailPeminjaman
import peminjaman
import buku
import pengunjung
import member
import users
import genre
import catatan
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def karyawan_menu(user_id):
    while True:
        clear_screen()
        print(f"===== Menu Karyawan PerpusMAF =====")
        print(f"User ID: {user_id}\n")
        print("1. Denda")
        print("2. Detail Peminjaman")
        print("3. Peminjaman")
        print("4. Buku")
        print("5. Pengunjung")
        print("6. Member")
        print("7. Users")
        print("8. Genre")
        print("9. Catatan")
        print("10. Kembali ke Login")
        print("0. Keluar Aplikasi")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            denda.kDenda()
        elif pilihan == '2':
            detailPeminjaman.kDetailPeminjaman()
        elif pilihan == '3':
            peminjaman.kPeminjaman()
        elif pilihan == '4':
            buku.kMenu()
        elif pilihan == '5':
            pengunjung.kPengunjung()
        elif pilihan == '6':
            member.kMember()
        elif pilihan == '7':
            users.kUsers()
        elif pilihan == '8':
            genre.kGenre()
        elif pilihan == '9':
            catatan.kCatatan()
        elif pilihan == '10':
            return
        elif pilihan == '0':
            exit()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")
            