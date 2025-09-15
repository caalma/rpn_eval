# Editor para sesiones de bytebeat

El **Editor S-bb** es una herramienta web interactiva diseñada para crear, editar y reproducir archivos de audio generados algorítmicamente (Bytebeat). La aplicación permite gestionar múltiples archivos JSON, editar sus datos, arrastrar y reorganizar elementos, y reproducir expresiones directamente desde la interfaz.

## Características Principales

- **Edición Visual:** Interfaz intuitiva para editar los datos (`data`) y tiempos (`elapsed_time`) de cada ítem.
- **Reproducción en Tiempo Real:** Escucha las expresiones Bytebeat directamente desde el editor.
- **Gestión de Archivos:** Lista, edita y organiza archivos JSON desde una carpeta específica.
- **Acciones Masivas:** Selecciona, elimina o actualiza múltiples ítems a la vez.
- **Arrastrar y Soltar:** Reorganiza los ítems fácilmente con funcionalidad de drag and drop.
- **Filtrado Dinámico:** Filtra archivos por nombre en tiempo real.
- **Diseño Responsivo:** Interfaz adaptable para diferentes tamaños de pantalla.

## Capturas de Pantalla

### Página Principal (`index.html`)
![Index](https://via.placeholder.com/800x400?text=Lista+de+Archivos)

### Editor (`edit.html`)
![Editor](https://via.placeholder.com/800x400?text=Editor+de+Archivos)

## Requisitos

Para ejecutar este proyecto localmente, necesitarás:

- Python 3.x
- Flask (`pip install flask`)
- Un navegador moderno (Chrome, Firefox, Edge, etc.)

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/editor-sbb.git
   cd editor-sbb
   ```

2. **Instala las dependencias:**
   Asegúrate de tener Python instalado y luego instala Flask:
   ```bash
   pip install flask
   ```

3. **Configura la carpeta de datos:**
   - Crea una carpeta llamada `data` en la raíz del proyecto.
   - Coloca tus archivos JSON dentro de esta carpeta. Cada archivo debe tener el formato:
     ```json
     [
         {"data": "t 15 %", "elapsed_time": 9.36},
         {"data": "t 15 % 155 ^", "elapsed_time": 14.67}
     ]
     ```

4. **Inicia el servidor:**
   Ejecuta el siguiente comando para iniciar el servidor Flask:
   ```bash
   python app.py
   ```

5. **Abre la aplicación en tu navegador:**
   Ve a `http://localhost:5000` para acceder al editor.

## Uso

1. **Página de Inicio (`index.html`):**
   - Muestra una lista de archivos disponibles en la carpeta `data`.
   - Usa el campo de filtrado para buscar archivos específicos.
   - Haz clic en un archivo para abrirlo en el editor.

2. **Editor (`edit.html`):**
   - Edita los valores de `data` y `elapsed_time` para cada ítem.
   - Usa las acciones masivas para seleccionar, eliminar o actualizar múltiples ítems.
   - Arrastra y suelta los ítems para reorganizarlos.
   - Reproduce las expresiones Bytebeat haciendo clic en el botón "Escuchar".

3. **Guardar Cambios:**
   - Haz clic en el botón "Guardar" para almacenar los cambios en el archivo original o en uno nuevo.

## Estructura del Proyecto

```
bytebeat-editor/
├── app.py                      # Servidor Flask
├── config.py                   # Configuración personalizada (ruta de la carpeta data)
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css   # Framework Bootstrap 5.3.0
│   │   ├── style-edit.css      # Estilo para edit.html
│   │   └── style-index.css     # Estilo para index.html
│   └── js/
│       ├── init-edit.js        # Lógica interactiva para edit.html
│       └── init-index.js       # Lógica interactiva para index.html
├── templates/
│   ├── index.html              # Página principal
│   └── edit.html               # Editor visual
├── data/                       # Carpeta para almacenar archivos JSON
└── README.md                   # Documentación del proyecto
```

## Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras errores, tienes ideas para mejorar la aplicación o quieres agregar nuevas características, no dudes en abrir un issue o enviar un pull request.

## Licencia

Este proyecto está bajo la licencia [MIT License](LICENSE). Consulta el archivo `LICENSE` para más detalles.

## Créditos

- **Bootstrap 5:** Framework CSS utilizado para el diseño responsivo.
- **Flask:** Framework Python utilizado para el backend.
- **Bytebeat:** Inspiración para la creación de audio algorítmico.
