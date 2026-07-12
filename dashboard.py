import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db_manager import DatabaseManager
from receipt_generator import ReceiptGenerator
from modals.barang_modal import BarangModal
from modals.pelanggan_modal import PelangganModal
from auth_window import AuthWindow

class DashboardKasir:
    def __init__(self, master, user_data=None, launch_dashboard=None):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.master = master
        self.master.title("Dashboard Kasir")
        self.master.geometry("1100x700")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.db = DatabaseManager()
        self.cart = []
        self.user_data = user_data
        self.launch_dashboard = launch_dashboard
        self.pelanggan_id = None
        self.hasil_pelanggan = []

        self.container = ctk.CTkFrame(self.master)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.master.bind("<F2>", lambda event: self.tampilkan_pencarian_pelanggan())

        self.build_ui()
        print(self.user_data)
    
    def open_barang_modal(self):
        BarangModal(self.master)

    def open_pelanggan_modal(self):
        PelangganModal(self.master)

    def build_ui(self):
        #bagian Top
        header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        header_frame.grid_columnconfigure(0, weight=1)

        label_judul = ctk.CTkLabel(
            header_frame,
            text="SISTEM KASIR - MINIMARKET IPWIJA",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="red"
        )
        label_judul.grid(row=0, column=0)

        ctk.CTkButton(
            header_frame,
            text="Logout",
            width=90,
            fg_color="#E53935",
            hover_color="#C62828",
            command=self.logout
        ).grid(row=0, column=1, padx=(20,0))

        frame_top = ctk.CTkFrame(self.container)
        frame_top.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.entry_tanggal = ctk.CTkEntry(frame_top, width=120)
        self.entry_tanggal.insert(0, datetime.now().strftime("%d/%m/%Y"))

        ctk.CTkLabel(frame_top, text="TANGGAL").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_tanggal.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_top, text="PELANGGAN").grid(row=0, column=2, padx=5, pady=5)

        self.entry_pelanggan = ctk.CTkEntry(frame_top, width=200)
        self.entry_pelanggan.grid(row=0, column=3, padx=5, pady=5)

        self.btn_cari_pelanggan = ctk.CTkButton(
            frame_top,
            text="Cari Pelanggan",
            command=self.tampilkan_pencarian_pelanggan
        )
        self.btn_cari_pelanggan.grid(row=0, column=4, padx=5, pady=5)

        # Pindahkan Master Pelanggan ke samping Cari Pelanggan
        ctk.CTkButton(
            frame_top,
            text="Master Pelanggan",
            command=self.open_pelanggan_modal
        ).grid(row=0, column=5, padx=5, pady=5)

        ctk.CTkLabel(frame_top, text="TUNAI/KREDIT").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_pembayaran = ctk.CTkComboBox(frame_top, values=["TUNAI", "KREDIT"], width=100)
        self.combo_pembayaran.set("TUNAI")
        self.combo_pembayaran.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_top, text="SALES").grid(row=1, column=2, padx=5, pady=5)
        self.entry_sales = ctk.CTkEntry(frame_top, width=200)
        self.entry_sales.grid(row=1, column=3, padx=5, pady=5)
        if self.user_data:
            self.sales_id = self.user_data.get("id", "")
            self.entry_sales.insert(0, self.user_data.get("username", ""))
            self.entry_sales.configure(state="disabled")

        self.frame_pelanggan = ctk.CTkFrame(self.container)
        self.frame_pelanggan.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.frame_pelanggan.grid_remove()

        self.search_by = ctk.CTkComboBox(self.frame_pelanggan, values=["Nama", "No Telepon"], width=150)
        self.search_by.set("Nama")
        self.search_by.grid(row=0, column=0, padx=5, pady=5)

        self.entry_search = ctk.CTkEntry(self.frame_pelanggan, placeholder_text="Masukkan kata kunci")
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)

        self.btn_search = ctk.CTkButton(self.frame_pelanggan, text="Cari", command=self.cari_pelanggan)
        self.btn_search.grid(row=0, column=2, padx=5, pady=5)

        self.listbox_pelanggan = tk.Listbox(self.frame_pelanggan, height=5)
        self.listbox_pelanggan.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.listbox_pelanggan.bind("<Double-Button-1>", self.pilih_pelanggan)
        
        #Bagian Tengah

        frame_input = ctk.CTkFrame(self.container)
        frame_input.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        for i in range(5):
            frame_input.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(frame_input, text="Kode Barang").grid(row=0, column=0, sticky="w")
        self.entry_kode = ctk.CTkEntry(frame_input)
        self.entry_kode.grid(row=0, column=1, sticky="ew", padx=5)
        self.entry_kode.bind("<KeyRelease>", self.show_suggestions)

        ctk.CTkLabel(frame_input, text="Jumlah").grid(row=0, column=2, padx=10, sticky="w")
        self.entry_jumlah = ctk.CTkEntry(frame_input)
        self.entry_jumlah.insert(0, "1")
        self.entry_jumlah.grid(row=0, column=3, sticky="ew")

        self.listbox_suggest = tk.Listbox(frame_input, height=4)
        self.listbox_suggest.grid(row=1, column=1, columnspan=3, sticky="ew")
        self.listbox_suggest.bind("<Double-Button-1>", self.select_suggestion)

        btn_tambah = ctk.CTkButton(
            frame_input,
            text="Tambah",
            command=self.tambah_barang
        )
        btn_tambah.grid(row=0, column=4, padx=10, sticky="ew")

        ctk.CTkButton(
            frame_input,
            text="Master Barang",
            command=self.open_barang_modal
        ).grid(row=1, column=4, padx=10, pady=(5,0), sticky="ew")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", rowheight=28)

        columns = ("Kode Barang", "Nama Barang", "Jumlah", "Harga", "Diskon", "After Diskon", "Total")
        self.tree = ttk.Treeview(self.container, columns=columns, show="headings", height=10)
        self.tree.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
            
        #Bagian Bawah

        frame_bottom = ctk.CTkFrame(self.container, fg_color="white")
        frame_bottom.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        for i in range(4):
            frame_bottom.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(frame_bottom, text="Total Pembelian", fg_color="white").grid(row=0, column=0, padx=5, pady=2, sticky="ew")
        ctk.CTkLabel(frame_bottom, text="Disc 5%", fg_color="white").grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        ctk.CTkLabel(frame_bottom, text="Pajak", fg_color="white").grid(row=0, column=2, padx=5, pady=2, sticky="ew")
        ctk.CTkLabel(frame_bottom, text="GRAND TOTAL", fg_color="white", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=5, pady=2, sticky="ew")

        self.label_subtotal = ctk.CTkLabel(frame_bottom, text="Rp 0", fg_color="white")
        self.label_subtotal.grid(row=1, column=0, padx=5, pady=2, sticky="ew")

        self.label_diskon = ctk.CTkLabel(frame_bottom, text="Rp 0", fg_color="white")
        self.label_diskon.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        self.label_pajak = ctk.CTkLabel(frame_bottom, text="Rp 0", fg_color="white")
        self.label_pajak.grid(row=1, column=2, padx=5, pady=2, sticky="ew")

        self.label_grandtotal = ctk.CTkLabel(frame_bottom, text="Rp 0", font=ctk.CTkFont(weight="bold"), fg_color="white")
        self.label_grandtotal.grid(row=1, column=3, padx=5, pady=2, sticky="ew")

        # Baris horizontal untuk Pembayaran dan Kembalian
        frame_bayar = ctk.CTkFrame(frame_bottom, fg_color="white")
        frame_bayar.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0), padx=5)
        for i in range(4):
            frame_bayar.grid_columnconfigure(i, weight=1, uniform="equal")

        # Pembayaran
        frame_bayar_kiri = ctk.CTkFrame(frame_bayar, fg_color="transparent")
        frame_bayar_kiri.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        frame_bayar_kiri.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(frame_bayar_kiri, text="Pembayaran:", text_color="black").grid(row=0, column=0, sticky="e", padx=5)
        self.entry_bayar = ctk.CTkEntry(frame_bayar_kiri)
        self.entry_bayar.grid(row=0, column=1, sticky="ew", padx=5)
        self.entry_bayar.bind("<KeyRelease>", self.hitung_kembalian)
        self.entry_bayar.bind("<Return>", self.hitung_kembalian)
        self.entry_bayar.bind("<KeyPress>", self.hanya_angka)

        # Kembalian
        frame_kembali = ctk.CTkFrame(frame_bayar, fg_color="transparent")
        frame_kembali.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)
        frame_kembali.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(frame_kembali, text="Kembalian:", text_color="black").grid(row=0, column=0, sticky="e", padx=5)
        self.label_kembali = ctk.CTkLabel(frame_kembali, text="Rp 0", text_color="black")
        self.label_kembali.grid(row=0, column=1, sticky="w", padx=5)


        # Tombol simpan dan batal
        frame_tombol = ctk.CTkFrame(frame_bottom, fg_color="white")
        frame_tombol.grid(row=5, column=0, columnspan=4, sticky="ew", pady=10)
        frame_tombol.grid_columnconfigure((0, 2), weight=1)  # Spasi di kiri dan kanan
        frame_tombol.grid_columnconfigure(1, weight=0)       # Tengah

        # Frame kecil untuk tombol-tombol
        frame_tombol_tengah = ctk.CTkFrame(frame_tombol, fg_color="transparent")
        frame_tombol_tengah.grid(row=0, column=1)

        # Tombol simpan dan batal ditaruh dalam grid vertikal/tumpuk horizontal
        self.btn_simpan = ctk.CTkButton(frame_tombol_tengah, text="Simpan Transaksi", command=self.simpan_transaksi, width=200)
        self.btn_simpan.grid(row=0, column=0, padx=10, pady=5)

        self.btn_batal = ctk.CTkButton(frame_tombol_tengah, text="Batal", command=self.reset_transaksi, width=200)
        self.btn_batal.grid(row=0, column=1, padx=10, pady=5)

    def format_rupiah(self, angka):
        return f"Rp {angka:,.0f}".replace(",", ".")

    def show_suggestions(self, event=None):
        keyword = self.entry_kode.get().strip()
        self.listbox_suggest.delete(0, tk.END)

        if keyword:
            try:
                results = self.db.search_barang(keyword)
                print(f"Hasil pencarian untuk '{keyword}':", results)

                if not results:
                    self.listbox_suggest.insert(tk.END, "Tidak ditemukan")
                else:
                    for row in results:
                        # Validasi struktur dan tipe data
                        if isinstance(row, (list, tuple)) and len(row) >= 2:
                            kode, nama = row[0], row[1]

                            if isinstance(kode, str) and isinstance(nama, str):
                                self.listbox_suggest.insert(tk.END, f"{kode} - {nama}")
                            else:
                                print("Data tidak valid (bukan string):", row)
                        else:
                            print("Format baris tidak sesuai (bukan tuple berisi 2 elemen):", row)

            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Error saat mengambil saran barang:\n{str(e)}")

    def select_suggestion(self, event=None):
        try:
            if self.listbox_suggest.curselection():
                selection = self.listbox_suggest.get(self.listbox_suggest.curselection())
                if " - " in selection:
                    kode = selection.split(" - ")[0]
                    self.entry_kode.delete(0, tk.END)
                    self.entry_kode.insert(0, kode)
            self.listbox_suggest.delete(0, tk.END)
        except Exception as e:
            print("Gagal memilih kode barang:", e)

    def tambah_barang(self):
        kode = self.entry_kode.get().strip()

        try:
            jumlah = int(self.entry_jumlah.get())
        except ValueError:
            jumlah = 1

        # Ambil data barang
        barang = self.db.get_barang_by_kode(kode)

        # Cek apakah barang ditemukan
        if not barang:
            messagebox.showerror(
                "Tidak ditemukan",
                f"Barang dengan kode '{kode}' tidak ditemukan."
            )
            return

        print("DEBUG barang dari DB:", barang)

        # Unpack sesuai urutan SELECT
        kode, nama, satuan, harga, stok, diskon = barang

        # Jika diskon NULL
        if diskon is None:
            diskon = 0

        # Validasi stok
        if jumlah > stok:
            messagebox.showwarning(
                "Stok Tidak Cukup",
                f"Stok '{nama}' hanya tersedia {stok}."
            )
            return

        try:
            harga = int(harga)
            diskon = float(diskon)
        except ValueError:
            messagebox.showerror(
                "Error",
                f"Data harga atau diskon barang '{nama}' tidak valid."
            )
            return

        # Hitung harga setelah diskon
        after_diskon = round(harga - (harga * diskon / 100))

        # Hitung total
        total = after_diskon * jumlah

        # Tampilkan ke Treeview
        self.tree.insert(
            "",
            tk.END,
            values=(
                kode,
                nama,
                jumlah,
                self.format_rupiah(harga),
                f"{diskon:.0f}%",
                self.format_rupiah(after_diskon),
                self.format_rupiah(total)
            )
        )

        # Simpan ke cart
        self.cart.append((
            kode,
            nama,
            jumlah,
            satuan,
            harga,
            diskon,
            after_diskon
        ))

        # Update total transaksi
        self.update_total()

        # Bersihkan input
        self.entry_kode.delete(0, tk.END)
        self.entry_jumlah.delete(0, tk.END)
        self.entry_jumlah.insert(0, "1")

        self.hitung_kembalian()

    def update_total(self):
        subtotal = sum(item[6] * item[2] for item in self.cart)

        # Cek apakah pelanggan diisi
        is_pelanggan = self.pelanggan_id is not None

        diskon = subtotal * 0.05 if is_pelanggan else 0
        pajak = (subtotal - diskon) * 0.11
        grand_total = subtotal - diskon + pajak

        # Simpan untuk digunakan di fungsi lain
        self.subtotal = subtotal
        self.diskon = diskon
        self.pajak = pajak
        self.grand_total = grand_total

        # Tampilkan hasil
        self.label_subtotal.configure(text=self.format_rupiah(subtotal))
        self.label_diskon.configure(text=self.format_rupiah(diskon))
        self.label_pajak.configure(text=self.format_rupiah(pajak))
        self.label_grandtotal.configure(text=self.format_rupiah(grand_total))


    def hitung_kembalian(self, event=None):
        try:
            bayar = int(self.entry_bayar.get())
        except ValueError:
            bayar = 0

        kembali = max(bayar - self.grand_total, 0)
        self.label_kembali.configure(text=f"Kembali: {self.format_rupiah(kembali)}")

    def hanya_angka(self, event):
        if not event.char.isdigit() and event.keysym not in ("BackSpace", "Delete", "Left", "Right"):
            return "break"

    def simpan_transaksi(self):
        if not self.cart:
            messagebox.showwarning("Kosong", "Tidak ada item untuk disimpan.")
            return

        try:
            bayar = int(self.entry_bayar.get())
        except:
            messagebox.showerror("Error", "Masukkan jumlah bayar yang valid.")
            return

        total = self.grand_total
        kembali = bayar - total

        data_penjualan = (
            datetime.now(),
            self.pelanggan_id,
            self.sales_id,
            self.combo_pembayaran.get(),
            total,
            bayar,
            kembali
        )

        data_detail = []
        for (kode, nama, jumlah, satuan, harga, diskon, after_diskon) in self.cart:
            barang = self.db.get_barang_by_kode(kode)
            satuan = barang[2] if barang else "-"  # ambil satuan dari DB
            data_detail.append((kode, nama, jumlah, satuan, harga, diskon, after_diskon))

        penjualan_id = self.db.simpan_transaksi(
            data_penjualan,
            data_detail
        )
        generator = ReceiptGenerator()

        pdf_file = generator.generate(
            penjualan_id
        )
        
        messagebox.showinfo("Berhasil", f"Transaksi berhasil disimpan. ID: {penjualan_id}")
        self.label_kembali.configure(text=f"Kembali: {self.format_rupiah(kembali)}")
        self.reset_transaksi(clear_form=False)

    def reset_transaksi(self, clear_form=True):
        self.tree.delete(*self.tree.get_children())
        self.cart = []
        self.pelanggan_id = None
        self.update_total()
        self.entry_kode.delete(0, tk.END)
        self.entry_jumlah.delete(0, tk.END)
        self.entry_jumlah.insert(0, "1")
        if clear_form:
            self.entry_bayar.delete(0, tk.END)
            self.label_kembali.configure(text="Kembali: Rp 0")

    def tampilkan_pencarian_pelanggan(self):
        if self.frame_pelanggan.winfo_ismapped():
            self.frame_pelanggan.grid_remove()
        else:
            self.frame_pelanggan.grid()
            self.entry_search.focus()

    def cari_pelanggan(self):
        keyword = self.entry_search.get().strip()
        mode = self.search_by.get()

        self.listbox_pelanggan.delete(0, tk.END)

        # Simpan hasil pencarian agar ID tetap bisa diakses
        self.hasil_pelanggan = []

        if keyword:
            self.hasil_pelanggan = self.db.search_pelanggan(keyword, mode)

            for row in self.hasil_pelanggan:
                self.listbox_pelanggan.insert(
                    tk.END,
                    f"{row[1]} - {row[2]}"
                )

    def pilih_pelanggan(self, event):
        if not self.listbox_pelanggan.curselection():
            return

        index = self.listbox_pelanggan.curselection()[0]

        pelanggan = self.hasil_pelanggan[index]

        # Simpan ID pelanggan
        self.pelanggan_id = pelanggan[0]

        # Tampilkan nama saja di Entry
        self.entry_pelanggan.delete(0, tk.END)
        self.entry_pelanggan.insert(0, pelanggan[1])

        self.frame_pelanggan.grid_remove()

    def logout(self):
        if not messagebox.askyesno(
            "Logout",
            "Apakah Anda yakin ingin logout?"
        ):
            return

        self.master.destroy()

        root = tk.Tk()

        db = DatabaseManager()

        auth = AuthWindow(root, db)
        auth.launch_dashboard = self.launch_dashboard

        root.mainloop()