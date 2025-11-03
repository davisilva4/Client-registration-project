from sqlite3 import *
from contextlib import closing
from tkinter import messagebox

class DataBase():
    def __init__(self, db, parent_window):
        self.parent_window = parent_window
        self.db = db
        self.create_dataBase()

    def create_dataBase(self):
        try:
            with closing(connect(self.db)) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute("""CREATE TABLE IF NOT EXISTS Clientes (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Nome TEXT NOT NULL,
                                Email TEXT NOT NULL
                                )""")
                    conn.commit()
        except Error as e:
           messagebox.showerror(parent=self.parent_window, message=f"{e}.\nNão foi possível criar o banco.")

    def insert_data(self, data):
        insert_data = data
        try:
            with closing(connect(self.db)) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute("""INSERT INTO Clientes (
                                Nome,
                                Email
                                ) VALUES (?, ?)
                                """, insert_data)
                    conn.commit()
                    messagebox.showinfo(title="Sucesso", message="Usuário cadastrado com sucesso")
        except Error as e:
            messagebox.showerror(parent=self.parent_window, message=f"{e}.\nNão foi possível inserir os dados no banco")
    
    def get_data(self):
        rows = []
        try:
            with closing(connect(self.db)) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute("""SELECT * FROM Clientes""")
                    rows = cursor.fetchall()
        except Error as e:
            messagebox.showerror(parent=self.parent_window, message=f"{e}.\nNão foi possível extrair os dados do banco")

        return rows
    
    def delete_data(self, id):
        try:
            with closing(connect(self.db)) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute("""DELETE FROM Clientes WHERE ID = ?""", (id,))
                    messagebox.showinfo(parent=self.parent_window, message=f"Usuário com o id {id} foi excluído com sucesso")
                    conn.commit()
        except Error as e:
            messagebox.showerror(parent=self.parent_window, message=f"{e}.\nNão foi possível excluir os dados do banco")

    def update_data(self, data):
        try:
            with closing(connect(self.db)) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute("""UPDATE Clientes SET Nome = ?, Email = ? WHERE ID = ?""", data)
                    conn.commit()
                    messagebox.showinfo(title="Sucesso", message="Usuário atualizado com sucesso")
        except Error as e:
            messagebox.showerror(parent=self.parent_window, message=f"{e}.\nNão foi possível atualizar o cliente")

    def search_data(self, data):
        search = None
        try:
            with closing(connect(self.db)) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute("""SELECT * FROM Clientes WHERE LOWER(Nome) LIKE ? OR LOWER(Email) LIKE ?""", (f"%{data}%", f"%{data}%"))
                    search = cursor.fetchall()
                    return search
        except Error as e:
            messagebox.showerror(parent=self.parent_window, message=f"{e}.\nNão foi possível pesquisar o cliente")

