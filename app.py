from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from datetime import datetime
import shelve

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['DATABASE'] = 'employees.db'

# Datenbank-Initialisierung
def initialize_database():
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Verbindung zur SQLite-Datenbank herstellen
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Benutzer in der Datenbank speichern
def add_employee(first_name, last_name, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO employee (first_name, last_name, email, password) VALUES (?, ?, ?, ?)', (first_name, last_name, email, password))
    conn.commit()
    conn.close()

# Überprüfung, ob der Benutzer angemeldet ist
def user_is_logged_in():
    return 'user_id' in session

# Startseite
@app.route('/')
def index():
    return render_template('index.html')

# Anmeldeseite
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Überprüfung der Anmeldedaten
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employee WHERE email = ? AND password = ?', (email, password))
        employee = cursor.fetchone()
        conn.close()

        if employee:
            # Setzen der Benutzer-ID in der Sitzung
            session['user_id'] = employee['id']
            # Weiterleitung zum Dashboard
            return redirect(url_for('dashboard'))
        else:
            return 'Ungültige Anmeldedaten'

    return render_template('login.html')


########################################
db = shelve.open("tasks.db")

# Mitarbeiter-Dashboard
@app.route('/dashboard')
def dashboard():
    if user_is_logged_in():
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/start', methods=['POST'])
def start():
    task = request.json['task']
    if task in db and db[task]['end'] is None:
        return jsonify({'status': 'error', 'message': 'Task is already running.'})

    db[task] = {'start': datetime.now().isoformat(), 'end': None}
    return jsonify({'status': 'started', 'task': task, 'start_time': db[task]['start']})

@app.route('/stop', methods=['POST'])
def stop():
    task = request.json['task']
    if task not in db or db[task]['end'] is not None:
        return jsonify({'status': 'error', 'message': 'Task is not running.'})

    db[task]['end'] = datetime.now().isoformat()
    return jsonify({'status': 'stopped', 'task': task, 'start_time': db[task]['start'], 'end_time': db[task]['end']})

@app.route('/pause', methods=['POST'])
def pause():
    task = request.json['task']
    if task not in db or db[task]['end'] is not None:
        return jsonify({'status': 'error', 'message': 'Task is not running.'})

    db[task]['end'] = datetime.now().isoformat()
    return jsonify({'status': 'paused', 'task': task, 'start_time': db[task]['start'], 'end_time': db[task]['end']})

@app.route('/resume', methods=['POST'])
def resume():
    task = request.json['task']
    if task not in db or db[task]['end'] is None:
        return jsonify({'status': 'error', 'message': 'Task is not paused.'})

    db[task] = {'start': datetime.now().isoformat(), 'end': None}
    return jsonify({'status': 'resumed', 'task': task, 'start_time': db[task]['start']})
    

############################################

# Abmelde-Routen
@app.route('/logout')
def logout():
    # Sitzung beenden und den Nutzer ausloggen
    session.clear()  # Löscht alle Sitzungsvariablen und setzt die Sitzung zurück

    # Weiterleitung zur Startseite
    return redirect(url_for('index'))

# Registrierungsseite
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        # Überprüfung, ob der Benutzer bereits existiert
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employee WHERE email = ?', (email,))
        employee = cursor.fetchone()
        if employee:
            return 'Ein Benutzer mit dieser E-Mail-Adresse existiert bereits!'

        # Speichern des Benutzers in der Datenbank
        add_employee(first_name, last_name, email, password)

        # Erfolgsmeldung für die Template-Variable festlegen
        success_message = 'Registrierung erfolgreich!'

        return render_template('register.html', message=success_message)

    return render_template('register.html')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=False, host='0.0.0.0')
