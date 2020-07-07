# file: buatDataKasir.py
# membuat database kasir --> datatoko.db
# terdiri dari :
#   1. tabel supplier
#   2. tabel produk
#   3. tabel pengguna
#   4. tabel barang_masuk
#   5. tabel detbarang_masuk
#   6. tabel penjualan
#   7. tabel detpenjualan
# tgl buat: 15 okt 2010 12.08 AM
# tgl revisi: -
# lisensi: GPL
# dibuat oleh: masbiggie -- www.pythondahsyat.blogspot.com

import sqlite3
import os

class DatabaseToko():
    def __init__(self, file):
        self.file = file
        self.formLoad()
        
    def koneksiDatabase(self):
        self.db = sqlite3.connect(self.file)
        self.cur = self.db.cursor()
        
    def formLoad(self):
        self.status = os.path.exists(self.file)
        
        if self.status:
            print ("File database sudah ada...")
        else:
            self.koneksiDatabase()
            self.createTable()
        
    def createTable(self):
        self.buatTableSupplier()
        self.buatTableProduk()
        self.buatTablePengguna()
        self.buatTableBarangMasuk()
        self.buatTableDetBarangMasuk()
        self.buatTablePenjualan()
        self.buatTableDetPenjualan()
        
        # simpan ke database
        self.db.commit()
        print ("semua table tersimpan...")
        
        # tutup database
        self.cur.close()
        self.db.close()
        print ("database ditutup...")
        
    def buatTableSupplier(self):
        sqlSup = """CREATE TABLE supplier(
            kd_supplier TEXT PRIMARY KEY,
            nm_supplier TEXT NOT NULL,
            no_telp TEXT NOT NULL,
            alamat TEXT NOT NULL)"""
            
        self.cur.execute(sqlSup)
        
        print ("table supplier...")

    def buatTableProduk(self):
        sqlPro = """CREATE TABLE produk(
            kd_produk TEXT PRIMARY KEY,
            nm_produk TEXT NOT NULL,
            hrg_produk INTEGER NOT NULL DEFAULT 0,
            stok_produk INTEGER NOT NULL DEFAULT 0)"""
            
        self.cur.execute(sqlPro)
        
        print ("table produk...")
        
    def buatTablePengguna(self):
        sqlUser = """CREATE TABLE pengguna(
            kd_pengguna TEXT PRIMARY KEY,
            nm_pengguna TEXT NOT NULL,
            pass_pengguna TEXT NOT NULL,
            status TEXT NOT NULL)"""
            
        self.cur.execute(sqlUser)
        print ("table pengguna...",)
        
        sqlInsertUser = """INSERT INTO pengguna(kd_pengguna,
            nm_pengguna, pass_pengguna, status)
            VALUES("PG01", "root", "master", "admin")"""
        
        self.cur.execute(sqlInsertUser)
        print ("isi pengguna(root)...")
        
    def buatTableBarangMasuk(self):
        sqlBarmas = """CREATE TABLE barang_masuk(
            no_masuk TEXT PRIMARY KEY,
            tgl_masuk TEXT NOT NULL,
            kd_supplier TEXT NOT NULL,
            total INTEGER NOT NULL DEFAULT 0,
            kd_pengguna TEXT NOT NULL)"""
            
        self.cur.execute(sqlBarmas)
        print ("table barang_masuk...")
        
    def buatTableDetBarangMasuk(self):
        sqlDetBarmas = """CREATE TABLE detbarang_masuk(
            no_masuk TEXT NOT NULL,
            kd_produk TEXT NOT NULL,
            hrg_beli INTEGER NOT NULL DEFAULT 0,
            jml_beli INTEGER NOT NULL DEFAULT 0,
            subtotal INTEGER NOT NULL DEFAULT 0)"""
            
        self.cur.execute(sqlDetBarmas)
        print ("table detbarang_masuk...")
        
    def buatTablePenjualan(self):
        sqlJual = """CREATE TABLE penjualan(
            no_nota TEXT PRIMARY KEY,
            tgl_nota TEXT NOT NULL,
            total_bayar INTEGER NOT NULL DEFAULT 0,
            kd_pengguna TEXT NOT NULL)"""
            
        self.cur.execute(sqlJual)
        print ("table penjualan...")
        
    def buatTableDetPenjualan(self):
        sqlDetJual = """CREATE TABLE detpenjualan(
            no_nota TEXT NOT NULL,
            kd_produk TEXT NOT NULL,
            hrg_jual INTEGER NOT NULL DEFAULT 0,
            jml_jual INTEGER NOT NULL DEFAULT 0,
            subtotal INTEGER NOT NULL DEFAULT 0)"""
            
        self.cur.execute(sqlDetJual)
        print ("table detpenjualan...")
        
if __name__ == '__main__':
    buatData = DatabaseToko("./data/datatoko.db")
