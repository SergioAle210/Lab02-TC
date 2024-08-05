# Librerías necesarias y cómo instalarlas:
# - json: Esta librería es parte de la biblioteca estándar de Python, no necesita instalación.
# - yaml: Para manejar archivos YAML. Instalar con: pip install pyyaml
# - xml.etree.ElementTree: Parte de la biblioteca estándar de Python para manejar XML.
# - pandas: Para manejar archivos CSV. Instalar con: pip install pandas
# - csv: Parte de la biblioteca estándar de Python para manejar archivos CSV.
# - colorama: Para agregar color a la salida de la consola. Instalar con: pip install colorama

import json
import yaml
import xml.etree.ElementTree as ET
import pandas as pd
import csv
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def cargar_automata(ruta_archivo):
    if ruta_archivo.endswith('.json'):
        with open(ruta_archivo, 'r') as archivo:
            automata = json.load(archivo)
    elif ruta_archivo.endswith('.yml') or ruta_archivo.endswith('.yaml'):
        with open(ruta_archivo, 'r') as archivo:
            automata = yaml.safe_load(archivo)
    elif ruta_archivo.endswith('.xml'):
        arbol = ET.parse(ruta_archivo)
        raiz = arbol.getroot()
        automata = xml_a_diccionario(raiz)
    elif ruta_archivo.endswith('.csv'):
        automata = csv_a_diccionario(ruta_archivo)
    else:
        raise ValueError("Formato de archivo no soportado")
    return automata

def xml_a_diccionario(raiz):
    automata = {}
    for hijo in raiz:
        if hijo.tag == 'delta':
            automata['delta'] = []
            for item in hijo:
                automata['delta'].append(tuple(subitem.text for subitem in item))
        elif hijo.tag in ['Q', 'Sigma', 'F']: 
            automata[hijo.tag] = [item.text for item in hijo]
        else:  
            automata[hijo.tag] = hijo.text
    return automata

def csv_a_diccionario(ruta_archivo):
    automata = {
        "Q": [],
        "Sigma": [],
        "q0": "",
        "F": [],
        "delta": []
    }

    with open(ruta_archivo, 'r') as archivo:
        reader = csv.reader(archivo)
        for row in reader:
            # Verificar si hay comentarios y saltar la línea
            if not row or row[0].startswith("#"):
                # Procesar metadatos de los comentarios
                if row and len(row) > 1:
                    if row[0] == "# Estados":
                        automata["Q"] = row[2:]  # Omitir el identificador
                    elif row[0] == "# Alfabeto":
                        automata["Sigma"] = row[2:]  # Omitir el identificador
                    elif row[0] == "# EstadoInicial":
                        automata["q0"] = row[2]  # Omitir el identificador
                    elif row[0] == "# EstadosAceptacion":
                        automata["F"] = row[2:]  # Omitir el identificador
                continue  # Saltar las líneas de comentarios

            # Procesar transiciones
            if len(row) == 3:  # Asegurarse de que haya exactamente 3 elementos para una transición válida
                automata["delta"].append((row[0], row[1], row[2]))

    return automata

def transicion(estado_actual, simbolo, delta):
    for (estado, char, estado_siguiente) in delta:
        if estado == estado_actual and char == simbolo:
            return estado_siguiente
    return None

def estado_final(q0, w, delta):
    estado_actual = q0
    for simbolo in w:
        estado_actual = transicion(estado_actual, simbolo, delta)
        if estado_actual is None:
            break
    return estado_actual

def derivacion(q0, w, delta):
    estado_actual = q0
    camino = [estado_actual]
    for simbolo in w:
        estado_actual = transicion(estado_actual, simbolo, delta)
        if estado_actual is None:
            break
        camino.append(estado_actual)
    return camino

def aceptado(q0, w, F, delta):
    final = estado_final(q0, w, delta)
    return final in F

def imprimir_afd(automata):
    print(Fore.YELLOW + "\nEstados y Transiciones del AFD:")
    print(Fore.CYAN + f"Estados: {', '.join(automata['Q'])}")
    print(Fore.CYAN + f"Alfabeto: {', '.join(automata['Sigma'])}")
    print(Fore.CYAN + f"Estado Inicial: {automata['q0']}")
    print(Fore.CYAN + f"Estados de Aceptación: {', '.join(automata['F'])}")
    print(Fore.MAGENTA + "Transiciones:")
    for (estado_origen, simbolo, estado_destino) in automata['delta']:
        print(Fore.GREEN + f"  {estado_origen} --{simbolo}--> {estado_destino}")

print(Style.BRIGHT + Fore.RED + "---------------------------------Primer inciso---------------------------------")

# Prueba AFD 1
# Cambiar la direccion del archivo para probar con los diferentes formatos

path1 = './assets/dfa.xml'
automata1 = cargar_automata(path1)
q0_1 = automata1['q0']
F_1 = automata1['F']
delta_1 = automata1['delta']

# Cambiar la palabra 
w1 = "aabbaa"
afd1_salida = {
    "automata": automata1,
    "resultados": {
        "Transición": transicion(q0_1, "a", delta_1),
        "Estado Final": estado_final(q0_1, w1, delta_1),
        "Derivación": derivacion(q0_1, w1, delta_1),
        "Aceptado": aceptado(q0_1, w1, F_1, delta_1)
    }
}

print("\n---------------Detalles y Resultados del AFD 1---------------\n")
print(Fore.BLUE + "Archivo que se está ejecutando:", path1)
print(Fore.BLUE + "Cadena w1:", w1)
print(Fore.BLUE + "Estado Final:", afd1_salida["resultados"]["Estado Final"])
print(Fore.BLUE + "Camino de Derivación:", ' -> '.join(afd1_salida["resultados"]["Derivación"]))
print(Fore.BLUE + "Aceptado:", afd1_salida["resultados"]["Aceptado"])
imprimir_afd(automata1)

# Prueba AFD 2
# Cambiar la direccion del archivo para probar con los diferentes formatos
path2 = './assets/dfa1.yml'
automata2 = cargar_automata(path2)
q0_2 = automata2['q0']
F_2 = automata2['F']
delta_2 = automata2['delta']

# Cambiar la palabra
w2 = "abbaab"
afd2_salida = {
    "automata": automata2,
    "resultados": {
        "Transición": transicion("q0", "a", delta_2),
        "Estado Final": estado_final(q0_2, w2, delta_2),
        "Derivación": derivacion(q0_2, w2, delta_2),
        "Aceptado": aceptado(q0_2, w2, F_2, delta_2)
    }
}

print(Style.BRIGHT + Fore.RED + "\n---------------Detalles y Resultados del AFD 2---------------\n")
print(Fore.BLUE + "Archivo que se está ejecutando:", path2)
print(Fore.BLUE + "Cadena w2:", w2)
print(Fore.BLUE + "Estado Final:", afd2_salida["resultados"]["Estado Final"])
print(Fore.BLUE + "Camino de Derivación:", ' -> '.join(afd2_salida["resultados"]["Derivación"]))
print(Fore.BLUE + "Aceptado:", afd2_salida["resultados"]["Aceptado"])
imprimir_afd(automata2)

# Segundo ejercicio. 
# No cambiar la ruta.
automata = cargar_automata('./AFD/lab2-2b.json')
q0 = automata['q0']
F = automata['F']
delta = automata['delta']

print(Style.BRIGHT + Fore.RED + "\n---------------------------------Segundo Inciso---------------------------------")

# Cadenas de prueba
cadenas_prueba = {
    "w3": "+0.1234567",
    "w4": "1.61-8081",
    "w5": "2024.3.3.3"
}

# Función para probar una cadena con el AFD
def probar_cadena(automata, w, etiqueta):
    q0 = automata['q0']
    F = automata['F']
    delta = automata['delta']
    
    afd_salida = {
        "automata": automata,
        "resultados": {
            "Estado Final": estado_final(q0, w, delta),
            "Derivación": derivacion(q0, w, delta),
            "Aceptado": aceptado(q0, w, F, delta)
        }
    }
    
    print(Style.BRIGHT + Fore.YELLOW + f"\nProbando cadena {etiqueta}: {w}")
    print(Fore.CYAN + "Estado Final:", afd_salida["resultados"]["Estado Final"])
    print(Fore.CYAN + "Camino de Derivación:", ' -> '.join(afd_salida["resultados"]["Derivación"]))
    print(Fore.CYAN + "Aceptado:", afd_salida["resultados"]["Aceptado"])

# Imprimir estructura del AFD
imprimir_afd(automata)

# Probar cada cadena
for etiqueta, w in cadenas_prueba.items():
    probar_cadena(automata, w, etiqueta)
