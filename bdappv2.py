#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 23:00:35 2021

@author: swalk
"""

import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector 


class product:
    def __init__(self):
        self.prodid = int()
        self.prodname = str()
        self.produnit = str()
        self.prodcount = str()
        self.price = str()
        self.sum = str()
        
    def set_prod_data(self, rec):
        self.prodid = rec[0]
        self.prodname = rec[1]
        self.produnit = rec[2]
        self.prodcount = rec[3]
        self.price = rec[4]
        self.sum = rec[5]
    
    def print_prod(self):
        print(self.prodid, self.prodname, self.produnit, self.prodcount, self.price, self.sum)
    
class document:
    def __init__(self):
        self.docid = int()
        self.docnum = str()
        self.docdate = str()
        self.docsum = str()
        self.products = []
    
    def set_doc_data(self, rec):
        self.docid = int(rec[0])
        self.docnum = rec[1]
        self.docdate = rec[2]
        self.docsum = rec[3]
            
    def print_doc(self):
        print(self.docid, self.docnum, self.docdate, self.docsum)
    

class App(tk.Tk):
    def __init__(self, path):
        super().__init__()
        self.title("Database app")
        
#FIRST TABLE
        columns = ("#1", "#2", "#3")
        self.doclist = ttk.Treeview(self, show="headings", columns=columns)
        self.doclist.heading("#1", text="# Документа")
        self.doclist.heading("#2", text="Дата документа")
        self.doclist.heading("#3", text="На сумму")
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.doclist.yview)
        self.doclist.configure(yscroll=ysb.set)
        self.doclist.grid(row=1, column=0, sticky=tk.W)
        self.doclist.bind("<<TreeviewSelect>>", self.doc_selection)
        ysb.grid(row=1, column=0, sticky=tk.N + tk.S+tk.E,padx=(0, 10))
        

#FIRST TABLE CONTROL
        
        self.adddoc = ttk.Button(self, text="Добавить документ")
        self.adddoc.grid(row=1,column=1, padx=(0, 180))
        
        self.editdoc = ttk.Button(self, text="Изменить документ")
        self.editdoc.grid(row=1,column=1, padx=(0, 180), pady=(50,0))
        
        self.deletedoc = ttk.Button(self, text="удалить документ")
        self.deletedoc.grid(row=1,column=1, padx=(0, 180), pady=(100,0))

        
#LABEL BETWEEN
        self.midlable = ttk.Label(text="Doc name and data", font="Arial 24")   
        self.midlable.grid(row=2,column=0)


#SECOND TABLE
        prodcolumns = ("#1", "#2", "#3", "#4", "#5")
        self.prodlist = ttk.Treeview(self, show="headings", columns=prodcolumns)
        self.prodlist.heading("#1", text="Товар")
        self.prodlist.heading("#2", text="Ед. Изм.")
        self.prodlist.heading("#3", text="Количество")
        self.prodlist.heading("#4", text="Цена")
        self.prodlist.heading("#5", text="Стоимость")
        psb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.prodlist.yview)
        self.prodlist.configure(yscroll=psb.set)
        
        
        
        self.prodlist.grid(row=3, column=0, columnspan=2)
        psb.grid(row=3,column=2, sticky=tk.N+tk.S)

#SECOND TABLE CONTROL
        self.addprod = ttk.Button(self, text="Добавить товар")
        #self.addprod.bind('<Button-1>', lambda e: self.edit_prod())
        self.addprod.grid(row=4,column=0, sticky=tk.W)
        
        self.editprod = ttk.Button(self, text="Изменить товар")
        #self.editprod.bind('<Button-1>', lambda e: self.edit_row())
        self.editprod.grid(row=4,column=0, padx=(200, 0), sticky=tk.W)
        
        self.deleteprod = ttk.Button(self, text="удалить товар")
        #self.deleteprod.bind('<Button-1>', lambda e: self.delete_prod())
        self.deleteprod.grid(row=4,column=0, padx=(400, 0), sticky=tk.W)


#FIELDS
        
        self.documents = []

#METHODS
        self.strtup()
    
#STARTUP
    def strtup(self):
        tmp_list = []
        for i in self.doclist.get_children(): 
            self.doclist.delete(i)
        mycursor.execute("select Document.DocID, Document.DocNumber, Document.DocDate, sum(ProdCost) from Document left join (select Receive.RecID, Receive.ProdID, Products.Cost*Receive.Count as ProdCost from Products left join Receive on Products.ProdID=Receive.ProdID) as t1 on Document.DocID = t1.RecID group by DocID;")
        for x in mycursor:
            self.documents.append(document())
            self.documents[-1].set_doc_data(x)
            self.documents[-1].print_doc()
            self.doclist.insert("", tk.END, values=(self.documents[-1].docnum,self.documents[-1].docdate, self.documents[-1].docsum))
        
            
    def doc_selection(self, event):
        for i in self.prodlist.get_children(): 
                self.prodlist.delete(i)
        ind = int()
        for selection in self.doclist.selection():
            ind = self.doclist.index(selection)
        
        
        que1 = "select *, Products.Cost*Receive.Count as ProdCost from Products left join Receive on Products.ProdID=Receive.ProdID where Receive.RecID=" + str(ind+1) + ";"
            
            
        mycursor.execute(que1)
        
        cur_doc = self.documents[ind]
        for x in mycursor:
            cur_doc.products.append(product())
            cur_doc.products[-1].set_prod_data(x)
            cur_doc.products[-1].print_prod()
            self.prodlist.insert("", tk.END, values=(cur_doc.products[-1].prodid, cur_doc.products[-1].prodname, cur_doc.products[-1].produnit, cur_doc.products[-1].prodcount, cur_doc.products[-1].price, cur_doc.products[-1].sum))
        
        
        
if __name__ == "__main__":
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456787"
    )
    mycursor = mydb.cursor()
    mycursor.execute("use Sells")
    
    app = App(path=".")
    app.mainloop()