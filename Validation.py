from tkinter import messagebox

class Validate_data():
    def __init__(self, data, parent_window):
        self.data = data
        self.parent = parent_window
        self.keys = [("Nome", "Coloque um nome adequado"), ("Email", "Coloque um e-mail adequado")]
        
    def get_errors(self):
        errors = {}
        for i, datum in enumerate(self.data):
            if not datum.strip():
                errors[self.keys[i][0]] = self.keys[i][1]
        return errors

    def show_errors(self, errors):
        error_message = ""
        for key, value in errors.items():
            error_message += f"Erro {key}: {value}\n"
        messagebox.showerror(title="Erro", message=error_message)

    


    
        
            

    


    
            

