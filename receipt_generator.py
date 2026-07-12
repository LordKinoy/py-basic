import os
import subprocess

from matplotlib import lines
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader

from db_manager import DatabaseManager


class ReceiptGenerator:

    PAPER_WIDTH = 80 * mm
    LEFT = 5 * mm
    RIGHT = 75 * mm

    def __init__(self):
        self.db = DatabaseManager()

    # =========================================================
    # HELPER
    # =========================================================

    def wrap_text(self,text,max_char):

        words=text.split()

        lines=[]

        current=""

        for w in words:

            if len(current+" "+w)<=max_char:

                current=(current+" "+w).strip()

            else:

                lines.append(current)

                current=w

        if current:

            lines.append(current)

        return lines

    def rupiah(self, angka):
        return f"Rp {angka:,.0f}".replace(",", ".")

    def garis(self, pdf, y):
        """
        Garis putus-putus seperti struk minimarket
        """
        pdf.setFont("Courier", 8)
        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            "=" * 42
        )
        return y - 8

    def kanan(self, pdf, y, text):
        pdf.drawRightString(
            self.RIGHT,
            y,
            str(text)
        )

    def buka_pdf(self, filename):
        try:
            os.startfile(filename)
        except:
            try:
                subprocess.Popen(["xdg-open", filename])
            except:
                pass

    # =========================================================
    # HEADER
    # =========================================================

    def draw_header(self, pdf, y, header):

        logo = "assets/images.jpg"

        # ==========================
        # JUDUL
        # ==========================
        pdf.setFont("Courier-Bold", 13)

        title_y = y + 2

        pdf.drawCentredString(
            (self.PAPER_WIDTH - 18 * mm) / 2,
            title_y,
            "SUPERMARKET IPWIJA"
        )

        # ==========================
        # LOGO
        # ==========================
        logo_size = 12 * mm
        logo_x = self.PAPER_WIDTH - 17 * mm

        # Sejajarkan tengah logo dengan tengah tulisan
        logo_y = title_y - (logo_size / 2) + 4

        if os.path.exists(logo):
            pdf.drawImage(
                logo,
                logo_x,
                logo_y,
                width=logo_size,
                height=logo_size,
                preserveAspectRatio=True,
                mask="auto"
            )
        else:
            pdf.rect(
                logo_x,
                logo_y,
                logo_size,
                logo_size
            )

        y -= 20

        y = self.garis(pdf, y)

        # ==========================
        # ALAMAT
        # ==========================
        pdf.setFont("Courier-Bold", 9)

        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            "IPWIJA KAMPUS 2"
        )

        y -= 10

        pdf.setFont("Courier", 8)

        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            "Jl. Letda Nasir No.7 Nagrak, Gunung Putri"
        )

        y -= 9

        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            "Kabupaten Bogor, Jawa Barat 16967"
        )

        y -= 12

        y = self.garis(pdf, y)

        # ==========================
        # INFO TRANSAKSI
        # ==========================
        pdf.setFont("Courier", 8)

        member = header["no_hp"] if header["no_hp"] else "-"

        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            f"{header['invoice']}/{header['kasir']}/{member}"
        )

        y -= 10

        y = self.garis(pdf, y)

        return y    

    # =========================================================
    # DETAIL BARANG
    # =========================================================

    def draw_items(self, pdf, y, detail):

        pdf.setFont("Courier", 8)

        for item in detail:

            subtotal = item["harga"] * item["jumlah"]
            potongan = subtotal - (item["after_diskon"] * item["jumlah"])

            # Pecah nama barang maksimal ±22 karakter
            nama_lines = self.wrap_text(item["nama_barang"], max_char=16)

            # Baris pertama
            pdf.drawString(
                self.LEFT,
                y,
                nama_lines[0]
            )

            pdf.drawRightString(
                self.RIGHT,
                y,
                f"{item['jumlah']:>2}   {item['harga']:>8}   {subtotal:>8}"
            )

            y -= 9

            # Jika nama lebih dari satu baris
            for line in nama_lines[1:]:

                pdf.drawString(
                    self.LEFT,
                    y,
                    line
                )

                y -= 9

            # Diskon
            if item["diskon"] > 0:

                pdf.drawString(
                    self.LEFT,
                    y,
                    f"Disc {item['diskon']}%"
                )

                pdf.drawRightString(
                    self.RIGHT,
                    y,
                    f"-{potongan}"
                )

                y -= 9

            # Space antar item
            y -= 6

        return y

    # =========================================================
    # SUMMARY
    # =========================================================

    def draw_summary(self, pdf, y, header, summary):

        y = self.garis(pdf, y)

        pdf.setFont("Courier", 8)

        pdf.drawString(
            self.LEFT,
            y,
            "Subtotal"
        )

        self.kanan(
            pdf,
            y,
            self.rupiah(summary["subtotal"])
        )

        y -= 10

        if summary["member_diskon"] > 0:

            pdf.drawString(
                self.LEFT,
                y,
                "Disc Member"
            )

            self.kanan(
                pdf,
                y,
                "-" + self.rupiah(summary["member_diskon"])
            )

            y -= 10

        pdf.drawString(
            self.LEFT,
            y,
            "PPN 11%"
        )

        self.kanan(
            pdf,
            y,
            self.rupiah(summary["ppn"])
        )

        y -= 10

        pdf.setFont(
            "Courier-Bold",
            9
        )

        pdf.drawString(
            self.LEFT,
            y,
            "GRAND TOTAL"
        )

        self.kanan(
            pdf,
            y,
            self.rupiah(summary["grand_total"])
        )

        y -= 15

        pdf.setFont(
            "Courier",
            8
        )

        if header["jenis_pembayaran"] == "TUNAI":

            pdf.drawString(
                self.LEFT,
                y,
                "Bayar"
            )

            self.kanan(
                pdf,
                y,
                self.rupiah(header["bayar"])
            )

            y -= 10

            pdf.drawString(
                self.LEFT,
                y,
                "Kembali"
            )

            self.kanan(
                pdf,
                y,
                self.rupiah(header["kembali"])
            )

            y -= 10

        else:

            pdf.drawString(
                self.LEFT,
                y,
                "Pembayaran"
            )

            self.kanan(
                pdf,
                y,
                header["jenis_pembayaran"]
            )

            y -= 10

        return y


    # =========================================================
    # FOOTER
    # =========================================================

    def draw_footer(self, pdf, y):

        y = self.garis(pdf, y)

        pdf.setFont(
            "Courier-Bold",
            9
        )

        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            "TERIMA KASIH"
        )

        y -= 12

        pdf.setFont(
            "Courier",
            8
        )

        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            "SELAMAT BERBELANJA"
        )

        y -= 18

        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            "LAYANAN KONSUMEN"
        )

        y -= 10

        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            "SMS / WA 0899-4566-999"
        )

        y -= 10

        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            "TELP 021998234"
        )

        y -= 10

        pdf.drawCentredString(
            self.PAPER_WIDTH / 2,
            y,
            "KONTAK@IPWIJA.AC.ID"
        )

        return y


    # =========================================================
    # GENERATE PDF
    # =========================================================

    def generate(self, penjualan_id):

        data = self.db.get_receipt_data(
            penjualan_id
        )

        if not data:
            raise Exception(
                "Data tidak ditemukan."
            )

        header = data["header"]
        detail = data["detail"]
        summary = data["summary"]

        os.makedirs(
            "receipts",
            exist_ok=True
        )

        filename = (
            f"receipts/{header['invoice']}.pdf"
        )

        # =====================================================
        # Dynamic Height
        # =====================================================

        base = 115

        per_barang = 28

        footer = 60

        tinggi = (base + footer + (len(detail)*per_barang))*mm

        pdf = canvas.Canvas(
            filename,
            pagesize=(
                self.PAPER_WIDTH,
                tinggi
            )
        )

        y = tinggi - 10 * mm

        # HEADER
        y = self.draw_header(
            pdf,
            y,
            header
        )

        # BARANG
        y = self.draw_items(
            pdf,
            y,
            detail
        )

        # SUMMARY
        y = self.draw_summary(
            pdf,
            y,
            header,
            summary
        )

        # FOOTER
        self.draw_footer(
            pdf,
            y
        )

        pdf.save()

        self.buka_pdf(
            filename
        )

        return filename