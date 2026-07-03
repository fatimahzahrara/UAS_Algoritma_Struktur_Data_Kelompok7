import os
import sys

# Tambahkan direktori file ini ke sys.path agar modul-modul anggota kelompok dapat diimpor dari mana saja
sys.path.append(os.path.dirname(__file__))

from Tugas1_FatimahAzZahra import Queue, Stack
from Tugas2_ArofaBima import RekamMedisBST
from Tugas3_ZahraFaizzaK import MaxHeap


# ===== OBJEK DATA =====
class Pasien:
    """Data rekam medis satu pasien (disimpan di BST)."""
    def __init__(self, no_rm, nama, umur, diagnosa):
        self.no_rm = no_rm
        self.nama = nama
        self.umur = umur
        self.diagnosa = diagnosa

    def __str__(self):
        return f"RM{self.no_rm} - {self.nama} ({self.umur} th), diagnosa: {self.diagnosa}"


class KasusIGD:
    """Entri prioritas penanganan (disimpan di Max-Heap, dibaca via .skor)."""
    def __init__(self, pasien, skor):
        self.pasien = pasien
        self.skor = skor            # 0..100, semakin besar semakin gawat

    def kategori(self):
        if self.skor >= 80:  return "MERAH (kritis)"
        if self.skor >= 50:  return "KUNING (darurat)"
        if self.skor >= 20:  return "HIJAU (ringan)"
        return "PUTIH (non-urgen)"

    def __str__(self):
        return f"[Skor {self.skor}-{self.kategori()}] {self.pasien.nama} (RM{self.pasien.no_rm})"


# ===== SISTEM UTAMA (integrasi keempat struktur data) =====
class RumahSakitSystem:
    def __init__(self):
        self.pendaftaran = Queue()          # Queue: antrean daftar IGD
        self.rekam_medis = RekamMedisBST()  # BST  : data pasien
        self.igd = MaxHeap()                # Heap : prioritas penanganan
        self.riwayat = Stack()              # Stack: riwayat & undo
        self._next_rm = 2001

    # ---------- pendaftaran (Queue) ----------
    def daftar_pasien(self):
        nama = input("Nama pasien: ").strip()
        try:
            umur = int(input("Umur: "))
        except ValueError:
            print("   ! Umur tidak valid."); return
        diagnosa = input("Keluhan/diagnosa awal: ").strip()
        pasien = Pasien(self._next_rm, nama, umur, diagnosa)
        self._next_rm += 1
        self.pendaftaran.enqueue(pasien)
        print(f"   > Terdaftar & masuk antrean: {pasien}")

    def lihat_antrean(self):
        print("\n=== ANTREAN PENDAFTARAN IGD (Queue - FIFO) ===")
        self.pendaftaran.display()

    def proses_pendaftaran(self):
        """Panggil pasien terdepan -> simpan rekam medis (BST) -> prioritas IGD (Heap)."""
        pasien = self.pendaftaran.dequeue()
        if not pasien:
            print("   ! Antrean pendaftaran kosong."); return
        self.rekam_medis.insert(pasien)
        while True:
            try:
                skor = int(input(f"Skor kegawatan {pasien.nama} (0-100): "))
                if 0 <= skor <= 100:
                    break
                print("   ! Skor harus bernilai 0 - 100.")
            except ValueError:
                print("   ! Input tidak valid. Masukkan angka.")
        self.igd.insert(KasusIGD(pasien, skor))
        print(f"   > Rekam medis disimpan & masuk prioritas IGD (skor {skor}).")

    # ---------- rekam medis (BST) ----------
    def tampilkan_rekam_medis(self):
        print("\n=== REKAM MEDIS (Inorder, urut No. RM) ===")
        data = self.rekam_medis.inorder()
        if not data:
            print("   (belum ada rekam medis)")
        for p in data:
            print("  ", p)

    def tampilkan_level_order(self):
        print("\n=== REKAM MEDIS (Level Order / BFS) ===")
        data = self.rekam_medis.level_order()
        if not data:
            print("   (belum ada rekam medis)")
        for p in data:
            print("  ", p)

    def cari_rekam_medis(self):
        try:
            no = int(input("No. RM dicari: "))
        except ValueError:
            print("   ! Input tidak valid."); return
        p = self.rekam_medis.search(no)
        print("   > Ditemukan:", p) if p else print("   ! Rekam medis tidak ada.")

    def hapus_rekam_medis(self):
        try:
            no = int(input("No. RM dihapus: "))
        except ValueError:
            print("   ! Input tidak valid."); return
        if self.rekam_medis.search(no):
            self.rekam_medis.delete(no)
            print("   > Rekam medis dihapus.")
        else:
            print("   ! Rekam medis tidak ada.")

    # ---------- penanganan dokter (Heap) ----------
    def lihat_prioritas(self):
        print("\n=== ANTREAN PRIORITAS IGD (Max-Heap, skor tertinggi dulu) ===")
        self.igd.display()

    def tangani_pasien(self):
        k = self.igd.delete_root()
        if not k:
            print("   ! Tidak ada pasien untuk ditangani."); return
        self.riwayat.push(k)
        print(f"   > DITANGANI DOKTER: {k}")

    # ---------- riwayat (Stack) ----------
    def lihat_riwayat(self):
        print("\n=== RIWAYAT PENANGANAN (Stack - LIFO) ===")
        self.riwayat.display()

    def undo_penanganan(self):
        k = self.riwayat.pop()
        if not k:
            print("   ! Tidak ada yang bisa di-undo."); return
        self.igd.insert(k)
        print(f"   > UNDO, dikembalikan ke antrean IGD: {k}")

    # ---------- info struktur ----------
    def info_struktur(self):
        print("\n=== INFO STRUKTUR DATA ===")
        print(f"   BST rekam medis -> jumlah node: {self.rekam_medis.count()}, "
              f"tinggi: {self.rekam_medis.height()}")
        print(f"   Queue           -> {self.pendaftaran.size()} pasien menunggu daftar")
        print(f"   Heap IGD        -> {len(self.igd.data)} pasien menunggu penanganan")
        print(f"   Stack riwayat   -> {self.riwayat.jumlah} penanganan selesai")


# ===== MENU CLI =====
def main():
    rs = RumahSakitSystem()
    menu_teks = """
==================================================
   RS "HARAPAN BUNDA" - SISTEM IGD (UAS ASD)
==================================================
 [1] Daftar pasien               [7] Lihat prioritas IGD
 [2] Lihat antrean pendaftaran   [8] Tangani pasien (dokter)
 [3] Proses pendaftaran          [9] Lihat riwayat penanganan
 [4] Rekam medis (Inorder)      [10] Undo penanganan terakhir
 [5] Rekam medis (Level Order)  [11] Cari rekam medis
 [6] Hapus rekam medis          [12] Info struktur data
 [0] Keluar
=================================================="""
    aksi = {
        "1": rs.daftar_pasien,        "2": rs.lihat_antrean,
        "3": rs.proses_pendaftaran,   "4": rs.tampilkan_rekam_medis,
        "5": rs.tampilkan_level_order,"6": rs.hapus_rekam_medis,
        "7": rs.lihat_prioritas,      "8": rs.tangani_pasien,
        "9": rs.lihat_riwayat,        "10": rs.undo_penanganan,
        "11": rs.cari_rekam_medis,    "12": rs.info_struktur,
    }
    while True:
        print(menu_teks)
        pilih = input("Pilih menu: ").strip()
        if pilih == "0":
            print("Terima kasih, semoga lekas sehat!")
            break
        fungsi = aksi.get(pilih)
        if fungsi:
            fungsi()
        else:
            print("   ! Pilihan tidak valid.")


if __name__ == "__main__":
    main()