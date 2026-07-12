from db_manager import DatabaseManager

class BarangController:

    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        return self.db.get_all_barang()

    def insert(self,kode,nama,satuan,harga,stok,diskon):
        self.db.insert_barang(
            kode,
            nama,
            satuan,
            harga,
            stok,
            diskon
        )

    def update(self,id_barang,kode,nama,satuan,harga,stok,diskon):
        self.db.update_barang(
            id_barang,
            kode,
            nama,
            satuan,
            harga,
            stok,
            diskon
        )

    def delete(self,id_barang):
        self.db.delete_barang(id_barang)

    def search(self,keyword):
        return self.db.search_barang_crud(keyword)
    
    def get_next_kode(self):
        return self.db.get_next_kode_barang()