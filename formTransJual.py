# file: formTransJual.py
# desain form untuk transaksi penjualan
# tgl_buat: 9 okt 2010 08.10 AM
# tgl_revisi : 28 okt 2010 07.28 AM
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
from datetime import *
import sqlite3
import tkinter.messagebox as tkMessageBox
import formCariProduk
import string

class FormTransJual(Toplevel):
    def __init__(self, parent, kdpengguna):
        Toplevel.__init__(self, parent)
                
        self.geometry("+%d+%d" % (parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
                        
        self.koneksiDatabase()
        self.aturKomponen()
        self.aturKejadian()
        
        self.resizable(width=False, height=False)
        self.title("Transaksi Penjualan")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onPass)
        self.parent = parent
        self.kdpengguna = kdpengguna
        
        # setting awal
        self.formLoad()
        self.total_harga = 0

        self.wait_window()
        
    def aturKomponen(self):
        # frame utama
        mainFrame = Frame(self)
        mainFrame.pack(fill=BOTH, expand=YES)
        
        # >>> frame_data
        fr_data = Frame(mainFrame)
        fr_data.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        
        # nomor trans
        Label(fr_data, text='Nomor Transaksi').grid(row=0, 
            column=0, sticky=W)
        self.entryNoTrans = Entry(fr_data, width=15)
        self.entryNoTrans.grid(row=0, column=1, sticky=W)
        
        # blank column
        Label(fr_data, text='  ').grid(row=0, 
            column=2, sticky=W)
        
        # tgl trans
        Label(fr_data, text='Tgl Trans (th-bl-hr)').grid(row=0, 
            column=3, sticky=W)
        
        fr_tgl = Frame(fr_data)
        fr_tgl.grid(row=0, column=4, sticky=W)
        
        self.tahunSpin = Spinbox(fr_tgl, from_=2010, to=2099, width=5)
        self.tahunSpin.pack(side=LEFT)
        self.bulanSpin = Spinbox(fr_tgl, from_=1, to=12, width=3)
        self.bulanSpin.pack(side=LEFT, padx=5)
        self.hariSpin = Spinbox(fr_tgl, from_=1, to=31, width=3)
        self.hariSpin.pack(side=LEFT)
        
        # kosongkan tgl
        self.hariSpin.delete(0, END)
        self.bulanSpin.delete(0, END)
        self.tahunSpin.delete(0, END)
                
        # kode produk
        Label(fr_data, text='Kode Produk').grid(row=1, 
            column=0, sticky=W)

        fr_kdPro = Frame(fr_data)
        fr_kdPro.grid(row=1, column=1, sticky=W, pady=5)
        
        self.entryKdPro = Entry(fr_kdPro, width=7)
        self.entryKdPro.pack(side=LEFT)
        self.buttonKdPro = Button(fr_kdPro, text='Cari', 
            command=self.cariKdPro)
        self.buttonKdPro.pack(side=LEFT, padx=5)
            
        # nama produk
        Label(fr_data, text='Nama Produk').grid(row=2, 
            column=0, sticky=W)
        self.entryNmPro = Entry(fr_data, width=30)
        self.entryNmPro.grid(row=2, column=1, sticky=W,
            columnspan=3)
            
        # stok produk
        Label(fr_data, text='Stok Produk').grid(row=3, 
            column=0, sticky=W)
        self.entryStokPro = Entry(fr_data, width=5)
        self.entryStokPro.grid(row=3, column=1, sticky=W, pady=5)
        
        # harga jual
        Label(fr_data, text='Harga Jual').grid(row=3, 
            column=3, sticky=W)
        self.entryHrgPro = Entry(fr_data, width=15)
        self.entryHrgPro.grid(row=3, column=4, sticky=W)
        
        # jumlah produk
        Label(fr_data, text='Jumlah').grid(row=4, 
            column=0, sticky=W)

        fr_kdPro = Frame(fr_data)
        fr_kdPro.grid(row=4, column=1, sticky=W)
        
        self.entryJmlPro = Entry(fr_kdPro, width=7)
        self.entryJmlPro.pack(side=LEFT)
        self.buttonInput = Button(fr_kdPro, text='Input Data', 
            command=self.onInputEnter, width=7)
        self.buttonInput.pack(side=LEFT, padx=5)
        
        # sub total
        Label(fr_data, text='Sub Total').grid(row=4, 
            column=3, sticky=W)
        self.entrySubTot = Entry(fr_data, width=15)
        self.entrySubTot.grid(row=4, column=4, sticky=W)
        
        # >>> frame_tombol
        fr_tombol = Frame(mainFrame, bd=2, relief=SUNKEN)
        fr_tombol.pack(expand=YES, pady=10)
        
        self.buttonTransBaru = Button(fr_tombol, 
            text='Transaksi Baru', command=self.onTransBaru,
            width=10)
        self.buttonTransBaru.pack(side=LEFT)
        
        self.buttonSimpan = Button(fr_tombol, 
            text='Simpan', command=self.onSimpanKlik,
            width=10)
        self.buttonSimpan.pack(side=LEFT)
        
        self.buttonKeluar = Button(fr_tombol, 
            text='Keluar', command=self.onKeluarKlik,
            width=10)
        self.buttonKeluar.pack(side=LEFT)
        
        # >>> frame_list
        fr_list = Frame(mainFrame)
        fr_list.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        
        self.list = Listbox(fr_list, width=30)
        self.list.pack(side=LEFT, fill=BOTH, expand=YES)
        
        scrollbar = Scrollbar(fr_list, orient=VERTICAL,
            command=self.list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list.config(yscrollcommand=scrollbar.set)
        
        # >>> frame_total
        fr_total = Frame(mainFrame, bd=10)
        fr_total.pack(fill=BOTH, expand=YES)
        
        fr_grid = Frame(fr_total)
        fr_grid.pack(side=RIGHT)
        
        Label(fr_grid, text='Total Harga (Rp)', 
            font=("Arial", 14, "bold")).grid(row=0, 
            column=0, sticky=W)
        self.entryTotal = Entry(fr_grid, width=15,
            font=("Arial", 14, "bold"), justify=RIGHT)
        self.entryTotal.grid(row=0, column=1)

        Label(fr_grid, text='Cash (Rp)', 
            font=("Arial", 14, "bold")).grid(row=1, 
            column=0, sticky=W)
        self.entryCash = Entry(fr_grid, width=15,
            font=("Arial", 14, "bold"), justify=RIGHT)
        self.entryCash.grid(row=1, column=1)

        Label(fr_grid, text='Kembali (Rp)', 
            font=("Arial", 14, "bold")).grid(row=2, 
            column=0, sticky=W)
        self.entryKembali = Entry(fr_grid, width=15,
            font=("Arial", 14, "bold"), justify=RIGHT)
        self.entryKembali.grid(row=2, column=1)
        
    def aturKejadian(self):
        self.entryKdPro.bind("<Return>", self.onKdProEnter) 
        self.entryJmlPro.bind("<Return>", self.onJmlProEnter) 
        self.buttonInput.bind("<Return>", self.onInputEnter)
        
        self.bind("<KeyPress-F9>", self.onStopTrans)
        self.entryCash.bind("<Return>", self.onCashEnter)
        self.list.bind("<Double-Button-1>", self.onListDblKlik)
        
    def onListDblKlik(self, event):
        """ Menghapus Data yang ada di ListData """
        
        if tkMessageBox.askyesno(
            "Hapus Data:", "Anda yakin akan menghapus record ini?",
            parent=self):
                index = self.list.curselection()
        
                # ambil data(str) dari list
                strDataIndex = self.list.get(index)
                dataIndex = strDataIndex.split('::')
                #print dataIndex
            
                # hapus data list
                self.list.delete(index)
        
                # ubah isi total-harga
                self.total_harga -= int(dataIndex[-1])
                
                self.entryTotal.delete(0, END)
                self.entryTotal.insert(END, str(self.total_harga))
        
    def onCashEnter(self, event):
        if self.entryCash.get() == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Uang Cash tidak boleh kosong!",
                parent=self)
            self.entryCash.focus_set()
        else:
            self.buttonSimpan.focus_set()
            totalTrans = int(self.entryTotal.get())     
            uangCash = int(self.entryCash.get())
        
            kembali = uangCash - totalTrans
            
            if kembali < 0:
                tkMessageBox.showwarning("Perhatian!", 
                    "Uang Cash kurang!",
                    parent=self)
                self.entryCash.focus_set()
            else:
                self.entryKembali.insert(END, str(kembali))
        
    def onStopTrans(self, event):
        self.entryCash.focus_set()

    def onInputEnter(self, event=None):
        if self.entryKdPro.get() == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Kode produk tidak boleh kosong!",
                parent=self)
            self.entryKdPro.focus_set()
        elif self.entryJmlPro.get() == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Jumlah produk tidak boleh kosong!",
                parent=self)
            self.entryJmlPro.focus_set()
        else:
            self.entryTotal.delete(0, END)
        
            kd_pro = self.entryKdPro.get()
            nm_pro = self.entryNmPro.get()
            hrg_pro = self.entryHrgPro.get()
            jumlah = self.entryJmlPro.get()
            sub_total = self.entrySubTot.get()
        
            strData = "  >>  ::%s::%s::%s::%s::%s" %(kd_pro.upper(), 
                nm_pro, hrg_pro, jumlah, sub_total)
        
            self.list.insert(END, strData)
        
            self.total_harga += int(sub_total)
            self.entryTotal.insert(END, str(self.total_harga))
        
            self.kosongProdukTrans()
            self.entryKdPro.focus_set()
                
    def onJmlProEnter(self, event):
        if self.entryJmlPro.get() == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Jumlah produk tidak boleh kosong!",
                parent=self)
            self.entryJmlPro.focus_set()
        else:
            self.buttonInput.focus_set()
            harga = int(self.entryHrgPro.get())     
            jumlah = int(self.entryJmlPro.get())
        
            subTotal = harga * jumlah
            
            self.entrySubTot.delete(0, END)
            self.entrySubTot.insert(END, str(subTotal))
        
    def onTglTransEnter(self, event):
        self.entryKdPro.focus_set()
        
    def onKdProEnter(self, event=None):
        strCari = self.entryKdPro.get()
        self.entryNmPro.delete(0, END)
        self.entryStokPro.delete(0, END)
        self.entryHrgPro.delete(0, END)
        
        cariSQL = self.sqlPro + " WHERE UPPER(kd_produk)=UPPER('" + strCari + "')"
        
        self.barPro, jum = self.eksekusi(cariSQL)
        #print self.barPro
        
        if jum == 0:
            tkMessageBox.showwarning("Perhatian!",
                "Data Produk Tidak Ada!", parent=self)
        else:
            self.entryNmPro.insert(END, self.barPro[0][1])
            self.entryStokPro.insert(END, self.barPro[0][3])
            self.entryHrgPro.insert(END, self.barPro[0][2])

            self.entryJmlPro.focus_set()
                    
    def koneksiDatabase(self):
        self.db = sqlite3.connect("./data/datatoko.db")
        self.cur = self.db.cursor()     
        
        self.sqlPro = "SELECT * FROM produk"
        self.sqlJual = "SELECT * FROM penjualan"
        self.sqlDetJual = "SELECT * FROM detpenjualan"
        
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
        
    def cariKdPro(self, event=None):
        app = formCariProduk.FormCariProduk(self)
        
        kd_pro = app.getKdProduk()
        
        self.entryKdPro.delete(0, END)
        self.entryKdPro.insert(END, kd_pro)
        
        self.onKdProEnter()
        
    def onTransBaru(self, event=None):
        self.formHidup()
        
        self.buttonTransBaru.configure(state=DISABLED)
        self.buttonSimpan.configure(state=NORMAL)
        self.buttonKeluar.configure(state=NORMAL)
        self.buttonKeluar["text"] = "Batal"
        
        self.setToday()
        self.entryNoTrans.insert(0, self.buatKode())
        self.entryNoTrans.configure(state=DISABLED)
        
        #self.tahunSpin.configure(state=DISABLED)
        #self.bulanSpin.configure(state=DISABLED)
        #self.hariSpin.configure(state=DISABLED)

        self.entryKdPro.focus_set()
        
    def onSimpanKlik(self, event=None):
        # simpan ke tabel barang_masuk
        tglMasuk = self.editTanggal(
            self.tahunSpin.get(),self.bulanSpin.get(),self.hariSpin.get())
        
        strJual = "INSERT INTO penjualan VALUES('%s','%s','%s','%s')" %(
            self.entryNoTrans.get(), tglMasuk,
            self.entryTotal.get(),self.kdpengguna)
            
        self.cur.execute(strJual)
        self.db.commit()
        
        # simpan ke tabel detbarang_masuk
        jumData = self.list.size()
        
        for item in range(jumData):
            strDataIndex = self.list.get(item)
            dataIndex = strDataIndex.split('::')
            
            kd_pro = dataIndex[1]
            hrg_pro = dataIndex[3]
            jml_pro = dataIndex[4]
            sub_tot = dataIndex[5]

            strDetJual = "INSERT INTO detpenjualan VALUES('%s','%s','%s','%s','%s')" %(
                self.entryNoTrans.get(), kd_pro, hrg_pro, jml_pro, sub_tot)
            
            self.cur.execute(strDetJual)
            self.db.commit()
        
            # update data stok_produk
            strUpdateStok = "UPDATE produk SET stok_produk=stok_produk-%i WHERE kd_produk='%s'" %(
                int(jml_pro), kd_pro)

            self.cur.execute(strUpdateStok)
            self.db.commit()
            
        tkMessageBox.showinfo("Informasi!", 
            "Data telah tersimpan!",
                parent=self)
        
        self.entryNoTrans.configure(state=NORMAL)
        
        self.formKosong()
        self.formLoad()
        self.buttonKeluar["text"] = "Keluar"
        self.total_hrg = 0
            
    def onKeluarKlik(self, event=None):
        if self.buttonKeluar["text"] == 'Keluar':
            self.onClose()
        else:
            self.entryNoTrans.configure(state=NORMAL)
            self.formKosong()
            self.buttonKeluar["text"] = 'Keluar'
            self.formLoad()
            self.total_harga = 0
                                
    def formMati(self):
        self.entryNoTrans.configure(state=DISABLED)
    
        #self.tahunSpin.configure(state=DISABLED)
        #self.bulanSpin.configure(state=DISABLED)
        #self.hariSpin.configure(state=DISABLED)
     
        self.entryKdPro.configure(state=DISABLED)
        self.buttonKdPro.configure(state=DISABLED)
        self.entryNmPro.configure(state=DISABLED)
        self.entryStokPro.configure(state=DISABLED)
        self.entryHrgPro.configure(state=DISABLED)
        self.entryJmlPro.configure(state=DISABLED)
        self.buttonInput.configure(state=DISABLED)
        self.entrySubTot.configure(state=DISABLED)

        self.list.configure(state=DISABLED)
        self.entryTotal.configure(state=DISABLED)
        self.entryCash.configure(state=DISABLED)
        self.entryKembali.configure(state=DISABLED)

    def formHidup(self):
        self.entryNoTrans.configure(state=NORMAL)

        self.tahunSpin.configure(state=NORMAL)
        self.bulanSpin.configure(state=NORMAL)
        self.hariSpin.configure(state=NORMAL)
     
        self.entryKdPro.configure(state=NORMAL)
        self.buttonKdPro.configure(state=NORMAL)
        self.entryNmPro.configure(state=NORMAL)
        self.entryStokPro.configure(state=NORMAL)
        self.entryHrgPro.configure(state=NORMAL)
        self.entryJmlPro.configure(state=NORMAL)
        self.buttonInput.configure(state=NORMAL)
        self.entrySubTot.configure(state=NORMAL)

        self.list.configure(state=NORMAL)
        self.entryTotal.configure(state=NORMAL)
        self.entryCash.configure(state=NORMAL)
        self.entryKembali.configure(state=NORMAL)

    def formLoad(self):
        self.formMati()
        
        self.buttonTransBaru.configure(state=NORMAL)
        self.buttonSimpan.configure(state=DISABLED)
        self.buttonKeluar.configure(state=NORMAL)
        self.buttonTransBaru.focus_set()
        
    def formKosong(self):
        self.entryNoTrans.delete(0, END)
        self.hariSpin.delete(0, END)
        self.bulanSpin.delete(0, END)
        self.tahunSpin.delete(0, END)
        
        self.kosongProdukTrans()
        
        self.list.delete(0, END)
        self.entryTotal.delete(0, END)
        self.entryCash.delete(0, END)
        self.entryKembali.delete(0, END)

    def kosongDataProduk(self):
        self.entryKdPro.delete(0, END)
        self.entryNmPro.delete(0, END)
        self.entryStokPro.delete(0, END)
        self.entryHrgPro.delete(0, END)
    
    def kosongProdukTrans(self):
        self.kosongDataProduk()
        self.entryJmlPro.delete(0, END)
        self.entrySubTot.delete(0, END)
        
    def buatKode(self):
        cek, jum = self.eksekusi(self.sqlJual)
        
        if jum == 0:
            teks = "TJ-0001"
        else:
            kd = cek[jum-1][0]
            #print kd
            kode_fak = int(kd[-4:]) + 1
            #print kode_sup
            
            if kode_fak < 10:
                teks = "TJ-000" + str(kode_fak)
            elif kode_fak < 100:
                teks = "TJ-00" + str(kode_fak)
            elif kode_fak < 1000:
                teks = "TJ-0" + str(kode_fak)           
            elif kode_fak < 10000:
                teks = "TJ-" + str(kode_fak)
            
        return teks
        
    def onPass(self, event=None):
        pass 
        
    def setToday(self):
        tglSkrg = str(date.today())
        strTglSkrg = tglSkrg.split('-')
        
        self.setTanggal(strTglSkrg[0], strTglSkrg[1], strTglSkrg[2])
        
    def setTanggal(self, tah, bul, har):
        self.hariSpin.delete(0, END)
        self.bulanSpin.delete(0, END)
        self.tahunSpin.delete(0, END)
        
        self.hariSpin.insert(END, har)
        self.bulanSpin.insert(END, bul)
        self.tahunSpin.insert(END, tah)      
        
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
        import formTransJual
        obj = formTransJual.FormTransJual(root, "PG01")
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()

