from tkinter import *
from tkinter import ttk
from tkinter import filedialog


def abrir_archivo():
    archivo = filedialog.LoadFileDialog(initialdir="/", title="Seleccionar", filetypes=(("Archivos texto", "*.txt"), ("Todos los archivos" , "*.*")))
    print("Archivo", archivo)



root = Tk()
root.title("Huffman")
root.geometry("200x300")


ttk.Label(root, text="Codificacion de Huffman", font="Arial").grid(column=0,row=0)
ttk.Button(root, text="Seleccionar Archivo", command=abrir_archivo).grid()
ttk.Button(root, text="Comprimir").grid()
ttk.Button(root, text="Descomprimir").grid()
ttk.Button(root, text="Salir", command=root.destroy).grid()


root.mainloop()
