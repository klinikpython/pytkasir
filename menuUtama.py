# file: menuUtama.py
# File utama yang berisi menu program pyTKasir
# tgl.release: 15 Oktober 2010 12.59 AM
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
import formLogin
import formSupplier
import formProduk
import formPengguna
import formTransBeli
import formTransJual
import formLapSup
import formLapPro
import formLapBarmas
import formLapJual
import formLapLaris
import formAbout
import formLapMasPer
import formLapJualPer
import formLapRL


class MenuUtama():
    def __init__(self, parent, title):
        self.parent = parent
        
        parent.title(title)
        parent.geometry("+200+50")
        parent.resizable(width=False, height=False)
        parent.protocol('WM_DELETE_WINDOW', self.onPass)
        
        self.aturKomponen()
        self.aturKejadian()
        
        # setting awal
        self.tampilanAwal()
        self.pengguna = 'kosong'
        self.kdPengguna = "PG"
        
    def aturKomponen(self):
        # atur main frame
        MainFrame = Frame(self.parent)
        MainFrame.pack(fill=BOTH, expand=YES)
        
        # setting tampilan menu
        self.mainMenu = Menu(self.parent)
        self.parent.config(menu=self.mainMenu)      
        # sub menu :: Utama
        self.utama = Menu(self.mainMenu)
        self.utama.add_command(label='Login', underline=0,
            command=self.loginDatabase)
        self.utama.add_command(label='Logout', underline=1,
            command=self.logoutDatabase)
        self.utama.add_separator()
        self.utama.add_command(label='Keluar', underline=0, 
            command=self.onClose)
        self.mainMenu.add_cascade(label='Utama', 
            menu=self.utama, underline=0)
        # sub menu :: Input Data
        self.input = Menu(self.mainMenu)
        self.input.add_command(label='Data Supplier', 
            underline=5, command=self.datSupplier)
        self.input.add_command(label='Data Produk', 
            underline=5, command=self.datProduk)
        self.input.add_separator()
        self.input.add_command(label='Data Pengguna', 
            underline=5, command=self.datPengguna)
        self.mainMenu.add_cascade(label='Input Data', 
            menu=self.input, underline=0)
        # sub menu :: Transaksi
        self.transaksi = Menu(self.mainMenu)
        self.transaksi.add_command(label='Transaksi Barang Masuk', 
            underline=10, command=self.tranMasuk)
        self.transaksi.add_command(label='Transaksi Penjualan',
            underline=10, command=self.tranJual)
        self.mainMenu.add_cascade(label='Transaksi', 
            menu=self.transaksi, underline=0)       
        # sub menu :: Laporan
        self.laporan = Menu(self.mainMenu)
        self.laporan.add_command(label='Laporan Seluruh Supplier', 
            underline=16, command=self.lapSupplier)
        self.laporan.add_command(label='Laporan Seluruh Produk',
            underline=16, command=self.lapProduk)
        self.laporan.add_separator()
        self.laporan.add_command(label='Laporan Seluruh Barang Masuk',
            underline=16, command=self.lapMasuk)
        self.laporan.add_command(label='Laporan Barang Masuk Per Periode',
            underline=16, command=self.lapMasukPeriode)
        self.laporan.add_command(label='Laporan Laba Rugi',
            underline=15, command=self.lapRugiLaba)
        self.laporan.add_separator()
        self.laporan.add_command(label='Laporan Seluruh Penjualan',
            underline=17, command=self.lapJual)
        self.laporan.add_command(label='Laporan Penjualan Per Periode',
            underline=16, command=self.lapJualPeriode)
        self.laporan.add_separator()
        self.laporan.add_command(label='Laporan Produk Terlaris',
            underline=15, command=self.lapLaris)
        self.mainMenu.add_cascade(label='Laporan', 
            menu=self.laporan, underline=0)
        # sub menu :: Sistem
        self.sistem = Menu(self.mainMenu)
        self.sistem.add_command(label='Tentang Program',
            underline=0, command=self.sisAbout)
        self.mainMenu.add_cascade(label='Sistem', 
            menu=self.sistem, underline=0)      
            
        # setting background image via Canvas
        self.bgImage = PhotoImage(file="./data/background.GIF")
        
        bgCanvas = Canvas(MainFrame, width=901, height=600)
        bgCanvas.pack(fill=BOTH, expand=YES)
        bgCanvas.create_image(0, 0, image=self.bgImage, 
            anchor=NW)
            
        self.statusBar = Label(MainFrame, text="", bd=1, 
            relief=SUNKEN, anchor=E)
        self.statusBar.pack(side=BOTTOM, fill=X)
            
    def aturKejadian(self):
        pass 
        
    def tampilanAwal(self):
        self.mainMenu.entryconfig(2, state=DISABLED)
        self.mainMenu.entryconfig(3, state=DISABLED)
        self.mainMenu.entryconfig(4, state=DISABLED)
        self.mainMenu.entryconfig(5, state=DISABLED)
        self.utama.entryconfig(1, state=NORMAL)
        self.utama.entryconfig(2, state=DISABLED)
        self.utama.entryconfig(4, state=NORMAL)
        
    def menuKasir(self):
        self.mainMenu.entryconfig(2, state=DISABLED)
        self.mainMenu.entryconfig(3, state=NORMAL)
        self.mainMenu.entryconfig(4, state=NORMAL)
        self.mainMenu.entryconfig(5, state=NORMAL)
        self.utama.entryconfig(1, state=DISABLED)
        self.utama.entryconfig(2, state=NORMAL)
        self.utama.entryconfig(4, state=DISABLED)
        self.transaksi.entryconfig(1, state=DISABLED)
        self.laporan.entryconfig(1, state=DISABLED)
        self.laporan.entryconfig(2, state=DISABLED)
        self.laporan.entryconfig(4, state=DISABLED)
        self.laporan.entryconfig(5, state=DISABLED)
        self.laporan.entryconfig(6, state=DISABLED)
                
    def menuAdmin(self):
        self.mainMenu.entryconfig(2, state=NORMAL)
        self.mainMenu.entryconfig(3, state=NORMAL)
        self.mainMenu.entryconfig(4, state=NORMAL)
        self.mainMenu.entryconfig(5, state=NORMAL)
        self.utama.entryconfig(1, state=DISABLED)
        self.utama.entryconfig(2, state=NORMAL)
        self.utama.entryconfig(4, state=DISABLED)
                        
        self.transaksi.entryconfig(1, state=NORMAL)
        self.laporan.entryconfig(1, state=NORMAL)
        self.laporan.entryconfig(2, state=NORMAL)
        self.laporan.entryconfig(4, state=NORMAL)
        self.laporan.entryconfig(5, state=NORMAL)
        self.laporan.entryconfig(6, state=NORMAL)
                
    def loginDatabase(self):
        app = formLogin.FormLogin(self.parent)
        
        kode, nama, status = app.getNmPengguna()
        
        if status == "admin":
            self.menuAdmin()
            self.statusBar["text"] = ":: %s [%s] ::"%(nama, 
                status)
            self.kdPengguna = kode
        elif status == "kasir":
            self.menuKasir()
            self.statusBar["text"] = ":: %s [%s] ::"%(nama, 
                status)
            self.kdPengguna = kode

    def logoutDatabase(self):
        self.pengguna = "kosong"
        self.kdPengguna = "PG"
        self.statusBar["text"] = ""     
        self.tampilanAwal()
                        
    def onClose(self, event=None):
        self.parent.destroy()
        
    def datSupplier(self):
        formSupplier.FormSupplier(self.parent)
        
    def datProduk(self):
        formProduk.FormProduk(self.parent)
        
    def datPengguna(self):
        formPengguna.FormPengguna(self.parent)
    
    def tranMasuk(self):
        formTransBeli.FormTransBeli(self.parent, self.kdPengguna)
        
    def tranJual(self):
        formTransJual.FormTransJual(self.parent, self.kdPengguna)
        
    def lapSupplier(self):
        formLapSup.FormLapSup(self.parent)
        
    def lapProduk(self):
        formLapPro.FormLapPro(self.parent)
        
    def lapMasuk(self):
        formLapBarmas.FormLapBarmas(self.parent)

    def lapMasukPeriode(self):
        formLapMasPer.FormLapMasPer(self.parent)
        
    def lapJual(self):
        formLapJual.FormLapJual(self.parent)
    
    def lapJualPeriode(self):
        formLapJualPer.FormLapJualPer(self.parent)
                
    def lapLaris(self):
        formLapLaris.FormLapLaris(self.parent)
        
    def lapRugiLaba(self):
        formLapRL.FormLapRL(self.parent)
        
    def sisAbout(self):
        formAbout.FormAbout(self.parent)
                
    def onPass(self):
        #self.onClose()  
        pass
    
        
if __name__ == '__main__':
    root = Tk()
    
    aplikasi = MenuUtama(root, ":: pyTKasir 0.01.0 :: ")
    
    root.mainloop()
        
        
        
