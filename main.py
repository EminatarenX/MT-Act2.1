import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

class TuringMachine:
    def __init__(self):
        self.tape = []
        self.head = 0
        self.state = 'q0'
        self.transitions = {
            'q0': {'a': ('q1', 'R')},
            'q1': {'b': ('q2', 'R')},
            'q2': {'b': ('q3', 'R')},
            'q3': {'a': ('q1', 'R'), '_': ('qf', 'L')}
        }
        self.final_states = {'qf'}

    def run(self, input_string):
        self.tape = list(input_string) + ['_']
        self.head = 0
        self.state = 'q0'

        while self.state not in self.final_states:
            current_symbol = self.tape[self.head]
            if self.state in self.transitions and current_symbol in self.transitions[self.state]:
                new_state, move = self.transitions[self.state][current_symbol]
                self.state = new_state
                if move == 'R':
                    self.head += 1
                elif move == 'L':
                    self.head -= 1
                if self.head >= len(self.tape):
                    self.tape.append('_')
            else:
                return False  # Rechazar si no hay transición válida

        return True  # Aceptar si termina en un estado final

class TuringMachineGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Máquina de Turing para (ab²)ⁿ, n>0")
        self.master.geometry("600x400")

        self.tm = TuringMachine()
        self.valid_strings = []
        self.invalid_strings = []

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.Frame(self.master)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Ingrese una cadena:").pack(side=tk.LEFT, padx=5)
        self.input_entry = ttk.Entry(input_frame, width=30)
        self.input_entry.pack(side=tk.LEFT, padx=5)
        self.input_entry.bind('<Return>', lambda event: self.validate_string())

        ttk.Button(input_frame, text="Validar", command=self.validate_string).pack(side=tk.LEFT, padx=5)

        # Treeview para mostrar las cadenas y su validación
        self.tree = ttk.Treeview(self.master, columns=('Cadena', 'Estado'), show='headings')
        self.tree.heading('Cadena', text='Cadena')
        self.tree.heading('Estado', text='Estado')
        self.tree.column('Cadena', width=300)
        self.tree.column('Estado', width=100)
        self.tree.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        ttk.Button(self.master, text="Generar Reporte CSV", command=self.generate_csv).pack(pady=10)

    def validate_string(self):
        input_string = self.input_entry.get()
        if self.tm.run(input_string):
            estado = "Válida"
            self.valid_strings.append(input_string)
        else:
            estado = "Inválida"
            self.invalid_strings.append(input_string)
        
        self.tree.insert('', 'end', values=(input_string, estado))
        self.input_entry.delete(0, tk.END)  # Limpiar el campo de entrada

    def generate_csv(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"turing_machine_report_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Tipo", "Cadena"])
            for item in self.tree.get_children():
                values = self.tree.item(item)['values']
                writer.writerow([values[1], values[0]])
        
        messagebox.showinfo("Reporte Generado", f"El reporte ha sido guardado como {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TuringMachineGUI(root)
    root.mainloop()
