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

def admin_menu(user_id):
    while True:
        clear_screen()
        print(f"===== Menu Admin PerpusMAF =====")
        print(f"User ID: {user_id}\n")
        print("1. Kelola Denda")
        print("2. Kelola Detail Peminjaman")
        print("3. Kelola Peminjaman")
        print("4. Kelola Buku")
        print("5. Kelola Pengunjung")
        print("6. Kelola Member")
        print("7. Kelola Users")
        print("8. Kelola Genre")
        print("9. Kelola Catatan")
        print("10. Kembali ke Login")
        print("0. Keluar Aplikasi")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            denda.aDenda()
        elif pilihan == '2':
            detailPeminjaman.aDetailPeminjaman()
        elif pilihan == '3':
            peminjaman.aPeminjaman()
        elif pilihan == '4':
            buku.aMenu()
        elif pilihan == '5':
            pengunjung.aPengunjung()
        elif pilihan == '6':
            member.aMember()
        elif pilihan == '7':
            users.aUsers()
        elif pilihan == '8':
            genre.aGenre()
        elif pilihan == '9':
            catatan.aCatatan()
        elif pilihan == '10':
            return
        elif pilihan == '0':
            exit()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan...")