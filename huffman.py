import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import heapq
import pickle

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

class CompresorHuffmanGUI:
    def __init__(self, master):
        self.master = master
        master.title("Compresor Huffman")

        self.seleccionar_archivo_button = tk.Button(master, text="Seleccionar archivo", command=self.seleccionar_archivo)
        self.seleccionar_archivo_button.pack()

        self.comprimir_button = tk.Button(master, text="Comprimir", command=self.comprimir)
        self.comprimir_button.pack()

        self.descomprimir_button = tk.Button(master, text="Descomprimir", command=self.descomprimir)
        self.descomprimir_button.pack()

    def seleccionar_archivo(self):
        self.archivo_seleccionado = filedialog.askopenfilename()

    def calcular_frecuencias(self):
        with open(self.archivo_seleccionado, 'r', encoding="utf-8") as archivo:
            contenido = archivo.read()

        self.frecuencias = {}
        for caracter in contenido:
            if caracter in self.frecuencias:
                self.frecuencias[caracter] += 1
            else:
                self.frecuencias[caracter] = 1

    def construir_arbol_huffman(self):
        cola_prioridad = []
        for caracter, frecuencia in self.frecuencias.items():
            nodo = NodoHuffman(caracter, frecuencia)
            heapq.heappush(cola_prioridad, nodo)

        while len(cola_prioridad) > 1:
            nodo_izquierda = heapq.heappop(cola_prioridad)
            nodo_derecha = heapq.heappop(cola_prioridad)

            suma_frecuencias = nodo_izquierda.frecuencia + nodo_derecha.frecuencia
            nodo_padre = NodoHuffman(None, suma_frecuencias)
            nodo_padre.izquierda = nodo_izquierda
            nodo_padre.derecha = nodo_derecha

            heapq.heappush(cola_prioridad, nodo_padre)

        return cola_prioridad[0]

    def generar_codigos_huffman_recursivo(self, nodo, codigo_actual, codigos_huffman):
        if nodo.caracter is not None:
            codigos_huffman[nodo.caracter] = codigo_actual
            return

        self.generar_codigos_huffman_recursivo(nodo.izquierda, codigo_actual + '0', codigos_huffman)
        self.generar_codigos_huffman_recursivo(nodo.derecha, codigo_actual + '1', codigos_huffman)

    def generar_codigos_huffman(self, raiz_arbol):
        codigos_huffman = {}
        self.generar_codigos_huffman_recursivo(raiz_arbol, '', codigos_huffman)
        return codigos_huffman

    def guardar_codigos_huffman(self, codigos_huffman):
        with open("codigos_huffman.txt", "w", encoding="utf-8") as f:
            f.write("Códigos Huffman cargados exitosamente:\n")
            for caracter, codigo in codigos_huffman.items():
                f.write(f"Carácter: {caracter}, Código: {codigo}\n")

    def comprimir(self):
        if hasattr(self, 'archivo_seleccionado'):
            messagebox.showerror("Error", "Por favor, selecciona un archivo primero.")
            

        self.calcular_frecuencias()
        arbol_huffman = self.construir_arbol_huffman()
        codigos_huffman = self.generar_codigos_huffman(arbol_huffman)
        self.guardar_codigos_huffman(codigos_huffman)

        nombre_archivo_comprimido = os.path.splitext(self.archivo_seleccionado)[0] + '.huf'
        with open(self.archivo_seleccionado, 'r', encoding="utf-8") as archivo_original, open(nombre_archivo_comprimido, 'wb') as archivo_comprimido:
            contenido_original = archivo_original.read()
            bits = ""
            for caracter in contenido_original:
                bits += codigos_huffman[caracter]
                while len(bits) >= 8:
                    byte = int(bits[:8], 2)
                    bits = bits[8:]
                    archivo_comprimido.write(bytes([byte]))
            if len(bits) > 0:
                byte = int(bits + '0' * (8 - len(bits)), 2)
                archivo_comprimido.write(bytes([byte]))

        messagebox.showinfo("Éxito", "Archivo comprimido con éxito.")
    
    def descomprimir(self):
        if not hasattr(self, 'archivo_seleccionado'):
            messagebox.showerror("Error", "Por favor, selecciona un archivo primero.")
            return

        print("Descomprimiendo archivo...")

        nombre_archivo_comprimido = self.archivo_seleccionado
        nombre_archivo_original = os.path.splitext(nombre_archivo_comprimido)[0] + '_descomprimido.txt'

        with open(nombre_archivo_comprimido, 'rb') as archivo_comprimido, open("codigos_huffman.txt", 'r', encoding="utf-8") as f:
            # Cargar los códigos Huffman desde el archivo
            codigos_huffman = {}
            for linea in f:
                if 'Códigos Huffman cargados exitosamente' in linea:
                    continue
                partes = linea.strip().split(": ")
                if len(partes) != 2:
                    continue
                codigo = partes[-1]  # El código es la última parte de la línea
                caracter = partes[1].split(", Código: ")[0]  # El carácter es la primera parte después de ": "
                codigos_huffman[codigo] = caracter

            print("Códigos Huffman cargados:")
            for codigo, caracter in codigos_huffman.items():
                print(f"Carácter: {caracter}, Código: {codigo}")

            # Descomprimir el archivo y escribir los datos descomprimidos en el archivo de salida
            contenido_descomprimido = ""
            bits = ""
            byte = archivo_comprimido.read(1)
            while byte:
                bits += f"{ord(byte):08b}"
                for codigo, caracter in codigos_huffman.items():
                    if bits.startswith(codigo):
                        contenido_descomprimido += caracter
                        bits = bits[len(codigo):]
                        print("Código Huffman encontrado:", codigo)
                        print("Caracter descomprimido:", caracter)
                        break
                byte = archivo_comprimido.read(1)

        # Escribir el contenido descomprimido en el archivo de salida
        with open(nombre_archivo_original, 'wb') as archivo_descomprimido:
            archivo_descomprimido.write(bytes(contenido_descomprimido, 'utf-8'))

        print("Descompresión completada.")
        messagebox.showinfo("Éxito", "Archivo descomprimido con éxito.")

root = tk.Tk()
root.geometry("200x200")
my_gui = CompresorHuffmanGUI(root)
root.mainloop()
