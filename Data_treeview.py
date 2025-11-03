from tkinter import *
from tkinter import ttk

class DataTreeview(Frame):
    def __init__(self, parent, fields):
        super().__init__(master=parent)
        self.pack(expand=True, padx=10, pady=10)
        self.export_data = None

        self.treeview = ttk.Treeview(self, columns=(fields), show="headings")
        for field in fields:
            self.treeview.heading(field, text=field)
            self.treeview.column(field, width=150, anchor="center")
        self.treeview.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.treeview.yview_scroll)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

    def insert_data(self, i, data):
        self.treeview.insert(parent="", index=i, values=data)

    def clean_treeview(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def selected_item(self, event):
        selected_id = self.treeview.focus()
        selected_data = self.treeview.item(selected_id)
        self.export_data = selected_data["values"]