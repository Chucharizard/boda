from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import sqlite3
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave segura

# Función para obtener conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('invitados.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicializar la base de datos
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS invitados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            device_id TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Obtener o crear device_id desde la cookie
    device_id = request.cookies.get('device_id')
    
    # Verificar si este dispositivo ya se registró
    ya_registrado = False
    nombre_registrado = None
    
    if device_id:
        conn = get_db_connection()
        registro = conn.execute(
            'SELECT nombre FROM invitados WHERE device_id = ?', 
            (device_id,)
        ).fetchone()
        conn.close()
        
        if registro:
            ya_registrado = True
            nombre_registrado = registro['nombre']
    
    return render_template('index.html', ya_registrado=ya_registrado, nombre_registrado=nombre_registrado)

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre', '').strip()
    
    if not nombre:
        flash('Por favor, ingresa tu nombre', 'error')
        return redirect(url_for('index'))
    
    # Obtener o generar device_id
    device_id = request.cookies.get('device_id')
    if not device_id:
        device_id = str(uuid.uuid4())
    
    try:
        conn = get_db_connection()
        
        # Verificar si este dispositivo ya se registró
        existe = conn.execute(
            'SELECT nombre FROM invitados WHERE device_id = ?', 
            (device_id,)
        ).fetchone()
        
        if existe:
            conn.close()
            flash(f'Este dispositivo ya registró la asistencia de: {existe["nombre"]}', 'error')
            return redirect(url_for('index'))
        
        # Insertar el nuevo registro
        conn.execute('INSERT INTO invitados (nombre, device_id) VALUES (?, ?)', (nombre, device_id))
        conn.commit()
        conn.close()
        
        # Crear respuesta con cookie
        response = make_response(redirect(url_for('index')))
        response.set_cookie('device_id', device_id, max_age=60*60*24*365*2)  # Cookie válida por 2 años
        
        flash('¡Gracias por confirmar tu asistencia!', 'success')
        return response
        
    except Exception as e:
        flash('Hubo un error al registrar tu asistencia', 'error')
        return redirect(url_for('index'))

@app.route('/lista-invitados')
def lista_invitados():
    conn = get_db_connection()
    invitados = conn.execute('SELECT * FROM invitados ORDER BY fecha_registro DESC').fetchall()
    conn.close()
    return render_template('lista.html', invitados=invitados)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
