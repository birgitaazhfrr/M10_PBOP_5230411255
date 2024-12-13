import mysql.connector
import locale

# Mengatur lokal untuk format Rupiah Indonesia
locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

# Menghubungkan ke database MySQL
conn = mysql.connector.connect(
    user="root",
    host="localhost",
    password="",
    database="penjualan"
)

cur = conn.cursor()

while True:
    print("1. Tampil Data")
    print("2. Input All")
    print("3. Input Produk")
    print("4. Ubah Data")
    print("5. Hapus")
    print("0. Keluar")
    menu = input("Pilihan Menu : ")

    # Tampil Data
    if menu == '1':
        try:
            cur.execute("""SELECT Pegawai.Nama, Produk.Nama_Produk, Produk.Harga, Struk.Jumlah_Produk, Struk.Total_Harga
                        FROM Pegawai 
                        INNER JOIN Transaksi ON Pegawai.NIK = Transaksi.NIK
                        INNER JOIN Struk ON Transaksi.No_Transaksi = Struk.No_Transaksi
                        INNER JOIN Produk ON Struk.Kode_Produk = Produk.Kode_Produk""")
            result = cur.fetchall()

            if result:
                for row in result:
                    print(row)
            else:
                print("Tidak ada data untuk ditampilkan.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # Input All
    elif menu == '2':
        try:
            # Input Pegawai
            NIK = input("Masukan NIK Pegawai : ")
            Nama = input("Masukan Nama Pegawai : ")
            Alamat = input("Masukan Alamat Pegawai : ")

            # Memeriksa apakah NIK sudah ada
            cur.execute("SELECT COUNT(*) FROM Pegawai WHERE NIK = %s", [NIK])
            if cur.fetchone()[0] > 0:
                print("NIK sudah terdaftar.")
            else:
                cur.execute("""INSERT INTO Pegawai VALUES(%s,%s,%s)""", [NIK, Nama, Alamat])
                conn.commit()

            # Input Transaksi
            No_Transaksi = input("Masukan Nomor Transaksi : ")

            # Memeriksa apakah No_Transaksi sudah ada
            cur.execute("SELECT COUNT(*) FROM Transaksi WHERE No_Transaksi = %s", [No_Transaksi])
            if cur.fetchone()[0] > 0:
                print("Nomor Transaksi sudah ada.")
            else:
                cur.execute("""INSERT INTO Transaksi VALUES(%s,%s)""", [No_Transaksi, NIK])
                conn.commit()

            # Input Produk
            Kode_Produk = input("Masukan Kode Produk : ")
            Nama_Produk = input("Masukan Nama Produk : ")
            Jenis_Produk = input("Masukan Jenis Produk : ")

            # Meminta input harga dalam angka biasa
            Harga_input = input("Masukan Harga Produk (tanpa pemisah ribuan): ")

            # Menghapus karakter non-digit selain titik dan koma
            Harga_input = Harga_input.replace(".", "").replace(",", ".")

            try:
                Harga = float(Harga_input)  # Mengkonversi input menjadi float
            except ValueError:
                print("Input harga tidak valid. Harap masukkan angka yang valid.")
                continue

            # Menampilkan harga dalam format Rupiah
            Harga_Rupiah = locale.format_string("%0.2f", Harga, grouping=True)
            print(f"Harga Produk: Rp {Harga_Rupiah}")

            # Memasukkan harga ke dalam database
            cur.execute("""INSERT INTO Produk (Kode_Produk, Nama_Produk, Jenis_Produk, Harga) VALUES (%s, %s, %s, %s)""",
                        [Kode_Produk, Nama_Produk, Jenis_Produk, Harga])
            conn.commit()

            # Input Struk
            No_Struk = input("Masukan Nomor Struk : ")
            Jumlah_Produk = int(input("Masukan Jumlah Produk : "))
            Total_Harga = Jumlah_Produk * Harga
            cur.execute("""INSERT INTO Struk VALUES(%s,%s,%s,%s,%s)""", [No_Struk, No_Transaksi, Kode_Produk, Jumlah_Produk, Total_Harga])
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # Input Produk
    elif menu == '3':
        try:
            Kode_Produk = input("Masukan Kode Produk : ")
            Nama_Produk = input("Masukan Nama Produk : ")
            Jenis_Produk = input("Masukan Jenis Produk : ")

            # Meminta input harga dalam angka biasa
            Harga_input = input("Masukan Harga Produk (tanpa pemisah ribuan): ")

            # Menghapus karakter non-digit selain titik dan koma
            Harga_input = Harga_input.replace(".", "").replace(",", ".")

            try:
                Harga = float(Harga_input)  # Mengkonversi input menjadi float
            except ValueError:
                print("Input harga tidak valid. Harap masukkan angka yang valid.")
                continue

            # Menampilkan harga dalam format Rupiah
            Harga_Rupiah = locale.format_string("%0.2f", Harga, grouping=True)
            print(f"Harga Produk: Rp {Harga_Rupiah}")

            # Memasukkan harga ke dalam database
            cur.execute("""INSERT INTO Produk (Kode_Produk, Nama_Produk, Jenis_Produk, Harga) VALUES (%s, %s, %s, %s)""",
                        [Kode_Produk, Nama_Produk, Jenis_Produk, Harga])
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # Ubah Data
    elif menu == '4':
        try:
            Kode_Produk = input("Masukan Kode Produk yang akan diubah : ")
            Nama_Produk = input("Masukan Nama Produk Baru : ")
            Jenis_Produk = input("Masukan Jenis Produk Baru : ")
            Harga_input = input("Masukan Harga Baru : ")

            Harga_input = Harga_input.replace(".", "").replace(",", ".")

            try:
                Harga = float(Harga_input)
            except ValueError:
                print("Input harga tidak valid.")
                continue

            cur.execute("""UPDATE Produk SET Nama_Produk=%s, Jenis_Produk=%s, Harga=%s WHERE Kode_Produk=%s""",
                        [Nama_Produk, Jenis_Produk, Harga, Kode_Produk])
            conn.commit()

            print("Data produk berhasil diubah.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # Hapus Data
    elif menu == '5':
        try:
            Kode_Produk = input("Masukan Kode Produk yang ingin dihapus : ")

            # Cek jika produk ada
            cur.execute("SELECT COUNT(*) FROM Produk WHERE Kode_Produk = %s", [Kode_Produk])
            if cur.fetchone()[0] > 0:
                cur.execute("DELETE FROM Produk WHERE Kode_Produk = %s", [Kode_Produk])
                conn.commit()
                print(f"Produk dengan Kode {Kode_Produk} berhasil dihapus.")
            else:
                print(f"Produk dengan Kode {Kode_Produk} tidak ditemukan.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # Keluar
    elif menu == '0':
        break  # Keluar dari program

# Menutup koneksi dan cursor
cur.close()
conn.close()
