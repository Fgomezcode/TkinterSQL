import tkinter as tk
import tkinter.messagebox as messagebox
import os
import sqlite3 as sql

WINDOW_TITLE = "Database Project"

class MainWindow:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.minsize(780, 300)
        self.root.maxsize(880, 300)

        self.dbListFrame = tk.Frame(self.root)
        self.dbListFrame.pack(side = 'left' )
        self.dbList = tk.Listbox(self.dbListFrame, width = 20, height = 10)
        self.dbList.pack(side= 'top')
        self.dbListButton = tk.Button(self.dbListFrame, width = 8, text = 'GET DATA', command = self.getDataFromSelection).pack(side = 'left', pady = 20)
        self.dbRefreshButton = tk.Button(self.dbListFrame,width = 8, text = 'REFRESH', command =self.getDBList).pack(side = 'left')
        self.makeButton = tk.Button(self.dbListFrame,width = 8, text = 'MAKE', command = self.openMakeTable).pack(side = 'left')

        self.displayInfoFrame = tk.Frame(self.root)
        self.displayInfoFrame.pack(side = 'right')
        self.displayInfoList = tk.Listbox(self.displayInfoFrame, width = 80, height = 10)
        self.displayInfoList.pack(side = 'top', padx =(0,20))

        self.displayButtonFrame = tk.Frame(self.displayInfoFrame)
        self.displayButtonFrame.pack(side = 'bottom')
        self.insertButton = tk.Button(self.displayButtonFrame, width=10, text='INSERT', command = self.insertData).pack(side='left')
        self.deleteButton = tk.Button(self.displayButtonFrame, width = 10, text = 'DELETE', command = self.deleteItem).pack(side = 'left')
        self.deleteLabel = tk.Label(self.displayButtonFrame, text ="ID:").pack(side = 'left')
        self.deleteEntry = tk.Entry(self.displayButtonFrame, width = 3)
        self.deleteEntry.pack(side = 'left', padx = 10)


        self.insertFrame = tk.Frame(self.displayInfoFrame)
        self.insertFrame.pack()
        self.qtyLabel = tk.Label(self.insertFrame, text = 'QTY').pack(side = 'left')
        self.insertQtyEntry = tk.Entry(self.insertFrame, width = 5)
        self.insertQtyEntry.pack(side = 'left')
        self.insertEntry = tk.Entry(self.insertFrame, width = 40)
        self.insertEntry.pack(side = 'right')
        self.insertLabel = tk.Label(self.insertFrame, text='DATA').pack(side='right', padx = 5)

        self.getDBList()

        messagebox.showinfo('Welcome', 'Select a database from the list and \n Press "GET DATA" to display information ')
        tk.mainloop()

    def getDataFromSelection(self):

        indexes = self.dbList.curselection()

        if (len(indexes) > 0):

            NAME = str(indexes[0]) #int value of dblist
            selection = self.dbList.get(indexes) #xyz.db
            path = 'Databases/' + selection
            conn = sql.connect(path)
            cur = conn.cursor()
            print(' --- getting info --- ')
            call = f'SELECT * FROM {selection[0:len(selection) - 3]}'

            cur.execute(call)

            self.results = cur.fetchall()
            self.displayInfoList.delete(0, self.displayInfoList.size())
            for row in self.results:
                self.displayInfoList.insert(tk.END, f'{row[0]:<10}{row[1]:^20} {row[2]:^20}')
            print(selection)
        else:
            messagebox.showinfo(
                message= 'Make a selection')

    def getDBList(self):
        path = 'Databases/'
        dbList = os.listdir(path)
        self.dbList.delete(0, self.dbList.size())
        for file in dbList:
            print(file)
            self.dbList.insert(0, file)

    def openMakeTable(self):
        x = CreateWindow()

    def insertData(self):
        try:
            indexes = self.dbList.curselection()
            if (len(indexes) > 0):
                NAME = str(indexes[0])  # int value of dblist
                selection = self.dbList.get(indexes)  # xyz.db
                path = 'Databases/' + selection

                info = str(self.insertEntry.get())
                qty = int(self.insertQtyEntry.get())

                conn = sql.connect(path)
                cur = conn.cursor()

                print('preparing to insert')

                # FINISH THE INSERT FUNCTION
                cur.execute(f'''INSERT INTO {selection[0:len(selection) - 3]} ( itemName, itemQuantity)
                                                       VALUES(?,?)''', (info, qty))

                conn.commit()  # ACTUALLY PUSH THE DATA!
                conn.close()

                self.getDataFromSelection()

                self.insertEntry.delete(0, 'end')
                self.insertQtyEntry.delete(0, 'end')
        except:
            messagebox.showinfo('Error', 'Please check your input.')

    def deleteItem(self):
        try:
            indexes = self.dbList.curselection()
            itemToDelete = self.deleteEntry.get()

            if (len(indexes) > 0):

                NAME = str(indexes[0])  # int value of dblist
                selection = self.dbList.get(indexes)  # xyz.db
                path = 'Databases/' + selection
                conn = sql.connect(path)
                cur = conn.cursor()
                print(' --- getting info --- ')
                call = f'DELETE FROM {selection[0:len(selection) - 3]} WHERE itemID == {itemToDelete}'

                cur.execute(call)
                conn.commit()
                self.deleteEntry.delete(0, 'end')
                self.getDataFromSelection()
        except:
            messagebox.showinfo(message='Enter ID value.')



class CreateWindow:
    def __init__(self):

        self.databaseCreate = tk.Tk()

        self.databaseCreate.title("Create New Table")
        self.databaseCreate.minsize(300,120)
        self.databaseCreate.maxsize(300, 120)

        self.createLabelFrame = tk.Frame(self.databaseCreate)
        self.createLabelFrame.pack()

        self.nameLabel = tk.Label(self.createLabelFrame, text = "Enter Name:").pack()
        self.nameEntry = tk.Entry(self.databaseCreate, width = 30)
        self.nameEntry.pack()
        self.nameButton = tk.Button(self.databaseCreate, text = "CREATE", command = self.createDatabase).pack()
        tk.mainloop()


    def createDatabase(self):
        databaseName = str(self.nameEntry.get())
        try:
            if databaseName != "":  # if the name is not empty
                databaseName = str(self.nameEntry.get())

                sqlFeed = f'''CREATE TABLE IF NOT EXISTS {databaseName}(itemID INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                                                                    itemName TEXT,
                                                                                                    itemQuantity INTEGER  )'''

                conn = sql.connect(
                    'Databases/' + databaseName + '.db')

                cur = conn.cursor()
                cur.execute(sqlFeed)
                conn.close()
                tk.messagebox.showinfo("Success", "Database Successfully Created\nRefresh list after closing this window")
                self.databaseCreate.destroy()

            else:
                tk.messagebox.showinfo("ERROR", "PLEASE ENTER A NAME")
        except:
            tk.messagebox.showinfo("ERROR", "THERE WAS AN ERROR")




x = MainWindow()

