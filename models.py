import sqlite3
import pyodbc

# Verbindung zur SQLite-Datenbank herstellen
def get_db_connection():
    conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:antocars.database.windows.net,1433;Initial Catalog=employees;Persist Security Info=False;User ID=Carsten;Password=!Testing1234;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;")
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
