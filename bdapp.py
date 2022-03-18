#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 12:15:35 2021

@author: swalk
"""
import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector 

class App(tk.Tk):
    def __init__(self, path):
        super().__init__()
        self.title("Database app")
        self.doctpl = tuple()
        self.prodtpl = tuple()
        self.selected_num = int()
        self.selected_prod = int()
        


#FIRST TABLE

        columns = ("#1", "#2", "#3")
        self.doclist = ttk.Treeview(self, show="headings", columns=columns)
        self.doclist.heading("#1", text="# Документа")
        self.doclist.heading("#2", text="Дата документа")
        self.doclist.heading("#3", text="На сумму")
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.doclist.yview)
        self.doclist.configure(yscroll=ysb.set)

        
        
        self.doclist.bind("<<TreeviewSelect>>", self.doc_selection)
        
        
        self.doclist.grid(row=1, column=0, sticky=tk.W)
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
        self.addprod.bind('<Button-1>', lambda e: self.edit_prod())
        self.addprod.grid(row=4,column=0, sticky=tk.W)
        
        self.editprod = ttk.Button(self, text="Изменить товар")
        self.editprod.bind('<Button-1>', lambda e: self.edit_row())
        self.editprod.grid(row=4,column=0, padx=(200, 0), sticky=tk.W)
        
        self.deleteprod = ttk.Button(self, text="удалить товар")
        self.deleteprod.bind('<Button-1>', lambda e: self.delete_prod())
        self.deleteprod.grid(row=4,column=0, padx=(400, 0), sticky=tk.W)

        
    
    
        self.strtup()
    
#STARTUP
    def strtup(self):
        for i in self.doclist.get_children(): 
                self.doclist.delete(i)
        temp = list(self.doctpl)
        temp.clear()
        self.doctpl = tuple(temp)
        mycursor.execute("select Document.DocID, Document.DocNumber, Document.DocDate, sum(ProdCost) from Document left join (select Receive.RecID, Receive.ProdID, Products.Cost*Receive.Count as ProdCost from Products left join Receive on Products.ProdID=Receive.ProdID) as t1 on Document.DocID = t1.RecID group by DocID;")
        for x in mycursor:
            self.doctpl = self.doctpl + x
        print(self.doctpl)
        for i in range(0, len(self.doctpl)-1,4):
            self.doclist.insert("", tk.END, values=(self.doctpl[i+1],self.doctpl[i+2], self.doctpl[i+3]))


    def doc_selection(self, event):
        for selection in self.doclist.selection():
            self.item = self.doclist.item(selection)
            num, dat = self.item["values"][0:2]
            self.selected_num = num
            text = "Выбор: {}, {}"
            print(text.format(num, dat), self.doclist.index(selection))
            for i in self.prodlist.get_children(): 
                self.prodlist.delete(i)
                print(i)
            
            que1 = "select *, Products.Cost*Receive.Count as ProdCost from Products left join Receive on Products.ProdID=Receive.ProdID where Receive.RecID=" + str(self.doclist.index(selection)+1) + ";"
            
            
            mycursor.execute(que1)
            temp = list(self.prodtpl)
            temp.clear()
            self.prodtpl = tuple(temp)
            for y in mycursor:
                self.prodtpl = self.prodtpl + y
            print(self.prodtpl)
            for i in range(0, len(self.prodtpl)-7,8):
                self.prodlist.insert("", tk.END, values=(self.prodtpl[i+1], self.prodtpl[i+2], self.prodtpl[i+6], self.prodtpl[i+3], self.prodtpl[i+7]))
            
        
    def edit_prod(self):
        neww = Prod_edit(self.doctpl, self.selected_num, self.item, 1)

    def edit_row(self):
        for selection in self.prodlist.selection():
            self.item_prod = self.prodlist.item(selection)
            prod_sel, count_sel = [self.item_prod["values"][i] for i in (0,2)]
        new_edit = Prod_edit(self.doctpl, self.selected_num, self.item, 2, prod_sel, count_sel)
    
    def delete_prod(self):
        
        for selection in self.prodlist.selection():
            self.item_prod = self.prodlist.item(selection)
            sel_prod = self.prodlist.get_children(selection)
            prod_sel, count_sel = [self.item_prod["values"][i] for i in (0,2)]
        query_proddel = 'delete from Receive where RecID = {} and ProdID = {}'.format(int(self.selected_num), self.prodtpl[int(self.prodlist.index(sel_prod))])
        print(query_proddel)
        print(self.prodtpl)
        mycursor.execute(query_proddel)
        #mydb.commit
        #print(self.doctpl[int(self.doclist.index(self.item))]+1)
        #print(self.prodtpl[int(self.prodlist.index(sel_prod))])
        #print(query_proddel)
        
class Prod_edit(tk.Toplevel):
    def __init__(self, doctp, seln, selitem, ind, prodsel, countsel):
        super().__init__()
        self.title("Product Edit")
        self.geometry('900x200')
        self.prodlist = tuple() #For product select
        self.prodnames = [] #Array of names for drop_down menu
        self.chosen_prod = tk.StringVar()
        self.ProdCount = tk.StringVar()
        self.flag = False
        self.count = 0
        self.doc_tpl = doctp
        self.selected_doc = seln
        self.selit = selitem
        
        self.upd_prod = prodsel
        self.upd_count = countsel
        
        
#PRODUCT CHOOSE        
        que_prod = "select * from Products;"
        mycursor.execute(que_prod)
        for x in mycursor:
            self.prodlist += x

        for y in range(0, len(self.prodlist)-3,4):
            self.prodnames.append(self.prodlist[y+1])

        self.chosen_prod.set(self.prodnames[1])
        if ind==1:
            self.prod_menu = tk.OptionMenu(self, self.chosen_prod, *self.prodnames)
        else:
            self.chosen_prod.set(prodsel)
            self.prod_menu = tk.OptionMenu(self, self.chosen_prod, *self.prodnames)
            self.tdocID_init = self.doc_tpl[int(self.doc_tpl.index(self.selected_doc - 1))]
            self.tprodID_init = self.prodlist[int(self.prodlist.index(self.chosen_prod.get())-1)]
        self.prod_menu.grid(row=1, column=1)

#COUNT INPUT
        self.prod_count = tk.Entry(self, textvariable=self.ProdCount)
        if ind==2:
            self.prod_count.insert(0, str(countsel))
        self.prod_count.grid(row=1,column=2)

#ADD BUTTON
        self.go_button = tk.Button(self, text = "Добавить")
        if ind==1:
            self.go_button.bind('<Button-1>', lambda e: self.adding_prod())
        else:
            self.go_button.bind('<Button-1>', lambda e: self.editing_prod())
        self.go_button.grid(row=1,column=3)
        
     
    def adding_prod(self):  
        tdocID = self.doc_tpl[int(self.doc_tpl.index(self.selected_doc - 1))]
        tprodID = self.prodlist[int(self.prodlist.index(self.chosen_prod.get())-1)]
        print('---------')
        print(tdocID)
        print(tprodID)   
        query_add = "insert into Receive(RecID, ProdID, Count) values ({}, {}, {})".format(tdocID + 1, tprodID, self.ProdCount.get())
        mycursor.execute(query_add)
        self.flag = True
        app.strtup()
        child_id = app.doclist.get_children()[tdocID]
        app.doclist.focus(child_id)
        app.doclist.selection_set(child_id)
        self.destroy()
    
    def editing_prod(self):
        tdocID = self.doc_tpl[int(self.doc_tpl.index(self.selected_doc - 1))]
        tprodID = self.prodlist[int(self.prodlist.index(self.chosen_prod.get())-1)]
        query_edit = "update Receive set RecID = {}, ProdID = {}, Count = {} where RecID = {} and ProdID = {}".format(tdocID + 1, tprodID, self.ProdCount.get(), self.tdocID_init + 1, self.tprodID_init)
        mycursor.execute(query_edit)
        self.flag = True
        app.strtup()
        child_id = app.doclist.get_children()[tdocID]
        app.doclist.focus(child_id)
        app.doclist.selection_set(child_id)
        self.destroy()
            
    def get_prod(self):
        return self.chosen_prod
    
    def get_count(self):
        return self.ProdCount

        
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
    