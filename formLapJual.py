# file: formLapJual.py
# desain form laporan untuk penjualan
# tgl_buat: 14 okt 2010 09.32 PM
# tgl_revisi : -
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
import sqlite3
import tkinter.messagebox as tkMessageBox

class FormLapJual(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        self.geometry("+%d+%d" % (parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
            
        self.width = 970
        self.height = 400
                    
        self.aturKomponen()
        self.koneksiDatabase()
        
        self.resizable(width=False, height=False)
        self.title("Form Laporan Seluruh Penjualan")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.parent = parent
        
        # setting awal
        self.x1 = 15  #
        self.x2 = 100 #
        self.x3 = 200 #
        self.x4 = 270 #
        self.x5 = 500 #
        self.x6 = 620 #
        self.x7 = 720 #
        self.x8 = 820 #
        
        self.onShow(self.x1, self.x2, self.x3, self.x4,
            self.x5, self.x6, self.x7, self.x8)
        self.buttonExit.focus_set()
        
        self.wait_window()
    
    def aturKomponen(self):
        # frame utama
        mainFrame = Frame(self)
        mainFrame.pack(fill=BOTH, expand=YES)
        
        # >>> frame_canvas
        fr_canvas = Frame(mainFrame)
        fr_canvas.pack(fill=BOTH, expand=YES)
        
        self.kanvas = Canvas(fr_canvas, width=self.width, 
            height=self.height, bg="white")
        self.kanvas.pack(fill=BOTH, expand=YES)
        
        self.scrollReg(0)
        
        scroll = Scrollbar(fr_canvas)
        scroll.config(command=self.kanvas.yview)
        self.kanvas.config(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        self.kanvas.pack(side=LEFT, expand=YES, fill=BOTH)
        
        # >>> frame tombol
        fr_tombol = Frame(mainFrame, bd=10)
        fr_tombol.pack(fill=BOTH, expand=YES)
        
        self.buttonExit = Button(fr_tombol, text="Keluar",
            command=self.onClose, width=15, underline=0)
        self.buttonExit.pack()
                
    def koneksiDatabase(self):
        self.db = sqlite3.connect("./data/datatoko.db")
        self.cur = self.db.cursor()     
        
        self.sqlJual = """
            SELECT penjualan.no_nota, penjualan.tgl_nota, 
                detpenjualan.kd_produk, produk.nm_produk, 
                detpenjualan.hrg_jual, detpenjualan.jml_jual, 
                detpenjualan.subtotal, pengguna.nm_pengguna
            FROM penjualan, detpenjualan, produk, pengguna
            WHERE penjualan.no_nota=detpenjualan.no_nota AND 
                detpenjualan.kd_produk=produk.kd_produk AND 
                penjualan.kd_pengguna=pengguna.kd_pengguna;         
            """
            
    def eksekusi(self, sql):
        self.cur.execute(sql)
        lineData = self.cur.fetchall()
        totData = len(lineData)
        
        return lineData, totData
        
    def kopLaporan(self, x1, x2, x3, x4, x5, x6, x7, x8):
        self.kanvas.create_text(x1-5, 20, 
            text="Laporan Seluruh Penjualan", 
            font=("Arial", 14, "bold"), anchor=W)
        self.kanvas.create_line(x1-5, 40, 950, 40)
        self.kanvas.create_line(x1-5, 43, 950, 43)
        
        self.kanvas.create_text(x1, 55, 
            text="NO TRANS", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_text(x2, 55, 
            text="TGL TRANS", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_text(x3, 55, 
            text="KODE", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_text(x4, 55, 
            text="NAMA PRODUK", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_text(x5, 55, 
            text="HARGA JUAL", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_text(x6, 55, 
            text="JUMLAH", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_text(x7, 55, 
            text="SUBTOTAL", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_text(x8, 55, 
            text="NAMA PENGGUNA", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_line(x1-5, 67, 950, 67)
        self.kanvas.create_line(x1-5, 70, 950, 70)      
        
    def onShow(self, x1, x2, x3, x4, x5, x6, x7, x8, event=None):
        self.kopLaporan(x1, x2, x3, x4, x5, x6, x7, x8)
        
        bar, jum = self.eksekusi(self.sqlJual)
        
        if jum > 15:
            selisih = jum-15
            
            delta = selisih*20
            self.scrollReg(delta)
                    
        spasi = 0
        for data in range(jum):
            spasi += 20
            
            self.no_trans = self.kanvas.create_text(x1, 70+spasi,
                text=bar[data][0], anchor=W)
        
            self.tgl_trans = self.kanvas.create_text(x2, 70+spasi,
                text=bar[data][1], anchor=W)
        
            self.kd_pro = self.kanvas.create_text(x3, 70+spasi,
                text=bar[data][2], anchor=W)
        
            self.nm_pro = self.kanvas.create_text(x4, 70+spasi,
                text=bar[data][3], anchor=W)
        
            self.hrg_jual = self.kanvas.create_text(x5, 70+spasi,
                text=bar[data][4], anchor=W)
        
            self.jum = self.kanvas.create_text(x6, 70+spasi,
                text=bar[data][5], anchor=W)
        
            self.subtot = self.kanvas.create_text(x7, 70+spasi,
                text=bar[data][6], anchor=W)
        
            self.nm_user = self.kanvas.create_text(x8, 70+spasi,
                text=bar[data][7], anchor=W)
        
    def scrollReg(self, delta):
        self.kanvas.config(scrollregion=(0, 0, self.width, 
            self.height+delta))
                
    def onClose(self, event=None):
        self.cur.close()
        self.db.close()
        self.destroy()
        
if __name__ == '__main__':
    root = Tk()
    
    def run():
        import formLapJual
        obj = formLapJual.FormLapJual(root)
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()
