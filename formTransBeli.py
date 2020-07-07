# file: formTransBeli.py
# desain form untuk transaksi pembelian
# tgl_buat: 5 okt 2010 03.12 PM
# tgl_revisi : 28 okt 2010 07.11 AM
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
from dynOptionMenuWidget import DynOptionMenu
import sqlite3
import tkinter.messagebox as tkMessageBox
import formUbahHarga
import formCariProduk
from datetime import *
import string

class FormTransBeli(Toplevel):
    def __init__(self, parent, pengguna):
        Toplevel.__init__(self, parent)
                
        self.geometry("+%d+%d" % (parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
                        
        self.koneksiDatabase()
        self.aturKomponen()
        self.aturKejadian()
        
        self.resizable(width=False, height=False)
        self.title("Transaksi Barang Masuk")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.parent = parent
        self.pengguna = pengguna
        
        # setting awal
        self.formLoad()
        self.total_hrg = 0
        self.jumItem = 0

        self.wait_window()
    
    def aturKomponen(self):
        # frame utama
        mainFrame = Frame(self)
        mainFrame.pack(fill=BOTH, expand=YES)
        
        # >>> frame_data
        fr_data = Frame(mainFrame)
        fr_data.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        
        Label(fr_data, text='Nomor Masuk').grid(row=0, 
            column=0, sticky=W)
        self.entryNoMas = Entry(fr_data)
        self.entryNoMas.grid(row=0, column=1, sticky=W)
        kdFont = self.entryNoMas["font"]
        
        Label(fr_data, text='Tanggal (th-bl-hr)').grid(row=1, 
            column=0, sticky=W)
        
        fr_tgl = Frame(fr_data)
        fr_tgl.grid(row=1, column=1, sticky=W)
        
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
        
        Label(fr_data, text='Nama Supplier').grid(row=2, 
            column=0, sticky=W)
        
        self.setDataSup()
        self.pilihSup = StringVar()
        
        self.optNmSupplier = DynOptionMenu(fr_data, self.pilihSup, 
            None, command=self.onOptPilih)
        self.optNmSupplier.configure(width=13)
        self.optNmSupplier.SetMenu(self.namaSupplier)
        self.optNmSupplier.grid(row=2, column=1, sticky=W)

        Label(fr_data, text="Alamat").grid(row=3, 
            column=0, sticky=W)
        self.textAlamat = Text(fr_data, height=3, width=20,
            font=kdFont)
        self.textAlamat.grid(row=3, column=1, sticky=W, pady=5,
            rowspan=2)
        
        Label(fr_data, text="    ").grid(row=0, 
            column=2, sticky=W) # blank line

        Label(fr_data, text="Kode Produk").grid(row=0, 
            column=3, sticky=W) 
            
        fr_kdPro = Frame(fr_data)
        fr_kdPro.grid(row=0, column=4, sticky=W, pady=5)
        
        self.entryKdPro = Entry(fr_kdPro, width=7)
        self.entryKdPro.pack(side=LEFT)
        self.buttonKdPro = Button(fr_kdPro, text='Cari', 
            command=self.cariKdPro)
        self.buttonKdPro.pack(side=LEFT, padx=5)

        Label(fr_data, text='Nama Produk').grid(row=1, 
            column=3, sticky=W)
        self.entryNmPro = Entry(fr_data, width=30)
        self.entryNmPro.grid(row=1, column=4, sticky=W)
        
        Label(fr_data, text='Harga Beli').grid(row=2, 
            column=3, sticky=W)
        self.entryHrgPro = Entry(fr_data, width=15, justify=RIGHT)
        self.entryHrgPro.grid(row=2, column=4, sticky=W)
        
        Label(fr_data, text="Jumlah").grid(row=3, 
            column=3, sticky=W) 
            
        fr_jml = Frame(fr_data)
        fr_jml.grid(row=3, column=4, sticky=W, pady=5)
        
        self.entryJml = Entry(fr_jml, width=5, justify=RIGHT)
        self.entryJml.pack(side=LEFT)
        self.buttonMasuk = Button(fr_jml, text='Input Data', 
            command=self.inputList, width=6)
        self.buttonMasuk.pack(side=LEFT, padx=5)
        
        Label(fr_data, text='Sub Total').grid(row=4, 
            column=3, sticky=W)
        self.entrySubTot = Entry(fr_data, width=15, justify=RIGHT)
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
        
        self.entryTotal = Entry(fr_total, width=15,
            font=("Arial", 14, "bold"), justify=RIGHT)
        self.entryTotal.pack(side=RIGHT)
        Label(fr_total, text='Total Harga Rp.', 
            font=("Arial", 14, "bold")).pack(side=RIGHT)
            
        Label(fr_total, text='Jumlah Item: ').pack(side=LEFT)
        self.labelJumItem = Label(fr_total, text="")
        self.labelJumItem.pack(side=LEFT)
        
    def setDataSup(self):
        line, sumData = self.eksekusi(self.sqlSup)
        
        self.namaSupplier = []
        for i in range(sumData):
            self.namaSupplier.append(line[i][1])
            
    def cariKdPro(self):
        app = formCariProduk.FormCariProduk(self)
        
        kd_pro = app.getKdProduk()
        
        self.entryKdPro.delete(0, END)
        self.entryKdPro.insert(END, kd_pro)
        
        self.onKdProEnter()
                
    def inputList(self, event=None):
        if self.pilihSup.get() == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Nama supplier tidak boleh kosong!",
                parent=self)
            self.optNmSupplier.focus_set()
        elif self.entryKdPro.get() == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Kode produk tidak boleh kosong!",
                parent=self)
            self.entryKdPro.focus_set()
        elif self.entryHrgPro.get() == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Harga produk tidak boleh kosong!",
                parent=self)
            self.entryHrgPro.focus_set()
        elif self.entryJml.get() == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Jumlah beli tidak boleh kosong!",
                parent=self)
            self.entryJml.focus_set()
        else:
            self.entryTotal.delete(0, END)
        
            kd_pro = self.entryKdPro.get()
            nm_pro = self.entryNmPro.get()
            hrg_pro = self.entryHrgPro.get()
            jumlah = self.entryJml.get()
            sub_total = self.entrySubTot.get()
        
            strData = "  >>  ::%s::%s::%s::%s::%s" %(kd_pro.upper(), 
                nm_pro, hrg_pro, jumlah, sub_total)
        
            self.jumItem += 1
            self.labelJumItem["text"] = str(self.jumItem)
            self.list.insert(END, strData)
        
            self.total_hrg += int(sub_total)
            self.entryTotal.insert(END, str(self.total_hrg))
        
            self.dataProdukKosong()
            self.entryKdPro.focus_set()
        
    def onTransBaru(self, event=None):
        self.formHidup()
        
        self.buttonTransBaru.configure(state=DISABLED)
        self.buttonSimpan.configure(state=NORMAL)
        self.buttonKeluar.configure(state=NORMAL)
        self.buttonKeluar["text"] = "Batal"
        
        self.tahunSpin.focus_set()
        self.setToday()
        self.entryNoMas.insert(0, self.buatKode())
        self.entryNoMas.configure(state=DISABLED)
        
        self.labelJumItem["text"] = str(self.jumItem)
        
    def onSimpanKlik(self, event=None):
        # simpan ke tabel barang_masuk
        tglMasuk = self.editTanggal(
            self.tahunSpin.get(),self.bulanSpin.get(),self.hariSpin.get())
        
        strBarMas = "INSERT INTO barang_masuk VALUES('%s','%s','%s','%s','%s')" %(
            self.entryNoMas.get(), tglMasuk, self.barSup[0][0], 
            self.entryTotal.get(),self.pengguna)
            
        self.cur.execute(strBarMas)
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

            strDetBarMas = "INSERT INTO detbarang_masuk VALUES('%s','%s','%s','%s','%s')" %(
                self.entryNoMas.get(), kd_pro, hrg_pro, jml_pro, sub_tot)
            
            self.cur.execute(strDetBarMas)
            self.db.commit()
        
            # update data stok_produk
            strUpdateStok = "UPDATE produk SET stok_produk=stok_produk+%i WHERE kd_produk='%s'" %(
                int(jml_pro), kd_pro)

            self.cur.execute(strUpdateStok)
            self.db.commit()
            
        tkMessageBox.showinfo("Informasi!", 
            "Data telah tersimpan!",
                parent=self)
        
        self.entryNoMas.configure(state=NORMAL)
        
        self.formKosong()
        self.formLoad()
        self.buttonKeluar["text"] = "Keluar"
        self.labelJumItem["text"] = ""

        self.total_hrg = 0
        self.jumItem = 0
        
    def onKeluarKlik(self, event=None):
        if self.buttonKeluar["text"] == 'Keluar':
            self.onClose()
        else:
            self.jumItem = 0
            self.labelJumItem["text"] = ""
            
            self.entryNoMas.configure(state=NORMAL)
            self.formKosong()
            self.buttonKeluar["text"] = 'Keluar'
            self.formLoad()
                        
    def aturKejadian(self):
        self.tahunSpin.bind("<Return>", self.onTahSpinEnter)
        self.bulanSpin.bind("<Return>", self.onBulSpinEnter)
        self.hariSpin.bind("<Return>", self.onHarSpinEnter)
        self.entryKdPro.bind("<Return>", self.onKdProEnter)
        self.entryHrgPro.bind("<Return>", self.onHrgProEnter)
        self.entryJml.bind("<Return>", self.onJmlEnter)
        self.buttonMasuk.bind("<Return>", self.inputList)
        
        self.list.bind("<Double-Button-1>", self.onListDblKlik)
        
    def onTahSpinEnter(self, event):
        self.bulanSpin.focus_set()
        
    def onBulSpinEnter(self, event):
        self.hariSpin.focus_set()
        
    def onHarSpinEnter(self, event):
        self.optNmSupplier.focus_set()
        
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
                self.total_hrg -= int(dataIndex[-1])
                
                self.entryTotal.delete(0, END)
                self.entryTotal.insert(END, str(self.total_hrg))
                
                # ubah label jumlah produk
                self.jumItem -= 1
                self.labelJumItem["text"] = str(self.jumItem)
                        
    def onOptPilih(self, event=None):
        self.textAlamat.delete(1.0, END)
        strCari = self.pilihSup.get()
        
        cariSQL = self.sqlSup + " WHERE UPPER(nm_supplier) LIKE UPPER('%" + strCari + "%')"
        
        self.barSup, jum = self.eksekusi(cariSQL)
        self.textAlamat.insert(END, self.barSup[0][3])
        self.entryKdPro.focus_set()
        
        #print self.barSup
        
    def onKdProEnter(self, event=None):
        strCari = self.entryKdPro.get()
        self.entryNmPro.delete(0, END)
        
        cariSQL = self.sqlPro + " WHERE UPPER(kd_produk)=UPPER('" + strCari + "')"
        
        self.barPro, jum = self.eksekusi(cariSQL)
        #print self.barPro
        
        if jum == 0:
            tkMessageBox.showwarning("Perhatian!",
                "Data Produk Tidak Ada!", parent=self)
        else:
            self.entryNmPro.insert(END, self.barPro[0][1])
            self.entryHrgPro.focus_set()
            
    def onHrgProEnter(self, event):     
        harga_lama = int(self.barPro[0][2])
        harga_baru = int(self.entryHrgPro.get())
        
        strUbahHarga = "Harga jual : %i\nHarga beli: %i\nIngin ubah harga?"%(
            harga_lama, harga_baru)
            
        if tkMessageBox.askyesno(
            "Hapus Data:", strUbahHarga,
            parent=self):
                formUbahHarga.FormUbahHarga(self, self.barPro[0][0])
                
        self.entryJml.focus_set()
        
    def onJmlEnter(self, event):
        self.buttonMasuk.focus_set()
        harga = int(self.entryHrgPro.get())
        jumlah = int(self.entryJml.get())
        
        subTotal = harga * jumlah
        
        self.entrySubTot.insert(END, str(subTotal))
                        
    def koneksiDatabase(self):
        self.db = sqlite3.connect("./data/datatoko.db")
        self.cur = self.db.cursor()     
        
        self.sqlSup = "SELECT * FROM supplier"
        self.sqlPro = "SELECT * FROM produk"
        self.sqlUser = "SELECT * FROM pengguna"
        self.sqlBarMas = "SELECT * FROM barang_masuk"
        self.sqlDetBarMas = "SELECT * FROM detbarang_masuk"
        
    def eksekusi(self, sql):
        self.cur.execute(sql)
        lineData = self.cur.fetchall()
        totData = len(lineData)
        
        return lineData, totData
        
    def formMati(self):
        self.entryNoMas.configure(state=DISABLED)

        self.tahunSpin.configure(state=DISABLED)
        self.bulanSpin.configure(state=DISABLED)
        self.hariSpin.configure(state=DISABLED)
    
        self.optNmSupplier.configure(state=DISABLED)
        self.textAlamat.configure(state=DISABLED)

        self.entryKdPro.configure(state=DISABLED)
        self.buttonKdPro.configure(state=DISABLED)
        self.entryNmPro.configure(state=DISABLED)
        self.entryHrgPro.configure(state=DISABLED)
        self.entryJml.configure(state=DISABLED)
        self.buttonMasuk.configure(state=DISABLED)
        self.entrySubTot.configure(state=DISABLED)
        
        self.list.configure(state=DISABLED)
        self.entryTotal.configure(state=DISABLED)
        
    def formHidup(self):
        self.entryNoMas.configure(state=NORMAL)

        self.tahunSpin.configure(state=NORMAL)
        self.bulanSpin.configure(state=NORMAL)
        self.hariSpin.configure(state=NORMAL)
    
        self.optNmSupplier.configure(state=NORMAL)
        self.textAlamat.configure(state=NORMAL)

        self.entryKdPro.configure(state=NORMAL)
        self.buttonKdPro.configure(state=NORMAL)
        self.entryNmPro.configure(state=NORMAL)
        self.entryHrgPro.configure(state=NORMAL)
        self.entryJml.configure(state=NORMAL)
        self.buttonMasuk.configure(state=NORMAL)
        self.entrySubTot.configure(state=NORMAL)
        
        self.list.configure(state=NORMAL)
        self.entryTotal.configure(state=NORMAL)
        
    def formLoad(self):
        self.formMati()
        
        self.buttonTransBaru.configure(state=NORMAL)
        self.buttonSimpan.configure(state=DISABLED)
        self.buttonKeluar.configure(state=NORMAL)
        self.buttonTransBaru.focus_set()
        
    def formKosong(self):
        self.entryNoMas.delete(0, END)
        self.hariSpin.delete(0, END)
        self.bulanSpin.delete(0, END)
        self.tahunSpin.delete(0, END)
        
        self.pilihSup.set("")
        self.textAlamat.delete(1.0, END)

        self.dataProdukKosong()
        
        self.list.delete(0, END)
        self.entryTotal.delete(0, END)

    def dataProdukKosong(self):
        self.entryKdPro.delete(0, END)
        self.entryNmPro.delete(0, END)
        self.entryHrgPro.delete(0, END)
        self.entryJml.delete(0, END)
        self.entrySubTot.delete(0, END)
                
    def onClose(self, event=None):
        self.cur.close()
        self.db.close()
        #self.parent.destroy()
        self.destroy()
        
    def buatKode(self):
        cek, jum = self.eksekusi(self.sqlBarMas)
        
        if jum == 0:
            teks = "TB-0001"
        else:
            kd = cek[jum-1][0]
            #print kd
            kode_fak = int(kd[-4:]) + 1
            #print kode_sup
            
            if kode_fak < 10:
                teks = "TB-000" + str(kode_fak)
            elif kode_fak < 100:
                teks = "TB-00" + str(kode_fak)
            elif kode_fak < 1000:
                teks = "TB-0" + str(kode_fak)           
            elif kode_fak < 10000:
                teks = "TB-" + str(kode_fak)
            
        return teks
        
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
        import formTransBeli
        obj = formTransBeli.FormTransBeli(root, "PG01")
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()
