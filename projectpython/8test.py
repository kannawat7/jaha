from tkinter import* 
from PIL import *
from tkinter import messagebox
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
from datetime import date
from tkinter import Tk, Label ,ttk
from io import BytesIO
import requests
import numpy as np
import cv2
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
import subprocess
from reportlab.platypus import Frame
from reportlab.lib.units import inch
from reportlab.lib import colors
import time

font_path = r'C:\Users\steam\Downloads\THSarabunNew\THSarabunNew.ttf'

pdfmetrics.registerFont(TTFont('THSarabunNew', font_path))

title_style = ParagraphStyle(
    name='TitleStyle',
    fontSize=16,
    fontName='THSarabunNew',
    alignment=0,
    spaceAfter=12,
)

larger_title_style = ParagraphStyle(
    name='LargerTitleStyle',
    fontSize=22,
    fontName='THSarabunNew',
    alignment=0,
    spaceAfter=12,
)

content_style = ParagraphStyle(
    name='ContentStyle',
    fontSize=12,
    fontName='THSarabunNew',
)

today = date.today()

window = Tk()
window.geometry("850x650")
window.resizable(width=False,height=False)
main=Image.open(r'C:\Users\steam\OneDrive\Desktop\rr\FFF25.png')
window.mbg=ImageTk.PhotoImage(main)
Label(window,image=window.mbg).place(x=0,y=0)

def create_tables():
    try:
        conn = sqlite3.connect('9test.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY NOT NULL,
            username CHAR(20) NOT NULL,
            password CHAR(20) NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id_product CHAR(20) NOT NULL,
            product CHAR(20) NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY NOT NULL,
            usercart CHAR(20) NOT NULL,
            id_product_incart CHAR(20) NOT NULL,
            productincart CHAR(20) NOT NULL,
            quantityincart INTEGER NOT NULL,
            priceincart INTEGER NOT NULL,
            totaleach INTEGER NOT NULL,
            FOREIGN KEY (id_product_incart) REFERENCES products(id_product),
            FOREIGN KEY (usercart) REFERENCES users(username),
            FOREIGN KEY (productincart) REFERENCES products(product)
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_history (
            usernamecart NOT NULL,
            id_product CHAR(20) NOT NULL,
            product CHAR(20) NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            totale INTEGER NOT NULL,
            d TEXT NOT NULL,
            m TEXT NOT NULL,
            y TEXT NOT NULL,
            FOREIGN KEY (usernamecart) REFERENCES carts(usercart),
            FOREIGN KEY (totale) REFERENCES carts(totaleach)
                                         
            )
        ''')

        

        #cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "123"))
        conn.commit()
    except sqlite3.Error as e:
        print(f"sqlite error {e}")
    finally:
        conn.close()

def signin():

    def customermenu():
        tempproduct =[]
        cartproduct =[]

        def bill():
            def showbill():
                recipe_listbox.delete(0,tk.END)
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()
                cursor.execute("SELECT  id_product_incart,productincart,quantityincart,priceincart,totaleach FROM carts WHERE usercart =?",(username,))
                showbill = cursor.fetchall()
                if showbill:
                    totalbill=0
                    for bill in showbill:
                        idproduct,productname,quantityb,priceb,totalb = bill
                        totalbill +=totalb
                        recipe_listbox.insert(tk.END,"รหัสสินค้า   {}  สินค้า   {}   จำนวน   {}   ราคา   {}   รวม   {} บาท".format(idproduct,productname,quantityb,priceb,totalb))
            
            def showtotal_bill():
                total_recipe.delete(0,tk.END)
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id_product_incart,totaleach FROM carts WHERE usercart=?",(username,))
                totalbill = cursor.fetchall()
                if totalbill:
                    totalbillprice =0
                    for ttbill in totalbill:
                        idb,totalq = ttbill

                        totalbillprice += totalq
                    
                    total_recipe.insert(tk.END,"ราคารวม   {} บาท".format(totalbillprice))
                    return totalbillprice
                else:
                    return None
            
            def payb():
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()
                cursor.execute("SELECT usercart,id_product_incart,productincart,quantityincart,priceincart,totaleach  FROM carts WHERE usercart=?", (username,))
                d = today.strftime("%d")
                m = today.strftime("%m")
                y = today.strftime("%Y")
                payment = cursor.fetchall()
                if payment:
                    result = messagebox.askquestion("Question", "ยืนยันการซี้อ?")


                    def generate_report(file_name):
                        temp_root = Tk()
                        temp_root.withdraw()
                        cursor.execute("SELECT usercart,id_product_incart,productincart,quantityincart,priceincart,totaleach  FROM carts WHERE usercart=?", (username,))
                        data = cursor.fetchall()
                        recorder = []
                        ttb = 0
                        if data:
                            
                            for info in data:
                                userc,idpcart,prd, q, pri,totalpc = info
                                ttb += totalpc
                                recorder.append([prd, q, pri])

                        doc = SimpleDocTemplate(file_name, pagesize=letter)
                        recipe = []

                        recipetitle = Paragraph("ใบเสร็จรับเงิน", larger_title_style)
                        recipe.append(recipetitle)

                        spacing_paragraph = Paragraph("<br/><br/>", title_style)
                        recipe.append(spacing_paragraph)

                        customertitle = Paragraph(f"ชื่อลูกค้า :{username}", title_style)
                        recipe.append(customertitle)

                        datetitle = Paragraph(f"วันที่ :{d}/{m}/{y}", title_style)
                        recipe.append(datetitle)

                        storetitle = Paragraph("ผู้ออก : Mader", title_style)
                        recipe.append(storetitle)

                        taxtitle = Paragraph("เลขผู้เสียภาษี : 123 ปลาฉลามขึ้นบก", title_style)
                        recipe.append(taxtitle)

                        spacing_paragraph = Paragraph("<br/><br/>", title_style)
                        recipe.append(spacing_paragraph)

                        orderitle = Paragraph("รายการ", title_style)
                        recipe.append(orderitle)

                        spacing_paragraph = Paragraph("<br/><br/>", title_style)
                        recipe.append(spacing_paragraph)

                        

                        
                        table_data = [['สินค้า', 'จำนวน', 'ราคา']]  

                        for row in recorder:
                            table_data.append(row)

                        table = Table(table_data, colWidths=[200, 80, 80], style=[
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'THSarabunNew'),
                            ('FONTNAME', (0, 1), (-1, -1), 'THSarabunNew'),
                            ('FONTSIZE', (0, 0), (-1, -1), 13),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ])
                        
                        recipe.append(table)
                        

                        table_data1 = [[f'ยอดรวม {ttb}  บาท']]  

                        spacing_paragraph = Paragraph("<br/><br/>", title_style)
                        recipe.append(spacing_paragraph)


                        table = Table(table_data1, colWidths=[200, 80, 80], style=[
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'THSarabunNew'),
                            ('FONTNAME', (0, 1), (-1, -1), 'THSarabunNew'),
                            ('FONTSIZE', (0, 0), (-1, -1), 13),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ])
                        
                        recipe.append(table)

                        doc.build(recipe)

                        try:
                            subprocess.Popen(['start', '', 'recipe.pdf'], shell=True)
                        except FileNotFoundError:
                            print("Could not open 'recipe.pdf'. Make sure you have a PDF viewer installed.")

                    for pay in payment:
                        user,idp,product,quantity,price,total = pay
                        total = price*quantity
                        
                        
                        if result == "yes":
                            
                            cursor.execute("INSERT INTO purchase_history (usernamecart,id_product,product,quantity,price,totale,d,m,y) VALUES (?,?,?,?,?,?,?,?,?)", (user,idp,product,quantity,price,total,d,m,y))
                        elif result == "no":
                            break
                    else:
                        
                        generate_report('recipe.pdf')
                        time.sleep(0.5) 
                        cursor.execute("DELETE FROM carts WHERE usercart=?", (username,))

                    showbill()
                    showtotal_bill()
                    show_cart()
                    show_products_in_store()
                    show_totalprice()
                    
                    recipe.destroy()
                    conn.commit()
                    show_cart()
                    show_products_in_store()
                    show_totalprice()
                else:
                    

                    
                    showbill()
                    showtotal_bill()
                    show_cart()
                    show_products_in_store()
                    show_totalprice()
                    recipe.destroy()
                    conn.close()

            
            
                
            recipe = Toplevel(window)
            recipe.geometry("600x600")
            recipe.resizable(width=False,height=False)
            main=Image.open(r'C:\Users\steam\OneDrive\Desktop\rr\FFF33.png')
            recipe.mbg55=ImageTk.PhotoImage(main)
            Label(recipe,image=recipe.mbg55).place(x=0,y=0)

            recipe_listbox = Listbox(recipe,font=("THSarabunNew",15))
            recipe_listbox.place(x=20,y=50,width=557,height=350)

            total_recipe = Listbox(recipe,font=("THSarabunNew",15))
            total_recipe.place(x=320,y=420,width=240,height=30)

            iconpay = PhotoImage(file=r"C:\Users\steam\OneDrive\Desktop\rr\FFF35.png")
            button_pay = Button(recipe,command=payb,image=iconpay)
            button_pay.place(x=320,y=460,width=240,height=40) 

            sum= showtotal_bill()
            if sum != None:
                print(sum)
                text = "https://promptpay.io/0611100728/" + str(sum) + ".png"
                image_url = text


                response = requests.get(image_url)

                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    
                    
                    if image.mode != 'L':
                        image = image.convert('L')

                    img_np = np.array(image)

                    qr_decoder = cv2.QRCodeDetector()

                    
                    val, pts, qr_code = qr_decoder.detectAndDecode(img_np)

                    image = image.resize((int(image.width*0.5),int(image.height*0.5)))
                    img_tk = ImageTk.PhotoImage(image)
                    

                else:
                    print("Failed to download the image. HTTP status code:", response.status_code)
            else:
                sum == None
                print(sum)
                text = "https://promptpay.io/0611100728/" + str(sum) + ".png"
                image_url = text


                response = requests.get(image_url)

                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    
                    
                    if image.mode != 'L':
                        image = image.convert('L')

                    img_np = np.array(image)

                    qr_decoder = cv2.QRCodeDetector()

                    
                    val, pts, qr_code = qr_decoder.detectAndDecode(img_np)

                    image = image.resize((int(image.width*0.5),int(image.height*0.5)))
                    img_tk = ImageTk.PhotoImage(image)
                    

                else:
                    print("Failed to download the image. HTTP status code:", response.status_code)



            lebel_qr = Label(recipe,image=img_tk)
            lebel_qr.place(x=120,y=430,width=100,height=100)

            showbill()
            showtotal_bill()
            show_cart()
            show_products_in_store()
            show_totalprice()
            
            recipe.mainloop()
            

        def show_products_in_store():
            productlist.delete(0,tk.END)
            conn = sqlite3.connect('9test.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            tempproduct.clear()
            
            for product in products:
                id_product,product,price,quantity = product
                productlist.insert(tk.END,"รหัสสินค้า :   {}   สินค้า:   {}   ราคา:   {}  บาท จำนวน:   {}  ".format(id_product,product,price,quantity))
                tempproduct.append(id_product)
    
        def show_cart():
            try:
                cartlist.delete(0,tk.END)
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()
                cursor.execute("SELECT  id,id_product_incart ,productincart, priceincart,quantityincart,totaleach FROM carts WHERE usercart=?", (username,))
                cart_data = cursor.fetchall()
                
                cartproduct.clear()
                if cart_data:
                    total_cart_price = 0 

                    for cart_item in cart_data:
                        id,id_productincart,productincart, quantityincart, priceincart,total = cart_item

                        
                        cartlist.insert(tk.END,"Order{} รหัสสินค้าในตะกร้า: {}  สินค้า: {}  ราคา   {}  บาท จำนวน: {}  ราคารวม: {} บาท".format(id,id_productincart,productincart,quantityincart,priceincart,total))

                        total_cart_price += total
                        cartproduct.append(id_productincart)
                    
            except sqlite3.Error as e:
                messagebox.showerror(title=None,message=f"sqlite error: {e}")
            finally:
                conn.close()
                


        def add_product_to_cart():
            try:
                
                id_product_incart = productlist.curselection()
                for index  in id_product_incart:
                    id_product_incart = tempproduct[index]
                print(id_product_incart)
                quantityincart = int(entryaddquantitytocart.get())
                
                
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()

                cursor.execute("SELECT product, quantity, price FROM products WHERE id_product=?", (id_product_incart,))
                product_data = cursor.fetchone()

                if product_data:
                    product_name, available_quantity, product_price = product_data
                    if quantityincart <= available_quantity:
                        new_quantity = available_quantity - quantityincart
                        cursor.execute("UPDATE products SET quantity=? WHERE id_product=?", (new_quantity, id_product_incart))

                        total_price = product_price * quantityincart

                        cursor.execute("INSERT INTO carts (usercart,id_product_incart,productincart,priceincart,quantityincart,totaleach) VALUES (?, ?, ?, ?, ?, ?)", (username,id_product_incart,  product_name, product_price, quantityincart, total_price))
                        conn.commit()
                        conn.close()
                        
                        entryaddquantitytocart.delete(0,tk.END)
                        messagebox.showinfo(title=None,message=f"รหัสสินค้า '{id_product_incart}' ถูกเพิ่มในตะกร้า ราคารวม: {total_price} บาท")
                        show_cart()
                        show_products_in_store()
                        show_totalprice()
                        
                    else:
                        messagebox.showinfo(title=None,message=f"สินค้า {product_name} มีจำนวน {available_quantity} สินค้าไม่พอ")
                else:
                    messagebox.showinfo(title=None,message="ไม่พบสินค้าที่คุณเลือก")

            except sqlite3.Error as e:
                messagebox.showinfo(title=None,message=f"sqlite error: {e}")

        def delete_product_from_cart():
            try:
                id_cart = entryeditdelproductfromcart.get()
                
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()

                cursor.execute("SELECT productincart, quantityincart FROM carts WHERE id=?", (id_cart,))
                cart_data = cursor.fetchone()

                if cart_data:
                    productincart, current_quantity = cart_data

                    cursor.execute("SELECT price FROM products WHERE product=?", (productincart,))
                    product_price = cursor.fetchone()[0]
                    removed_price = product_price * current_quantity

                    cursor.execute("DELETE FROM carts WHERE id=?", (id_cart,))
                    conn.commit()

                    
                    cursor.execute("SELECT quantity FROM products WHERE product=?", (productincart,))
                    store_quantity = cursor.fetchone()[0]
                    new_store_quantity = store_quantity + current_quantity
                    cursor.execute("UPDATE products SET quantity=? WHERE product=?", (new_store_quantity, productincart))
                    conn.commit()
                    conn.close()
                    entryeditdelproductfromcart.delete(0,tk.END)
                    entryeditquantityfromcart.delete(0,tk.END)
                    show_cart()
                    show_products_in_store()
                    show_totalprice()
                    messagebox.showinfo(title=None,message=f"สินค้า '{productincart}' ได้ลบออกจากตะกร้า, ราคาในตะกร้าลดลง: {removed_price}")
                    
                else:
                    messagebox.showinfo(title=None,message="ไม่พบสินค้า")

            except sqlite3.Error as e:
                messagebox.showinfo(title=None,message=f"SQLite error: {e}")
            

        def update_cart():
            try:
                id_cart = entryeditdelproductfromcart.get()
                
                print(id_cart)

                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()

                cursor.execute("SELECT productincart, quantityincart FROM carts WHERE id=?", (id_cart))
                cart_data = cursor.fetchone()

                if cart_data:
                    productincart, current_quantity = cart_data

                    cursor.execute("SELECT price FROM products WHERE product=?", (productincart,))
                    product_price = cursor.fetchone()[0]

                    messagebox.showinfo(title=None,message=f"อัพเดทสินค้า : {productincart}, จำนวนสินค้าที่มีอยู่ในตะกร้าขณะนี้ : {current_quantity}")

                    new_quantity = int(entryeditquantityfromcart.get())

                    total_price = product_price * new_quantity

                    cursor.execute("UPDATE carts SET quantityincart=?, priceincart=? , totaleach=? WHERE id=?", (new_quantity, product_price,total_price, id_cart))
                    conn.commit()

                    
                    cursor.execute("SELECT quantity FROM products WHERE product=?", (productincart,))
                    store_quantity = cursor.fetchone()[0]
                    new_store_quantity = store_quantity + (current_quantity - new_quantity)
                    cursor.execute("UPDATE products SET quantity=? WHERE product=?", (new_store_quantity, productincart))
                    conn.commit()
                    conn.close()
                    entryeditdelproductfromcart.delete(0,tk.END)
                    entryeditquantityfromcart.delete(0,tk.END)
                    show_cart()
                    show_products_in_store()
                    show_totalprice()
                    messagebox.showinfo(title=None,message=f"สินค้า '{productincart}' ได้อัพเดทเป็นจำนวน {new_quantity}, ราคาทั้งหมด: {total_price} บาท")
                    
                else:
                    messagebox.showinfo(title=None,message="หาสินค้าไม่เจอ")

            except sqlite3.Error as e:
                messagebox.showerror(title=None,message=f"SQLite error: {e}")
            
        def show_totalprice():
            try:
                totalprice_listbox.delete(0,tk.END)
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id_product_incart,totaleach FROM carts WHERE usercart=?", (username,))
                cart_data = cursor.fetchall()
                
                cartproduct.clear()
                if cart_data:
                    total_cart_price = 0 

                    for cart_item in cart_data:
                        id_productincart,total = cart_item

                        
                        

                        total_cart_price += total
                    
                    
                    totalprice_listbox.insert(tk.END,"ราคารวม {} บาท".format(total_cart_price))
            except sqlite3.Error as e:
                messagebox.showerror(title=None,message=f"sqlite error: {e}")
            finally:
                conn.close()

        
        

            

        def back():
            customermenugui.destroy()
        

        customermenugui = Toplevel(window)
        customermenugui.geometry("850x650")
        customermenugui.resizable(width=False,height=False)
        main=Image.open(r'C:\Users\steam\OneDrive\Desktop\rr\FFF31.png')
        customermenugui.gg=ImageTk.PhotoImage(main)
        Label(customermenugui,image=customermenugui.gg).place(x=0,y=0) 

        productlist = Listbox(customermenugui,font=("THSarabunNew",15))
        productlist.place(x=90,y=90,width=665,height=228)

        buttonaddproducttocart = Button(customermenugui,text="Add",font=("THSarabunNew",15),command=add_product_to_cart)
        buttonaddproducttocart.place(x=540,y=340,width=70,height=25)

        

       
        entryaddquantitytocart = Entry(customermenugui,text="add quantity",font=("THSarabunNew",15))
        entryaddquantitytocart.place(x=430,y=340,width=70,height=25)

        entrydelcartproduct =Entry(customermenugui,text="del product id",font=("THSarabunNew",15))
        entrydelcartproduct.place

        cartlist = Listbox(customermenugui,font=("THSarabunNew",15))
        cartlist.place(x=90,y=380,width=665,height=187)


        entryeditdelproductfromcart = Entry(customermenugui,text="edit product",font=("THSarabunNew",15))
        entryeditdelproductfromcart.place(x=150,y=590,width=70,height=25)

        entryeditquantityfromcart = Entry(customermenugui,text="edit quantity",font=("THSarabunNew",15))
        entryeditquantityfromcart.place(x=290,y=590,width=70,height=25)

        totalprice_listbox = Listbox(customermenugui,font=("THSarabunNew",15))
        totalprice_listbox.place(x=550,y=590,width=110,height=25)

        buttonpayment = Button(customermenugui,text="check bill",font=("THSarabunNew",15),command=bill)
        buttonpayment.place(x=670,y=590,width=110,height=25)

        buttoneditcart =  Button(customermenugui,text="edit",font=("THSarabunNew",15),command=update_cart)
        buttoneditcart.place(x=450,y=590,width=70,height=25)

        buttondelcart =Button(customermenugui,text="delete",font=("THSarabunNew",15),command=delete_product_from_cart)
        buttondelcart.place(x=370,y=590,width=70,height=25)

        buttonbacktolog = Button(customermenugui,text="X",font=("THSarabunNew",15),command=back) #ปุ่ม back
        buttonbacktolog.place(x=760,y=10,width=25,height=25) 

        show_products_in_store()
        show_cart()
        show_totalprice()
        customermenugui.mainloop()

    
    def admin_menu():
        tempaccount=[]
        tempproduct=[]

        def show_products_in_store():
            productlist.delete(0,tk.END)
            conn = sqlite3.connect('9test.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            tempproduct.clear()
            for product in products:
                id_product,product,price,quantity = product
                productlist.insert(tk.END,"รหัสสินค้า   {}   สินค้า   {}   ราคา   {} บาท  จำนวน   {}  ".format(id_product,product,price,quantity))
                tempproduct.append(id_product)
                
            

        def showaccuser():
            acclist.delete(0, tk.END)
            conn = sqlite3.connect('9test.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ")
            accuser = cursor.fetchall()
            tempaccount.clear()
            for acc in accuser:
                id,username,password =acc
                acclist.insert(tk.END,"ลำดับ:  {}   ชื่อ:  {}   รหัส:  {}".format(id,username,password))
                tempaccount.append(id)
                

        def delete_user():
            try:
                user_idd = acclist.curselection()
                if not user_idd:
                    messagebox.showinfo(title=None,message="โปรดเลือกผู้ใช้งาน")
                    return
                result = messagebox.askquestion("Question", "ต้องการลบผู้ใช้คนนี้?")
                for index in user_idd:
                    if index <0 or index >=len(tempaccount):
                        messagebox.showerror(title=None,message=f"Invalid index: {index}")
                        return
                    user_id  = tempaccount[index] 
                     
                    conn = sqlite3.connect('9test.db')
                    
                    cursor = conn.cursor()
                    if result == "yes":
                        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))

                        conn.commit()
                        messagebox.showinfo(title=None,message=f"ลบผู้ใช้งานรหัส {user_id} แล้ว")
                    elif result == "no":
                        conn.close()
                    showaccuser()
                
            except sqlite3.Error as e:
                messagebox.showerror(title=None,message=f"sqlite error: {e}")
            
        def delete_product_from_store():
            try:
                product_idd = productlist.curselection()
                if not product_idd:
                    messagebox.showinfo(title=None,message="โปรดเลือกสินค้าก่อนลบ")
                    return
                for index in product_idd:
                    if index <0 or index >=len(tempproduct):
                        messagebox.showerror(title=None,message=f"Invalid index: {index}")
                        return
                    product_id = tempproduct[index]  
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE id_product=?", (product_id,))
                conn.commit()
                show_products_in_store()
                messagebox.showinfo(title=None,message=f"ลบสินค้ารหัส {product_id} แล้ว")
            except sqlite3.Error as e:
                messagebox.showerror(title=None,message=f"sqlite {e}")
            finally:
                conn.close()
        
        def add_product_to_store():
            try:
                id_product =entryidproduct.get()
                product = entryproductname.get()
                price = int(entryprice.get())
                quantity = int(entryquantity.get())
                if not id_product and not product and not price and not quantity:
                    messagebox.showinfo(title=None,message="ใส่ข้อมูลให้ครบ")
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO products (id_product,product, price, quantity) VALUES (?,?, ?, ?)', (id_product,product, price, quantity))
                entryidproduct.delete(0,tk.END)
                entryproductname.delete(0,tk.END)
                entryprice.delete(0,tk.END)
                entryquantity.delete(0,tk.END)
                conn.commit()
                show_products_in_store()
                messagebox.showinfo(title=None,message=f"เพิ่มสินค้า {product} เรียบร้อยแล้ว")
            except sqlite3.Error as e:
                messagebox.showerror(title=None,message=f"sqlite error: {e}")
            finally:
                conn.close()
        
        def update_product():
            try:
                product_id = entryidproduct.get()
                new_product = entryproductname.get()
                new_price = int(entryprice.get())
                new_quantity = int(entryquantity.get())
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET product=?, price=?, quantity=? WHERE id_product=?", (new_product, new_price, new_quantity, product_id))
                entryidproduct.delete(0,tk.END)
                entryproductname.delete(0,tk.END)
                entryprice.delete(0,tk.END)
                entryquantity.delete(0,tk.END)
                
                conn.commit()
                show_products_in_store()
                messagebox.showinfo(title=None,message=f"อัปเดตสินค้ารหัส {product_id} เรียบร้อยแล้ว")
            except sqlite3.Error as e:
                messagebox.showerror(title=None,message=f"sqlite error {e}")
            finally:
                conn.close()
        
        
        

        def Purchasehistory(event=None):
            Purchasehistorygui = Toplevel(window)
            Purchasehistorygui.geometry("900x700")
            Purchasehistorygui.resizable(width=False,height=False)
            main=Image.open(r'C:\Users\steam\OneDrive\Desktop\rr\FFF30.png')
            Purchasehistorygui.ww=ImageTk.PhotoImage(main)
            Label(Purchasehistorygui,image=Purchasehistorygui.ww).place(x=0,y=0)

            def dayshistory():

                def showPurchasehistoryday():
                    d = dselected_day.get()
                    m = dselected_month.get()
                    y = dselected_year.get()
                
                    Purchasehistory_listbox.delete(0,tk.END)
                    conn = sqlite3.connect('9test.db')
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT usernamecart,id_product,product,price,quantity,totale,d,m,y FROM purchase_history WHERE d=? AND m=? AND y=?",(d,m,y))
                    showshitory = cursor.fetchall()
                    if showshitory:
                        for showh in showshitory:
                            totalp=0
                            usercart,id,product,price,quantity,total,d,m,y = showh
                            totalp += total
                            Purchasehistory_listbox.insert(tk.END,"ลูกค้า  {}   รหัสสินค้า    {}   สินค้า   {}  ราคา    {} บาท  จำนวน   {}     ราคารวม   {}   เวลาที่ซื้อ  {}/{}/{}".format(usercart,id,product,price,quantity,totalp,d,m,y))
                    
                    cursor.execute("SELECT price , quantity,totale FROM purchase_history WHERE d=? AND m=? AND y=?",(d,m,y))
                    totalhistoryp = cursor.fetchall()
                    if totalhistoryp:
                        total_history_price = 0 
                        for showtotal in totalhistoryp:
                            priceh,quantityh,total=showtotal
                            total_history_price += total
                        
                        total_listbox = Label(Purchasehistorygui,font=("THSarabunNew",17),text=f"รายได้ {total_history_price} บาท")
                        total_listbox.place(x=350,y=600,width=172,height=22)
                    else:
                        total_history_price=0
                        total_listbox = Label(Purchasehistorygui,font=("THSarabunNew",17),text=f"รายได้ {total_history_price} บาท")
                        total_listbox.place(x=350,y=600,width=172,height=22)
                    
                showPurchasehistoryday()

            def monthshistory():

                def showPurchasehistorymonth():
                    
                    m = mselected_month.get()
                    y = mselected_year.get()
                
                    Purchasehistory_listbox.delete(0,tk.END)
                    conn = sqlite3.connect('9test.db')
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT usernamecart,id_product,product,price,quantity,totale,m,y FROM purchase_history WHERE  m=? AND y=?",(m,y))
                    showshitory = cursor.fetchall()
                    if showshitory:
                        for showh in showshitory:
                            totalp=0
                            usercart,id,product,price,quantity,total,m,y = showh
                            totalp += total

                            Purchasehistory_listbox.insert(tk.END,"ลูกค้า  {}   รหัสสินค้า    {}   สินค้า   {}  ราคา    {} บาท  จำนวน   {}     ราคารวม   {}   เวลาที่ซื้อ  {}/{}".format(usercart,id,product,price,quantity,totalp,m,y))
                    
                    cursor.execute("SELECT price , quantity,totale FROM purchase_history WHERE  m=? AND y=?",(m,y))
                    totalhistoryp = cursor.fetchall()
                    if totalhistoryp:
                        total_history_price = 0 
                        for showtotal in totalhistoryp:
                            priceh,quantityh,total=showtotal
                            total_history_price += total
                        
                        total_listbox = Label(Purchasehistorygui,font=("THSarabunNew",17),text=f"รายได้ {total_history_price} บาท")
                        total_listbox.place(x=350,y=600,width=172,height=22)
                    else:
                        total_history_price=0
                        total_listbox = Label(Purchasehistorygui,font=("THSarabunNew",17),text=f"รายได้ {total_history_price} บาท")
                        total_listbox.place(x=350,y=600,width=172,height=22)
                        
                showPurchasehistorymonth()

            dselected_day = StringVar()
            dday = ttk.Combobox(Purchasehistorygui, textvariable=dselected_day, values=[str(i) for i in range(1, 32)])
        
            dday.place(x=40,y=20,width=50,height=20)
            dday.bind('<<ComboboxSelected>>')

            
            dselected_month = StringVar()
            dmonth = ttk.Combobox(Purchasehistorygui, textvariable=dselected_month, values=[
                                    '1', '2', '3', '4', '5', '6', 
                                    '7', '8', '9', '10', '11', '12'])
            
            dmonth.place(x=95,y=20,width=50,height=20)
            dmonth.bind('<<ComboboxSelected>>')

            
            dselected_year = StringVar()
            dyear = ttk.Combobox(Purchasehistorygui, textvariable=dselected_year, values=[str(i) for i in range(2000, 2031)])
            
            dyear.bind('<<ComboboxSelected>>')
            dyear.place(x=150,y=20,width=50,height=20)

            buttonserch = Button(Purchasehistorygui,text="ค้นประวัติรายวัน",command=dayshistory)
            buttonserch.place(x=205,y=20,width=85,height=20)

#----------------------------------------------------------
            mselected_month = StringVar()
            mmonth = ttk.Combobox(Purchasehistorygui, textvariable=mselected_month, values=[
                                    '1', '2', '3', '4', '5', '6', 
                                    '7', '8', '9', '10', '11', '12'])
            
            mmonth.place(x=650,y=20,width=50,height=20)
            mmonth.bind('<<ComboboxSelected>>')

            
            mselected_year = StringVar()
            myear = ttk.Combobox(Purchasehistorygui, textvariable=mselected_year, values=[str(i) for i in range(2000, 2031)])
            
            myear.bind('<<ComboboxSelected>>')
            myear.place(x=705,y=20,width=50,height=20)

            buttonserch = Button(Purchasehistorygui,text="ค้นประวัติรายเดือน",command=monthshistory)
            buttonserch.place(x=765,y=20,width=85,height=20)

            Purchasehistory_listbox = Listbox(Purchasehistorygui,font=("THSarabunNew",15))
            Purchasehistory_listbox.place(x=30,y=60,width=850,height=528)

            total_listbox = Label(Purchasehistorygui,font=("THSarabunNew",15))
            total_listbox.place(x=375,y=600,width=172,height=22)

            
            
            
                
            Purchasehistorygui.mainloop()
        
        

        
        # admingui----------------------------------------------
        admingui = Toplevel(window)
        admingui.geometry("850x650")
        admingui.resizable(width=False,height=False)
        main=Image.open(r'C:\Users\steam\OneDrive\Desktop\rr\FFF37.png')
        admingui.pp=ImageTk.PhotoImage(main)
        Label(admingui,image=admingui.pp).place(x=0,y=0)

        entryidproduct= Entry(admingui,text="ID product",font=("THSarabunNew",15)) #ปุ่ม ใส่ id product
        entryidproduct.place(x=470,y=190,width=84,height=30)

        entryproductname= Entry(admingui,text="Product name",font=("THSarabunNew",15)) #ปุ่มใส่ name product
        entryproductname.place(x=470,y=260,width=84,height=30)

        entryprice= Entry(admingui,text="Price",font=("THSarabunNew",15)) #ปุ่มใส่ price product
        entryprice.place(x=470,y=330,width=84,height=30)

        entryquantity= Entry(admingui,text="Quantity",font=("THSarabunNew",15)) #ปุ่มใส่ quantity product
        entryquantity.place(x=470,y=400,width=84,height=30)

        buttondelacc = Button(admingui,text="del ac",font=("THSarabunNew",15),command=delete_user) #ปุ่ม ลบaccount
        buttondelacc.place(x=660,y=530,width=70,height=25)
        
        buttonaddproduct = Button(admingui,text="Add",font=("THSarabunNew",15),command=add_product_to_store)  #ปุ่ม addproduct
        buttonaddproduct.place(x=470,y=470,width=84,height=30)

        buttoneditproduct = Button(admingui,text="Edit",font=("THSarabunNew",15),command=update_product) #ปุ่ม edit product
        buttoneditproduct.place(x=470,y=530,width=84,height=30)

        buttondelproduct = Button(admingui,text="Delete",font=("THSarabunNew",15),command=delete_product_from_store) #ปุ่ม del product
        buttondelproduct.place(x=230,y=530,width=70,height=25)

        buttonPurchasehistory = Button(admingui,text="Purchase history",font=("THSarabunNew",15),command=Purchasehistory) 
        buttonPurchasehistory.place(x=700,y=10,width=110,height=25)

        

        acclist = Listbox(admingui,font=("THSarabunNew",15))
        acclist.place(x=570,y=160,width=241,height=333)

        productlist = Listbox(admingui,font=("THSarabunNew",14))
        productlist.place(x=60,y=160,width=402,height=329)

        


        showaccuser()
        show_products_in_store()
        admingui.mainloop()
        #-------------------------------------------------------
        
            

    def get_usernamepassword(username_login, password_login):
        try:
            conn = sqlite3.connect('9test.db')
            cursor = conn.cursor()
            cursor.execute("SELECT username, password FROM users WHERE username=? and password=?", (username_login, password_login))
            user_data = cursor.fetchone()
            print(user_data)
            if user_data:
                username, password = user_data
                return username, password
            else:
                return None, None  
        except sqlite3.Error as e:
            print(f"sqlite error {e}")
        finally:
            conn.close()

    username_login = entryusername.get()
    password_login = entrypassword.get()
       
    username, password = get_usernamepassword(username_login, password_login)

    entryusername.delete(0,tk.END)
    entrypassword.delete(0,tk.END)
    if username == "admin" and password == "123":
        admin_menu()
    elif username and password:
        customermenu()
    else:
        messagebox.showerror(title=None,message="ไม่พบชื่อผู้ใช่งาน")

    
def signup():
    def back():
        registergui.destroy()
    def create_user():
        try:
            username = entryregisterusername.get()
            password = entryregisterpassword.get()
            if username.lower() == "admin":
                messagebox.showinfo(title=None,message="ใช้ชื่อนี้ไม่ได้")
            elif not username:
                messagebox.showinfo(title=None,message="ใส่ข้อมูลให้ครบ")
            else:
                conn = sqlite3.connect('9test.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                entryregisterusername.delete(0,tk.END)
                entryregisterpassword.delete(0,tk.END)
                
                conn.commit()
                messagebox.showinfo(title=None,message=f"{username}บัญชีผู้ใช้ถูกสร้างเรียบร้อยแล้ว")
        except sqlite3.Error as e:
            messagebox.showerror(f"sqlite error {e}")
        finally:
            conn.close()
        registergui.destroy()
    

    registergui = Toplevel(window)
    registergui.geometry("661x470")
    registergui.resizable(width=False,height=False)
    main=Image.open(r'C:\Users\steam\OneDrive\Desktop\rr\FFF23.png')
    registergui.qq=ImageTk.PhotoImage(main)
    Label(registergui,image=registergui.qq).place(x=0,y=0)

    
    entryregisterusername = Entry(registergui,font=("THSarabunNew",25),)
    entryregisterusername.place(x=240,y=140,width=180,height=43)

    entryregisterpassword = Entry(registergui,font=("THSarabunNew",25),show="*")
    entryregisterpassword.place(x=240,y=240,width=181,height=38)

    registerbutton = Button(registergui,text="Register",font=("THSarabunNew",15),command=create_user)
    registerbutton.place(x=300,y=330,width=52,height=30)

    buttonbacktologin = Button(registergui,text="x",font=("THSarabunNew",15),command=back)
    buttonbacktologin.place(x=600,y=20,width=41,height=30)

    registergui.mainloop()


def Creator():

    creatorgui = Toplevel(window)
    creatorgui.geometry("850x650")
    creatorgui.resizable(width=False,height=False)
    main=Image.open(r'C:\Users\steam\OneDrive\Desktop\rr\FFF40.png')
    creatorgui.gg=ImageTk.PhotoImage(main)
    Label(creatorgui,image=creatorgui.gg).place(x=0,y=0)

    creatorgui.mainloop()

#หน้า login
create_tables()

entryusername = Entry(font=("THSarabunNew",25))
entryusername.place(x=300,y=240,width=299,height=51)

entrypassword= Entry(font=("THSarabunNew",25),show="*")
entrypassword.place(x=300,y=350,width=299,height=51)

iconlogin = PhotoImage(file=r"C:\Users\steam\OneDrive\Desktop\rr\FFF26.png")
buttonsingin = Button(command=signin,image= iconlogin )
buttonsingin.place(x=330,y=420,width=80,height=42)

iconsignup = PhotoImage(file=r"C:\Users\steam\OneDrive\Desktop\rr\FFF27.png")
buttonsingup=Button(command=signup,image= iconsignup)
buttonsingup.place(x=480,y=420,width=80,height=42)

Creatorr = Button(text="Creator",font=("THSarabunNew",15),command=Creator) 
Creatorr.place(x=700,y=55,width=100,height=25)  

window.mainloop()
