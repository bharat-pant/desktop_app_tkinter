from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import tkinter.messagebox as tmsg
import pymysql
import time
import pandas as pd
from matplotlib import pyplot as plt

con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
cur = con.cursor()
cur.execute("select uniquecode from overall")
gg=cur.fetchall()
gg1=max(gg)
k=gg1[0]+1

def Electronics():
    global root3
    if u_name=="E":
        root.destroy()
    else:
        root1.destroy()

    def Mark_In():
        global current_time1
        current_time1 = time.strftime('%H %M')

    def Mark_Out():
        global j
        current_time = time.strftime('%H %M')
        con = pymysql.connect(host="localhost", user="root", password="", database="Attendance")
        cur = con.cursor()
        cur.execute("insert into Electronics values(%s,%s,%s,%s)", ("Electronics", current_time1, current_time, j))
        j = j + 1
        con.commit()
        con.close()

    def number_update():
        global i
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
            cur = con.cursor()
            cur.execute("select uniquecode from billing")
            row = cur.fetchall()
            length = max(row)
            i = length[0] + 1
        except:
            i=1

    def Add_item():
        number_update()
        global i
        global k
        if (Order_ID.get() == "" or
                Customer_Name.get() == "" or
                Order_Date.get() == "" or
                Sub_Category.get() == "" or
                Price.get() == "" or
                Quantity.get() == ""):
            tmsg.showinfo("ERROR", "All fields are mandatory")

        else:
            try:
                print(Price.get())
                print(2/Price.get())
                print(2/Quantity.get())
                con_MRP = pymysql.connect(host="localhost", user="root", password="", database="purchase")
                cur_MRP = con_MRP.cursor()
                cur_MRP.execute(
                    "select price from purchase_bill where Productname LIKE '%" + str(Sub_Category.get() + "%'"))
                rows = cur_MRP.fetchone()
                MRP = rows

                Total = Quantity.get() * Price.get()
                print(Quantity.get())
                print(Total)
                print(MRP[0])
                Profit = Total - Quantity.get() * int(MRP[0])

                con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
                cur = con.cursor()
                cur.execute("insert into billing values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Order_ID.get(),
                                                                                          Customer_Name.get(),
                                                                                          Order_Date.get(),
                                                                                          "Electronics",
                                                                                          Sub_Category.get(),
                                                                                          Price.get(),
                                                                                          Quantity.get(),
                                                                                          Total,
                                                                                          Profit,
                                                                                          i))
                print(Profit)
                con.commit()
                i = i + 1
                fetch()
                con.close()

                con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
                cur = con.cursor()
                cur.execute("insert into overall values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Order_ID.get(),
                                                                                          Customer_Name.get(),
                                                                                          Order_Date.get(),
                                                                                          "Electronics",
                                                                                          Sub_Category.get(),
                                                                                          Price.get(),
                                                                                          Quantity.get(),
                                                                                          Total,
                                                                                          Profit,
                                                                                          k))

                print(Profit)
                con.commit()
                k = k + 1
                fetch()
                clear_display()
                con.close()
            except:
                row=1


    def fetch():
        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        cur.execute("select * from billing")
        rows = cur.fetchall()
        if len(rows) != 0:
            Edetails.delete(*Edetails.get_children())
            for x in rows:
                Edetails.insert('', END, value=x)
            con.commit()
        con.close()

    def Remove_item():
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="Productdetails")
            cur = con.cursor()
            cur.execute("delete from billing where uniquecode=%s", selection)
            con.commit()
            con.close()
            fetch()
        except:
            tmsg.showinfo("ERROR","Nothing selected to remove")

    def get_cursor(event):
        global selection
        cursor_row = Edetails.focus()
        contents = Edetails.item(cursor_row)
        row = contents['values']
        Order_ID.set(row[0])
        Customer_Name.set(row[1])
        Order_Date.set(row[2])
        Sub_Category.set(row[4])
        Quantity.set(row[6])
        Price.set(row[5])
        selection = row[9]

    def clear_display():
        Sub_Category.set("")
        Price.set("")
        Quantity.set("")

    def Submit():
        summ=0
        for Total in Edetails.get_children():
            summ=summ+Edetails.item(Total)["values"][7]
        tmsg.showinfo("CUSTOMER BILL","THANK YOU FOR COMING\nYour total is {}".format(summ))

        Order_ID.set("")
        Customer_Name.set("")
        Order_Date.set("")
        Edetails.delete(*Edetails.get_children())
        clear_display()

    def Employee_Logout():
        if u_name=="E":
            root3.destroy()
            main_window()
        else:
            root3.destroy()
            Sign_up_interior()

    def clock():
        try:
            current_time = time.strftime('%I:%M:%S %p')
            Label(root, font=("Arial", 14), bg="#023E84", fg="white", text=current_time).place(x=600, y=570)
            root.after(200, clock)
        except:
            pass

    root3 = Tk()
    root3.geometry("1520x800")
    root3.maxsize(width=1520,height=800)
    root3.minsize(width=1520,height=800)
    root3.title("ELECTRONICS SECION")

    # IMAGES
    background = Image.open("Images\electronics_dept_3D.jpg")
    bg = ImageTk.PhotoImage(background)

    # BACKGROUND
    Label(root3, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    Label(root3, text="ELECTRONICS SECTION", font=("Comic Sans MS", 32, "bold"), fg="#041B50", bg="white").place(
        x=0, y=5, relwidth=1)

    # FRAME
    f1 = Frame(root3, bg="white", bd=0, width=450, height=200)
    f2 = Frame(root3, bg="white", bd=0, width=450, height=300)
    f3 = Frame(root3, bg="white", bd=5)

    # LABELS
    Label(f1, text="CUSTOMER DETAILS", bg="white", font=("Arial,18")).place(x=120, y=10)
    Label(f2, text="PRODUCT DETAILS", bg="white", font=("Arial,18")).place(x=120, y=20)
    product_id = Label(f1, text="◼ ORDER ID", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=70)
    product_type = Label(f1, text="◼ CUSTOMER NAME", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=110)
    product_name = Label(f1, text="◼ ORDER DATE", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=150)
    category = Label(f2, text="◼ CATEGORY", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=70)
    sub_category = Label(f2, text="◼ SUB CATEGORY", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=110)
    price = Label(f2, text="◼ PRICE (per unit)", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=150)
    quantity = Label(f2, text="◼ QUANTITY", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=190)
    order_details = Label(f3, text="ORDER DETAILS", font=("Arial", 14), bg="#041B50", fg="white").pack(fill=X)
    section = Label(f2, width=20, text="Electronics", bg="white", font=("Arial", 11)).place(x=220, y=70)
    Label(root3, text="ELECTRONICS SECTION", bg="white", fg="#041B50",
          font=("Arial", 14, "bold", "underline")).place(x=275, y=565)

    # TEXTVARIABLE:
    Order_ID = StringVar()
    Customer_Name = StringVar()
    Order_Date = StringVar()
    Sub_Category = StringVar()
    Price = IntVar()
    Quantity = IntVar()

    # ENTRY WIDGETS
    EE1 = Entry(f1, width=25, font=("Arial", 11), textvariable=Order_ID).place(x=220, y=70)
    EE2 = Entry(f1, width=25, font=("Arial", 11), textvariable=Customer_Name).place(x=220, y=110)
    EE3 = Entry(f1, width=25, font=("Arial", 11), textvariable=Order_Date).place(x=220, y=150)
    EE4 = Entry(f2, width=25, font=("Arial", 11), textvariable=Sub_Category).place(x=220, y=110)
    EE5 = Entry(f2, width=25, font=("Arial", 11), textvariable=Price).place(x=220, y=150)
    EE6 = Entry(f2, width=25, font=("Arial", 11), textvariable=Quantity).place(x=220, y=190)


    # TREEVIEW
    scroll_x = Scrollbar(f3, orient=HORIZONTAL)
    scroll_y = Scrollbar(f3, orient=VERTICAL)
    Edetails = ttk.Treeview(f3, columns=(
        "Order ID", "Name", "Order date", "Category", "Product", "Quantity", "Price per Unit", "Total"),
                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=Edetails.xview)
    scroll_y.config(command=Edetails.yview)
    Edetails.heading("Order ID", text="Order ID")
    Edetails.heading("Name", text="Name")
    Edetails.heading("Order date", text="Order date")
    Edetails.heading("Category", text="Category")
    Edetails.heading("Product", text="Product")
    Edetails.heading("Price per Unit", text="Price per Unit")
    Edetails.heading("Quantity", text="Quantity")
    Edetails.heading("Total", text="Total")
    Edetails['show'] = 'headings'
    Edetails.column("Order ID", width=100)
    Edetails.column("Name", width=150)
    Edetails.column("Order date", width=100)
    Edetails.column("Category", width=200)
    Edetails.column("Product", width=200)
    Edetails.column("Price per Unit", width=100)
    Edetails.column("Quantity", width=100)
    Edetails.column("Total", width=100)
    Edetails.pack(fill=BOTH, expand=1)
    Edetails.bind("<ButtonRelease-1>", get_cursor)


    # BUTTON
    b1 = Button(f2, text="ADD ITEM", font=("Arial", 10), bg="white", command=Add_item).place(x=200, y=240)
    b12 = Button(root3, text="SHOW ALL", width=16, activebackground="#041B50", activeforeground="white",
                font=("Arial", 14, "bold"), bg="white", command=fetch).place(x=1245, y=608)
    b2 = Button(root3, text="SUBMIT", width=16, activebackground="#041B50", activeforeground="white",
                font=("Arial", 14, "bold"), bg="white", command=Submit).place(x=1040, y=608)

    b3 = Button(f2, text="REMOVE ITEM", font=("Arial", 10), bg="white", command=Remove_item).place(x=300, y=240)
    b4 = Button(root3, text="MARK IN TIME", width=15, bg="#041B50", activeforeground="#041B50",
                activebackground="white", fg="white", font=("Arial", 12, "bold"), command=Mark_In).place(x=310,
                                                                                                         y=605)
    b5 = Button(root3, text="MARK OUT TIME", width=15, bg="#041B50", activeforeground="#041B50",
                activebackground="white", fg="white", font=("Arial", 12, "bold"), command=Mark_Out).place(x=310,
                                                                                                          y=645)
    b6 = Button(root3, text="EMPLOYEE LOGOUT", width=32, bg="white", fg="#041B50", activebackground="#041B50",
                activeforeground="white", font=("Arial", 14, "bold"), command=Employee_Logout).place(x=110, y=710)
    f1.place(x=580, y=135)
    f2.place(x=580, y=345)
    f3.place(x=1040, y=135, width=405, height=465)

    clock()

    root3.mainloop()


def Add_Employee():
    global root2
    root1.destroy()

    def clock():
        try:
            current_time = time.strftime('%I:%M:%S %p')
            Label(root, font=("Arial", 14), bg="#023E84", fg="white", text=current_time).place(x=600, y=570)
            root.after(200, clock)
        except:
            pass

    def Back():
        root2.destroy()
        Sign_up_interior()

    def Add():
        if (ID.get() == "" or
                Name.get() == "" or
                Contact_number.get() == "" or
                PAN_Card_Number.get() == "" or
                Aadhar_Card_Number.get() == "" or
                E_Mail_ID.get() == "" or
                Department.get() == ""):
            tmsg.showinfo("ERROR", "All fields are mandatory")

        else:
            try:
                    print(2/eval(Contact_number.get()))
                    con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
                    cur = con.cursor()
                    cur.execute("insert into edit_employee values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (ID.get(),
                                                                                                     Name.get(),
                                                                                                     Contact_number.get(),
                                                                                                     E_Mail_ID.get(),
                                                                                                     Department.get(),
                                                                                                     Date_of_Birth.get(),
                                                                                                     PAN_Card_Number.get(),
                                                                                                     Aadhar_Card_Number.get(),
                                                                                                     Address.get('1.0', END)
                                                                                                     ))
                    con.commit()
                    fetch()
                    Login()
                    clear_display()
                    con.close()
            except TypeError:
                    tmsg.showinfo("ERROR","Invalid Phone Number")

    def fetch():
        con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
        cur = con.cursor()
        cur.execute("select * from edit_employee")
        rows = cur.fetchall()
        if len(rows) != 0:
            details.delete(*details.get_children())
            for x in rows:
                details.insert('', END, value=x)
            con.commit()
        con.close()

    def Search_Data():
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
            cur = con.cursor()
            cur.execute(
                "select * from edit_employee where " + str(search_by.get()) + " LIKE '%" + str(search_for.get()) + "%'")
            rows = cur.fetchall()
            if len(rows) != 0:
                details.delete(*details.get_children())
                for x in rows:
                    details.insert('', END, value=x)
                con.commit()
            con.close()
        except:
            tmsg.showinfo("ERROR","Search parameters can't be left Empty")

    def clear_display():
        ID.set("")
        Name.set("")
        Contact_number.set("")
        E_Mail_ID.set("")
        Department.set("")
        Date_of_Birth.set("")
        PAN_Card_Number.set("")
        Aadhar_Card_Number.set("")
        Address.delete('1.0', END)

    def get_cursor(event):
        cursor_row = details.focus()
        contents = details.item(cursor_row)
        row = contents['values']
        ID.set(row[0])
        Name.set(row[1])
        Contact_number.set(row[2])
        E_Mail_ID.set(row[3])
        Department.set(row[4])
        Date_of_Birth.set(row[5])
        PAN_Card_Number.set(row[6])
        Aadhar_Card_Number.set(row[7])
        Address.delete('1.0', END)
        Address.insert(END, row[8])

    def Remove():
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
            cur = con.cursor()
            cur.execute("delete from edit_employee where id=%s", ID.get())
            con.commit()
            con.close()
            fetch()

            con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
            cur = con.cursor()
            cur.execute("delete from login where LoginID=%s", ID.get())
            con.commit()
            con.close()
            clear_display()
            fetch()
        except:
            tmsg.showinfo("ERROR","Nothing selected to remove")

    def Login():
        dob = Date_of_Birth.get()
        phone = Contact_number.get()
        password = dob[6:] + "@" + phone[6:]
        con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
        cur = con.cursor()
        cur.execute("insert into Login values(%s,%s)", (ID.get(), password))
        con.commit()
        con.close()

    root2 = Tk()
    root2.geometry("1520x820")
    root2.maxsize(width=1520,height=820)
    root2.minsize(width=1520, height=820)
    root2.title("EMPLOYEE SECTION")
    background = Image.open("Images\YYYY.jpg")
    bg = ImageTk.PhotoImage(background)
    Label(root2, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    f1 = Frame(root2, bg="white", bd=0, width=500, height=335)
    f2 = Frame(root2, bg="white", bd=0, width=500, height=275)
    f3 = Frame(root2, bg="white", bd=5)

    # LABELS
    Label(root2, text="EMPLOYEE SECTION", font=("Comic Sans MS", 32, "bold"), fg="#0A2C61", bg="white").place(x=0,
                                                                                                              y=5,
                                                                                                              relwidth=1)
    Label(f2, text="EMPLOYEE PRIMARY DETAILS", font=("Arial", 16, "bold", "underline"), bg="white",
          fg="#041B50").place(
        x=90, y=25)
    Label(f1, text="EMPLOYEE SECONDARY DETAILS", font=("Arial", 16, "bold", "underline"), bg="white",
          fg="#041B50").place(
        x=70, y=25)
    Label(f2, text="◼ Employee ID", font=("Arial", 12), bg="white").place(x=30, y=80)
    Label(f2, text="◼ Name", font=("Arial", 12), bg="white").place(x=30, y=130)
    Label(f2, text="◼ Contact Number", font=("Arial", 12), bg="white").place(x=30, y=180)
    Label(f2, text="◼ E-Mail ID", font=("Arial", 12), bg="white").place(x=30, y=230)
    Label(f1, text="◼ Department", font=("Arial", 12), bg="white").place(x=30, y=70)
    Label(f1, text="◼ Date of Birth", font=("Arial", 12), bg="white").place(x=30, y=120)
    Label(f1, text="◼ PAN Card Number*", font=("Arial", 12), bg="white").place(x=30, y=170)
    Label(f1, text="◼ Aadhar Card Number*", font=("Arial", 12), bg="white").place(x=30, y=220)
    Label(f1, text="◼ Permanent Address ", font=("Arial", 12), bg="white").place(x=30, y=270)
    Label(f3, text="Search by category:", font=("Arial", 12), bg="white").pack(anchor="w")
    Label(f3, text=" EMPLOYEE DETAILS ", font=("Arial", 16, "bold"), bg="#041B50", fg="white").pack(fill=X)

    # VARIABLES
    ID = StringVar()
    Name = StringVar()
    Contact_number = StringVar()
    E_Mail_ID = StringVar()
    Department = StringVar()
    Date_of_Birth = StringVar()
    PAN_Card_Number = StringVar()
    Aadhar_Card_Number = StringVar()
    search_by = StringVar()
    search_for = StringVar()

    # ENTRY
    E1 = Entry(f2, width=28, font=("Arial", 12), textvariable=ID).place(x=210, y=80)
    E2 = Entry(f2, width=28, font=("Arial", 12), textvariable=Name).place(x=210, y=130)
    E3 = Entry(f2, width=28, font=("Arial", 12), textvariable=Contact_number).place(x=210, y=180)
    E4 = Entry(f2, width=28, font=("Arial", 12), textvariable=E_Mail_ID).place(x=210, y=230)
    E5 = Entry(f1, width=28, font=("Arial", 12), textvariable=Department).place(x=210, y=70)
    E6 = Entry(f1, width=28, font=("Arial", 12), textvariable=Date_of_Birth).place(x=210, y=120)
    E7 = Entry(f1, width=28, font=("Arial", 12), textvariable=PAN_Card_Number).place(x=210, y=170)
    E8 = Entry(f1, width=28, font=("Arial", 12), textvariable=Aadhar_Card_Number).place(x=210, y=220)
    Address = Text(f1, width=31, height=3)
    Address.place(x=210, y=270)
    E9 = Entry(root2, font=("Arial", 10), width=30, bg="white", textvariable=search_for).place(x=1010, y=145)

    # BUTTON
    b4 = Button(root2, text="ADD EMPLOYEE", width=15, fg="#041B50", activebackground="#041B50",
                activeforeground="white",
                bg="white", font=("Arial", 14, "bold"), bd=0, command=Add).place(x=257, y=720)
    b5 = Button(root2, text="BACK", width=12, fg="#041B50", activebackground="#041B50", activeforeground="white",
                bg="white",
                font=("Arial", 14, "bold"), bd=0, command=Back).place(x=100, y=720)
    Button(root2, text="SEARCH", width=13, bg="#041B50", fg="white", font=("Arial", 10, "bold"), bd=0,
           command=Search_Data).place(x=1230, y=143)
    Button(root2, text="REMOVE", width=12, fg="#041B50", activebackground="#041B50", activeforeground="white",
           bg="white",
           font=("Arial", 14, "bold"), bd=0, command=Remove).place(x=450, y=720)
    Button(root2, text="DISPLAY ALL", width=13, bg="#041B50", fg="white", font=("Arial", 10, "bold"), bd=0,
           command=fetch).place(x=1350, y=143)
    # COMBOBOX
    search = ttk.Combobox(root2, font=("Arial", 10), state='readonly', textvariable=search_by)
    search['values'] = ["ID", "Department", "Contact", "Name"]
    search.place(x=810, y=145)

    # TREEVIEW
    scroll_x = Scrollbar(f3, orient=HORIZONTAL)
    scroll_y = Scrollbar(f3, orient=VERTICAL)
    details = ttk.Treeview(f3, columns=(
        "Employee ID", "Name", "E Mail", "Department", "Contact", "Date of Birth", "PAN Details", "Aadhar Details",
        "Address"),
                           xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=details.xview)
    scroll_y.config(command=details.yview)
    details.heading("Employee ID", text="Employee ID")
    details.heading("Name", text="Name")
    details.heading("E Mail", text="Contact")
    details.heading("Department", text="E Mail")
    details.heading("Contact", text="Department")
    details.heading("Date of Birth", text="Date of Birth")
    details.heading("PAN Details", text="PAN Details")
    details.heading("Aadhar Details", text="Aadhar Details")
    details.heading("Address", text="Address")
    details['show'] = 'headings'
    details.column("Employee ID", width=100)
    details.column("Name", width=150)
    details.column("E Mail", width=150)
    details.column("Department", width=250)
    details.column("Contact", width=150)
    details.column("Date of Birth", width=100)
    details.column("PAN Details", width=150)
    details.column("Aadhar Details", width=150)
    details.column("Address", width=300)
    details.pack(fill=BOTH, expand=1)
    details.bind("<ButtonRelease-1>", get_cursor)
    fetch()

    f1.place(x=100, y=380)
    f2.place(x=100, y=100)
    f3.place(x=660, y=140, width=805, height=575)
    clock()

    root2.mainloop()


def Attendance():
    global root7
    def cleartime():
        current_time = time.strftime('%I:%M:%S %p')
        cc = current_time[9:]
        tt = int(current_time[0:1])
        if cc == "PM" and tt >= 7:
            con = pymysql.connect(host="localhost", user="root", password="", database="Attendance")
            cur = con.cursor()
            cur.execute("delete from Electronics")
            con.commit()
            con.close()

            con = pymysql.connect(host="localhost", user="root", password="", database="Attendance")
            cur = con.cursor()
            cur.execute("delete from Clothing")
            con.commit()
            con.close()

            con = pymysql.connect(host="localhost", user="root", password="", database="Attendance")
            cur = con.cursor()
            cur.execute("delete from Furniture")
            con.commit()
            con.close()

    def clock():
        try:
            current_time = time.strftime('%I:%M:%S %p')
            Label(root, font=("Arial", 14), bg="#023E84", fg="white", text=current_time).place(x=600, y=570)
            root.after(200, clock)
        except:
            pass

    def fetch_total():
        con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
        cur = con.cursor()
        cur.execute("select * from edit_employee")
        rows = cur.fetchall()
        rowa = len(rows)
        print(rowa)
        Label(f1, text=rowa, bg="white", padx=45, pady=5, font=("Arial", 9)).grid(row=1, column=1, sticky="w")
        con.commit()
        con.close()

        con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
        cur = con.cursor()
        cur.execute("select * from edit_employee where department like '%Electronics%'")
        rows = cur.fetchall()
        rowb = len(rows)
        print(rowb)
        Label(f1, text=rowb, bg="white", padx=45, pady=5, font=("Arial", 9)).grid(row=7, column=1, sticky="w")
        con.commit()
        con.close()

        con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
        cur = con.cursor()
        cur.execute("select * from edit_employee where department like '%Furniture%'")
        rows = cur.fetchall()
        rowc = len(rows)
        print(rowc)
        Label(f1, text=rowc, bg="white", padx=45, pady=5, font=("Arial", 9)).grid(row=7, column=5, sticky="w")
        con.commit()
        con.close()

        con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
        cur = con.cursor()
        cur.execute("select * from edit_employee where department like '%Clothing%'")
        rows = cur.fetchall()
        rowd = len(rows)
        print(rowd)
        Label(f1, text=rowd, bg="white", padx=45, pady=5, font=("Arial", 9)).grid(row=7, column=3, sticky="w")
        con.commit()
        con.close()

        con = pymysql.connect(host="localhost", user="root", password="", database="Attendance")
        cur = con.cursor()
        cur.execute("select * from Electronics")
        rows = cur.fetchall()
        row1 = len(rows)
        print(row1)
        Label(f1, text=row1, bg="white", padx=45, pady=5, font=("Arial", 9)).grid(row=8, column=1, sticky="w")

        con.commit()
        con.close()

        con = pymysql.connect(host="localhost", user="root", password="", database="Attendance")
        cur = con.cursor()
        cur.execute("select * from Clothing")
        rows = cur.fetchall()
        row2 = len(rows)
        print(row2)
        Label(f1, text=row2, bg="white", padx=45, pady=5, font=("Arial", 9)).grid(row=8, column=5, sticky="w")
        con.commit()
        con.close()

        con = pymysql.connect(host="localhost", user="root", password="", database="Attendance")
        cur = con.cursor()
        cur.execute("select * from Furniture")
        rows = cur.fetchall()
        row3 = len(rows)
        print(row3)
        Label(f1, text=row3, padx=45, pady=5, bg="white", font=("Arial", 9)).grid(row=8, column=3, sticky="w")
        con.commit()
        con.close()

        total = row1 + row2 + row3
        Label(f1, text=total, padx=45, pady=5, bg="white", font=("Arial", 9)).grid(row=2, column=1, sticky="w")

        Label(f1, text=(rowa - total), bg="white", padx=45, pady=5, font=("Arial", 9)).grid(row=3, column=1, sticky="w")
        Label(f1, text=(rowb - row1), bg="white", padx=45, pady=5, font=("Arial", 9)).grid(row=9, column=1, sticky="w")
        Label(f1, text=(rowd - row3), bg="white", padx=45, pady=5, font=("Arial", 9)).grid(row=9, column=3, sticky="w")
        Label(f1, text=(rowc - row2), bg="white", padx=45, pady=5, font=("Arial", 9)).grid(row=9, column=5, sticky="w")

    root7 = Toplevel()
    root7.geometry("500x700")
    root7.maxsize(height=450, width=800)
    root7.minsize(height=450, width=800)
    root7.title("ATTENDACE DETAILS")

    # BACKGROUND
    background = Image.open("Images\YYYY.jpg")
    bg = ImageTk.PhotoImage(background)
    Label(root7, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    f1 = Frame(root7, bg="white", bd=5)

    # LABEL
    Label(f1, text="TOTAL", fg="#041B50", bg="white", padx=5, pady=5,
          font=("Comic Sans MS", 11, "bold", "underline")).grid(row=0, column=0, columnspan=2)
    Label(f1, text="Total Employees", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=1, column=0, sticky="w")
    Label(f1, text="Present", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=2, column=0, sticky="w")
    Label(f1, text="Absent", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=3, column=0, sticky="w")

    Label(f1, bg="white", padx=5, pady=5, font=("Arial", 9)).grid(row=5, column=0, sticky="w")

    Label(f1, text="ELECTRONICS DEPARTMENT", bg="white", fg="#041B50", padx=15, pady=15,
          font=("Comic Sans MS", 11, "bold", "underline")).grid(row=6, column=0, columnspan=2)
    Label(f1, text="Total Employees", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=7, column=0, sticky="w")
    Label(f1, text="Present", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=8, column=0, sticky="w")
    Label(f1, text="Absent", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=9, column=0, sticky="w")

    Label(f1, text="FURNITURE DEPARTMENT", fg="#041B50", bg="white", padx=15, pady=15,
          font=("Comic Sans MS", 11, "bold", "underline")).grid(row=6, column=2, columnspan=2)
    Label(f1, text="Total Employees", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=7, column=2, sticky="w")
    Label(f1, text="Present", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=8, column=2, sticky="w")
    Label(f1, text="Absent", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=9, column=2, sticky="w")

    Label(f1, text="CLOTHING DEPARTMENT", fg="#041B50", bg="white", padx=15, pady=15,
          font=("Comic Sans MS", 11, "bold", "underline")).grid(row=6, column=4, columnspan=2)
    Label(f1, text="Total Employees", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=7, column=4, sticky="w")
    Label(f1, text="Present", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=8, column=4, sticky="w")
    Label(f1, text="Absent", bg="white", padx=15, pady=5, font=("Arial", 9)).grid(row=9, column=4, sticky="w")

    Button(root7, text="BACK", width=12, bg="#041B50", activeforeground="#041B50", activebackground="white", fg="white",
           font=("Arial", 10), bd=0, command=root7.destroy).place(x=70, y=360)
    fetch_total()
    cleartime()
    f1.place(x=20, y=20, height=380, width=750)
    clock()

    root7.mainloop()


def Furniture():
    global root5

    if u_name=="F":
        root.destroy()
    else:
        root1.destroy()

    def Mark_In():
        global current_time1
        current_time1 = time.strftime('%H %M')

    def Mark_Out():
        global j
        current_time = time.strftime('%H %M')
        con = pymysql.connect(host="localhost", user="root", password="", database="Attendance")
        cur = con.cursor()
        cur.execute("insert into Furniture values(%s,%s,%s,%s)", ("Furniture", current_time1, current_time, j))
        j = j + 1
        con.commit()
        con.close()

    def number_update():
        global i
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
            cur = con.cursor()
            cur.execute("select uniquecode from billingfurniture")
            row = cur.fetchmany(9)
            length = max(row)
            i = length[0] + 1
        except:
            i=1

    def Add_item():
        number_update()
        global i
        global k
        if (Order_ID.get() == "" or
                Customer_Name.get() == "" or
                Order_Date.get() == "" or
                Sub_Category.get() == "" or
                Price.get() == "" or
                Quantity.get() == ""):
            tmsg.showinfo("ERROR", "All fields are mandatory")

        else:
            try:
                print(2/Price.get())
                print(2/Quantity.get())
                con_MRP = pymysql.connect(host="localhost", user="root", password="", database="purchase")
                cur_MRP = con_MRP.cursor()
                cur_MRP.execute(
                    "select price from purchase_bill where Productname LIKE '%" + str(Sub_Category.get() + "%'"))
                rows = cur_MRP.fetchone()
                MRP = rows

                Total = Quantity.get() * Price.get()
                print(Quantity.get())
                print(Total)
                print(MRP[0])
                Profit = Total - Quantity.get() * int(MRP[0])

                con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
                cur = con.cursor()
                cur.execute("insert into billingfurniture values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Order_ID.get(),
                                                                                                   Customer_Name.get(),
                                                                                                   Order_Date.get(),
                                                                                                   "Electronics",
                                                                                                   Sub_Category.get(),
                                                                                                   Price.get(),
                                                                                                   Quantity.get(),
                                                                                                   Total,
                                                                                                   Profit,
                                                                                                   i))
                print(Profit)
                con.commit()
                i = i + 1
                fetch()
                con.close()

                con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
                cur = con.cursor()
                cur.execute("insert into overall values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Order_ID.get(),
                                                                                          Customer_Name.get(),
                                                                                          Order_Date.get(),
                                                                                          "Furniture",
                                                                                          Sub_Category.get(),
                                                                                          Price.get(),
                                                                                          Quantity.get(),
                                                                                          Total,
                                                                                          Profit,
                                                                                          k))

                print(Profit)
                con.commit()
                k = k + 1
                fetch()
                clear_display()
                con.close()
            except TypeError:
                tmsg.showinfo("ERROR", "Invalid Price or Quantity")

    def fetch():
        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        cur.execute("select * from billingfurniture")
        rows = cur.fetchmany(7)
        if len(rows) != 0:
            Edetails.delete(*Edetails.get_children())
            for x in rows:
                Edetails.insert('', END, value=x)
            con.commit()
        con.close()

    def Remove_item():
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="Productdetails")
            cur = con.cursor()
            cur.execute("delete from billingfurniture where uniquecode=%s", selection)
            con.commit()
            con.close()
            fetch()
        except:
            tmsg.showinfo("ERROR","Nothing selected to remove")

    def get_cursor(event):
        global selection
        cursor_row = Edetails.focus()
        contents = Edetails.item(cursor_row)
        row = contents['values']
        Order_ID.set(row[0])
        Customer_Name.set(row[1])
        Order_Date.set(row[2])
        Sub_Category.set(row[4])
        Quantity.set(row[6])
        Price.set(row[5])
        selection = row[9]

    def clear_display():
        Sub_Category.set("")
        Price.set("")
        Quantity.set("")

    def Submit():
        summ=0
        for Total in Edetails.get_children():
            summ=summ+Edetails.item(Total)["values"][7]
        tmsg.showinfo("CUSTOMER BILL","THANK YOU FOR COMING\nYour total is {}".format(summ))

        Order_ID.set("")
        Customer_Name.set("")
        Order_Date.set("")
        Edetails.delete(*Edetails.get_children())
        clear_display()

    def Employee_Logout():
        if u_name=="F":
            root5.destroy()
            main_window()
        else:
            root5.destroy()
            Sign_up_interior()


    def clock():
        try:
            current_time = time.strftime('%I:%M:%S %p')
            Label(root, font=("Arial", 14), bg="#023E84", fg="white", text=current_time).place(x=600, y=570)
            root.after(200, clock)
        except:
            pass

    root5 = Tk()
    root5.geometry("1520x800")
    root5.maxsize(width=1520, height=800)
    root5.minsize(width=1520, height=800)
    root5.title("FURNITURE SECION")

    # IMAGES
    background = Image.open("Images\\furniture_dept_3D.jpg")
    bg = ImageTk.PhotoImage(background)

    # BACKGROUND
    Label(root5, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    Label(root5, text="FURNITURE SECTION", font=("Comic Sans MS", 32, "bold"), fg="#0A2C61", bg="white").place(x=0,
                                                                                                               y=5,
                                                                                                               relwidth=1)

    # FRAME
    f1 = Frame(root5, bg="white", bd=0, width=450, height=200)
    f2 = Frame(root5, bg="white", bd=0, width=450, height=300)
    f3 = Frame(root5, bg="white", bd=5)

    # LABELS
    Label(f1, text="CUSTOMER DETAILS", bg="white", font=("Arial,18")).place(x=120, y=10)
    Label(f2, text="PRODUCT DETAILS", bg="white", font=("Arial,18")).place(x=120, y=20)
    product_id = Label(f1, text="◼ ORDER ID", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=70)
    product_type = Label(f1, text="◼ CUSTOMER NAME", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=110)
    product_name = Label(f1, text="◼ ORDER DATE", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=150)
    category = Label(f2, text="◼ CATEGORY", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=70)
    sub_category = Label(f2, text="◼ SUB CATEGORY", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=110)
    price = Label(f2, text="◼ PRICE (per unit)", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=150)
    quantity = Label(f2, text="◼ QUANTITY", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=190)
    order_details = Label(f3, text="ORDER DETAILS", font=("Arial", 14), bg="#041B50", fg="white").pack(fill=X)
    section = Label(f2, width=20, text="Furniture", bg="white", font=("Arial", 11)).place(x=220, y=70)
    Label(root5, text="FURNITURE SECTION", bg="white", fg="#041B50", font=("Arial", 16, "bold", "underline")).place(
        x=290,
        y=560)

    # TEXTVARIABLES
    Order_ID = StringVar()
    Customer_Name = StringVar()
    Order_Date = StringVar()
    Sub_Category = StringVar()
    Price = IntVar()
    Quantity = IntVar()

    # ENTRY WIDGETS
    Entry(f1, width=25, font=("Arial", 11), textvariable=Order_ID).place(x=220, y=70)
    Entry(f1, width=25, font=("Arial", 11), textvariable=Customer_Name).place(x=220, y=110)
    Entry(f1, width=25, font=("Arial", 11), textvariable=Order_Date).place(x=220, y=150)
    Entry(f2, width=25, font=("Arial", 11), textvariable=Sub_Category).place(x=220, y=110)
    Entry(f2, width=25, font=("Arial", 11), textvariable=Price).place(x=220, y=150)
    Entry(f2, width=25, font=("Arial", 11), textvariable=Quantity).place(x=220, y=190)

    # TREEVIEW
    scroll_x = Scrollbar(f3, orient=HORIZONTAL)
    scroll_y = Scrollbar(f3, orient=VERTICAL)
    Edetails = ttk.Treeview(f3, columns=(
        "Order ID", "Name", "Order date", "Category", "Product", "Quantity", "Price per Unit", "Total"),
                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=Edetails.xview)
    scroll_y.config(command=Edetails.yview)
    Edetails.heading("Order ID", text="Order ID")
    Edetails.heading("Name", text="Name")
    Edetails.heading("Order date", text="Order date")
    Edetails.heading("Category", text="Category")
    Edetails.heading("Product", text="Product")
    Edetails.heading("Price per Unit", text="Price per Unit")
    Edetails.heading("Quantity", text="Quantity")
    Edetails.heading("Total", text="Total")
    Edetails['show'] = 'headings'
    Edetails.column("Order ID", width=100)
    Edetails.column("Name", width=150)
    Edetails.column("Order date", width=100)
    Edetails.column("Category", width=200)
    Edetails.column("Product", width=200)
    Edetails.column("Price per Unit", width=100)
    Edetails.column("Quantity", width=100)
    Edetails.column("Total", width=100)
    Edetails.pack(fill=BOTH, expand=1)
    Edetails.bind("<ButtonRelease-1>", get_cursor)
    fetch()

    # BUTTON
    b1 = Button(f2, text="ADD ITEM", font=("Arial", 10), bg="white", command=Add_item).place(x=200, y=240)
    b12 = Button(root5, text="SHOW ALL", width=16, activebackground="#041B50", activeforeground="white",
                 font=("Arial", 14, "bold"), bg="white", command=fetch).place(x=1245, y=608)
    b2 = Button(root5, text="SUBMIT", width=16, activebackground="#041B50", activeforeground="white",
                font=("Arial", 14, "bold"), bg="white", command=Submit).place(x=1040, y=608)
    b3 = Button(f2, text="REMOVE ITEM", font=("Arial", 10), bg="white", command=Remove_item).place(x=300, y=240)
    b4 = Button(root5, text="MARK IN TIME", width=15, bg="#041B50", activeforeground="#041B50",
                activebackground="white",
                fg="white", font=("Arial", 12, "bold"), command=Mark_In).place(x=310, y=605)
    b5 = Button(root5, text="MARK OUT TIME", width=15, bg="#041B50", activeforeground="#041B50",
                activebackground="white",
                fg="white", font=("Arial", 12, "bold"), command=Mark_Out).place(x=310, y=645)
    b6 = Button(root5, text="EMPLOYEE LOGOUT", width=32, bg="white", fg="#041B50", activebackground="#041B50",
                activeforeground="white", font=("Arial", 14, "bold"), command=Employee_Logout).place(x=110, y=710)
    f1.place(x=580, y=130)
    f2.place(x=580, y=340)
    f3.place(x=1040, y=130, width=405, height=465)

    clock()

    root5.mainloop()


def Clothing():
    global root4
    if u_name == "C":
        root.destroy()
    else:
        root1.destroy()

    def Mark_In():
        global current_time1
        current_time1 = time.strftime('%H %M')

    def Mark_Out():
        global j
        current_time = time.strftime('%H %M')
        con = pymysql.connect(host="localhost", user="root", password="", database="Attendance")
        cur = con.cursor()
        cur.execute("insert into Furniture values(%s,%s,%s,%s)", ("Clothing", current_time1, current_time, j))
        j = j + 1
        con.commit()
        con.close()

    def number_update():
        global i
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
            cur = con.cursor()
            cur.execute("select uniquecode from billingclothing")
            row = cur.fetchmany(9)
            length = max(row)
            i = length[0] + 1
        except:
            i=1

    def Add_item():
        number_update()
        global i
        global k
        if (Order_ID.get() == "" or
                Customer_Name.get() == "" or
                Order_Date.get() == "" or
                Sub_Category.get() == "" or
                Price.get() == "" or
                Quantity.get() == ""):
            tmsg.showinfo("ERROR", "All fields are mandatory")

        else:
            try:
                print(2/Price.get())
                print(2/Quantity.get())
                con_MRP = pymysql.connect(host="localhost", user="root", password="", database="purchase")
                cur_MRP = con_MRP.cursor()
                cur_MRP.execute(
                    "select price from purchase_bill where Productname LIKE '%" + str(Sub_Category.get() + "%'"))
                rows = cur_MRP.fetchone()
                MRP = rows

                Total = Quantity.get() * Price.get()
                print(Quantity.get())
                print(Total)
                print(MRP[0])
                Profit = Total - Quantity.get() * int(MRP[0])

                con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
                cur = con.cursor()
                cur.execute("insert into billingclothing values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Order_ID.get(),
                                                                                                  Customer_Name.get(),
                                                                                                  Order_Date.get(),
                                                                                                  "Clothing",
                                                                                                  Sub_Category.get(),
                                                                                                  Price.get(),
                                                                                                  Quantity.get(),
                                                                                                  Total,
                                                                                                  Profit,
                                                                                                  i))

                print(Profit)
                con.commit()
                i = i + 1
                fetch()
                con.close()

                con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
                cur = con.cursor()
                cur.execute("insert into overall values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Order_ID.get(),
                                                                                          Customer_Name.get(),
                                                                                          Order_Date.get(),
                                                                                          "Cothing",
                                                                                          Sub_Category.get(),
                                                                                          Price.get(),
                                                                                          Quantity.get(),
                                                                                          Total,
                                                                                          Profit,
                                                                                          k))

                print(Profit)
                con.commit()
                k = k + 1
                fetch()
                clear_display()
                con.close()
            except TypeError:
                tmsg.showinfo("ERROR", "Invalid Price or Quantity")

    def fetch():
        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        cur.execute("select * from billingclothing")
        rows = cur.fetchmany(7)
        if len(rows) != 0:
            Edetails.delete(*Edetails.get_children())
            for x in rows:
                Edetails.insert('', END, value=x)
            con.commit()
        con.close()

    def Remove_item():
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="Productdetails")
            cur = con.cursor()
            cur.execute("delete from billingclothing where uniquecode=%s", selection)
            con.commit()
            con.close()
            fetch()
        except:
            tmsg.showinfo("ERROR","Nothing selected to Remove")

    def get_cursor(event):
        global selection
        cursor_row = Edetails.focus()
        contents = Edetails.item(cursor_row)
        row = contents['values']
        Order_ID.set(row[0])
        Customer_Name.set(row[1])
        Order_Date.set(row[2])
        Sub_Category.set(row[4])
        Quantity.set(row[6])
        Price.set(row[5])
        selection = row[9]

    def clear_display():
        Sub_Category.set("")
        Price.set("")
        Quantity.set("")

    def Submit():
        summ = 0
        for Total in Edetails.get_children():
            summ = summ + Edetails.item(Total)["values"][7]
        tmsg.showinfo("CUSTOMER BILL", "THANK YOU FOR COMING\nYour total is {}".format(summ))

        Order_ID.set("")
        Customer_Name.set("")
        Order_Date.set("")
        Edetails.delete(*Edetails.get_children())
        clear_display()

    def Employee_Logout():
        if u_name=="C":
            root4.destroy()
            main_window()
        else:
            root4.destroy()
            Sign_up_interior()


    def clock():
        try:
            current_time = time.strftime('%I:%M:%S %p')
            Label(root, font=("Arial", 14), bg="#023E84", fg="white", text=current_time).place(x=600, y=570)
            root.after(200, clock)
        except:
            pass

    root4 = Tk()
    root4.geometry("1520x800")
    root4.maxsize(width=1520, height=800)
    root4.minsize(width=1520, height=800)
    root4.title("CLOTHING SECION")

    # IMAGES
    background = Image.open("Images\clothing_dept_3D.jpg")
    bg = ImageTk.PhotoImage(background)

    # BACKGROUND
    Label(root4, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    Label(root4, text="CLOTHING SECTION", font=("Comic Sans MS", 32, "bold"), fg="#0A2C61", bg="white").place(x=0,
                                                                                                              y=5,
                                                                                                              relwidth=1)

    # FRAME
    f1 = Frame(root4, bg="white", bd=0, width=450, height=200)
    f2 = Frame(root4, bg="white", bd=0, width=450, height=300)
    f3 = Frame(root4, bg="white", bd=5)

    # LABELS
    Label(f1, text="CUSTOMER DETAILS", bg="white", font=("Arial,18")).place(x=120, y=10)
    Label(f2, text="PRODUCT DETAILS", bg="white", font=("Arial,18")).place(x=120, y=20)
    product_id = Label(f1, text="◼ ORDER ID", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=70)
    product_type = Label(f1, text="◼ CUSTOMER NAME", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=110)
    product_name = Label(f1, text="◼ ORDER DATE", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=150)
    category = Label(f2, text="◼ CATEGORY", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=70)
    sub_category = Label(f2, text="◼ SUB CATEGORY", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=110)
    price = Label(f2, text="◼ PRICE (per unit)", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=150)
    quantity = Label(f2, text="◼ QUANTITY", bg="white", fg="black", font=("Arial", 11)).place(x=30, y=190)
    order_details = Label(f3, text="ORDER DETAILS", font=("Arial", 14), bg="#041B50", fg="white").pack(fill=X)
    section = Label(f2, width=20, text="Clothing", bg="white", font=("Arial", 11)).place(x=220, y=70)
    Label(root4, text="CLOTHING SECTION", bg="white", fg="#041B50", font=("Arial", 16, "bold", "underline")).place(
        x=290, y=560)

    # TEXTVARIABLES
    Order_ID = StringVar()
    Customer_Name = StringVar()
    Order_Date = StringVar()
    Sub_Category = StringVar()
    Price = IntVar()
    Quantity = IntVar()

    # ENTRY WIDGETS
    Entry(f1, width=25, font=("Arial", 11), textvariable=Order_ID).place(x=220, y=70)
    Entry(f1, width=25, font=("Arial", 11), textvariable=Customer_Name).place(x=220, y=110)
    Entry(f1, width=25, font=("Arial", 11), textvariable=Order_Date).place(x=220, y=150)
    Entry(f2, width=25, font=("Arial", 11), textvariable=Sub_Category).place(x=220, y=110)
    Entry(f2, width=25, font=("Arial", 11), textvariable=Price).place(x=220, y=150)
    Entry(f2, width=25, font=("Arial", 11), textvariable=Quantity).place(x=220, y=190)

    # TREEVIEW
    scroll_x = Scrollbar(f3, orient=HORIZONTAL)
    scroll_y = Scrollbar(f3, orient=VERTICAL)
    Edetails = ttk.Treeview(f3, columns=(
        "Order ID", "Name", "Order date", "Category", "Product", "Quantity", "Price per Unit", "Total"),
                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=Edetails.xview)
    scroll_y.config(command=Edetails.yview)
    Edetails.heading("Order ID", text="Order ID")
    Edetails.heading("Name", text="Name")
    Edetails.heading("Order date", text="Order date")
    Edetails.heading("Category", text="Category")
    Edetails.heading("Product", text="Product")
    Edetails.heading("Price per Unit", text="Price per Unit")
    Edetails.heading("Quantity", text="Quantity")
    Edetails.heading("Total", text="Total")
    Edetails['show'] = 'headings'
    Edetails.column("Order ID", width=100)
    Edetails.column("Name", width=150)
    Edetails.column("Order date", width=100)
    Edetails.column("Category", width=200)
    Edetails.column("Product", width=200)
    Edetails.column("Price per Unit", width=100)
    Edetails.column("Quantity", width=100)
    Edetails.column("Total", width=100)
    Edetails.pack(fill=BOTH, expand=1)
    Edetails.bind("<ButtonRelease-1>", get_cursor)
    fetch()

    # BUTTON
    b1 = Button(f2, text="ADD ITEM", font=("Arial", 10), bg="white", command=Add_item).place(x=200, y=240)
    b12 = Button(root4, text="SHOW ALL", width=16, activebackground="#041B50", activeforeground="white",
                 font=("Arial", 14, "bold"), bg="white", command=fetch).place(x=1245, y=608)
    b2 = Button(root4, text="SUBMIT", width=16, activebackground="#041B50", activeforeground="white",
                font=("Arial", 14, "bold"), bg="white", command=Submit).place(x=1040, y=608)
    b3 = Button(f2, text="REMOVE ITEM", font=("Arial", 10), bg="white", command=Remove_item).place(x=300, y=240)
    b4 = Button(root4, text="MARK IN TIME", width=15, bg="#041B50", activeforeground="#041B50",
                activebackground="white", fg="white", font=("Arial", 12, "bold"), command=Mark_In).place(x=310,
                                                                                                         y=605)
    b5 = Button(root4, text="MARK OUT TIME", width=15, bg="#041B50", activeforeground="#041B50",
                activebackground="white", fg="white", font=("Arial", 12, "bold"), command=Mark_Out).place(x=310,
                                                                                                          y=645)
    b6 = Button(root4, text="EMPLOYEE LOGOUT", width=29, fg="#041B50", activebackground="#041B50",
                activeforeground="white", bg="white", font=("Arial", 14, "bold"), command=Employee_Logout).place(
        x=110, y=710)
    f1.place(x=580, y=130)
    f2.place(x=580, y=340)
    f3.place(x=1040, y=130, width=405, height=465)

    clock()

    root4.mainloop()


def Sales():
    global root6
    root1.destroy()

    def clock():
        try:
            current_time = time.strftime('%I:%M:%S %p')
            Label(root, font=("Arial", 14), bg="#023E84", fg="white", text=current_time).place(x=600, y=570)
            root.after(200, clock)
        except:
            pass

    def Employee_Logout():
        root6.destroy()
        Sign_up_interior()

    def Add():
        if (ID.get() == "" or
                Name.get() == ""):
            tmsg.showinfo("ERROR", "All fields are mandatory")

        else:
            try:
                print(2/eval( Name.get()))
                con = pymysql.connect(host="localhost", user="root", password="", database="purchase")
                cur = con.cursor()
                cur.execute("insert into purchase_bill values(%s,%s)", (ID.get(), Name.get()))
                con.commit()
                con.close()
                fetch1()
            except TypeError:
                tmsg.showinfo("ERROR", "Invalid Price Entered")
                fetch1()

    def fetch1():
        con = pymysql.connect(host="localhost", user="root", password="", database="purchase")
        cur = con.cursor()
        cur.execute("select * from purchase_bill")
        rows = cur.fetchall()
        if len(rows) != 0:
            details.delete(*details.get_children())
            for x in rows:
                details.insert('', END, value=x)
            con.commit()
        con.close()

    def fetch2():
        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        cur.execute("select * from overall")
        rows = cur.fetchall()
        if len(rows) != 0:
            Edetails.delete(*Edetails.get_children())
            for x in rows:
                Edetails.insert('', END, value=x)
            con.commit()
        con.close()

    def clear_display():
        ID.set("")
        Name.set("")

    def Remove():
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="purchase")
            cur = con.cursor()
            cur.execute("delete from purchase_bill where productname=%s", ID.get())
            con.commit()
            con.close()
            clear_display()
            fetch1()
        except:
            tmsg.showinfo("ERROR","Nothing seleted to Remove")

    def get_cursor(event):
        cursor_row = details.focus()
        contents = details.item(cursor_row)
        row = contents['values']
        ID.set(row[0])
        Name.set(row[1])

    def get_profit():
        prof = 0
        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        cur.execute("select profit from overall")
        over = cur.fetchall()
        print(list(over))
        for x in over:
            prof = prof + x[0]
        Department.set(prof)

        prof = 0
        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        cur.execute("select profit from billing")
        over = cur.fetchall()
        print(list(over))
        for x in over:
            prof = prof + x[0]
        PAN_Card_Number.set(prof)

        prof = 0
        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        cur.execute("select profit from billingfurniture")
        over = cur.fetchall()
        print(list(over))
        for x in over:
            prof = prof + x[0]
        Aadhar_Card_Number.set(prof)

        prof = 0

        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        cur.execute("select profit from billing clothing")
        over = cur.fetchall()
        print(list(over))
        for x in over:
            prof = prof + x[0]
        Date_of_Birth.set(prof)

    root6 = Tk()
    root6.geometry("1520x800")
    root6.maxsize(width=1520, height=800)
    root6.minsize(width=1520, height=800)
    root6.title("FINANCE SECTION")
    background = Image.open("Images\YYYY_finane.jpg")
    bg = ImageTk.PhotoImage(background)
    Label(root6, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    # FRAMES
    f1 = Frame(root6, bg="white", bd=0, width=500, height=335)
    f2 = Frame(root6, bg="white", bd=5, width=500, height=235)
    f3 = Frame(root6, bg="white", bd=5)
    f4 = Frame(root6, bg="white", bd=5)

    # VARIABLES
    ID = StringVar()
    Name = StringVar()
    Contact_number = StringVar()
    E_Mail_ID = StringVar()
    Department = StringVar()
    Date_of_Birth = StringVar()
    PAN_Card_Number = StringVar()
    Aadhar_Card_Number = StringVar()

    # ENTRY
    E1 = Entry(f2, width=28, font=("Arial", 12), textvariable=ID)
    E1.place(x=210, y=80)
    E2 = Entry(f2, width=28, font=("Arial", 12), textvariable=Name)
    E2.place(x=210, y=130)
    E5 = Entry(f1, width=28, font=("Arial", 12), textvariable=Department)
    E5.place(x=210, y=70)
    E7 = Entry(f1, width=28, font=("Arial", 12), textvariable=PAN_Card_Number)
    E7.place(x=210, y=170)
    E8 = Entry(f1, width=28, font=("Arial", 12), textvariable=Aadhar_Card_Number)
    E8.place(x=210, y=220)
    E9 = Entry(f1, width=28, font=("Arial", 12), textvariable=Date_of_Birth)
    E9.place(x=210, y=270)

    # LABELS
    Label(root6, text="SALES AND FINANCE SECTION", font=("Comic Sans MS", 32, "bold"), fg="#0A2C61",
          bg="white").place(x=0, y=5, relwidth=1)
    Label(f2, text="PRODUCT DETAILS", font=("Arial", 16, "bold", "underline"), bg="white", fg="#041B50").place(
        x=150, y=25)
    Label(f1, text="REVENUE STATUS", font=("Arial", 16, "bold", "underline"), bg="white", fg="#041B50").place(
        x=150, y=25)
    Label(f2, text=" Product Name", font=("Arial", 12), bg="white").place(x=30, y=80)
    Label(f2, text=" Price", font=("Arial", 12), bg="white").place(x=30, y=130)
    Label(f1, text=" Overall Revenue Status", font=("Arial", 10), bg="white").place(x=30, y=70)
    Label(f1, text=" DEPARTMENT-WISE REVENUE", font=("Arial", 12), bg="white").place(x=120, y=130)
    Label(f1, text=" Electronics", font=("Arial", 10), bg="white").place(x=30, y=170)
    Label(f1, text=" Furniture", font=("Arial", 10), bg="white").place(x=30, y=220)
    Label(f1, text=" Clothing ", font=("Arial", 10), bg="white").place(x=30, y=270)
    Label(f4, text=" PRODUCT PURCHASED ", font=("Arial", 16, "bold"), bg="#041B50", fg="white").pack(fill=X)
    Label(f3, text=" OVERALL ORDER DETAILS ", font=("Arial", 16, "bold"), bg="#041B50", fg="white").pack(fill=X)

    # BUTTONS
    b4 = Button(root6, text="ADD PRODUCT", width=15, bg="#041B50", activeforeground="#041B50",
                activebackground="white",
                fg="white", font=("Arial", 11, "bold"), bd=0, command=Add).place(x=680, y=280)
    b3 = Button(f4, text="REMOVE ITEM", font=("Arial", 10), bg="white", command=Remove).pack(side=BOTTOM)
    b6 = Button(root6, text="EMPLOYEE LOGOUT", width=20, bg="white", fg="#041B50", activebackground="#041B50",
                activeforeground="white", font=("Arial", 14, "bold"), command=Employee_Logout).place(x=70, y=600)

    # TREEVIEW
    scroll_x = Scrollbar(f4, orient=HORIZONTAL)
    scroll_y = Scrollbar(f4, orient=VERTICAL)
    details = ttk.Treeview(f4, columns=("Product Name", "Price"),
                           xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=details.xview)
    scroll_y.config(command=details.yview)
    details.heading("Product Name", text="Product Name")
    details.heading("Price", text="Price")
    details['show'] = 'headings'
    details.column("Product Name", width=150)
    details.column("Price", width=50)
    details.pack(fill=BOTH, expand=1)

    details.bind("<ButtonRelease-1>", get_cursor)
    fetch1()

    # TREEVIEW
    scroll_x = Scrollbar(f3, orient=HORIZONTAL)
    scroll_y = Scrollbar(f3, orient=VERTICAL)
    Edetails = ttk.Treeview(f3, columns=(
        "Order ID", "Name", "Order date", "Category", "Product", "Quantity", "Price per Unit", "Total", "Profit"),
                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=Edetails.xview)
    scroll_y.config(command=Edetails.yview)
    Edetails.heading("Order ID", text="Order ID")
    Edetails.heading("Name", text="Name")
    Edetails.heading("Order date", text="Order date")
    Edetails.heading("Category", text="Category")
    Edetails.heading("Product", text="Product")
    Edetails.heading("Price per Unit", text="Price per Unit")
    Edetails.heading("Quantity", text="Quantity")
    Edetails.heading("Total", text="Total")
    Edetails.heading("Profit", text="Profit")
    Edetails['show'] = 'headings'
    Edetails.column("Order ID", width=100)
    Edetails.column("Name", width=150)
    Edetails.column("Order date", width=100)
    Edetails.column("Category", width=200)
    Edetails.column("Product", width=200)
    Edetails.column("Price per Unit", width=100)
    Edetails.column("Quantity", width=100)
    Edetails.column("Total", width=100)
    Edetails.column("Profit", width=100)
    Edetails.pack(fill=BOTH, expand=1)
    fetch2()
    # Edetails.bind("<ButtonRelease-1>",get_cursor)

    f1.place(x=420, y=355)
    f2.place(x=420, y=100)
    f3.place(x=935, y=355, width=500, height=335)
    f4.place(x=935, y=100, width=500, height=235)
    get_profit()
    clock()
    root6.mainloop()


def Sales_Analysis():
    root1.destroy()
    def clock():
        try:
            current_time = time.strftime('%I:%M:%S %p')
            Label(root, font=("Arial", 14), bg="#023E84", fg="white", text=current_time).place(x=600, y=570)
            root.after(200, clock)
        except:
            pass

    def get_weekday(dt):
        return dt.weekday()

    def get_dom(dt):
        return dt.day

    df = pd.read_csv("dataset for pandas\datasets_615631_1100614_List of Orders.csv")
    df1 = pd.read_csv("dataset for pandas\datasets_615631_1100614_Order Details.csv")
    df2 = pd.read_csv("dataset for pandas\datasets_615631_1100614_Sales target.csv")
    # print(c)
    df['Order Date'] = df['Order Date'].map(pd.to_datetime)
    df['dom'] = df['Order Date'].map(get_dom)

    df['weekday'] = df['Order Date'].map(get_weekday)
    c = df.head(20)

    def weekday_analysis():
        try:
            plt.close()
        except:
            pass
        plt.hist(df.weekday, bins=7, rwidth=0.6, range=(0, 7.5))
        plt.title(
            "Frequency of Customer purchasing product from \noutlet on different days of week :\n April 2019 - March 2020")
        plt.xlabel("DAY OF WEEK")
        plt.ylabel("Frequency of customer")
        plt.show()


    def dom_analysis():

        try:
            plt.close()
        except:
            pass

        plt.hist(df.dom, bins=30, rwidth=0.6, range=(0.5, 30.5))
        plt.title(
            "Frequency of Customer purchasing product from \noutlet on different days month :\n April 2019 - March 2020")
        plt.xlabel("DAY OF MONTH")
        plt.ylabel("Frequency of customer")
        plt.show()

    def dept_analysis():
        sum = 0
        item_value = []
        items = []

        print(df1['Sub-Category'])
        x_axis = list(set(df1['Category']))
        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        for x in x_axis:
            cur.execute("select Profit from overall where category like '%" + x + "%'")
            rows = cur.fetchall()
            for y in rows:
                item_value.append(x)
                items.append(y)
                sum = sum + rows[0][0]

        con.commit()
        con.close()
        plt.title("Average revenue generated over one year")
        plt.scatter(items, item_value, label="circle", color="red", marker="o", s=40)
        plt.grid(color="red")
        plt.show()

    def profit_analysis():

        try:
            plt.close()
        except:
            pass

        sum = 0
        item_value = []
        items = []

        print(df1['Sub-Category'])
        x_axis = list(set(df1['Sub-Category']))
        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        for x in x_axis:
            cur.execute("select Profit from overall where Subcategory like '%" + x + "%'")
            rows = cur.fetchall()
            for y in rows:
                item_value.append(x)
                items.append(y)
                sum = sum + rows[0][0]

        con.commit()
        con.close()
        plt.title("Average revenue generated over one year")
        plt.scatter(items, item_value, label="circle", color="red", marker="o", s=40)
        plt.grid(color="red")
        plt.show()

    def overall_revenue():

        try:
            plt.close()
        except:
            pass

        item_value = []

        print(df1['Sub-Category'])
        x_axis = list(set(df1['Sub-Category']))
        con = pymysql.connect(host="localhost", user="root", password="", database="productdetails")
        cur = con.cursor()
        for x in x_axis:
            sum = 0
            cur.execute("select Profit from overall where Subcategory like '%" + x + "%'")
            rows = cur.fetchall()
            for y in rows:
                sum = sum + rows[0][0]
            item_value.append(sum)
        con.commit()
        con.close()
        plt.title("Average revenue generated by product \nover one year")
        plt.plot(item_value, x_axis, linewidth=3, color="red", marker="o", markersize=8)
        plt.grid(color="green")
        plt.show()

    def BACK():
        root8.destroy()
        plt.close()
        Sign_up_interior()

    root8 = Tk()
    root8.geometry("1520x820")
    root8.maxsize(width=1520, height=820)
    root8.minsize(width=1520, height=820)
    root8.title("SALES ANALYSIS")
    background = Image.open("Images\YYYY_sales_analysis.jpg")
    bg = ImageTk.PhotoImage(background)
    Label(root8, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    f1 = Frame(root8, bg="white", bd=0)
    Label(root8, text="SALES ANALYSIS", font=("Comic Sans MS", 32, "bold"), fg="#0A2C61", bg="white").place(x=0, y=5,
                                                                                                            relwidth=1)

    Button(f1, text="SALES ANALYSIS OF THE COMPANY", font=("Arial", 19, "bold", "underline"), bg="white", fg="#041B50",
           bd=0).place(
        x=20, y=25)
    Button(f1, text=" WEEK-DAY ANALYSIS", width=33, bg="#041B50", fg="white", font=("Arial", 16, "bold"), bd=0,
           command=weekday_analysis).place(x=30, y=100)

    Button(f1, text=" MONTHLY ANALYSIS", width=33, bg="#041B50", fg="white", font=("Arial", 16, "bold"), bd=0,
           command=dom_analysis).place(x=30, y=180)

    Button(f1, text=" PRODUCT RELATED SALES ANALYSIS", width=33, bg="#041B50", fg="white", font=("Arial", 16, "bold"),
           bd=0, command=profit_analysis).place(x=30, y=260)

    Button(f1, text=" OVERALL SALES ANALYSIS", width=33, bg="#041B50", fg="white", font=("Arial", 16, "bold"), bd=0,
           command=overall_revenue).place(x=30, y=340)

    Button(f1, text=" BACK ", width=20, bg="#041B50", fg="white", font=("Arial", 14, "bold"), bd=0,
           command=BACK).place(x=130, y=520)

    Label(root8, text="", font=("Comic Sans MS", 32, "bold"), fg="#0A2C61", bg="white").place(x=0, y=710,
                                                                                              relwidth=1)

    clock()

    f1.place(x=900, y=100, width=500, height=600)
    root8.mainloop()


def Sign_up_interior():
    global root1
    try:
        root.destroy()
    except:
        pass

    try:
        root2.destroy()
    except:
        pass

    try:
        root3.destroy()
    except:
        pass

    try:
        root4.destroy()
    except:
        pass

    try:
        root5.destroy()
    except:
        pass

    try:
        root6.destroy()
    except:
        pass

    try:
        root7.destroy()
    except:
        pass


    def Login_Window():

        root1.destroy()
        main_window()


    def Send():
        t.delete('1.0', END)

    def clock():
        try:
            current_time = time.strftime('%I:%M:%S %p')
            Label(root, font=("Arial", 14), bg="#023E84", fg="white", text=current_time).place(x=600, y=570)
            root.after(200, clock)
        except:
            pass

    root1 = Tk()
    root1.geometry("1520x820")
    root1.maxsize(width=1520, height=820)
    root1.minsize(width=1520, height=820)
    root1.title("ADMIN")

    # IMAGES
    background = Image.open("Images\YYYY.jpg")
    bg = ImageTk.PhotoImage(background)
    employee = Image.open("Images\employee.png")
    employee_image = ImageTk.PhotoImage(employee)
    dept = Image.open("Images\dept.jpg")
    dept_img = ImageTk.PhotoImage(dept)
    sales = Image.open("Images\sales.png")
    sales_img = ImageTk.PhotoImage(sales)
    info = Image.open("Images\information-icon-new[1].jpg")
    info_img = ImageTk.PhotoImage(info)

    # BACKGROUND
    Label(root1, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    # FRAME
    f = Frame(root1, bg="white", bd=5)

    # CANVAS
    c1 = Canvas(root1, width=270, height=430, bg="white").place(x=45, y=150)
    Canvas(root1, width=270, height=430, bg="white").place(x=355, y=150)
    Canvas(root1, width=270, height=430, bg="white").place(x=667, y=150)
    Canvas(root1, width=270, height=430, bg="white").place(x=1165, y=150)

    # c1.create_image(100,100,anchor=NW,image=bg)

    # HEADING
    Label(root1, text="MANAGEMENT SYSTEM", bg="white", fg="#041B50", font=("Comic Sans MS", 28, "bold")).place(x=0, y=5,
                                                                                                               relwidth=1)

    #   #FOOTER
    #  Label(root1,text="Number of employees = 100",bg="white",fg="black",font=("Arial",12)).place(x=45,y=650)

    # EMPLOYEE SECTION
    Label(root1, image=employee_image, bg="white").place(x=155, y=170)
    Label(root1, text="EMPLOYEE SECTION", pady=5, fg="#0A2C61", bg="white", borderwidth=0,
          font=("Comic Sans MS", 18, "bold", "underline")).place(x=55, y=250)
    b1 = Button(root1, text="EDIT EMPLOYEE\nDETAILS", padx=5, pady=5, width=18, bg="#0A2C61", fg="white", borderwidth=0,
                font=("Arial", 14, "bold"), command=Add_Employee).place(x=65, y=380)
    b2 = Button(root1, text="ATTENDANCE\nDETAILS", padx=5, pady=5, width=18, bg="#0A2C61", fg="white", borderwidth=0,
                font=("Arial", 14, "bold"), command=Attendance)
    b2.place(x=65, y=470)
    # b2.bind("<Button-1>",Remove_Employee)
    # b3=Button(root1, text="ATTENDANCE", padx=5, pady=5,width=18,bg="#0A2C61",fg="white",borderwidth=0,font=("Arial",14,"bold"))
    # b3.place(x=65,y=520)

    # SUB-SECTION DATA
    Label(root1, image=dept_img, bg="white").place(x=465, y=170)
    Label(root1, text="SUB-SECTION DATA", pady=5, fg="#0A2C61", bg="white", borderwidth=0,
          font=("Comic Sans MS", 18, "bold", "underline")).place(x=362, y=250)
    Button(root1, text="ELECTRONICS", padx=5, pady=5, width=18, bg="#0A2C61", fg="white", borderwidth=0,
           font=("Arial", 14, "bold"), command=Electronics).place(x=375, y=360)
    Button(root1, text="CLOTHING", padx=5, pady=5, width=18, bg="#0A2C61", fg="white", borderwidth=0,
           font=("Arial", 14, "bold"), command=Clothing).place(x=375, y=440)
    Button(root1, text="FURNITURE", padx=5, pady=5, width=18, bg="#0A2C61", fg="white", borderwidth=0,
           font=("Arial", 14, "bold"), command=Furniture).place(x=375, y=520)

    # REVENUE SECTION
    Label(root1, image=sales_img, bg="white").place(x=767, y=170)
    Label(root1, text="REVENUE STATUS", pady=5, fg="#0A2C61", bg="white", borderwidth=0,
          font=("Comic Sans MS", 18, "bold", "underline")).place(x=685, y=250)
    Button(root1, text="PURCHASE AND \nSALES STATUS", padx=5, pady=5, width=18, bg="#0A2C61", fg="white", borderwidth=0,
           font=("Arial", 14, "bold"), command=Sales).place(x=685, y=380)
    # Button(root1, text="SELL STATUS", padx=5, pady=5, width=18,bg="#0A2C61",fg="white",borderwidth=0,font=("Arial",14,"bold")).place(x=685, y=440)
    Button(root1, text="SALES \nANALYSIS", padx=5, pady=5, width=18, bg="#0A2C61", fg="white", borderwidth=0,
           font=("Arial", 14, "bold"), command=Sales_Analysis).place(x=685, y=470)

    # INFO WINDOW
    Label(root1, image=info_img, bg="white").place(x=1275, y=170)
    Label(root1, text="\nDEVELOPER DETAILS", padx=10, fg="#0A2C61", bg="white", borderwidth=0,
          font=("Comic Sans MS", 16, "bold", "underline")).place(x=1180, y=230)
    Label(root1, text="\nDELELOPED BY:\nBharat Pant\nbpant267@gmail.com"
                      "\n\n\nCOMPANY NAME:\nABCD Company\nabcd@gmail.com\n\n\n"
                      "CONTACT :\nXXXXXXX879\nXXXXXXX100\n", padx=10, fg="black", bg="white",
          borderwidth=0, font=("Arial", 10,)).place(x=1227, y=330)

    # TEXTBOX
    scroll_x = Scrollbar(f, orient=HORIZONTAL)
    scroll_y = Scrollbar(f, orient=VERTICAL)
    t = Text(f, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=t.xview)
    scroll_y.config(command=t.yview)
    t.pack(fill=BOTH, expand=1)

    bt = Button(root1, text="LOGOUT", padx=10, pady=5, width=10, bg="white", fg="#0A2C61", activebackground="#041B50",
                activeforeground="white", font=("Arial", 14, "bold"), borderwidth=0, command=Login_Window)
    bt.place(x=1290, y=650)
    bt = Button(root1, text="SEND", padx=10, width=10, bg="white", fg="#0A2C61", activebackground="#041B50",
                activeforeground="white", font=("Arial", 14, "bold"), borderwidth=0, command=Send)
    bt.place(x=795, y=705)

    f.place(x=50, y=600, height=100, width=890)
    clock()
    root1.mainloop()


def Check():
    global u_name

    con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
    cur = con.cursor()
    cur.execute("select * from login where LoginID LIKE '%" + str(username.get()) + "%'")
    row = cur.fetchone()
    print(row)
    row = row[0]
    u_name = row[0]
    print(u_name[0])
    username.set("")
    password.set("")
    if u_name[0] == "E":
        Electronics()
    elif u_name[0] == "C":
        Clothing()
    elif u_name[0] == "F":
        Furniture()
    else:
        print("Admin")
        Sign_up_interior()


def Sign_Up():
    con = pymysql.connect(host="localhost", user="root", password="", database="Employee")
    cur = con.cursor()
    cur.execute("select * from login where LoginID LIKE '%" + str(username.get()) + "%'")
    row = cur.fetchall()
    row = row[0]
    u_name = row[0]
    u_pass = row[1]
    if username.get() == u_name and password.get() == u_pass:
        Check()


    else:
        print("wrong pass")
        username.set("")
        password.set("")
        tmsg.showinfo("ERROR", "Incorrect Username or Password")
    con.commit()
    con.close()


def clock():
    try:
        current_time = time.strftime('%I:%M:%S %p')
        Label(root, font=("Arial", 14), bg="#023E84", fg="white", text=current_time).place(x=600, y=570)
        root.after(200, clock)
    except:
        pass


def main_window():
    global username
    global password
    global root

    root = Tk()
    root.title("LOGIN SYSTEM")
    root.geometry("740x650")
    root.maxsize(width=740, height=630)
    root.minsize(width=740, height=630)

    # BACKGROUND IMAGE
    background = Image.open("Images\login_page_3D.jpg")
    bg = ImageTk.PhotoImage(background)
    img_pass = Image.open("images\\130-1303682_security-password-2-icon-password-icon-in-png[1].png")
    pass_img = ImageTk.PhotoImage(img_pass)
    Label(root, image=bg).place(x=0, y=0, relheight=1, relwidth=1)
    img_log_in = Image.open("Images\\USER[1].png")
    log_img = ImageTk.PhotoImage(img_log_in)

    # VARIABLES
    username = StringVar()
    password = StringVar()

    # LABELS AND ENTRIES
    Label(root, image=log_img, padx=5, pady=5, bg="white").place(x=250, y=237)
    password_image = Label(root, image=pass_img, padx=5, pady=5, bg="white").place(x=250, y=290)
    blank4 = Label(root, text="Sales and Finance Management System\nDeveloped by: Bharat Pant\n E-mail:bpant267@gmail.com",
                   font=("Arial", 9), bg="#023E84", fg="white", padx=10, pady=10).place(x=260, y=545)
    login_entry = Entry(root, width=25, bg="white", font=("Arial", 13), bd=0, textvariable=username).place(x=285, y=237)
    password_entry = Entry(root, width=25, bg="white", font=("Arial", 13), bd=0, textvariable=password).place(x=285, y=290)

    # BUTTONS
    b1 = Button(root, text="LOGIN", width=12, font=("Arial", 13, "bold"), bg="#03357A", fg="white",
                activebackground="#03357A", activeforeground="yellow", bd=0, padx=0, pady=0, command=Sign_Up)
    b1.place(x=320, y=442)

    #clock()
    root.mainloop()

main_window()
