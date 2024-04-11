
def contar(nombre_archivo, archivo_salida): #Funcion Principal
    try:
        with open(nombre_archivo,'r', encoding="utf-8") as archivo:
            contenido = archivo.read()
            contador = {}   #Guarda los caracteres en un diccionario

            #Ciclo que recorre el contenido del texto y va guardando los caracteres en el diccionario
            for caracter in contenido:
                if caracter in contador:
                    contador[caracter] +=1 #Si el caracter ya existe en contenido se suma 1
                else:
                    contador[caracter] = 1 #Si el caracter es nuevo se agrega al diccionario con 1
            caracteres_orde = sorted(contador.items(), key=lambda x: x[1], reverse=True) #Ordena la frecuencia de caracteres en el diccionario

        with open(archivo_salida,'w') as archivo_salida:
            for caracter, frecuencia in caracteres_orde:
                archivo_salida.write(f"{caracter}: {frecuencia}\n")
            return "Resultados guardados"
    except FileNotFoundError:
        return "Error de archivo"



archivo = "Gullivers_Travels.txt"
salida = "Resultados.txt"
resultado = contar(archivo, salida)
print(resultado)
