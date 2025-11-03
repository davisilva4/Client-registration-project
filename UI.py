from tkinter import *
from tkinter import messagebox
from Exercise1 import DataBase
from Data_treeview import DataTreeview
from Validation import Validate_data

class MainWindow():
    def __init__(self):
        # Tela principal
        self.window = Tk()
        self.window.geometry("600x400")
        self.window.title("Cadastro Teste")
        self.window.resizable(0, 0)
        self.data_base = DataBase("Clientes.db", self.window)

        # Variáveis para os dados das entradas
        
        self.entries_dict = {}
        self.search = None

        # Botões

        self.buttons_frame = Frame(self.window, height=50)
        self.buttons_frame.pack(padx=10, pady=10)

        self.buttons_list = [("Salvar", lambda e=self.entries_dict: self.save_data(e)),
                            ("Excluir", lambda: self.delete_data()),
                            ("Editar", lambda: self.update_client()),
                            ("Pesquisar", lambda: self.search_data())]
        for button in self.buttons_list:
            self.create_buttons(self.buttons_frame, button).pack(side="left", padx=10, pady=10)

        # Entrada de pesquisa

        self.create_search_entry()

        # Entradas

        self.main_frame = Frame(self.window)
        self.main_frame.pack(fill="x", padx=10, pady=10)

        self.widgets_list = ["Nome", "Email"]

        for widget in self.widgets_list:
            self.create_widgets(widget, self.main_frame).pack()

        # Treeview

        self.lower_frame = Frame(self.window)
        self.lower_frame.pack(fill="x")

        self.treeview_obj = DataTreeview(self.lower_frame, ("ID", "Nome", "Email"))
        self.treeview_obj.treeview.bind("<ButtonRelease-1>", self.treeview_obj.selected_item)
        self.update_treeview()

        self.window.mainloop()

    # Funções de widgets    

    def create_buttons(self, parent, buttons_list):
        button = Button(parent, text=buttons_list[0], command=buttons_list[1])
        return button
    
    def create_search_entry(self):
        search_entry = Entry(self.buttons_frame, width=15)
        search_entry.pack(side="left", padx=10, pady=10)
        self.search = search_entry

    def create_widgets(self, widget, parent):
        frame = Frame(parent)
        label = Label(frame, text=widget, font="Arial 8")
        label.pack(side="left", padx=3, pady=3)
        entry = Entry(frame, width=20)
        entry.pack(side="left", padx=3, pady=3)
        self.entries_dict[widget] = entry

        return frame
    
    def destroy_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def clean_entries(self, entries_dict):
        for entry in entries_dict.values():
            entry.delete(0, END)

    # Funções de dados
    
    def get_entries_data(self, entries_dict):
        entry_values = []
        for value in entries_dict.values():
            entry_values.append(value.get())

        return entry_values 
            
    def save_data(self, entries_dict):
        data = self.get_entries_data(entries_dict)
        validator = Validate_data(data, self.window)
        errors = validator.get_errors()
        if errors:
            validator.show_errors(errors)
        else:
            self.data_base.insert_data(data)
            self.update_treeview()
            self.clean_entries(entries_dict)

    def delete_data(self):
        item_data = self.get_select()
        if not item_data:
            messagebox.showwarning(title="Aviso", message="selecione um item")
            return
        confirm = messagebox.askyesno(title="Exclusão", message="Tem certeza que quer excluir este usuário?")
        if confirm:
            self.data_base.delete_data(item_data[0])
            self.update_treeview()
        return

    def update_treeview(self):
        self.treeview_obj.clean_treeview()
        rows = self.data_base.get_data()
        for i, row in enumerate(rows):
            self.treeview_obj.insert_data(i, row)

    def get_select(self):
        return self.treeview_obj.export_data
    
    def update_client(self):
        item_data = self.get_select()
        if not item_data:
            messagebox.showwarning(title="Aviso", message="Selecione um item")
        else:
            self.destroy_widgets(self.buttons_frame)
            buttons_list = [("Salvar edição", lambda e=self.entries_dict: self.save_edition(e)),
                            ("Cancelar", lambda e=self.entries_dict: self.cancel_edition(e))]
            for button in buttons_list:
                self.create_buttons(self.buttons_frame, button).pack(side="left", padx=10, pady=10)
            for i, entry in enumerate(self.entries_dict.values()):
                entry.insert(END, item_data[i+1])

    def save_edition(self, entries_dict):
        updated_data = self.get_entries_data(entries_dict)
        validator = Validate_data(updated_data, self.window)
        errors = validator.get_errors()
        if errors:
            validator.show_errors(errors)
        else: 
            client_id = self.get_select()[0]
            updated_data.append(client_id)
            self.data_base.update_data(updated_data)
            self.clean_entries(entries_dict)
            self.update_treeview()
            self.destroy_widgets(self.buttons_frame)
            for button in self.buttons_list:
                self.create_buttons(self.buttons_frame, button).pack(side="left", padx=10, pady=10)
            self.create_search_entry()

    def cancel_edition(self, entries_dict):
        self.destroy_widgets(self.buttons_frame)
        for button in self.buttons_list:
            self.create_buttons(self.buttons_frame, button).pack(side="left", padx=10, pady=10)
        self.create_search_entry()
        self.clean_entries(entries_dict)
        self.update_treeview()

    def get_search(self):
        return self.search.get()

    def search_data(self):
        cancel_search_buttons = [("Excluir", lambda: self.exclude_and_cancel()),
                                ("Editar", lambda: self.update_client()),
                                ("Cancelar pesquisa", lambda: self.cancel_search())]
        data = self.get_search()
        if not data:
            messagebox.showwarning(title="Aviso", message="Coloque um termo na pesquisa")
            return
        search_result = self.data_base.search_data(data)
        if not search_result:
            messagebox.showwarning(title="Termo não localizado", message="Não há nenhum usuário com este nome ou email no sistema.")
            return
        self.destroy_widgets(self.buttons_frame)
        for button in cancel_search_buttons:
            self.create_buttons(self.buttons_frame, button).pack(side="left", padx=10, pady=10)
        self.treeview_obj.clean_treeview()
        for i, row in enumerate(search_result):
            self.treeview_obj.insert_data(i, row)

    def cancel_search(self):
        self.destroy_widgets(self.buttons_frame)
        for button in self.buttons_list:
                self.create_buttons(self.buttons_frame, button).pack(side="left", padx=10, pady=10)
        self.create_search_entry()
        self.treeview_obj.clean_treeview()
        self.update_treeview()

    def exclude_and_cancel(self):
        self.delete_data()
        self.cancel_search()

if __name__ == "__main__":
    app = MainWindow()
