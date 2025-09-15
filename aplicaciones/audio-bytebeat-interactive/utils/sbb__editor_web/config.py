# Carpeta donde se almacenarán los archivos JSON
DATA_FOLDER = "../../sesiones_grabadas/"


# Comando para generar y reproducir la expresión
#AUDIO_PROGRAM = 'echo "{expression}" >> /tmp/abb_edit-test.txt'
#AUDIO_PROGRAM = '../../../../base/bin/audio_rpn_i "{expression}" "0" | ffplay -hide_banner -infbuf -f s16le -ar 8000  -ac 1 -vn -i -'
AUDIO_PROGRAM = '../../../../base/bin/audio_rpn_i "{expression}" "0" | ../../../../extra/audpv -f s16le -r 8000 -c 1 -v freqwalklog -t ":)"'
