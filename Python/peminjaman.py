import csv
import os
from datetime import datetime, timedelta

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_peminjaman():
    peminjaman_list = []
    try:
        with open('./Database/peminjaman.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                peminjaman_list.append(row)
    except FileNotFoundError:
        print("File peminjaman.csv tidak ditemukan. Membuat file baru.")
        save_peminjaman([])
    return peminjaman_list

def save_peminjaman(peminjaman_list):
    fieldnames = ['peminjaman_id', 'tanggal_peminjaman', 'tenggat_pengembalian', 
                  'tanggal_pengembalian', 'harga_peminjaman', 'member_id', 'pengunjung_id', 'buku_id', 'user_id']
    with open('./Database/peminjaman.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(peminjaman_list)

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
            if str(left[left_idx][kolom]).lower() >= str(right[right_idx][kolom]).lower():
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
            current_val_int = int(current_item_value)
            target_val_int = int(target_value)

            if current_val_int == target_val_int:
                left = mid
                while left >= 0 and int(data[left][key_column]) == target_val_int:
                    found_items.append(data[left])
                    left -= 1
                right = mid + 1
                while right < len(data) and int(data[right][key_column]) == target_val_int:
                    found_items.append(data[right])
                    right += 1
                return list({frozenset(d.items()) for d in found_items})

            elif current_val_int < target_val_int:
                high = mid - 1
            else:
                low = mid + 1
        except ValueError:
            current_val_str = str(current_item_value).lower()
            target_val_str = str(target_value).lower()

            if current_val_str == target_val_str:
                left = mid
                while left >= 0 and str(data[left][key_column]).lower() == target_val_str:
                    found_items.append(data[left])
                    left -= 1
                right = mid + 1
                while right < len(data) and str(data[right][key_column]).lower() == target_val_str:
                    found_items.append(data[right])
                    right += 1
                return list({frozenset(d.items()) for d in found_items})

            elif current_val_str < target_val_str:
                high = mid - 1
            else:
                low = mid + 1
    return found_items


def load_buku():
    buku_list = []
    try:
        with open('./Database/buku.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['stok'] = int(row.get('stok', 0))
                row['bobot_buku'] = int(row.get('bobot_buku', 1))
                row['jumlah_peminjaman'] = int(row.get('jumlah_peminjaman', 0))
                buku_list.append(row)
    except FileNotFoundError:
        pass
    return buku_list

def save_buku(buku_list):
    fieldnames = ['buku_id', 'judul_buku', 'isbn', 'tahun_terbit', 'penerbit', 'genre_id', 
                      'status_buku', 'jumlah_peminjaman', 'posisi_lantai', 'posisi_rak', 'posisi_nomor', 'bobot']
    with open('./Database/buku.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(buku_list)

def load_member():
    member_list = []
    try:
        with open('./Database/member.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['jumlah_pinjam_saat_ini'] = int(row.get('jumlah_pinjam_saat_ini', 0))
                row['batas_pinjam'] = int(row.get('batas_pinjam', 7))
                row['batas_bobot_pinjam'] = int(row.get('batas_bobot_pinjam', 100))
                row['total_bobot_pinjam'] = int(row.get('total_bobot_pinjam', 0))
                member_list.append(row)
    except FileNotFoundError:
        pass
    return member_list

def save_member(member_list):
    fieldnames = ['member_id', 'nama', 'alamat', 'no_telepon', 'email', 'tanggal_lahir', 
                  'passcode', 'status_keanggotaan', 'jumlah_pinjam_saat_ini', 'batas_pinjam', 'batas_bobot_pinjam', 'total_bobot_pinjam']
    with open('./Database/member.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(member_list)

def load_pengunjung():
    pengunjung_list = []
    try:
        with open('./Database/pengunjung.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['jumlah_pinjam_saat_ini'] = int(row.get('jumlah_pinjam_saat_ini', 0))
                row['batas_pinjam'] = int(row.get('batas_pinjam', 2))
                row['batas_bobot_pinjam'] = int(row.get('batas_bobot_pinjam', 20))
                row['total_bobot_pinjam'] = int(row.get('total_bobot_pinjam', 0))
                pengunjung_list.append(row)
    except FileNotFoundError:
        pass
    return pengunjung_list

def save_pengunjung(pengunjung_list):
    fieldnames = ['pengunjung_id', 'nama', 'asal_instansi', 'tujuan_kunjungan', 
                  'waktu_masuk', 'waktu_keluar', 'jumlah_pinjam_saat_ini', 'batas_pinjam', 'batas_bobot_pinjam', 'total_bobot_pinjam']
    with open('./Database/pengunjung.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pengunjung_list)

def load_detail_peminjaman():
    detail_list = []
    try:
        with open('./Database/detail_peminjaman.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                detail_list.append(row)
    except FileNotFoundError:
        pass
    return detail_list

def save_detail_peminjaman(detail_list):
    fieldnames = ['detail_id', 'peminjaman_id', 'buku_id', 'status_peminjaman']
    with open('./Database/detail_peminjaman.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(detail_list)


def aPeminjaman():
    while True:
        clear_screen()
        print("===== Kelola Peminjaman (Admin) =====")
        print("1. Lihat Daftar Peminjaman")
        print("2. Tambah Peminjaman")
        print("3. Edit Peminjaman")
        print("4. Hapus Peminjaman")
        print("5. Pengembalian Buku")
        print("6. Kembali")
        
        pilihan = input("Pilih menu: ")
        peminjaman_list = load_peminjaman()
        
        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data Peminjaman =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in peminjaman_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., peminjaman_id, member_id, user_id, status_peminjaman): ").strip()
                    if not kolom_cari or kolom_cari not in peminjaman_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()
                    
                    peminjaman_list_sorted = merge_sort_desc(peminjaman_list.copy(), kolom_cari)
                    hasil = binary_search(peminjaman_list_sorted, kolom_cari, keyword)
                    
                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                    else:
                        print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., peminjaman_id, tanggal_peminjaman): ").strip()
                    if not kolom or kolom not in peminjaman_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    hasil_sort = merge_sort_desc(peminjaman_list.copy(), kolom)
                    
                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., peminjaman_id, member_id): ").strip()
                    if not kolom_cari or kolom_cari not in peminjaman_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., tanggal_peminjaman, status_peminjaman): ").strip()
                    if not kolom_urut or kolom_urut not in peminjaman_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(peminjaman_list.copy(), kolom_cari)
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
            print("Tambah Peminjaman Baru:")
            peminjaman_id = input("ID Peminjaman: ")
            if any(p['peminjaman_id'] == peminjaman_id for p in peminjaman_list):
                print("ID Peminjaman sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            member_id = input("ID Member (kosongkan jika Pengunjung): ")
            pengunjung_id = ""
            if not member_id:
                pengunjung_id = input("ID Pengunjung: ")
            
            user_id = input("ID User (petugas yang melayani): ")
            
            buku_ids_str = input("Masukkan ID Buku yang dipinjam (pisahkan dengan koma, cth: B001,B002): ")
            buku_ids = [b.strip() for b in buku_ids_str.split(',') if b.strip()]

            buku_data = load_buku()
            member_data = load_member()
            pengunjung_data = load_pengunjung()
            detail_peminjaman_data = load_detail_peminjaman()

            peminjam_obj = None
            is_member = False
            if member_id:
                for m in member_data:
                    if m['member_id'] == member_id:
                        peminjam_obj = m
                        is_member = True
                        break
            elif pengunjung_id:
                for p in pengunjung_data:
                    if p['pengunjung_id'] == pengunjung_id:
                        peminjam_obj = p
                        break
            
            if not peminjam_obj:
                print("Member/Pengunjung dengan ID tersebut tidak ditemukan.")
                input("Tekan Enter untuk kembali")
                continue

            batas_pinjam = int(peminjam_obj.get('batas_pinjam', 0))
            jumlah_pinjam_saat_ini = int(peminjam_obj.get('jumlah_pinjam_saat_ini', 0))
            total_bobot_pinjam_saat_ini = int(peminjam_obj.get('total_bobot_pinjam', 0))

            buku_untuk_dipinjam = []
            total_bobot_buku_baru = 0
            for b_id in buku_ids:
                found_buku = False
                for buku_item in buku_data:
                    if buku_item['buku_id'] == b_id:
                        if int(buku_item['stok']) > 0: 
                            buku_untuk_dipinjam.append(buku_item)
                            total_bobot_buku_baru += int(buku_item['bobot'])
                            found_buku = True
                            break
                if not found_buku:
                    print(f"Buku dengan ID {b_id} tidak ditemukan atau stok kosong.")
                    input("Tekan Enter untuk kembali")
                    continue

            if not buku_untuk_dipinjam:
                print("Tidak ada buku yang valid untuk dipinjam.")
                input("Tekan Enter untuk kembali")
                continue

            if (jumlah_pinjam_saat_ini + len(buku_untuk_dipinjam)) > batas_pinjam:
                print(f"Peminjaman dibatalkan: melebihi batas jumlah buku ({batas_pinjam}).")
                input("Tekan Enter untuk kembali")
                continue
            
            if (total_bobot_pinjam_saat_ini + total_bobot_buku_baru) > int(peminjam_obj.get('batas_bobot_pinjam', 100)):
                print(f"Peminjaman dibatalkan: melebihi batas bobot pinjam ({peminjam_obj.get('batas_bobot_pinjam', 100)}).")
                input("Tekan Enter untuk kembali")
                continue

            tanggal_peminjaman = datetime.now().strftime("%Y-%m-%d")
            tanggal_kembali = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            status_peminjaman = "dipinjam"

            peminjaman_list.append({
                'peminjaman_id': peminjaman_id,
                'member_id': member_id if is_member else '',
                'pengunjung_id': pengunjung_id if not is_member else '',
                'user_id': user_id,
                'tanggal_peminjaman': tanggal_peminjaman,
                'tanggal_kembali': tanggal_kembali,
                'status_peminjaman': status_peminjaman,
                'jumlah_buku_dipinjam': str(len(buku_untuk_dipinjam))
            })
            save_peminjaman(peminjaman_list)

            for buku_item in buku_untuk_dipinjam:
                buku_item['stok'] = str(int(buku_item.get('stok', 0)) - 1)
                buku_item['jumlah_peminjaman'] = str(int(buku_item.get('jumlah_peminjaman', 0)) + 1)
                
                new_detail_id = f"DTL{len(detail_peminjaman_data) + 1:03d}"
                detail_peminjaman_data.append({
                    'detail_id': new_detail_id,
                    'peminjaman_id': peminjaman_id,
                    'buku_id': buku_item['buku_id'],
                    'status_peminjaman': 'terpinjam'
                })
            save_buku(buku_data)
            save_detail_peminjaman(detail_peminjaman_data)

            if is_member:
                for m in member_data:
                    if m['member_id'] == member_id:
                        m['jumlah_pinjam_saat_ini'] = str(int(m.get('jumlah_pinjam_saat_ini', 0)) + len(buku_untuk_dipinjam))
                        m['total_bobot_pinjam'] = str(int(m.get('total_bobot_pinjam', 0)) + total_bobot_buku_baru)
                        break
                save_member(member_data)
            else:
                for p in pengunjung_data:
                    if p['pengunjung_id'] == pengunjung_id:
                        p['jumlah_pinjam_saat_ini'] = str(int(p.get('jumlah_pinjam_saat_ini', 0)) + len(buku_untuk_dipinjam))
                        p['total_bobot_pinjam'] = str(int(p.get('total_bobot_pinjam', 0)) + total_bobot_buku_baru)
                        break
                save_pengunjung(pengunjung_data)

            print("Peminjaman berhasil ditambahkan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '3':
            clear_screen()
            print("Edit Peminjaman")
            peminjaman_id = input("Masukkan ID Peminjaman yang akan diedit: ")
            target_peminjaman = None
            for peminjaman_item in peminjaman_list: 
                if peminjaman_item['peminjaman_id'] == peminjaman_id:
                    target_peminjaman = peminjaman_item
                    break
            
            if target_peminjaman:
                print(f"Data saat ini: Member ID: {target_peminjaman.get('member_id', '')}, Pengunjung ID: {target_peminjaman.get('pengunjung_id', '')}, User ID: {target_peminjaman['user_id']}, Tanggal Pinjam: {target_peminjaman['tanggal_peminjaman']}, Tanggal Kembali: {target_peminjaman['tanggal_kembali']}, Status: {target_peminjaman['status_peminjaman']}")
                
                new_member_id = input("ID Member baru (kosongkan jika tidak diubah): ")
                new_pengunjung_id = input("ID Pengunjung baru (kosongkan jika tidak diubah): ")
                new_user_id = input("ID User baru (kosongkan jika tidak diubah): ")
                new_tgl_kembali = input("Tanggal Kembali baru (YYYY-MM-DD) (kosongkan jika tidak diubah): ")
                new_status = input("Status Peminjaman baru (dipinjam/selesai/terlambat) (kosongkan jika tidak diubah): ").lower()
                while new_status and new_status not in ['dipinjam', 'selesai', 'terlambat']:
                    print("Status tidak valid. Gunakan 'dipinjam', 'selesai', atau 'terlambat'.")
                    new_status = input("Status Peminjaman baru (dipinjam/selesai/terlambat) (kosongkan jika tidak diubah): ").lower()

                if new_member_id:
                    target_peminjaman['member_id'] = new_member_id
                    target_peminjaman['pengunjung_id'] = ''
                if new_pengunjung_id:
                    target_peminjaman['pengunjung_id'] = new_pengunjung_id
                    target_peminjaman['member_id'] = ''
                if new_user_id:
                    target_peminjaman['user_id'] = new_user_id
                if new_tgl_kembali:
                    target_peminjaman['tanggal_kembali'] = new_tgl_kembali
                if new_status:
                    target_peminjaman['status_peminjaman'] = new_status
                
                save_peminjaman(peminjaman_list)
                print("Peminjaman berhasil diupdate.")
            else:
                print("Peminjaman dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '4':
            clear_screen()
            print("Hapus Peminjaman")
            peminjaman_id = input("Masukkan ID Peminjaman yang akan dihapus: ")
            
            found = False
            for i, peminjaman_item in enumerate(peminjaman_list):
                if peminjaman_item['peminjaman_id'] == peminjaman_id:
                    found = True
                    konfirmasi = input(f"Yakin menghapus peminjaman ID {peminjaman_id}? (y/n): ").lower()
                    if konfirmasi == 'y':
                        detail_data = load_detail_peminjaman()
                        buku_data = load_buku()
                        member_data = load_member()
                        pengunjung_data = load_pengunjung()

                        buku_yang_dihapus = []
                        total_bobot_dihapus = 0

                        details_to_keep = []
                        for d in detail_data:
                            if d['peminjaman_id'] == peminjaman_id:
                                for buku_item in buku_data:
                                    if buku_item['buku_id'] == d['buku_id']:
                                        buku_item['stok'] = str(int(buku_item.get('stok',0)) + 1)
                                        buku_item['jumlah_peminjaman'] = str(max(0, int(buku_item.get('jumlah_peminjaman', 0)) - 1))
                                        buku_yang_dihapus.append(buku_item)
                                        total_bobot_dihapus += int(buku_item['bobot'])
                                        break
                            else:
                                details_to_keep.append(d)
                        
                        save_detail_peminjaman(details_to_keep)
                        save_buku(buku_data)

                        if peminjaman_item.get('member_id'):
                            for m in member_data:
                                if m['member_id'] == peminjaman_item['member_id']:
                                    m['jumlah_pinjam_saat_ini'] = str(max(0, int(m.get('jumlah_pinjam_saat_ini', 0)) - len(buku_yang_dihapus)))
                                    m['total_bobot_pinjam'] = str(max(0, int(m.get('total_bobot_pinjam', 0)) - total_bobot_dihapus))
                                    break
                            save_member(member_data)
                        elif peminjaman_item.get('pengunjung_id'):
                            for p in pengunjung_data:
                                if p['pengunjung_id'] == peminjaman_item['pengunjung_id']:
                                    p['jumlah_pinjam_saat_ini'] = str(max(0, int(p.get('jumlah_pinjam_saat_ini', 0)) - len(buku_yang_dihapus)))
                                    p['total_bobot_pinjam'] = str(max(0, int(p.get('total_bobot_pinjam', 0)) - total_bobot_dihapus))
                                    break
                            save_pengunjung(pengunjung_data)

                        del peminjaman_list[i]
                        save_peminjaman(peminjaman_list)
                        print("Peminjaman berhasil dihapus.")
                    else:
                        print("Penghapusan dibatalkan.")
                    break

            if not found:
                print("Peminjaman dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")

        elif pilihan == '5':
            clear_screen()
            print("Pengembalian Buku")
            peminjaman_id = input("Masukkan ID Peminjaman yang akan dikembalikan: ")
            target_peminjaman = None
            for peminjaman_item in peminjaman_list:
                if peminjaman_item['peminjaman_id'] == peminjaman_id:
                    target_peminjaman = peminjaman_item
                    break
            
            if target_peminjaman:
                if target_peminjaman['status_peminjaman'] == 'selesai':
                    print("Buku sudah dikembalikan sebelumnya.")
                    input("Tekan Enter untuk kembali")
                    continue

                tanggal_kembali_aktual = datetime.now()
                try:
                    tanggal_kembali_seharusnya = datetime.strptime(target_peminjaman['tanggal_kembali'], "%Y-%m-%d")
                except ValueError:
                    print("Format tanggal kembali di data tidak valid. Tidak bisa cek denda.")
                    tanggal_kembali_seharusnya = tanggal_kembali_aktual

                denda_jumlah = 0
                if tanggal_kembali_aktual > tanggal_kembali_seharusnya:
                    selisih_hari = (tanggal_kembali_aktual - tanggal_kembali_seharusnya).days
                    denda_per_hari = 1000
                    denda_jumlah = selisih_hari * denda_per_hari
                    print(f"Terlambat {selisih_hari} hari. Denda: Rp{denda_jumlah}")
                else:
                    print("Buku dikembalikan tepat waktu.")

                target_peminjaman['status_peminjaman'] = 'selesai'
                save_peminjaman(peminjaman_list)

                buku_data = load_buku()
                detail_data = load_detail_peminjaman()
                member_data = load_member()
                pengunjung_data = load_pengunjung()

                buku_yang_dikembalikan = []
                total_bobot_dikembalikan = 0

                for detail in detail_data:
                    if detail['peminjaman_id'] == peminjaman_id and detail['status_peminjaman'] == 'terpinjam':
                        detail['status_peminjaman'] = 'selesai'
                        for buku_item in buku_data:
                            if buku_item['buku_id'] == detail['buku_id']:
                                buku_item['stok'] = str(int(buku_item.get('stok',0)) + 1)
                                buku_yang_dikembalikan.append(buku_item)
                                total_bobot_dikembalikan += int(buku_item['bobot'])
                                break
                save_buku(buku_data)
                save_detail_peminjaman(detail_data)

                if target_peminjaman.get('member_id'):
                    for m in member_data:
                        if m['member_id'] == target_peminjaman['member_id']:
                            m['jumlah_pinjam_saat_ini'] = str(max(0, int(m.get('jumlah_pinjam_saat_ini', 0)) - len(buku_yang_dikembalikan)))
                            m['total_bobot_pinjam'] = str(max(0, int(m.get('total_bobot_pinjam', 0)) - total_bobot_dikembalikan))
                            break
                    save_member(member_data)
                elif target_peminjaman.get('pengunjung_id'):
                    for p in pengunjung_data:
                        if p['pengunjung_id'] == target_peminjaman['pengunjung_id']:
                            p['jumlah_pinjam_saat_ini'] = str(max(0, int(p.get('jumlah_pinjam_saat_ini', 0)) - len(buku_yang_dikembalikan)))
                            p['total_bobot_pinjam'] = str(max(0, int(p.get('total_bobot_pinjam', 0)) - total_bobot_dikembalikan))
                            break
                    save_pengunjung(pengunjung_data)

                print("Buku berhasil dikembalikan.")
            else:
                print("Peminjaman dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '6':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")

def kPeminjaman():
    while True:
        clear_screen()
        print("===== Peminjaman (Karyawan) =====")
        print("1. Lihat Daftar Peminjaman")
        print("2. Tambah Peminjaman")
        print("3. Pengembalian Buku")
        print("4. Kembali")
        
        pilihan = input("Pilih menu: ")
        peminjaman_list = load_peminjaman()
        
        if pilihan == '1':
            while True:
                clear_screen()
                print("===== Lihat Data Peminjaman =====")
                print("1. Lihat Semua Data")
                print("2. Cari Data (Binary Search)")
                print("3. Urutkan Data Menurun (Merge Sort)")
                print("4. Cari + Urutkan")
                print("5. Kembali")
                pilihan2 = input("Pilih opsi: ")

                if pilihan2 == '1':
                    for item in peminjaman_list:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '2':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., peminjaman_id, member_id, user_id, status_peminjaman): ").strip()
                    if not kolom_cari or kolom_cari not in peminjaman_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()
                    
                    peminjaman_list_sorted = merge_sort_desc(peminjaman_list.copy(), kolom_cari)
                    hasil = binary_search(peminjaman_list_sorted, kolom_cari, keyword)
                    
                    if hasil:
                        print("\nHasil Pencarian:")
                        for item in hasil:
                            print(item)
                        else:
                            print("Data tidak ditemukan.")
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '3':
                    kolom = input("Kolom untuk pengurutan menurun (e.g., peminjaman_id, tanggal_peminjaman): ").strip()
                    if not kolom or kolom not in peminjaman_list[0]:
                        print("Kolom tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue
                    
                    hasil_sort = merge_sort_desc(peminjaman_list.copy(), kolom)
                    
                    print("\nHasil Urut Menurun:")
                    for item in hasil_sort:
                        print(item)
                    input("\nTekan Enter untuk kembali...")

                elif pilihan2 == '4':
                    kolom_cari = input("Masukkan nama kolom untuk pencarian (e.g., peminjaman_id, member_id): ").strip()
                    if not kolom_cari or kolom_cari not in peminjaman_list[0]:
                        print("Kolom pencarian tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    keyword = input(f"Masukkan nilai '{kolom_cari}' yang dicari: ").strip()

                    kolom_urut = input("Masukkan nama kolom untuk pengurutan hasil (e.g., tanggal_peminjaman, status_peminjaman): ").strip()
                    if not kolom_urut or kolom_urut not in peminjaman_list[0]:
                        print("Kolom pengurutan tidak valid atau kosong.")
                        input("\nTekan Enter untuk kembali...")
                        continue

                    data_sorted_for_search = merge_sort_desc(peminjaman_list.copy(), kolom_cari)
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
            print("Tambah Peminjaman Baru:")
            peminjaman_id = input("ID Peminjaman: ")
            if any(p['peminjaman_id'] == peminjaman_id for p in peminjaman_list):
                print("ID Peminjaman sudah ada. Gunakan ID lain.")
                input("Tekan Enter untuk kembali")
                continue

            member_id = input("ID Member (kosongkan jika Pengunjung): ")
            pengunjung_id = ""
            if not member_id:
                pengunjung_id = input("ID Pengunjung: ")
            
            user_id = input("ID User (petugas yang melayani): ")
            
            buku_ids_str = input("Masukkan ID Buku yang dipinjam (pisahkan dengan koma, cth: B001,B002): ")
            buku_ids = [b.strip() for b in buku_ids_str.split(',') if b.strip()]

            buku_data = load_buku()
            member_data = load_member()
            pengunjung_data = load_pengunjung()
            detail_peminjaman_data = load_detail_peminjaman()

            peminjam_obj = None
            is_member = False
            if member_id:
                for m in member_data:
                    if m['member_id'] == member_id:
                        peminjam_obj = m
                        is_member = True
                        break
            elif pengunjung_id:
                for p in pengunjung_data:
                    if p['pengunjung_id'] == pengunjung_id:
                        peminjam_obj = p
                        break
            
            if not peminjam_obj:
                print("Member/Pengunjung dengan ID tersebut tidak ditemukan.")
                input("Tekan Enter untuk kembali")
                continue

            batas_pinjam = int(peminjam_obj.get('batas_pinjam', 0))
            jumlah_pinjam_saat_ini = int(peminjam_obj.get('jumlah_pinjam_saat_ini', 0))
            total_bobot_pinjam_saat_ini = int(peminjam_obj.get('total_bobot_pinjam', 0))

            buku_untuk_dipinjam = []
            total_bobot_buku_baru = 0
            for b_id in buku_ids:
                found_buku = False
                for buku_item in buku_data:
                    if buku_item['buku_id'] == b_id:
                        if int(buku_item['stok']) > 0:
                            buku_untuk_dipinjam.append(buku_item)
                            total_bobot_buku_baru += int(buku_item['bobot'])
                            found_buku = True
                            break
                if not found_buku:
                    print(f"Buku dengan ID {b_id} tidak ditemukan atau stok kosong.")
                    input("Tekan Enter untuk kembali")
                    continue

            if not buku_untuk_dipinjam:
                print("Tidak ada buku yang valid untuk dipinjam.")
                input("Tekan Enter untuk kembali")
                continue

            if (jumlah_pinjam_saat_ini + len(buku_untuk_dipinjam)) > batas_pinjam:
                print(f"Peminjaman dibatalkan: melebihi batas jumlah buku ({batas_pinjam}).")
                input("Tekan Enter untuk kembali")
                continue
            
            if (total_bobot_pinjam_saat_ini + total_bobot_buku_baru) > int(peminjam_obj.get('batas_bobot_pinjam', 100)):
                print(f"Peminjaman dibatalkan: melebihi batas bobot pinjam ({peminjam_obj.get('batas_bobot_pinjam', 100)}).")
                input("Tekan Enter untuk kembali")
                continue

            tanggal_peminjaman = datetime.now().strftime("%Y-%m-%d")
            tanggal_kembali = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            status_peminjaman = "dipinjam"

            peminjaman_list.append({
                'peminjaman_id': peminjaman_id,
                'member_id': member_id if is_member else '',
                'pengunjung_id': pengunjung_id if not is_member else '',
                'user_id': user_id,
                'tanggal_peminjaman': tanggal_peminjaman,
                'tanggal_kembali': tanggal_kembali,
                'status_peminjaman': status_peminjaman,
                'jumlah_buku_dipinjam': str(len(buku_untuk_dipinjam))
            })
            save_peminjaman(peminjaman_list)

            for buku_item in buku_untuk_dipinjam:
                buku_item['stok'] = str(int(buku_item.get('stok',0)) - 1)
                buku_item['jumlah_peminjaman'] = str(int(buku_item.get('jumlah_peminjaman', 0)) + 1)
                
                new_detail_id = f"DTL{len(detail_peminjaman_data) + 1:03d}"
                detail_peminjaman_data.append({
                    'detail_id': new_detail_id,
                    'peminjaman_id': peminjaman_id,
                    'buku_id': buku_item['buku_id'],
                    'status_peminjaman': 'terpinjam'
                })
            save_buku(buku_data)
            save_detail_peminjaman(detail_peminjaman_data)

            if is_member:
                for m in member_data:
                    if m['member_id'] == member_id:
                        m['jumlah_pinjam_saat_ini'] = str(int(m.get('jumlah_pinjam_saat_ini', 0)) + len(buku_untuk_dipinjam))
                        m['total_bobot_pinjam'] = str(int(m.get('total_bobot_pinjam', 0)) + total_bobot_buku_baru)
                        break
                save_member(member_data)
            else:
                for p in pengunjung_data:
                    if p['pengunjung_id'] == pengunjung_id:
                        p['jumlah_pinjam_saat_ini'] = str(int(p.get('jumlah_pinjam_saat_ini', 0)) + len(buku_untuk_dipinjam))
                        p['total_bobot_pinjam'] = str(int(p.get('total_bobot_pinjam', 0)) + total_bobot_buku_baru)
                        break
                save_pengunjung(pengunjung_data)

            print("Peminjaman berhasil ditambahkan.")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '3':
            clear_screen()
            print("Pengembalian Buku")
            peminjaman_id = input("Masukkan ID Peminjaman yang akan dikembalikan: ")
            target_peminjaman = None
            for peminjaman_item in peminjaman_list:
                if peminjaman_item['peminjaman_id'] == peminjaman_id:
                    target_peminjaman = peminjaman_item
                    break
            
            if target_peminjaman:
                if target_peminjaman['status_peminjaman'] == 'selesai':
                    print("Buku sudah dikembalikan sebelumnya.")
                    input("Tekan Enter untuk kembali")
                    continue

                tanggal_kembali_aktual = datetime.now()
                try:
                    tanggal_kembali_seharusnya = datetime.strptime(target_peminjaman['tanggal_kembali'], "%Y-%m-%d")
                except ValueError:
                    print("Format tanggal kembali di data tidak valid. Tidak bisa cek denda.")
                    tanggal_kembali_seharusnya = tanggal_kembali_aktual

                denda_jumlah = 0
                if tanggal_kembali_aktual > tanggal_kembali_seharusnya:
                    selisih_hari = (tanggal_kembali_aktual - tanggal_kembali_seharusnya).days
                    denda_per_hari = 1000
                    denda_jumlah = selisih_hari * denda_per_hari
                    print(f"Terlambat {selisih_hari} hari. Denda: Rp{denda_jumlah}")
                else:
                    print("Buku dikembalikan tepat waktu.")

                target_peminjaman['status_peminjaman'] = 'selesai'
                save_peminjaman(peminjaman_list)

                buku_data = load_buku()
                detail_data = load_detail_peminjaman()
                member_data = load_member()
                pengunjung_data = load_pengunjung()

                buku_yang_dikembalikan = []
                total_bobot_dikembalikan = 0

                for detail in detail_data:
                    if detail['peminjaman_id'] == peminjaman_id and detail['status_peminjaman'] == 'terpinjam':
                        detail['status_peminjaman'] = 'selesai'
                        for buku_item in buku_data:
                            if buku_item['buku_id'] == detail['buku_id']:
                                buku_item['stok'] = str(int(buku_item.get('stok',0)) + 1)
                                buku_yang_dikembalikan.append(buku_item)
                                total_bobot_dikembalikan += int(buku_item['bobot'])
                                break
                save_buku(buku_data)
                save_detail_peminjaman(detail_data)

                if target_peminjaman.get('member_id'):
                    for m in member_data:
                        if m['member_id'] == target_peminjaman['member_id']:
                            m['jumlah_pinjam_saat_ini'] = str(max(0, int(m.get('jumlah_pinjam_saat_ini', 0)) - len(buku_yang_dikembalikan)))
                            m['total_bobot_pinjam'] = str(max(0, int(m.get('total_bobot_pinjam', 0)) - total_bobot_dikembalikan))
                            break
                    save_member(member_data)
                elif target_peminjaman.get('pengunjung_id'):
                    for p in pengunjung_data:
                        if p['pengunjung_id'] == target_peminjaman['pengunjung_id']:
                            p['jumlah_pinjam_saat_ini'] = str(max(0, int(p.get('jumlah_pinjam_saat_ini', 0)) - len(buku_yang_dikembalikan)))
                            p['total_bobot_pinjam'] = str(max(0, int(p.get('total_bobot_pinjam', 0)) - total_bobot_dikembalikan))
                            break
                    save_pengunjung(pengunjung_data)

                print("Buku berhasil dikembalikan.")
            else:
                print("Peminjaman dengan ID tersebut tidak ditemukan.")
            input("Tekan Enter untuk kembali")
        
        elif pilihan == '4':
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan")