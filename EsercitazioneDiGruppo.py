from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import csv
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="BlackDeath12!",
        database="PyDB"
    )

class Evento:
    def __init__(self, nome, categoria, prezzo, url):
        self.nome = nome
        self.categoria = categoria
        self.prezzo = prezzo
        self.url = url

@app.route('/')
def index():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM eventi")
    eventi = cursor.fetchall()
    db.close()
    return render_template('index.html', eventi=eventi)

@app.route('/gestore', methods=['GET', 'POST'])
def gestore():
    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        prezzo = request.form['prezzo']
        url = request.form['url']

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO eventi (nome, categoria, prezzo, url) VALUES (%s, %s, %s, %s)", 
                       (nome, categoria, prezzo, url))
        db.commit()
        db.close()

        flash('Evento aggiunto con successo!')
        return redirect(url_for('gestore'))

    return render_template('gestore.html')

@app.route('/categoria', methods=['POST'])
def eventi_per_categoria():
    categoria = request.form['categoria']
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM eventi WHERE categoria = %s", (categoria,))
    eventi = cursor.fetchall()
    db.close()
    return render_template('eventi_categoria.html', eventi=eventi)

@app.route('/rimuovi_evento', methods=['POST'])
def rimuovi_evento():
    evento_id = request.form['evento_id']
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM eventi WHERE id = %s", (evento_id,))
    db.commit()
    db.close()

    flash('Evento rimosso con successo!')
    return redirect(url_for('gestore'))

@app.route('/genera_csv')
def genera_csv():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM eventi")
    eventi = cursor.fetchall()

    # Scrivi i dati nel file CSV
    file_csv = 'eventi.csv'
    with open(file_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nome', 'Categoria', 'Prezzo', 'URL'])  # intestazione
        writer.writerows(eventi)

    db.close()
    flash('File CSV generato con successo!')
    return redirect(url_for('gestore'))

# Integrazione con API esterna
@app.route('/tracks')
def tracks():
    response = requests.get('https://openwhyd.org/hot/electro?format=json')
    track_list = response.json()
    return render_template('tracks.html', tracks=track_list)

if __name__ == '__main__':
    app.run(debug=True)
