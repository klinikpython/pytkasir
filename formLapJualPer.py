# file: formLapJualPer.py
# desain form laporan Penjualan per periode
# tgl_buat: 28 okt 2010 11.39 AM
# tgl_revisi : -
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
from datetime import *
import sqlite3
import tkinter.messagebox as tkMessageBox
import string

class FormLapJualPer(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        self.geometry("+%d+%d" % (parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
            
        self.width = 970
        self.height = 400
                    
        self.aturKomponen()
        self.koneksiDatabase()
        
        self.resizable(width=False, height=False)
        self.title("Form Laporan Penjualan Per Periode")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.parent = parent
        
        # setting awal
        self.setToday()

        self.x1 = 15  #
        self.x2 = 100 #
        self.x3 = 200 #
        self.x4 = 270 #
        self.x5 = 500 #
        self.x6 = 620 #
        self.x7 = 720 #
        self.x8 = 820 #
        
        self.buttonShow.focus_set()
                
        self.wait_window()
    
    def aturKomponen(self):
        # frame utama
        mainFrame = Frame(self)
        mainFrame.pack(fill=BOTH, expand=YES)
        
        # >>> frame_tanggal
        fr_tgl = Frame(mainFrame, bd=10)
        fr_tgl.pack()
        
        Label(fr_tgl, text='Tanggal Awal (th-bl-hr)').grid(row=0,
            column=0, sticky=W)
        self.spinAwalTah = Spinbox(fr_tgl, from_=2010, to=2099,
            width=5)
        self.spinAwalTah.grid(row=0, column=1)
        self.spinAwalBul = Spinbox(fr_tgl, from_=1, to=12,
            width=3)
        self.spinAwalBul.grid(row=0, column=2)
        self.spinAwalHar = Spinbox(fr_tgl, from_=1, to=31,
            width=3)
        self.spinAwalHar.grid(row=0, column=3)
        
        Label(fr_tgl, text='Tanggal Akhir (th-bl-hr)').grid(row=1,
            column=0, sticky=W)
        self.spinAkhirTah = Spinbox(fr_tgl, from_=2010, to=2099,
            width=5)
        self.spinAkhirTah.grid(row=1, column=1)
        self.spinAkhirBul = Spinbox(fr_tgl, from_=1, to=12,
            width=3)
        self.spinAkhirBul.grid(row=1, column=2)
        self.spinAkhirHar = Spinbox(fr_tgl, from_=1, to=31,
            width=3)
        self.spinAkhirHar.grid(row=1, column=3)     
        
        self.buttonShow = Button(fr_tgl, text="Show Data",
            command=self.onShowData, width=10)
        self.buttonShow.grid(row=0, column=4, rowspan=2, 
            sticky=W+E+N+S, padx=5)
        
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
        
    def eksekusi(self, sql):
        self.cur.execute(sql)
        lineData = self.cur.fetchall()
        totData = len(lineData)
        
        return lineData, totData
        
    def kopLaporan(self, x1, x2, x3, x4, x5, x6, x7, x8, a, b):
        self.kanvas.create_text(x1-5, 20, 
            text="Laporan Penjualan Per Periode", 
            font=("Arial", 14, "bold"), anchor=W)
            
        self.kanvas.create_text(x1+300, 20, 
            text="Periode ::  %s s/d %s"%(a, b), 
            font=("Arial", 12), anchor=W)

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
        
    def onShowData(self, event=None):
        self.onShow(self.x1, self.x2, self.x3, self.x4,
            self.x5, self.x6, self.x7, self.x8)
            
        self.buttonShow.focus_set()
        
    def onShow(self, x1, x2, x3, x4, x5, x6, x7, x8, event=None):
        self.kanvas.delete(ALL)
        
        tglAwal = self.editTanggal(self.spinAwalTah.get(), 
            self.spinAwalBul.get(), self.spinAwalHar.get())         
        tglAkhir = self.editTanggal(self.spinAkhirTah.get(), 
            self.spinAkhirBul.get(), self.spinAkhirHar.get())
                            
        self.kopLaporan(x1, x2, x3, x4, x5, x6, x7, x8,
            tglAwal, tglAkhir)
        
        self.sqlJual = """
            SELECT penjualan.no_nota, penjualan.tgl_nota, 
                detpenjualan.kd_produk, produk.nm_produk, 
                detpenjualan.hrg_jual, detpenjualan.jml_jual, 
                detpenjualan.subtotal, pengguna.nm_pengguna
            FROM penjualan, detpenjualan, produk, pengguna
            WHERE penjualan.no_nota=detpenjualan.no_nota AND 
                detpenjualan.kd_produk=produk.kd_produk AND 
                penjualan.kd_pengguna=pengguna.kd_pengguna AND      
                ((penjualan.tgl_nota >= '%s') AND 
                (penjualan.tgl_nota <= '%s'));
            """ %(tglAwal, tglAkhir)
                    
        bar, jum = self.eksekusi(self.sqlJual)
        
        if jum > 15:
            selisih = jum-15
            
            delta = selisih*20
            self.scrollReg(delta)
                    
        spasi = 0
        sumTotal =0
        
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
                
            sumTotal += int(bar[data][6])
        
        self.kanvas.create_text(x1+600, 20, 
            text="TOTAL PENJUALAN :: %s"%(str(sumTotal)), 
            font=("Arial", 12, 'bold'), anchor=W)
                
    def scrollReg(self, delta):
        self.kanvas.config(scrollregion=(0, 0, self.width, 
            self.height+delta))
                
    def onClose(self, event=None):
        self.cur.close()
        self.db.close()
        self.destroy()
        
    def setToday(self):
        tglSkrg = str(date.today())
        strTglSkrg = tglSkrg.split('-')
        
        self.setTanggal(strTglSkrg[0], strTglSkrg[1], strTglSkrg[2])
        
    def setTanggal(self, tah, bul, har):
        self.spinAwalTah.delete(0, END)
        self.spinAwalBul.delete(0, END)
        self.spinAwalHar.delete(0, END)
        self.spinAkhirTah.delete(0, END)
        self.spinAkhirBul.delete(0, END)
        self.spinAkhirHar.delete(0, END)
        
        self.spinAwalTah.insert(END, tah)
        self.spinAwalBul.insert(END, bul)
        self.spinAwalHar.insert(END, har)       
        self.spinAkhirTah.insert(END, tah)
        self.spinAkhirBul.insert(END, bul)
        self.spinAkhirHar.insert(END, har)
        
    def editTanggal(self, tah, bul, har):
        if int(har) < 10:
            har = "0"+har
            
        if int(bul) < 10:
            bul = "0"+bul
            
        teks = "%s%s%s"%(tah, bul, har)
        
        return teks
                
if __name__ == '__main__':
    root = Tk()
    
    def run():
        import formLapJualPer
        obj = formLapJualPer.FormLapJualPer(root)
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()

                
        
    
