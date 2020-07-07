# file: formCariProduk.py
# desain form untuk ubah harga satuan
# tgl_buat: 8 OKT 2010 08.40 AM
# tgl_revisi : -
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
import sqlite3
import tkinter.messagebox as tkMessageBox


class FormCariProduk(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
                
        self.geometry("+%d+%d" % (parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
                        
        self.koneksiDatabase()
        self.aturKomponen()
        self.aturKejadian()
        
        self.resizable(width=False, height=False)
        self.title("Cari Produk")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.parent = parent
        
        # setting awal
        self.entryCariPro.focus_set()
        self.isiDataList(self.sqlPro)
        self.kodeProduk = ""
        
        self.wait_window()
        
    def aturKomponen(self):
        # atur frame utama
        mainFrame = Frame(self, bd=10)
        mainFrame.pack(fill=BOTH, expand=YES)
        
        # >> atur komponen frame_data
        fr_data = Frame(mainFrame)
        fr_data.pack(fill=BOTH, expand=YES)
        
        Label(fr_data, text='Pencarian berdasar nama:').grid(row=0, 
            column=0, sticky=W)
        self.entryCariPro = Entry(fr_data, width=30)
        self.entryCariPro.grid(row=0, column=1, sticky=W)
                
        # >> atur komponen frame_list
        fr_list = Frame(mainFrame)
        fr_list.pack(fill=BOTH, expand=YES, pady=5)
        
        self.list = Listbox(fr_list, width=30)
        self.list.pack(side=LEFT, fill=BOTH, expand=YES)
        
        scrollbar = Scrollbar(fr_list, orient=VERTICAL,
            command=self.list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list.config(yscrollcommand=scrollbar.set)      
        
    def aturKejadian(self):
        self.entryCariPro.bind("<KeyRelease>", self.onCariKeyRelease)
        self.entryCariPro.bind("<Return>", self.onCariEnter)
        
        self.list.bind("<Double-Button-1>", self.onDblListKlik)
        self.list.bind("<Return>", self.onListEnter)
        
    def koneksiDatabase(self):
        self.db = sqlite3.connect("./data/datatoko.db")
        self.cur = self.db.cursor()     
        
        self.sqlPro = "SELECT * FROM produk"
        
    def eksekusi(self, sql):
        self.cur.execute(sql)
        lineData = self.cur.fetchall()
        totData = len(lineData)
        
        return lineData, totData
        
    def onClose(self, event=None):
        self.cur.close()
        self.db.close()
        #self.parent.destroy()
        self.destroy()
        
    def onListEnter(self, event=None):
        self.onDblListKlik()
        
    def onDblListKlik(self, event=None):
        index = self.list.curselection()
        
        # ambil data(str) dari list
        strDataIndex = self.list.get(index)
        dataIndex = strDataIndex.split('::')
        
        self.kodeProduk = dataIndex[0]
        
        #print dataIndex
        self.onClose()
        
    def onCariKeyRelease(self, event):
        strCari = self.entryCariPro.get()
        
        cariSQL = self.sqlPro + " WHERE UPPER(nm_produk) LIKE UPPER('%" + strCari + "%')"
        
        self.isiDataList(cariSQL)
        
    def onCariEnter(self, event):
        self.list.focus_set()
                
    def isiDataList(self, sql=None):
        self.list.delete(0, END)

        sql = sql + " ORDER BY nm_produk"
        
        baris, jumData = self.eksekusi(sql)
        
        if jumData == 0:
            tkMessageBox.showwarning("Perhatian!",
                "Data Produk masih kosong!", parent=self)
            self.buttonTambah.focus_set()
        else:       
            for data in range(jumData):
                teks = "%s::%s" %(baris[data][0], baris[data][1])
                self.list.insert(END, teks)
            self.list.selection_set(0)
        
        self.baris = baris
        self.jumData = jumData
        
    def getKdProduk(self):
        return self.kodeProduk
                
if __name__ == '__main__':
    root = Tk()
    
    def run():
        import formCariProduk
        obj = formCariProduk.FormCariProduk(root)
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()


