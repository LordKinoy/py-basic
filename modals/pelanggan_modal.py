import customtkinter as ctk
from tkinter import ttk, messagebox

from controllers.pelanggan_controller import PelangganController

class PelangganModal:

    def __init__(self, master):

        self.controller = PelangganController()
        self.selected_id = None

        # Simpan parent
        self.master = master

        # Buat hanya SATU modal
        self.window = ctk.CTkToplevel(self.master)

        self.window.title("Master Pelanggan")
        self.window.geometry("900x500")

        # Jadikan benar-benar modal
        self.window.transient(self.master)
        self.window.grab_set()
        self.window.focus_force()
        self.window.lift()

        # Bawa ke paling depan
        self.window.attributes("-topmost", True)
        self.window.after(
            100,
            lambda: self.window.attributes("-topmost", False)
        )

        # Optional: tidak bisa di-resize
        self.window.resizable(False, False)

        self.build_ui()
        self.load_data()

    # ===========================
    # UI
    # ===========================

    def build_ui(self):

        title = ctk.CTkLabel(
            self.window,
            text="MASTER PELANGGAN",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=15)

        form = ctk.CTkFrame(self.window)
        form.pack(fill="x", padx=20)

        # Nama

        ctk.CTkLabel(
            form,
            text="Nama"
        ).grid(row=0,column=0,padx=10,pady=10,sticky="w")

        self.entry_nama = ctk.CTkEntry(
            form,
            width=250
        )

        self.entry_nama.grid(row=0,column=1,padx=10)

        # No HP

        ctk.CTkLabel(
            form,
            text="No HP"
        ).grid(row=1,column=0,padx=10,pady=10,sticky="w")

        self.entry_hp = ctk.CTkEntry(
            form,
            width=250
        )

        self.entry_hp.grid(row=1,column=1,padx=10)

        # Search

        ctk.CTkLabel(
            form,
            text="Search"
        ).grid(row=0,column=2,padx=10)

        self.entry_search = ctk.CTkEntry(
            form,
            width=220,
            placeholder_text="Cari Nama / No HP"
        )

        self.entry_search.grid(row=0,column=3,padx=10)

        self.entry_search.bind("<KeyRelease>", self.search_data)

        # Tombol

        tombol = ctk.CTkFrame(self.window)
        tombol.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            tombol,
            text="Tambah",
            command=self.tambah
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            tombol,
            text="Update",
            command=self.update
        ).pack(side="left", padx=5)

        # ctk.CTkButton(
        #     tombol,
        #     text="Hapus",
        #     command=self.hapus,
        #     fg_color="red"
        # ).pack(side="left", padx=5)

        ctk.CTkButton(
            tombol,
            text="Clear",
            command=self.clear_form
        ).pack(side="left", padx=5)

        # ctk.CTkButton(
        #     tombol,
        #     text="Refresh",
        #     command=self.load_data
        # ).pack(side="left", padx=5)

        # Treeview

        columns = (
            "ID",
            "Nama",
            "No HP"
        )

        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",
            height=18
        )

        for col in columns:
            self.tree.heading(col,text=col)

        self.tree.column("ID",width=60,anchor="center")
        self.tree.column("Nama",width=300)
        self.tree.column("No HP",width=200)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_data
        )

    # ===========================
    # LOAD DATA
    # ===========================

    def load_data(self):

        self.tree.delete(*self.tree.get_children())

        data = self.controller.get_all()

        for row in data:

            self.tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["nama"],
                    row["no_hp"]
                )
            )

    # ===========================
    # SEARCH
    # ===========================

    def search_data(self,event=None):

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
                    row["nama"],
                    row["no_hp"]
                )
            )

    # ===========================
    # SELECT
    # ===========================

    def select_data(self,event):

        selected = self.tree.focus()

        if not selected:
            return

        data = self.tree.item(selected)["values"]

        self.selected_id = data[0]

        self.entry_nama.delete(0,"end")
        self.entry_hp.delete(0,"end")

        self.entry_nama.insert(0,data[1])
        self.entry_hp.insert(0,data[2])

    # ===========================
    # TAMBAH
    # ===========================

    def tambah(self):

        nama = self.entry_nama.get().strip()
        no_hp = self.entry_hp.get().strip()

        if nama == "" or no_hp == "":
            messagebox.showwarning(
                "Peringatan",
                "Semua field harus diisi."
            )
            return

        self.controller.insert(
            nama,
            no_hp
        )

        messagebox.showinfo(
            "Berhasil",
            "Data pelanggan berhasil ditambahkan."
        )

        self.clear_form()
        self.load_data()

    # ===========================
    # UPDATE
    # ===========================

    def update(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Peringatan",
                "Pilih data terlebih dahulu."
            )

            return

        self.controller.update(

            self.selected_id,

            self.entry_nama.get(),

            self.entry_hp.get()

        )

        messagebox.showinfo(
            "Berhasil",
            "Data berhasil diupdate."
        )

        self.clear_form()
        self.load_data()

    # ===========================
    # HAPUS
    # ===========================

    def hapus(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Peringatan",
                "Pilih data dahulu."
            )

            return

        jawab = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus pelanggan ini?"
        )

        if not jawab:
            return

        self.controller.delete(self.selected_id)

        messagebox.showinfo(
            "Berhasil",
            "Data berhasil dihapus."
        )

        self.clear_form()
        self.load_data()

    # ===========================
    # CLEAR
    # ===========================

    def clear_form(self):

        self.selected_id = None

        self.entry_nama.delete(0,"end")
        self.entry_hp.delete(0,"end")
        self.entry_search.delete(0,"end")

        self.tree.selection_remove(self.tree.selection())