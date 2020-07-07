# file: formSupplier.py
# desain form untuk data pengguna
# tgl_buat: 5 okt 2010 03.12 PM
# tgl_revisi : -
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
import sqlite3
import tkinter.messagebox as tkMessageBox

class FormPengguna(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        widthForm = 640
        heightForm = 250

        self.geometry("%dx%d+%d+%d" % (widthForm, heightForm, 
            parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
                    
        self.aturKomponen()
        self.aturKejadian()
        self.koneksiDatabase()
        
        self.resizable(width=False, height=False)
        self.title("Form Data Pengguna")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onPass)
        self.parent = parent
        
        # setting awal
        self.isiDataList(self.sql)
        self.displayToEntry()
        self.formLoad()

        self.wait_window()
    
    def aturKomponen(self):
        # frame utama
        mainFrame = Frame(self)
        mainFrame.pack(fill=BOTH, expand=YES)
        
        # olah fr_list beserta komponennya
        fr_kiri = Frame(mainFrame)
        fr_kiri.pack(side=LEFT, fill=BOTH, expand=YES)
        
        fr_list = Frame(fr_kiri)
        fr_list.pack(fill=BOTH, expand=YES, padx=5)
        
        self.list = Listbox(fr_list, width=30)
        self.list.pack(side=LEFT, fill=BOTH, expand=YES)
        
        scrollbar = Scrollbar(fr_list, orient=VERTICAL,
            command=self.list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list.config(yscrollcommand=scrollbar.set)
        
        # ---> atur fr_cari
        fr_cari = Frame(fr_kiri)
        fr_cari.pack(side=BOTTOM,fill=X, pady=5)
        
        self.statusCari = IntVar()
        self.checkCari = Checkbutton(fr_cari, text="Cari:",
            var=self.statusCari, command=self.onCekCari)
        self.checkCari.pack(side=LEFT)
        
        self.entryCari = Entry(fr_cari)
        self.entryCari.pack(side=LEFT, fill=X, expand=YES)
        
        # olah fr_kanan beserta komponennya
        fr_kanan = Frame(mainFrame, bd=5)
        fr_kanan.pack(fill=BOTH, expand=YES, side=LEFT)
        
        # ---> atur fr_data
        fr_data = Frame(fr_kanan)
        fr_data.pack()
        
        Label(fr_data, text="Kode Pengguna").grid(row=0, 
            column=0, sticky=W)
        self.entryKdUser = Entry(fr_data, width=7)
        self.entryKdUser.grid(row=0, column=1, sticky=W, pady=5)
        
        Label(fr_data, text="Nama Pengguna").grid(row=1, 
            column=0, sticky=W)
        self.entryNmUser = Entry(fr_data, width=15)
        self.entryNmUser.grid(row=1, column=1, sticky=W, pady=5)
        
        Label(fr_data, text="Password").grid(row=2, 
            column=0, sticky=W)
        self.entryPassUser = Entry(fr_data, width=15)
        self.entryPassUser.grid(row=2, column=1, sticky=W, pady=5)
        
        STATUS = ["admin", "kasir"]
        self.statusUser = StringVar()
        #self.statusUser.set("admin")
        
        Label(fr_data, text="Status").grid(row=3, 
            column=0, sticky=W)     
        self.optStatusUser = OptionMenu(fr_data, self.statusUser, 
            "admin","kasir")
        self.optStatusUser.configure(width=5)
        self.optStatusUser.grid(row=3, column=1, sticky=W, pady=5)
        
        # ---> fr_tombol
        fr_tombol = Frame(fr_kanan)
        fr_tombol.pack(side=BOTTOM, fill=X)
        
        self.buttonTambah = Button(fr_tombol, text='Tambah',
            command=self.onTambahKlik, underline=0, width=5)
        self.buttonTambah.pack(side=LEFT, fill=X, expand=YES)
        
        self.buttonSimpan = Button(fr_tombol, text='Simpan',
            command=self.onSimpanKlik, underline=0, width=5)
        self.buttonSimpan.pack(side=LEFT, fill=X, expand=YES)
        
        self.buttonHapus = Button(fr_tombol, text='Hapus',
            command=self.onHapusKlik, underline=0, width=5)
        self.buttonHapus.pack(side=LEFT, fill=X, expand=YES)
        
        self.buttonKeluar = Button(fr_tombol, text='Keluar',
            command=self.onKeluarKlik, underline=0, width=5)
        self.buttonKeluar.pack(side=LEFT, fill=X, expand=YES)
        
    def onPass(self):
        pass 
        
    def onCekCari(self, event=None):
        if self.statusCari.get() == 1:
            self.entryCari.configure(state=NORMAL)
            self.entryCari.focus_set()
        else:
            self.entryCari.delete(0, END)
            self.entryCari.configure(state=DISABLED)
            if self.jumData != 0:
                self.isiDataList(self.sql)
                self.displayToEntry()
                        
    def onTambahKlik(self, event=None):
        self.formKosong()

        self.entryKdUser.insert(END, self.buatKode())
        self.entryKdUser.configure(state=DISABLED)
        self.entryNmUser.focus_set()

        self.buttonTambah.configure(state=DISABLED)
        self.buttonSimpan.configure(state=NORMAL)
        self.buttonSimpan.configure(text='Simpan')
        self.buttonKeluar.configure(text='Batal')
        
        self.list.configure(state=DISABLED)
        self.checkCari.configure(state=DISABLED)
        
    def onSimpanKlik(self, event=None):
        kd_user = self.entryKdUser.get()
        nm_user = self.entryNmUser.get()
        pass_user = self.entryPassUser.get()
        stat_user = self.statusUser.get()
        
        if nm_user == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Nama pengguna tidak boleh kosong!",
                parent=self)
            self.entryNmUser.focus_set()
        elif pass_user == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Password pengguna tidak boleh kosong!", 
                parent=self)
            self.entryPassUser.focus_set()
        elif stat_user == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Status pengguna tidak boleh kosong!", 
                parent=self)
            self.optStatusUser.focus_set()
        else:
            if self.buttonSimpan["text"]=='Ubah':
                str = "UPDATE pengguna SET nm_pengguna='%s', pass_pengguna='%s', status='%s',  WHERE kd_pengguna='%s'"%(
                    nm_user, pass_user, stat_user, kd_user)
                tkMessageBox.showinfo("Informasi", 
                    "Data telah diubah.", parent=self)
            else:
                str = "INSERT INTO pengguna VALUES('%s','%s','%s','%s')" %(
                    kd_user, nm_user, pass_user, stat_user)
                tkMessageBox.showinfo("Informasi", 
                    "Data telah disimpan.", parent=self)

            self.cur.execute(str)
            self.db.commit()
            
            self.entryKdUser.configure(state=NORMAL)
            self.list.configure(state=NORMAL)
            self.entryCari.configure(state=NORMAL)
            
            self.entryCari.delete(0, END)
            self.checkCari.deselect()

            self.formNormal()
                    
            self.isiDataList(self.sql)
            self.displayToEntry()
            self.list.focus_set()
                        
    def onHapusKlik(self, event=None):
        if tkMessageBox.askyesno(
            "Hapus Data:", "Anda yakin akan menghapus record ini?",
            parent=self):
                sql = "DELETE FROM pengguna WHERE kd_pengguna='%s'"%(
                    self.entryKdUser.get())
                    
                self.cur.execute(sql)
                self.db.commit()
                
                self.entryKdUser.configure(state=NORMAL)
                self.entryCari.configure(state=NORMAL)
            
                self.entryCari.delete(0, END)
                self.checkCari.deselect()

                self.formNormal()
                self.formLoad()

                self.isiDataList(self.sql)
                self.displayToEntry()
                self.list.focus_set()
        else:
            self.entryKdUser.configure(state=NORMAL)
            self.formNormal()
            self.formLoad()

            self.isiDataList(self.sql)
            self.displayToEntry()
            self.list.focus_set()
        
    def onKeluarKlik(self, event=None):
        if self.buttonKeluar["text"] == 'Keluar':
            self.onClose()
        else:
            self.formNormal()
            self.buttonKeluar["text"] = 'Keluar'
            self.entryKdUser.configure(state=NORMAL)
            self.formKosong()
            self.displayToEntry()
            self.list.focus_set()
                        
    def aturKejadian(self):
        self.entryCari.bind("<KeyRelease>", 
            self.onCariKeyRelease) 
        self.entryCari.bind("<Return>", 
            self.onCariReturn) 
        
        self.list.bind("<ButtonRelease-1>", self.onListKlik)
        self.list.bind("<Double-Button-1>", self.onListDblKlik)
        self.list.bind("<Down>", self.onUpDownPress) 
        self.list.bind("<Up>", self.onUpDownPress) 
        
        self.entryNmUser.bind("<Return>", self.onEntryNmUserEnter)
        self.entryPassUser.bind("<Return>", self.onEntryPassUserEnter)
        self.optStatusUser.bind("<Return>", self.onOptStatUserEnter)
        
        self.buttonSimpan.bind("<Return>", self.onSimpanKlik)

    def onEntryNmUserEnter(self, event):
        self.entryPassUser.focus_set()

    def onEntryPassUserEnter(self, event):
        self.optStatusUser.focus_set()

    def onOptStatUserEnter(self, event):
        self.buttonSimpan.focus_set()

    def onCariKeyRelease(self, event):
        strCari = self.entryCari.get()
        
        cariSQL = self.sql + " WHERE UPPER(nm_pengguna) LIKE UPPER('%" + strCari + "%')"
        
        self.isiDataList(cariSQL)
        self.displayToEntry()
        
    def onCariReturn(self, event):
        self.list.focus_set()

    def onListKlik(self, event):
        self.displayToEntry()
        
    def onListDblKlik(self, event):
        self.buttonTambah.configure(state=DISABLED)
        self.buttonSimpan.configure(state=NORMAL)
        self.buttonHapus.configure(state=NORMAL)
        self.buttonSimpan.configure(text='Ubah')
        self.buttonKeluar.configure(text='Batal')
        
        self.list.configure(state=DISABLED)
        self.entryCari.configure(state=DISABLED)
        self.checkCari.configure(state=DISABLED)

        self.entryKdUser.configure(state=DISABLED)
        self.entryNmUser.focus_set()        
        self.displayToEntry()
        
    def onUpDownPress(self, event):
        self.list.bind("<KeyRelease>", self.onListKlik) 
            
    def koneksiDatabase(self):
        self.db = sqlite3.connect("./data/datatoko.db")
        self.cur = self.db.cursor()     
        
        self.sql = "SELECT * FROM pengguna"
        
    def eksekusi(self, sql):
        self.cur.execute(sql)
        lineData = self.cur.fetchall()
        totData = len(lineData)
        
        return lineData, totData

    def formLoad(self):
        self.buttonSimpan.configure(state=DISABLED)
        self.buttonHapus.configure(state=DISABLED)
        
        if self.jumData == 0:
            self.list.configure(state=DISABLED)
            self.entryCari.configure(state=DISABLED)
            self.checkCari.configure(state=DISABLED)
        else:
            self.list.configure(state=NORMAL)
            self.entryCari.configure(state=DISABLED)
            self.checkCari.configure(state=NORMAL)
        
    def formKosong(self):
        self.entryKdUser.delete(0, END)
        self.entryNmUser.delete(0, END)
        self.entryPassUser.delete(0, END)
        self.statusUser.set("")
        
    def formNormal(self):
        self.formKosong()
        
        self.buttonTambah.configure(state=NORMAL)
        self.buttonSimpan.configure(state=DISABLED)
        self.buttonHapus.configure(state=DISABLED)
        self.buttonHapus["text"] = 'Hapus'
        self.buttonSimpan["text"] = 'Simpan'
        self.buttonKeluar["text"] = 'Keluar'
                        
        self.list.configure(state=NORMAL)
        self.entryCari.configure(state=DISABLED)
        self.checkCari.configure(state=NORMAL)
                            
    def onClose(self, event=None):
        #self.parent.destroy()
        self.cur.close()
        self.db.close()
        self.destroy()

    def isiDataList(self, sql=None):
        self.list.delete(0, END)

        sql = sql + " ORDER BY nm_pengguna"
        
        baris, jumData = self.eksekusi(sql)
        
        if jumData == 0:
            tkMessageBox.showwarning("Perhatian!",
                "Data Pengguna masih kosong!", parent=self)
            self.buttonTambah.focus_set()
        else:       
            for data in range(jumData):
                teks = "%s" %(baris[data][1])
                self.list.insert(END, teks)
            self.list.selection_set(0)
        
        self.baris = baris
        self.jumData = jumData
                
    def displayToEntry(self):
        if self.jumData == 0:
            pass 
        else:
            index = self.list.curselection()
            strKlik = self.list.get(index)
        
            sql = "SELECT * FROM pengguna WHERE nm_pengguna='%s'"%strKlik
            
            baris, jumData = self.eksekusi(sql)

            self.formKosong()
            self.entryKdUser.insert(END, baris[0][0])
            self.entryNmUser.insert(END, baris[0][1])
            self.entryPassUser.insert(END, baris[0][2])
            self.statusUser.set(baris[0][3])
            
    def buatKode(self):
        sql = "SELECT * FROM pengguna"
        cek, jum = self.eksekusi(sql)
        
        if jum == 0:
            teks = "PG01"
        else:
            kd = cek[jum-1][0]
            #print kd
            kode_user = int(kd[-2:]) + 1
            #print kode_sup
            
            if kode_user < 10:
                teks = "PG0" + str(kode_user)
            elif kode_user < 100:
                teks = "PG" + str(kode_user)

        return teks
            
if __name__ == '__main__':
    root = Tk()
    
    def run():
        import formPengguna
        obj = formPengguna.FormPengguna(root)
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()

