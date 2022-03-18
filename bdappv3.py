#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 23:00:35 2021

@author: swalk
"""

import datetime
import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector 
from tkcalendar import DateEntry
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

class prod_elem:
    def __init__(self):
        self.prodid = int()
        self.prodname = str()
        self.produnit = str()
        self.price = str()
        
    def fill_prod_data(self, x):
        self.prodid = x[0]
        self.prodname = x[1]
        self.produnit = x[2]
        self.price = x[3]


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
        self.prodcount = rec[6]
        self.price = rec[3]
        self.sum = rec[7]
    
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
        self.adddoc.bind('<Button-1>', lambda e: self.new_document())
        self.adddoc.grid(row=1,column=1, padx=(0, 180))
        
        self.editdoc = ttk.Button(self, text="Изменить документ")
        self.editdoc.bind('<Button-1>', lambda e: self.edit_document())
        self.editdoc.grid(row=1,column=1, padx=(0, 180), pady=(50,0))
        
        self.deletedoc = ttk.Button(self, text="удалить документ")
        self.deletedoc.bind('<Button-1>', lambda e: self.del_document())
        self.deletedoc.grid(row=1,column=1, padx=(0, 180), pady=(100,0))

        


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
        self.addprod.bind('<Button-1>', lambda e: self.new_product())
        self.addprod.grid(row=4,column=0, sticky=tk.W)
        
        self.editprod = ttk.Button(self, text="Изменить товар")
        self.editprod.bind('<Button-1>', lambda e: self.edit_product())
        self.editprod.grid(row=5,column=0, sticky=tk.W)
        
        self.deleteprod = ttk.Button(self, text="удалить товар")
        self.deleteprod.bind('<Button-1>', lambda e: self.delete_product())
        self.deleteprod.grid(row=6,column=0, sticky=tk.W)
        
        self.prnt = ttk.Button(self, text="Печать")
        self.prnt.bind('<Button-1>', lambda e: self.helllo())
        self.prnt.grid(row=4,column=0, padx=(100, 0), sticky=tk.E)
        
        self.queask = ttk.Button(self, text="Запросы")
        self.queask.bind('<Button-1>', lambda e: self.gg())
        self.queask.grid(row=5,column=0, sticky=tk.E)
        
        self.commt = ttk.Button(self, text="Сохранить все")
        self.commt.bind('<Button-1>', lambda e: self.commt_f())
        self.commt.grid(row=6,column=0, sticky=tk.E)

#DATE PICKER

        self.calstart = DateEntry(self, width=5, background='darkblue',
                    foreground='white', borderwidth=2)
        self.calstart.bind("<<DateEntrySelected>>", self.strtup)
        self.calstart.grid(row=0,column=1, padx=(0,100))
        self.calend = DateEntry(self, width=5, background='darkblue',
                    foreground='white', borderwidth=2)
        self.calend.bind("<<DateEntrySelected>>", self.strtup)
        self.calend.grid(row=0,column=1, padx=(100,0))

#FIELDS
        
        self.documents = []
        self.products = []
        self.ind = int()
        self.indd = int()

#METHODS
        #self.strtup()
    
#STARTUP

    def commt_f(self):
        mydb.commit()
        

    def helllo(self):
        # fileName = "1.pdf"
        # pdf = canvas.Canvas(fileName)
        tmp = []
        tt = []
        shap = ["Name", "Unit", "Count", "Price", "Sum"]
        tmp.append(shap)
        for x in self.products:
            tt = [str(x.prodname), str(x.produnit), str(x.prodcount), str(x.price), str(x.sum)]
            tmp.append(tt)
        
        print(tmp)
        #t = table(tmp)
        #h = heading("KEK")
       # pdf.save()
        doc = SimpleDocTemplate("simple_table.pdf", pagesize=letter)
        
        style = ParagraphStyle(
        name='Normal',
        #fontName='Inconsolata',
        fontSize=16,
        )
        
        style2 = ParagraphStyle(
        name='Normal',
        #fontName='Inconsolata',
        fontSize=16,
        )
        
        # container for the 'Flowable' objects
        elements = []
        elements.append(Paragraph('products from document {} date {}'.format(self.documents[self.indd].docnum, self.documents[self.indd].docdate), style = style))
        #wrap(doc.width, doc.topMargin)
        elements.append(Paragraph('-----------------------', style = style2))
        elements.append(Paragraph('-----------------------', style = style2))
        t=Table(tmp,len(tmp[0])*[3.4*cm], len(tmp)*[1.4*cm])
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('TEXTCOLOR',(0,0),(len(tmp[0]),0),colors.red)]))
        elements.append(t)
        elements.append(Paragraph('-------------------------', style = style2))
        elements.append(Paragraph('Sum price: {}'.format(self.documents[self.indd].docsum), style = style2))
        elements.append(Paragraph('-------------------------', style = style2))
        elements.append(Paragraph('SERVED: ______________', style = style2))
        elements.append(Paragraph('-------------------------', style = style2))
        elements.append(Paragraph('GET: ______________', style = style2))
        # write the document to disk
        doc.build(elements)
        
        


    def gg(self):
        nwww = Query_in()

    def strtup(self, event):
        datefrom = self.calstart.get_date()
        dateto = self.calend.get_date()
        self.documents.clear()
        for i in self.doclist.get_children(): 
            self.doclist.delete(i)
        mycursor.execute("select Document.DocID, Document.DocNumber, Document.DocDate, sum(ProdCost) from Document left join (select Receive.RecID, Receive.ProdID, Products.Cost*Receive.Count as ProdCost from Products left join Receive on Products.ProdID=Receive.ProdID) as t1 on Document.DocID = t1.RecID where Document.DocDate between cast('{}' as date) and cast('{}' as date) group by DocID order by DocDate;".format(str(datefrom), str(dateto)))
        for x in mycursor:
            self.documents.append(document())
            self.documents[-1].set_doc_data(x)
            self.documents[-1].print_doc()
            self.doclist.insert("", tk.END, values=(self.documents[-1].docnum,self.documents[-1].docdate, self.documents[-1].docsum))
        
            
    def doc_selection(self, event):
        for i in self.prodlist.get_children(): 
                self.prodlist.delete(i)
        self.products.clear()
        
        for selection in self.doclist.selection():
            self.ind = self.documents[self.doclist.index(selection)].docid 
            self.indd = self.doclist.index(selection)
        
        self.text = tk.StringVar()
        self.text.set('products from document {} date {}'.format(self.documents[self.indd].docnum, self.documents[self.indd].docdate))
        self.midlable = ttk.Label(text=self.text.get(), font="Arial 10")   
        self.midlable.grid(row=2,column=0)
        print(self.ind)
        que1 = "select *, Products.Cost*Receive.Count as ProdCost from Products left join Receive on Products.ProdID=Receive.ProdID where Receive.RecID=" + str(self.ind) + ";"
        mycursor.execute(que1)
        for x in mycursor:
            self.products.append(product())
            self.products[-1].set_prod_data(x)
            self.products[-1].print_prod()
            self.prodlist.insert("", tk.END, values=(self.products[-1].prodname, self.products[-1].produnit, self.products[-1].prodcount, self.products[-1].price, self.products[-1].sum))
        
        
    def new_product(self):
        neww = New_prod(self.ind, 0, 1, self.indd)
        
    def edit_product(self):
        for selection in self.prodlist.selection():
            neww = New_prod(self.ind, self.products[self.prodlist.index(selection)], 2, self.indd)
            
    def delete_product(self):
        for selection in self.prodlist.selection():
            mycursor.execute('delete from Receive where RecID = {} and ProdID = {}'.format(self.ind, self.products[self.prodlist.index(selection)].prodid))
        self.strtup(0)
        child_id = self.doclist.get_children()[self.indd]
        self.doclist.focus(child_id)
        self.doclist.selection_set(child_id)                  

    def new_document(self):
        neww = New_doc(0, 1)
        
    def edit_document(self):
        #for selection in self.doclist.selection():
        neww = New_doc(self.documents[self.indd], 2)
        
    def del_document(self):
        mycursor.execute('delete from Document where DocID = {}'.format(self.documents[self.indd-1].docid))
        self.strtup(0)


        
        
class New_doc(tk.Toplevel):
    def __init__(self, seldoc, k):
        super().__init__()
        self.title("Document Edit")
        self.geometry('900x200')

        self.docnumber = str()
        
            
        self.doc_num = tk.Entry(self, textvariable=self.docnumber)
        if k==2:
            self.doc_num.insert(0, str(seldoc.docnum))
        self.doc_num.grid(row=1,column=1)
        
        self.datepicker = DateEntry(self, width=5, background='darkblue',
                    foreground='white', borderwidth=2)
        if k==2:
            print(int(str(seldoc.docdate)[0:4]), int(str(seldoc.docdate)[5:7]), int(str(seldoc.docdate)[9:11]))
            self.datepicker.set_date(datetime.date(int(str(seldoc.docdate)[0:4]), int(str(seldoc.docdate)[5:7]), int(str(seldoc.docdate)[8:10])))
            
        self.datepicker.grid(row=1,column=2)
        
        self.gobutton = ttk.Button(self, text="выполнить")
        if k==2:
            self.gobutton.bind('<Button-1>', lambda e: self.edit_doc(seldoc.docid))
        else:
            self.gobutton.bind('<Button-1>', lambda e: self.add_doc())
        self.gobutton.grid(row=1,column=3)
        
        
    def add_doc(self):
        mycursor.execute('select max(DocID) from document')
        for x in mycursor:
            new_ind = int(x[0]) 
        adddoc = "insert into document(DocID, DocNumber, DocDate) values({}, '{}', '{}')".format(str(new_ind+1), str(self.doc_num.get()), str(self.datepicker.get_date()).replace('-', ''))
        mycursor.execute(adddoc)
        app.strtup(0)
        self.destroy()
        
    def edit_doc(self, docid):
        query_edit = "update Document set DocID = {}, DocNumber = '{}', DocDate = {} where DocID = {}".format(str(docid), str(self.doc_num.get()), str(self.datepicker.get_date()).replace('-', ''), str(docid))
        mycursor.execute(query_edit)
        app.strtup(0)
        self.destroy()
        
        
class New_prod(tk.Toplevel):
    def __init__(self, docind, prod, k, indd):
        super().__init__()
        self.title("Product Edit")
        self.geometry('900x200')
        
        self.inddch = indd
        self.prod_lst = []
        self.chosen_prod = tk.StringVar()
        self.count = tk.StringVar()
        
        self.fill_prod_lst()
        
        if k==1:
            self.chosen_prod.set(self.prod_lst[0])
        else:
            self.chosen_prod.set(self.prod_lst[prod.prodid - 1])
        self.prod_menu = tk.OptionMenu(self, self.chosen_prod, *self.prod_lst)
        self.prod_menu.grid(row=1, column=1)
        
        self.prod_count = tk.Entry(self, textvariable=self.count)
        if k!=1:
            self.prod_count.insert(0, str(prod.prodcount))
        self.prod_count.grid(row=1,column=2)
        
        self.go_button = tk.Button(self, text = "Добавить")
        if k==1:
            self.go_button.bind('<Button-1>', lambda e: self.add_prod(docind))
        else:
            self.go_button.bind('<Button-1>', lambda e: self.edit_prod(docind, prod.prodid))
        self.go_button.grid(row=1,column=3)
        
        self.prod_create = tk.Button(self, text = "Список товаров")
        self.prod_create.bind('<Button-1>', lambda e: self.drop_prod_win())
        self.prod_create.grid(row=2, column=1)
        
    def edit_prod(self, docind, prodind):
        
        query_edit = "update Receive set RecID = {}, ProdID = {}, Count = {} where RecID = {} and ProdID = {}".format(docind, self.prod_lst.index(self.chosen_prod.get())+1, self.count.get(), docind, prodind)
        mycursor.execute(query_edit)
        app.strtup(0)
        child_id = app.doclist.get_children()[self.inddch]
        app.doclist.focus(child_id)
        app.doclist.selection_set(child_id)
        self.destroy()
    
    def add_prod(self, docind):
        
        
        query_add = "insert into Receive(RecID, ProdID, Count) values ({}, {}, {})".format(docind, self.prod_lst.index(self.chosen_prod.get())+1, self.count.get())
        print('-----', query_add)
        print('---', self.prod_lst)
        mycursor.execute(query_add)
        app.strtup(0)
        child_id = app.doclist.get_children()[self.inddch]
        app.doclist.focus(child_id)
        app.doclist.selection_set(child_id)
        self.destroy()
        
        
    def fill_prod_lst(self):
        self.prod_lst.clear()
        que_prod = "select * from Products;"
        mycursor.execute(que_prod)
        for x in mycursor:
            self.prod_lst.append(x[1]) 
    
    def drop_prod_win(self):
        print('lol')
        newwww = Prod_win(self)



class Prod_win(tk.Toplevel):
    def __init__(self, k):
        super().__init__()
        self.title("Product list")
        self.prodl = []
        self.parent = k    
        
        
        self.pron = str()
        self.unit = str()
        self.price = str()
        
        self.cache_prod = prod_elem()
        
        columns = ("#1", "#2", "#3")
        self.prodlist = ttk.Treeview(self, show="headings", columns=columns)
        self.prodlist.heading("#1", text="Название продукта")
        self.prodlist.heading("#2", text="Ед. Изм")
        self.prodlist.heading("#3", text="Цена")
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.prodlist.yview)
        self.prodlist.configure(yscroll=ysb.set)
        self.prodlist.bind("<<TreeviewSelect>>", self.fill_fields)
        self.prodlist.grid(row=1, column=0, sticky=tk.W)
        
        
        self.choose_button = ttk.Button(self, text="Выбрать")
        self.choose_button.bind('<Button-1>', lambda e: self.choose_prod())
        self.choose_button.grid(row=1,column=1, padx=(0, 180))
        self.fill_prod_list()


        self.pr_n = tk.Entry(self, textvariable=self.pron)
        self.pr_n.grid(row=2,column=1)
        self.un_t = tk.Entry(self, textvariable=self.unit)
        self.un_t.grid(row=3,column=1)
        self.pr_ce = tk.Entry(self, textvariable=self.price)
        self.pr_ce.grid(row=4,column=1)
     
        self.new_but = ttk.Button(self, text="Новый продукт")
        self.new_but.bind('<Button-1>', lambda e: self.ad())
        self.new_but.grid(row=2, column=0, sticky = tk.E)
        self.ed_but = ttk.Button(self, text="Редактировать")
        self.ed_but.bind('<Button-1>', lambda e: self.ed())
        self.ed_but.grid(row=3, column=0, sticky = tk.E)
        self.del_but = ttk.Button(self, text="Удалить")
        self.del_but.bind('<Button-1>', lambda e: self.rem())
        self.del_but.grid(row=4, column=0, sticky = tk.E)
     
    def ad(self):
        print("insert into products(ProdID, ProdName, unit, Cost) values({}, {}, {}, {})".format(self.prodl[-1].prodid+1, str(self.pr_n.get()), str(self.un_t.get()), str(self.pr_ce.get())))
        mycursor.execute("insert into products(ProdID, ProdName, unit, Cost) values({}, '{}', '{}', {})".format(self.prodl[-1].prodid+1, str(self.pr_n.get()), str(self.un_t.get()), str(self.pr_ce.get())))
        self.pr_n.delete(0, tk.END)
        self.un_t.delete(0, tk.END)
        self.pr_ce.delete(0, tk.END)
        self.fill_prod_list()
        self.parent.fill_prod_lst()
        
    def ed(self):
        print("update Products set ProdID = {}, ProdName = {}, unit = {}, Cost = {} where ProdID = {}".format(self.cache_prod.prodid ,str(self.pr_n.get()), str(self.un_t.get()), str(self.pr_ce.get()), self.cache_prod.prodid))
        mycursor.execute("update Products set ProdName = '{}', unit = '{}', Cost = '{}' where ProdID = {}".format(str(self.pr_n.get()), str(self.un_t.get()), str(self.pr_ce.get()), self.cache_prod.prodid))
        
    def rem(self):
        mycursor.execute("delete from Products where ProdID = {}".format(self.cache_prod.prodid))
        self.pr_n.delete(0, tk.END)
        self.un_t.delete(0, tk.END)
        self.pr_ce.delete(0, tk.END)
        self.fill_prod_list()
        self.parent.fill_prod_lst()

        self.pr_n.delete(0, tk.END)
        self.un_t.delete(0, tk.END)
        self.pr_ce.delete(0, tk.END)
        self.fill_prod_list()
        self.parent.fill_prod_lst()
        
    def fill_fields(self, event):
        self.pr_n.delete(0, tk.END)
        self.un_t.delete(0, tk.END)
        self.pr_ce.delete(0, tk.END)
        for selection in self.prodlist.selection():
            self.cache_prod = self.prodl[self.prodlist.index(selection)]
            #print(self.prodl[self.prodlist.index(selection)].prodname)
        self.pr_n.insert(0, self.cache_prod.prodname)
        self.un_t.insert(0, self.cache_prod.produnit)
        self.pr_ce.insert(0, self.cache_prod.price)
        print('______', self.pron, self.unit, self.price)
        
        
    
    def fill_prod_list(self):
        for i in self.prodlist.get_children(): 
                self.prodlist.delete(i)
        self.prodl.clear()
        que_prod = "select * from Products;"
        mycursor.execute(que_prod)
        for x in mycursor:
            self.prodl.append(prod_elem()) 
            self.prodl[-1].fill_prod_data(x)
            self.prodlist.insert("", tk.END, values=(self.prodl[-1].prodname, self.prodl[-1].produnit, self.prodl[-1].price))
    
    def choose_prod(self):
        tmp = tk.StringVar()
        for selection in self.prodlist.selection():
            tmp.set(self.prodl[self.prodlist.index(selection)].prodname)
            #self.ind = self.documents[self.doclist.index(selection)].docid 
            #self.indd = self.doclist.index(selection)
        self.parent.chosen_prod = tmp
        self.parent.prod_menu.destroy()
        self.parent.prod_menu = tk.OptionMenu(self.parent, self.parent.chosen_prod, *self.parent.prod_lst)
        self.parent.prod_menu.grid(row=1, column=1)
        print(self.parent.chosen_prod.get())
        self.destroy()
     
  
class Query_in(tk.Toplevel):
    def __init__(self):
        super().__init__()
        
        self.text_field = tk.Text(self, width=40,height=20, font="Arial 14")
        self.text_field.grid(row = 1, column=0)
        
        self.btn = ttk.Button(self, text="Выполнить")
        self.btn.bind('<Button-1>', lambda e: self.execute())
        self.btn.grid(row = 0, column=0)
        
        
        self.btn_stop = ttk.Button(self, text="Очистить")
        self.btn_stop.bind('<Button-1>', lambda e: self.ex_stop())
        self.btn_stop.grid(row = 0, column=1)
    def execute(self):
        data = []
        tmp = 1
        
        query = str(self.text_field.get("1.0", tk.END))
        mycursor.execute(query)
        for x in mycursor:
            data.append(x)
            
        print(data)
        tt = len(data[0])
        cols = [1]*tt
        #cols = ("#1", "#2", "#3")
        #mycursor.close()
        self.plist = ttk.Treeview(self, show="headings", columns=cols)
        self.plist.grid(row = 1, column=1)
        mycursor.execute(query)
        for x in mycursor:
            #for i in range(len(x)):
            self.plist.insert("", tk.END, values=(x))
        
    def ex_stop(self):
        self.plist.destroy()
        
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