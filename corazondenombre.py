import time 

class color:
    RED = "\x1b[0;31;50m"
    BOLD_RED = "\x1b[1;31;50m"
    NORMAL = "\x1b[0m"

def cargar_corazon():
    with open("heart_pattern.txt", "r") as f:
        return f.read ()
    
def romantizar(nombre):
    corazon = cargar_corazon
    letras = list (nomre)
    i = 0
    while "@" in corazon:
        corazon = corazon.replsce("@", letras ( i % len (letras)), 1)
        i += 1
    return cargar_corazon