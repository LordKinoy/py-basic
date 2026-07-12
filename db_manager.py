import mysql.connector

class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_oop"
        )

        self.cursor = self.conn.cursor(dictionary=True)
        self.create_users_table()

    def create_users_table(self):
        query = "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, email VARCHAR(100) UNIQUE NOT NULL)"
        self.cursor.execute(query)
        self.conn.commit()

    def register_user(self, username, password, email):
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (username, password, email))
        self.conn.commit()

    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()
    
    def get_barang_by_kode(self, kode):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                kode_barang,
                nama_barang,
                satuan_barang,
                harga_barang,
                stock,
                diskon
            FROM barang
            WHERE kode_barang = %s
        """, (kode,))
        return cursor.fetchone()
    
    def simpan_transaksi(self, data_penjualan, data_detail):
        cursor = self.conn.cursor()

        try:
            # Simpan header penjualan
            cursor.execute("""
                INSERT INTO penjualan
                (tanggal, pelanggan, sales, jenis_pembayaran, total, bayar, kembali)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, data_penjualan)

            penjualan_id = cursor.lastrowid

            # Simpan detail & kurangi stok
            for detail in data_detail:
                kode, nama, jumlah, satuan, harga, diskon, after_diskon = detail

                # Simpan detail transaksi
                cursor.execute("""
                    INSERT INTO penjualan_detail
                    (
                        penjualan_id,
                        kode_barang,
                        nama_barang,
                        jumlah,
                        satuan,
                        harga,
                        diskon,
                        after_diskon
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    penjualan_id,
                    kode,
                    nama,
                    jumlah,
                    satuan,
                    harga,
                    diskon,
                    after_diskon
                ))

                # Kurangi stok
                cursor.execute("""
                    UPDATE barang
                    SET stock = stock - %s
                    WHERE kode_barang = %s
                    AND stock >= %s
                """, (jumlah, kode, jumlah))

                if cursor.rowcount == 0:
                    raise Exception(f"Stok barang '{nama}' tidak mencukupi.")
    
            
            self.conn.commit()
            return penjualan_id

        except Exception as e:
            self.conn.rollback()
            raise e

    def search_barang(self, keyword):
        try:
            cursor = self.conn.cursor()
            query = "SELECT kode_barang, nama_barang FROM barang WHERE kode_barang LIKE %s OR nama_barang LIKE %s LIMIT 10"
            cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
            return cursor.fetchall()
        except Exception as e:
            print("Error pada searching barang:", e)
            return []
        
    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = %s"
        self.cursor.execute(query, (email,))
        return self.cursor.fetchone()
    
    def update_user_password(self, email, new_password):
        query = "UPDATE users SET password = %s WHERE email = %s"
        self.cursor.execute(query, (new_password, email))
        self.conn.commit()

    def search_pelanggan(self, keyword, mode):
        cursor = self.conn.cursor()
        if mode == "Nama":
            cursor.execute("SELECT * FROM pelanggan WHERE nama LIKE %s", (f"%{keyword}%",))
        else:
            cursor.execute("SELECT * FROM pelanggan WHERE no_hp LIKE %s", (f"%{keyword}%",))
        return cursor.fetchall()
    
    def get_receipt_data(self, penjualan_id):
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.id,
                p.tanggal,
                p.jenis_pembayaran,
                p.total,
                p.bayar,
                p.kembali,

                pl.nama AS pelanggan,
                pl.no_hp,

                u.username AS kasir

            FROM penjualan p

            LEFT JOIN pelanggan pl
                ON pl.id = p.pelanggan

            LEFT JOIN users u
                ON u.id = p.sales

            WHERE p.id=%s
        """,(penjualan_id,))

        header = cursor.fetchone()

        if not header:
            return None

        cursor.execute("""
            SELECT
                kode_barang,
                nama_barang,
                jumlah,
                satuan,
                harga,
                diskon,
                after_diskon
            FROM penjualan_detail
            WHERE penjualan_id=%s
        """,(penjualan_id,))

        detail = cursor.fetchall()

        subtotal = sum(
            item["after_diskon"] * item["jumlah"]
            for item in detail
        )

        member_diskon = subtotal * 0.05 if header["pelanggan"] else 0

        ppn = (subtotal-member_diskon)*0.11

        grand_total = subtotal-member_diskon+ppn

        header["invoice"] = self.generate_invoice_number(
            header["tanggal"],
            header["id"]
        )

        return {
            "header":header,
            "detail":detail,
            "summary":{
                "subtotal":int(subtotal),
                "member_diskon":int(member_diskon),
                "ppn":int(ppn),
                "grand_total":int(grand_total)
            }
        }
    
    def generate_invoice_number(self, tanggal, penjualan_id):
        tanggal = tanggal.strftime("%Y%m%d")
        return f"INV-{tanggal}-{penjualan_id:05d}"
    
    def search_barang_crud(self, keyword):
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM barang
            WHERE
                kode_barang LIKE %s
                OR nama_barang LIKE %s
            ORDER BY nama_barang
        """, (
            f"%{keyword}%",
            f"%{keyword}%"
        ))

        return cursor.fetchall()
    
    # Barang CRUD
    
    def get_all_barang(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                id,
                kode_barang,
                nama_barang,
                satuan_barang,
                harga_barang,
                stock,
                diskon
            FROM barang
            ORDER BY nama_barang
        """)
        return cursor.fetchall()
    
    def insert_barang(self, kode, nama, satuan, harga, stock, diskon):
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO barang
            (
                kode_barang,
                nama_barang,
                satuan_barang,
                harga_barang,
                stock,
                diskon
            )
            VALUES(%s,%s,%s,%s,%s,%s)
        """, (
            kode,
            nama,
            satuan,
            harga,
            stock,
            diskon
        ))

        self.conn.commit()

    def update_barang(self, id_barang, kode, nama, satuan, harga, stock, diskon):
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE barang
            SET
                kode_barang=%s,
                nama_barang=%s,
                satuan_barang=%s,
                harga_barang=%s,
                stock=%s,
                diskon=%s
            WHERE id=%s
        """, (
            kode,
            nama,
            satuan,
            harga,
            stock,
            diskon,
            id_barang
        ))

        self.conn.commit()

    def delete_barang(self, id_barang):
        cursor = self.conn.cursor()

        cursor.execute("""
            DELETE FROM barang
            WHERE id=%s
        """, (id_barang,))

        self.conn.commit()

    def get_barang_by_id(self, id_barang):
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM barang
            WHERE id=%s
        """, (id_barang,))

        return cursor.fetchone()
    
    def get_next_kode_barang(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT kode_barang
            FROM barang
            ORDER BY id DESC
            LIMIT 1
        """)

        result = cursor.fetchone()

        if result is None:
            return "BRG0001"

        kode = result[0]          # BRG0005
        nomor = int(kode[3:]) + 1

        return f"BRG{nomor:04d}"
    
    # Pelanggan CRUD

    def get_all_pelanggan(self):
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                nama,
                no_hp
            FROM pelanggan
            ORDER BY nama
        """)

        return cursor.fetchall()
    
    def insert_pelanggan(self, nama, no_hp):
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO pelanggan
            (
                nama,
                no_hp
            )
            VALUES(%s,%s)
        """, (
            nama,
            no_hp
        ))

        self.conn.commit()

    def update_pelanggan(self, id, nama, no_hp):
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE pelanggan
            SET
                nama=%s,
                no_hp=%s
            WHERE id=%s
        """, (
            nama,
            no_hp,
            id
        ))

        self.conn.commit()

    def delete_pelanggan(self, id_pelanggan):
        cursor = self.conn.cursor()

        cursor.execute("""
            DELETE FROM pelanggan
            WHERE id=%s
        """, (id_pelanggan,))

        self.conn.commit()

    def get_pelanggan_by_id(self, id_pelanggan):
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM pelanggan
            WHERE id=%s
        """, (id_pelanggan,))

        return cursor.fetchone()
    
    def search_pelanggan(self, keyword):
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM pelanggan
            WHERE
                nama LIKE %s
                OR no_hp LIKE %s
            ORDER BY nama
        """, (
            f"%{keyword}%",
            f"%{keyword}%"
        ))

        return cursor.fetchall()