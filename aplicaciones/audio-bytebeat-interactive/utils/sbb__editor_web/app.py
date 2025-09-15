#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from config import *
import subprocess
import signal

app = Flask(__name__)

# Diccionario para almacenar el proceso activo
active_process = None

@app.route('/')
def index():
    # Obtener la lista de archivos y sus tamaños
    files = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith('.json'):
            file_path = os.path.join(DATA_FOLDER, file)
            size_kb = round(os.path.getsize(file_path) / 1024, 2)  # Tamaño en Kb
            files.append({"name": file, "size_kb": size_kb})

    # Ordenar alfabéticamente de forma decreciente
    files.sort(key=lambda x: x["name"], reverse=True)
    return render_template('index.html', files=files, data_folder=DATA_FOLDER)

@app.route('/edit/<filename>')
def edit(filename):
    # Leer el archivo JSON
    file_path = os.path.join(DATA_FOLDER, filename)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return render_template('edit.html', filename=filename, data=data)

@app.route('/update/<filename>', methods=['POST'])
def update(filename):
    # Actualizar el archivo JSON con los datos enviados desde el frontend
    file_path = os.path.join(DATA_FOLDER, filename)
    updated_data = request.json
    with open(file_path, 'w') as f:
        json.dump(updated_data, f, indent=4)
    return jsonify({"status": "success"})


@app.route('/listen', methods=['POST'])
def listen():
    global active_process

    # Si ya hay un proceso activo, no permitir iniciar otro
    if active_process and active_process.poll() is None:
        return jsonify({"status": "error", "message": "Ya hay un proceso de reproducción activo"}), 400

    expression = request.json.get('expression')
    if not expression:
        return jsonify({"status": "error", "message": "No se proporcionó una expresión"}), 400

    try:
        # Construir el comando
        command = AUDIO_PROGRAM.format(expression=expression)
        # Iniciar el proceso con un grupo de procesos
        active_process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/listen_stop', methods=['POST'])
def listen_stop():
    global active_process

    # Si no hay un proceso activo, no hacer nada
    if not active_process or active_process.poll() is not None:
        return jsonify({"status": "error", "message": "No hay ningún proceso de reproducción activo"}), 400

    try:
        # Detener el grupo de procesos
        os.killpg(os.getpgid(active_process.pid), signal.SIGTERM)
        active_process = None
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
