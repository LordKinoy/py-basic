from db_manager import DatabaseManager

class PelangganController:

    def __init__(self):
        self.db = DatabaseManager()

    def get_all(self):
        return self.db.get_all_pelanggan()

    def insert(self, nama, no_hp):
        self.db.insert_pelanggan(
            nama,
            no_hp
        )

    def update(self, id, nama, no_hp ):
        self.db.update_pelanggan(
            id,
            nama,
            no_hp
        )

    def delete(self, id):
        self.db.delete_pelanggan(id)

    def search(self, keyword):
        return self.db.search_pelanggan(keyword)