from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ponto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ponto ORDER BY id DESC")
    registros = cursor.fetchall()
    conn.close()
    return render_template('index.html', registros=registros)

@app.route('/registrar', methods=['POST'])
def registrar():
    nome = request.form['nome']
    tipo = request.form['tipo']
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ponto (nome, tipo, data_hora) VALUES (?, ?, ?)",
                   (nome, tipo, data_hora))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
