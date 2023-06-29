import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
def get_db_connection():
    conn = sqlite3.connect('employees.db')
    conn.row_factory = sqlite3.Row
    return conn

# Benutzer in der Datenbank speichern
def add_employee(first_name, last_name, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO employee (first_name, last_name, email, password) VALUES (?, ?, ?, ?)', (first_name, last_name, email, password))
    conn.commit()
    conn.close()

# Benutzer anhand der E-Mail-Adresse abrufen
def get_employee_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employee WHERE email = ?', (email,))
    employee = cursor.fetchone()
    conn.close()
    return employee
