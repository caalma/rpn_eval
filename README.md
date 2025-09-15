# Evaluador RPN

Dispone de generador de audio y calculadora en modo i (enteros) y f (decimales). Además de un repl calculadora en modo i.

En aplicaciones hay diversas utilidades que utilizan los binarios base.

**IMPORTANTE:** Este proyecto está en etapa de desarrollo y solamente fue testeado en un sistema operativo GNU/Linux con base Debian.

## Compilación

    cd base
    make

## Test

    cd base
    make test_audio_f
    make test_audio_i
    make test_calc_f
    make test_calc_i
    make test_repl_i

## Limpieza de proyecto

    cd base
    make clean


## Tareas pendientes

Corregir el modo f porque no funciona de la forma esperada.
