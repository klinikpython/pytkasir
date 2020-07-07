# file: formLogin.py
# desain form untuk Login
# tgl_buat: 9 okt 2010 08.32 AM
# tgl_revisi : -
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
import sqlite3
import tkinter.messagebox as tkMessageBox

class FormLogin(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
                
        self.geometry("+%d+%d" % (parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
                        
        self.koneksiDatabase()
        self.aturKomponen()
        self.aturKejadian()
        
        self.resizable(width=False, height=False)
        self.title("Login Database")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.parent = parent
        
        # setting awal
        self.entryNmUser.focus_set()
        self.pengguna = "kosong"
        self.kdPengguna = "PG"
        self.nmPengguna = "user"

        self.wait_window()
    
    def aturKomponen(self):
        # frame utama
        mainFrame = Frame(self)
        mainFrame.pack(fill=BOTH, expand=YES)
        
        # >>> frame_data
        fr_data = Frame(mainFrame)
        fr_data.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        
        # nomor trans
        Label(fr_data, text='Nama Pengguna').grid(row=0, 
            column=0, sticky=W)
        self.entryNmUser = Entry(fr_data)
        self.entryNmUser.grid(row=0, column=1, sticky=W)
 
        Label(fr_data, text='Password').grid(row=1, 
            column=0, sticky=W)
        self.entryPassUser = Entry(fr_data, show="*")
        self.entryPassUser.grid(row=1, column=1, sticky=W)
        
        # >>> frame_tombol
        fr_tombol = Frame(mainFrame)
        fr_tombol.pack(expand=YES, pady=5)
        
        self.buttonLogin = Button(fr_tombol, text='Login',
            command=self.onLoginKlik, width=10)
        self.buttonLogin.pack(side=LEFT)
        
        self.buttonKeluar = Button(fr_tombol, text='Keluar',
            command=self.onKeluarKlik, width=10)
        self.buttonKeluar.pack(side=LEFT)
        
    def aturKejadian(self):
        self.entryNmUser.bind("<Return>", self.onNmUserEnter)
        self.entryPassUser.bind("<Return>", self.onPassUserEnter)
        self.buttonLogin.bind("<Return>", self.onLoginKlik)
        
    def onNmUserEnter(self, event):
        if self.entryNmUser.get() == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Nama pengguna tidak boleh kosong!",
                parent=self)
            self.entryNmUser.focus_set()
        else:
            self.entryPassUser.focus_set()      
        
    def onPassUserEnter(self, event):
        if self.entryPassUser.get() == "":
            tkMessageBox.showwarning("Perhatian!", 
                "Password tidak boleh kosong!",
                parent=self)
            self.entryPassUser.focus_set()
        else:
            self.buttonLogin.focus_set()        
        
    def onLoginKlik(self, event=None):
        strCari = self.entryNmUser.get()
        
        cariSQL = self.sqlLogin + " WHERE nm_pengguna='%s'"%(strCari)
        
        bar, jum = self.eksekusi(cariSQL)       
        
        if jum == 0:
            tkMessageBox.showwarning("Perhatian!", 
                "Nama Pengguna dan\nPassword tidak sesuai!",
                parent=self)
            self.formKosong()
            self.entryNmUser.focus_set()
        else:
            password = bar[0][2]
            if self.entryPassUser.get()!=password:
                tkMessageBox.showwarning("Perhatian!", 
                    "Nama Pengguna dan\nPassword tidak sesuai!",
                    parent=self)
                self.formKosong()
                self.entryNmUser.focus_set()
            else:
                tkMessageBox.showwarning("Perhatian!", 
                    "Login BERHASIL!!!",
                    parent=self)
                self.pengguna = bar[0][3]
                self.nmPengguna = bar[0][1]
                self.kdPengguna = bar[0][0]
                self.onClose()
            
    def getNmPengguna(self):
        return self.kdPengguna, self.nmPengguna, self.pengguna
                
    def onKeluarKlik(self, event=None):
        self.onClose()
        
    def koneksiDatabase(self):
        self.db = sqlite3.connect("./data/datatoko.db")
        self.cur = self.db.cursor()     
        
        self.sqlLogin = "SELECT * FROM pengguna"
        
    def eksekusi(self, sql):
        self.cur.execute(sql)
        lineData = self.cur.fetchall()
        totData = len(lineData)
        
        return lineData, totData
        
    def formKosong(self):
        self.entryNmUser.delete(0, END)
        self.entryPassUser.delete(0, END)
                        
    def onClose(self, event=None):
        self.cur.close()
        self.db.close()
        #self.parent.destroy()
        self.destroy()
        
if __name__ == '__main__':
    root = Tk()
    
    def run():
        import formLogin
        obj = formLogin.FormLogin(root)
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()

