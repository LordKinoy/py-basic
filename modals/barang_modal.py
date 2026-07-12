import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.barang_controller import BarangController


class BarangModal:

    def __init__(self, master):

        self.controller = BarangController()

        self.selected_id = None

        self.window = ctk.CTkToplevel(master)
        self.window.title("Master Barang")
        self.window.geometry("1200x700")
        self.window.resizable(False, False)

        # membuat benar-benar modal
        self.window.grab_set()

        self.build_ui()

        self.load_data()

    # ====================================================
    # MEMBANGUN UI
    # ====================================================

    def set_kode_barang(self, kode):
        self.entry_kode.configure(state="normal")
        self.entry_kode.delete(0, "end")
        self.entry_kode.insert(0, kode)
        self.entry_kode.configure(state="disabled")

    def build_ui(self):

        title = ctk.CTkLabel(
            self.window,
            text="MASTER DATA BARANG",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        title.pack(pady=15)

        ###################################################
        # FRAME FORM
        ###################################################

        form = ctk.CTkFrame(self.window)

        form.pack(
            fill="x",
            padx=20
        )

        # ------------------------
        # BARIS 1
        # ------------------------

        ctk.CTkLabel(
            form,
            text="Kode Barang"
        ).grid(row=0,column=0,padx=10,pady=10,sticky="w")

        self.entry_kode = ctk.CTkEntry(
            form,
            width=200
        )

        self.entry_kode.grid(
            row=0,
            column=1,
            padx=10
        )

        self.set_kode_barang(
            self.controller.get_next_kode()
        )

        ctk.CTkLabel(
            form,
            text="Nama Barang"
        ).grid(row=0,column=2,padx=10)

        self.entry_nama = ctk.CTkEntry(
            form,
            width=300
        )

        self.entry_nama.grid(
            row=0,
            column=3,
            padx=10
        )

        # ------------------------
        # BARIS 2
        # ------------------------

        ctk.CTkLabel(
            form,
            text="Satuan"
        ).grid(row=1,column=0,padx=10,pady=10,sticky="w")

        self.entry_satuan = ctk.CTkEntry(
            form,
            width=200
        )

        self.entry_satuan.grid(
            row=1,
            column=1,
            padx=10
        )

        ctk.CTkLabel(
            form,
            text="Harga"
        ).grid(row=1,column=2,padx=10)

        self.entry_harga = ctk.CTkEntry(
            form,
            width=300
        )

        self.entry_harga.grid(
            row=1,
            column=3,
            padx=10
        )

        # ------------------------
        # BARIS 3
        # ------------------------

        ctk.CTkLabel(
            form,
            text="Stock"
        ).grid(row=2,column=0,padx=10,pady=10,sticky="w")

        self.entry_stock = ctk.CTkEntry(
            form,
            width=200
        )

        self.entry_stock.grid(
            row=2,
            column=1,
            padx=10
        )

        ctk.CTkLabel(
            form,
            text="Diskon (%)"
        ).grid(row=2,column=2,padx=10)

        self.entry_diskon = ctk.CTkEntry(
            form,
            width=300
        )

        self.entry_diskon.grid(
            row=2,
            column=3,
            padx=10
        )

        ###################################################
        # FRAME SEARCH
        ###################################################

        frame_search = ctk.CTkFrame(
            self.window
        )

        frame_search.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkLabel(
            frame_search,
            text="Cari Barang"
        ).pack(
            side="left",
            padx=10
        )

        self.entry_search = ctk.CTkEntry(
            frame_search,
            width=300,
            placeholder_text="Kode / Nama Barang..."
        )

        self.entry_search.pack(
            side="left",
            padx=10
        )

        self.entry_search.bind(
            "<KeyRelease>",
            self.search_data
        )

        ###################################################
        # FRAME BUTTON
        ###################################################

        frame_button = ctk.CTkFrame(
            self.window
        )

        frame_button.pack(
            fill="x",
            padx=20
        )

        self.btn_tambah = ctk.CTkButton(
            frame_button,
            text="Tambah",
            width=120,
            command=self.tambah
        )

        self.btn_tambah.pack(
            side="left",
            padx=5,
            pady=10
        )

        self.btn_update = ctk.CTkButton(
            frame_button,
            text="Update",
            width=120,
            command=self.update
        )

        self.btn_update.pack(
            side="left",
            padx=5
        )

        self.btn_clear = ctk.CTkButton(
            frame_button,
            text="Clear",
            width=120,
            command=self.clear_form
        )

        self.btn_clear.pack(
            side="left",
            padx=5
        )

        ###################################################
        # TREEVIEW
        ###################################################

        frame_table = ctk.CTkFrame(
            self.window
        )

        frame_table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ID",
            "Kode",
            "Nama",
            "Satuan",
            "Harga",
            "Stock",
            "Diskon"
        )

        self.tree = ttk.Treeview(
            frame_table,
            columns=columns,
            show="headings",
            height=18
        )

        for col in columns:

            self.tree.heading(
                col,
                text=col
            )

        self.tree.column(
            "ID",
            width=60,
            anchor="center"
        )

        self.tree.column(
            "Kode",
            width=120
        )

        self.tree.column(
            "Nama",
            width=300
        )

        self.tree.column(
            "Satuan",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "Harga",
            width=120,
            anchor="e"
        )

        self.tree.column(
            "Stock",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "Diskon",
            width=100,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            frame_table,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_data
        )

        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        style.configure(
            "Treeview",
            rowheight=28
        )

    # ====================================================
    # LOAD DATA
    # ====================================================

    def load_data(self):

        self.tree.delete(*self.tree.get_children())

        data = self.controller.get_all()

        for row in data:

            self.tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["kode_barang"],
                    row["nama_barang"],
                    row["satuan_barang"],
                    f"Rp {row['harga_barang']:,}".replace(",", "."),
                    row["stock"],
                    f"{row['diskon']} %"
                )
            )

    # ====================================================
    # SEARCH DATA
    # ====================================================

    def search_data(self, event=None):

        keyword = self.entry_search.get().strip()

        self.tree.delete(*self.tree.get_children())

        if keyword == "":
            data = self.controller.get_all()
        else:
            data = self.controller.search(keyword)

        for row in data:

            self.tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["kode_barang"],
                    row["nama_barang"],
                    row["satuan_barang"],
                    f"Rp {row['harga_barang']:,}".replace(",", "."),
                    row["stock"],
                    f"{row['diskon']} %"
                )
            )

    # ====================================================
    # PILIH DATA
    # ====================================================

    def select_data(self, event=None):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]

        self.selected_id = values[0]

        self.clear_entry()

        # self.entry_kode.insert(0, values[1])
        self.entry_nama.insert(0, values[2])
        self.entry_satuan.insert(0, values[3])

        self.set_kode_barang(values[1])

        harga = str(values[4]).replace("Rp ", "").replace(".", "")
        self.entry_harga.insert(0, harga)

        self.entry_stock.insert(0, values[5])

        diskon = str(values[6]).replace("%", "").strip()
        self.entry_diskon.insert(0, diskon)

    # ====================================================
    # CLEAR ENTRY
    # ====================================================

    def clear_entry(self):

        self.set_kode_barang("")
        self.entry_nama.delete(0, "end")
        self.entry_satuan.delete(0, "end")
        self.entry_harga.delete(0, "end")
        self.entry_stock.delete(0, "end")
        self.entry_diskon.delete(0, "end")

    # ====================================================
    # CLEAR FORM
    # ====================================================

    def clear_form(self):

        self.selected_id = None

        self.clear_entry()

        self.set_kode_barang(
            self.controller.get_next_kode()
        )

        self.entry_search.delete(0, "end")

        self.tree.selection_remove(self.tree.selection())

        self.load_data()

        # ====================================================
    # VALIDASI INPUT
    # ====================================================

    def validasi_input(self):

        if self.entry_nama.get().strip() == "":
            messagebox.showwarning("Peringatan", "Nama barang wajib diisi.")
            self.entry_nama.focus()
            return False

        if self.entry_satuan.get().strip() == "":
            messagebox.showwarning("Peringatan", "Satuan wajib diisi.")
            self.entry_satuan.focus()
            return False

        try:
            harga = int(self.entry_harga.get())
            stok = int(self.entry_stock.get())
            diskon = int(self.entry_diskon.get())
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Harga, Stock dan Diskon harus berupa angka."
            )
            return False

        if harga < 0:
            messagebox.showwarning("Peringatan", "Harga tidak boleh negatif.")
            return False

        if stok < 0:
            messagebox.showwarning("Peringatan", "Stock tidak boleh negatif.")
            return False

        if diskon < 0 or diskon > 100:
            messagebox.showwarning(
                "Peringatan",
                "Diskon harus berada di antara 0 - 100."
            )
            return False

        return True

    # ====================================================
    # TAMBAH
    # ====================================================

    def tambah(self):

        if not self.validasi_input():
            return

        try:

            self.controller.insert(
                self.entry_kode.get().strip(),
                self.entry_nama.get().strip(),
                self.entry_satuan.get().strip(),
                int(self.entry_harga.get()),
                int(self.entry_stock.get()),
                int(self.entry_diskon.get())
            )

            messagebox.showinfo(
                "Berhasil",
                "Barang berhasil ditambahkan."
            )

            self.clear_form()
            self.load_data()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ====================================================
    # UPDATE
    # ====================================================

    def update(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Peringatan",
                "Silakan pilih data terlebih dahulu."
            )

            return

        if not self.validasi_input():
            return

        try:

            self.controller.update(
                self.selected_id,
                self.entry_kode.get().strip(),
                self.entry_nama.get().strip(),
                self.entry_satuan.get().strip(),
                int(self.entry_harga.get()),
                int(self.entry_stock.get()),
                int(self.entry_diskon.get())
            )

            messagebox.showinfo(
                "Berhasil",
                "Data berhasil diperbarui."
            )

            self.clear_form()
            self.load_data()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e))

    # ====================================================
    # HAPUS
    # ====================================================

    def hapus(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Peringatan",
                "Silakan pilih data terlebih dahulu."
            )

            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus barang ini?"
        )

        if not konfirmasi:
            return

        try:

            self.controller.delete(self.selected_id)

            messagebox.showinfo(
                "Berhasil",
                "Barang berhasil dihapus."
            )

            self.clear_form()
            self.load_data()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e))