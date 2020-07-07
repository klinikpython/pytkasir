# file: formUbahHarga.py
# desain form untuk ubah harga satuan
# tgl_buat: 8 OKT 2010 08.40 AM
# tgl_revisi : -
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
import sqlite3
import tkinter.messagebox as tkMessageBox


class FormUbahHarga(Toplevel):
    def __init__(self, parent, kdProduk):
        Toplevel.__init__(self, parent)
                
        self.geometry("+%d+%d" % (parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
                        
        self.koneksiDatabase()
        self.aturKomponen()
        self.aturKejadian()
        
        self.resizable(width=False, height=False)
        self.title("Perubahan Harga Satuan")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.parent = parent
        self.kdProduk = kdProduk
        
        # setting awal
        self.displayData(self.kdProduk)
        self.entryHrgPro.focus_set()
        
        self.wait_window()
        
    def aturKomponen(self):
        # atur frame utama
        mainFrame = Frame(self, bd=10)
        mainFrame.pack(fill=BOTH, expand=YES)
        
        # >> atur komponen frame_data
        fr_data = Frame(mainFrame)
        fr_data.pack(fill=BOTH, expand=YES)
        
        Label(fr_data, text='Kode Produk').grid(row=0, 
            column=0, sticky=W)
        self.entryKdPro = Entry(fr_data, width=7)
        self.entryKdPro.grid(row=0, column=1, sticky=W)
        
        Label(fr_data, text='Nama Produk').grid(row=1, 
            column=0, sticky=W)
        self.entryNmPro = Entry(fr_data, width=30)
        self.entryNmPro.grid(row=1, column=1, sticky=W)
        
        Label(fr_data, text='Harga Produk').grid(row=2, 
            column=0, sticky=W)
        self.entryHrgPro = Entry(fr_data, width=15, justify=RIGHT)
        self.entryHrgPro.grid(row=2, column=1, sticky=W)
        
        # >> atur komponen frame_tombol
        fr_tombol = Frame(mainFrame)
        fr_tombol.pack(fill=BOTH, expand=YES, pady=5)
        
        self.buttonUbah = Button(fr_tombol, text="Ubah Data", 
            command=self.onUbahData)
        self.buttonUbah.pack(side=BOTTOM, fill=BOTH, expand=YES)
        
        
    def aturKejadian(self):
        self.entryHrgPro.bind("<Return>", self.onHrgProEnter)
        self.buttonUbah.bind("<Return>", self.onUbahEnter)
        
    def koneksiDatabase(self):
        self.db = sqlite3.connect("./data/datatoko.db")
        self.cur = self.db.cursor()     
        
        self.sqlPro = "SELECT * FROM produk"
        
    def eksekusi(self, sql):
        self.cur.execute(sql)
        lineData = self.cur.fetchall()
        totData = len(lineData)
        
        return lineData, totData
        
    def onUbahData(self, event=None):
        hrg_pro = self.entryHrgPro.get()
        
        str = "UPDATE produk SET hrg_produk='%s' WHERE kd_produk='%s'"%(
            hrg_pro, self.kdProduk)
        
        tkMessageBox.showinfo("Informasi", 
            "Data telah diubah.", parent=self)
            
        self.cur.execute(str)
        self.db.commit()
        
        self.onClose()
        
    def onClose(self, event=None):
        #self.parent.destroy()
        self.cur.close()
        self.db.close()
        self.destroy()
        
    def displayData(self, kdProduk):
        cariSQL = self.sqlPro + " WHERE UPPER(kd_produk)=UPPER('" + kdProduk + "')"
        
        bar, jum = self.eksekusi(cariSQL)
        
        self.kosongkanEntry()
        
        self.entryKdPro.insert(END, bar[0][0])
        self.entryNmPro.insert(END, bar[0][1])
        self.entryHrgPro.insert(END, bar[0][2])
        
        self.entryKdPro.configure(state=DISABLED)
        self.entryNmPro.configure(state=DISABLED)       
        
    def kosongkanEntry(self):
        self.entryKdPro.delete(0, END)
        self.entryNmPro.delete(0, END)
        self.entryHrgPro.delete(0, END)
        
    def onHrgProEnter(self, event):
        self.buttonUbah.focus_set()
        
    def onUbahEnter(self, event):
        self.onUbahData()
        
if __name__ == '__main__':
    root = Tk()
    
    def run():
        import formUbahHarga
        obj = formUbahHarga.FormUbahHarga(root, "B0002")
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()


