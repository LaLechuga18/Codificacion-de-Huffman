import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import heapq
import os
import pickle
from collections import Counter, namedtuple





#--------------------------------BACKEND----------------------------------------------
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def calcular_frecuencias(texto):
    return Counter(texto)

def construir_arbol(frecuencias):
    cola = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
    heapq.heapify(cola)
    while len(cola) > 1:
        nodo_izquierda = heapq.heappop(cola)
        nodo_derecha = heapq.heappop(cola)
        nodo_padre = NodoHuffman(None, nodo_izquierda.frecuencia + nodo_derecha.frecuencia)
        nodo_padre.izquierda = nodo_izquierda
        nodo_padre.derecha = nodo_derecha
        heapq.heappush(cola, nodo_padre)
    return cola[0]

def codificar_arbol(arbol, ruta='', codigo={}):
    if arbol is not None:
        if arbol.caracter is not None:
            codigo[arbol.caracter] = ruta
        codificar_arbol(arbol.izquierda, ruta + '0', codigo)
        codificar_arbol(arbol.derecha, ruta + '1', codigo)
    return codigo

def serializar_arbol(arbol):
    if arbol is None:
        return None
    return {
        'caracter': arbol.caracter,
        'frecuencia': arbol.frecuencia,
        'izquierda': serializar_arbol(arbol.izquierda),
        'derecha': serializar_arbol(arbol.derecha)
    }

def deserializar_arbol(data):
    if data is None:
        return None
    nodo = NodoHuffman(data['caracter'], data['frecuencia'])
    nodo.izquierda = deserializar_arbol(data['izquierda'])
    nodo.derecha = deserializar_arbol(data['derecha'])
    return nodo

def comprimir(texto):
    frecuencias = calcular_frecuencias(texto)
    arbol = construir_arbol(frecuencias)
    codigo = codificar_arbol(arbol)
    
    #Codifica el texto usando VLC (Codificacion de Longitud Variable)
    texto_codificado = ''.join(codigo[caracter] for caracter in texto)
    bytes_comprimidos = bytearray()
    for i in range(0, len(texto_codificado), 8):
        byte = texto_codificado[i:i+8]
        if len(byte) < 8:
            byte += '0' * (8 - len(byte))  
        bytes_comprimidos.append(int(byte, 2))
    return bytes_comprimidos, serializar_arbol(arbol)


def descomprimir(comprimido, arbol_serializado):
    bits = ''.join(format(byte, '08b') for byte in comprimido)
    padding_info = int(bits[:8], 2)
    bits = bits[8:]
    bits = bits[:-padding_info]
    
    #Reconstruir el Arbol de Huffman
    arbol = deserializar_arbol(arbol_serializado)
    
    #Decodificar los bits utilizando el arbol
    nodo_actual = arbol
    texto = ''
    for bit in bits:
        if bit == '0':
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
        if nodo_actual.caracter is not None:
            texto += nodo_actual.caracter
            nodo_actual = arbol
    
    return texto

def comprimir_archivo(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r', encoding="utf-8") as archivo:
        texto = archivo.read()
    comprimido, arbol_serializado = comprimir(texto)
    with open(archivo_salida, 'wb') as archivo:
        pickle.dump((comprimido, arbol_serializado), archivo)

def comprimir_seleccionado():
    archivo_entrada = txt_ruta.get()
    if not archivo_entrada:
        return
    archivo_salida = archivo_entrada + ".bin"
    comprimir_archivo(archivo_entrada, archivo_salida)
    messagebox.showinfo("Exito", f"Archivo comprimido como {archivo_salida}")

def descomprimir_archivo(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'rb') as archivo:
        comprimido, arbol_serializado = pickle.load(archivo)
    texto = descomprimir(comprimido, arbol_serializado)
    with open(archivo_salida, 'w') as archivo:
        archivo.write(texto)

def descomprimir_seleccionado():
    archivo_entrada = txt_ruta.get()
    if not archivo_entrada:
        return
    if not archivo_entrada.endswith('.bin'):
        messagebox.showinfo("Error", "Seleccione un archivo binario (.bin)")
        return
    archivo_salida = archivo_entrada[:-4] + " (descomprimido).txt"
    descomprimir_archivo(archivo_entrada, archivo_salida)
    messagebox.showinfo("Exito", f"Archivo descomprimido como {archivo_salida}")


def seleccionar_archivo():
    archivo = filedialog.askopenfilename()
    if archivo:
        txt_ruta.delete(0, tk.END)
        txt_ruta.insert(0, archivo)
        
        



#--------------------------GUI----------------------------------------------------------------------
root = tk.Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()

ttk.Label(frm, text="Bienvenido").grid(column=0, row=0)
ttk.Label(frm, text ='el texto a leer:').grid(column=0,row=1)

txt_ruta = ttk.Entry(frm)   #Se agrego esta variable que permite ver la ruta del archivo elegido
txt_ruta.grid(column=1, row=1)

btn = ttk.Button(frm,text= 'Abrir', command=seleccionar_archivo).grid()

#Se agregaron los botones de comprir y descomprimir 
ttk.Button(frm, text="Comprimir", command=comprimir_seleccionado).grid()  
ttk.Button(frm, text="Descomprimir", command=descomprimir_seleccionado).grid()

root.mainloop()
