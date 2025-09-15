# Pasos a seguir

## 00 - procesar lista de comandos

Crear una lista con cada comando en una línea. Al comando se le debe anteponer la duración en segundo y luego el '@'. Luego:

    ./0_procesar_lista lista.txt


## 01 - sincronizar audio e imagen
Desplazar el inicio del audio a "00:00:00.12". Para 30fps es (/ 12 30.0) 0.4 que corresponde a 400 en adelay

    mkdir ajustados
    for a in *.mkv; do ffmpeg -i "$a" -af "adelay=400" -c:v copy ajustados/"$a"; done

## 02 - recorte de tiempo
Proceder en la carpeta correspondiente para ajustar todos los videos.

    mkdir recortados
    for a in *.mkv; do ./recorte "$a" "00:00:00.600" "00:00:56.021" "recortados/"; done
