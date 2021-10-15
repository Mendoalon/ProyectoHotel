from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "Secret Key"

app.config['SECRET_KEY'] = 'Esteesmimejorsecretoguardado!'

# aqui se define la base de datos que vamos a usar 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/mc/projects/room/room.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Aqui se crea la tabla para todo nuestro proceso de CRUD de la base de datos
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))
    piso = db.Column(db.String(20))
    numero = db.Column(db.String(4))

    def __init__(self, tipo, piso, numero):

        self.tipo = tipo
        self.piso = piso
        self.numero = numero


# Esta es la ruta index donde vamos hacer las consultas de la base de datos
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", xrooms=all_data)


# esta es la ruta insert para agregar  habitaciones usando formas en html
@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':

        tipo = request.form['tipo']
        piso = request.form['piso']
        numero = request.form['numero']

        my_data = Data(tipo, piso, numero)
        db.session.add(my_data)
        db.session.commit()

        flash("La habitación ha sido agregada")

        return redirect(url_for('Index'))

 
# Esta es la ruta update cuando se va a modificar una habitacion
@app.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.tipo = request.form['tipo']
        my_data.piso = request.form['piso']
        my_data.numero = request.form['numero']

        db.session.commit()
        flash("La habitación ha sido modificada y tambien actualizada ")

        return redirect(url_for('Index'))


# Esta es la ruta delete cuando se va eliminar  una habitacion
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    
    db.session.commit()
    flash("El registro de la habitación ha sido eliminado exitosamnete")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)


