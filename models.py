import sqlite3
import pyodbc
import os

# Verbindung zur SQLite-Datenbank herstellen
def get_db_connection():
    conn = pyodbc.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()
    return conn, cursor

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
