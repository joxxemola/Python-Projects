
s= str  (input("introduce la letra a si quieres sumar, letra b para restar, letra c para multiplicar y la letra d para dividir:"))
n1 = int (input("Introduzca el primer numero:"))
n2 = int (input("Introduzca el segundo numero:"))



if s == "a":   
    print ("tu resultado de la suma es:" )
    print(n1 + n2)

if s == "b":   
    print ("tu resultado de la resta es:" )
    print(n1 - n2)

    
if s == "c":   
    print ("tu resultado de la multuplicacion es:" )
    print(n1 * n2)


  
if s == "d":   
    print ("tu resultado de la diferencia es:" )
    print(n1 / n2)
