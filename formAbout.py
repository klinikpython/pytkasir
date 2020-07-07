# file: formAbout.py
# desain form untuk tentang program
# tgl_buat: 14 okt 2010 10.24 PM
# tgl_revisi : -
# lisensi: GPL
# dibuat oleh: masbiggie@PythonDahsyat.blogspot.com

from tkinter import *
import sqlite3
import tkinter.messagebox as tkMessageBox

class FormAbout(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        
        self.geometry("+%d+%d" % (parent.winfo_rootx()+80, 
            parent.winfo_rooty()+50))
        
        self.aturKomponen()
        
        self.resizable(width=False, height=False)
        self.title("Tentang Program")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.parent = parent
        
        # setting awal
        self.buttonKeluar.focus_set()
        
        self.wait_window()
    
    def aturKomponen(self):
        # frame utama
        mainFrame = Frame(self, bd=3, width=400, height=200)
        mainFrame.pack(fill=BOTH, expand=YES)
        
        # frame atas
        fr_atas = Frame(mainFrame, bg="white", bd=5)
        fr_atas.pack(fill=BOTH, expand=YES)
        
        # setting background image via Canvas
        self.imgAbout = PhotoImage(file="./data/about_img.gif")
        Label(fr_atas, image=self.imgAbout, 
            relief=FLAT).pack(pady=10)

        Label(fr_atas, text="pyTKasir 0.01.0", 
            font=("Arial", 16, 'bold'), bg='white').pack(pady=10)
        
        Label(fr_atas, 
            text="Program Pembelian dan Penjualan menggunakan Tkinter-Python.", 
            font=("Trebuchet", 10), bg='white').pack()
            
        Label(fr_atas, 
            text="Copyright @ 2010 Biggie Noviandi", 
            font=("Trebuchet", 9), bg='white').pack()

        Frame(fr_atas, borderwidth=2, relief=SUNKEN,
            height=2, bg="black").pack(pady=5, fill=X,
            expand=YES)
            
        Label(fr_atas, 
            text="www.pythondahsyat.blogspot.com", 
            font=("Trebuchet", 10, "bold"), bg='white').pack(pady=10)
            
        # frame bawah
        fr_bawah = Frame(mainFrame)
        fr_bawah.pack(side=BOTTOM, pady=5)
        
        self.buttonKeluar = Button(fr_bawah, text='Keluar',
            command=self.onClose, underline=0)
        self.buttonKeluar.pack()
        
    def onClose(self, event=None):
        self.destroy()
        
if __name__ == '__main__':
    root = Tk()
    
    def run():
        import formAbout
        obj = formAbout.FormAbout(root)
            
    Button(root, text="Tes Form", command=run, width=10).pack()
    
    root.mainloop()

