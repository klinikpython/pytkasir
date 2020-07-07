# file: formLapLaris.py
# desain form laporan untuk data terlaris
# tgl_buat: 14 okt 2010 09.42 PM
# tgl_revisi : -
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
import sqlite3
import tkinter.messagebox as tkMessageBox

class FormLapLaris(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        self.geometry("+%d+%d" % (parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
        
        self.height = 400
        self.width = 640
                    
        self.aturKomponen()
        self.koneksiDatabase()
        
        self.resizable(width=False, height=False)
        self.title("Form Laporan Produk")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.parent = parent
        
        # setting awal
        self.x1 = 15
        self.x2 = 100
        self.x3 = 360
        
        self.onShow(self.x1, self.x2, self.x3)
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
        
        self.sqlLaris = """
            SELECT produk.kd_produk, produk.nm_produk, 
                sum(detpenjualan.jml_jual)
            FROM produk, detpenjualan
            WHERE detpenjualan.kd_produk=produk.kd_produk
            GROUP BY 1 ORDER BY 3 DESC
            """
        
    def eksekusi(self, sql):
        self.cur.execute(sql)
        lineData = self.cur.fetchall()
        totData = len(lineData)
        
        return lineData, totData
        
    def kopLaporan(self, x1, x2, x3):
        self.kanvas.create_text(x1-5, 20, 
            text="Laporan Produk Terjual (Terlaris)", 
            font=("Arial", 14, "bold"), anchor=W)
        self.kanvas.create_line(x1-5, 40, 600, 40)
        self.kanvas.create_line(x1-5, 43, 600, 43)
        
        self.kanvas.create_text(x1, 55, 
            text="KODE", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_text(x2, 55, 
            text="NAMA PRODUK", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_text(x3, 55, 
            text="JUMLAH TERJUAL", 
            font=("Arial", 10, "bold"), anchor=W)

        self.kanvas.create_line(x1-5, 67, 600, 67)
        self.kanvas.create_line(x1-5, 70, 600, 70)
                        
    def onShow(self, x1, x2, x3, event=None):
        self.kopLaporan(x1, x2, x3)     
        
        bar, jum = self.eksekusi(self.sqlLaris)
        
        if jum > 15:
            selisih = jum-15
            
            delta = selisih*20
            self.scrollReg(delta)
        
        spasi = 0
        for data in range(jum):
            spasi += 20
            
            self.kode = self.kanvas.create_text(x1, 70+spasi,
                text=bar[data][0], anchor=W)
        
            self.nama = self.kanvas.create_text(x2, 70+spasi,
                text=bar[data][1], anchor=W)
        
            self.jml_jual = self.kanvas.create_text(x3, 70+spasi,
                text=bar[data][2], anchor=W)
        
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
        import formLapLaris
        obj = formLapLaris.FormLapLaris(root)
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()

    
