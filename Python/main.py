import csv
import os
from admin import admin_menu
from karyawan import karyawan_menu

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def login():
    clear_screen()
    print("===== Sistem Perpustakaan PerpusMAF =====")
    print("Silakan login")
    
    while True:
        username = input("Username: ").strip()
        passcode = input("Passcode: ").strip()
        
        try:
            with open('./Database/users.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'].strip() == username and row['passcode'].strip() == passcode:
                        return row['user_id'], row['role']
        except FileNotFoundError:
            print("File database tidak ditemukan")
            return None, None
        
        print("Login gagal. Username atau passcode salah. Silakan coba lagi.")
        choice = input("Coba lagi? (y/n): ").lower()
        if choice != 'y':
            return None, None

def main():
    while True:
        user_id, role = login()
        
        if not user_id:
            print("Keluar dari sistem")
            break
            
        if role == 'admin':
            admin_menu(user_id)
        elif role == 'karyawan':
            karyawan_menu(user_id)

if __name__ == "__main__":
    main()
    