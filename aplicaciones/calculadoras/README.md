# Modo de uso

La expresion a calcular debe ser el primer argumento.

La variable de t es la que asume los valores numéricos pasados como argumentos extras.

Ejemplos:

    ./calcular_enteros "1 1 +"
    ./calcular_enteros "t 2 /" 8
    ./calcular_enteros "t t t * *" 3 4 1 3
    ./calcular_enteros "t dup * 2 /" $(seq -5 5)
    ./calcular_enteros "1 t <<" 0 1 2 3 4 5 6 7 8 9
    ./calcular_flotantes "2 2 +"
    ./calcular_flotantes "t tan abs" -1 1
    ./calcular_flotantes "t dup * 2 / sin" $(seq 1 9)
    ./calcular_flotantes "t 2 << t cos * ~" $(seq -4 4)
