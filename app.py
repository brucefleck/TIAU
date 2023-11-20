from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId
from flask import url_for
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://admin123:admin123@Obelisk.lkhnesk.mongodb.net/Obelisk"
mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro.html')
def registro_page():
    return render_template('registro.html')

@app.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    if request.method == "POST":
        nombre = request.form['input-nombre']
        correo = request.form['input-correo']
        password = request.form['input-contrasenia']
        confirm_password = request.form['input-confirm-contrasenia']

        # Check if passwords match
        if password != confirm_password:
            # Handle password mismatch error (redirect, show error message, etc.)
            return render_template('registro.html', error="Las contraseñas no coinciden")

        # Insert user data into MongoDB
        usuario_id = ObjectId()
        db.Usuarios.insert_one({
            '_id': usuario_id,
            'nombre': nombre,
            'email': correo,
            'password': password
        })

        # Redirect to login page
        return render_template('index.html')

@app.route("/procesar_login", methods=['POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasenia = request.form['contrasenia']

        # Consultar el usuario en la base de datos
        usuario = db.Usuarios.find_one({'email': correo})

        if usuario and usuario['password'] == contrasenia:
            # Iniciar sesión del usuario (usando el módulo de sesiones de Flask)
            session['usuario_id'] = str(usuario['_id'])
            return redirect(url_for('inicio.html'))  # Cambia 'perfil' por la ruta de tu perfil de usuario

    return render_template('inicio.html')

@app.route('/makepost', methods=['POST'])
def crear_post():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['text-input']

        # Insert post data into MongoDB
        post_id = ObjectId()
        db.publicaciones.insert_one({
            '_id': post_id,
            'titulo': titulo,
            'contenido': contenido
        })
    return render_template('inicio.html')

#@app.route('/publicacion/<post_id>')
#def mostrar_publicacion(post_id):
#        # Obtener la publicación de la base de datos usando el ID
#        publicacion = db.publicaciones.find_one({'_id': ObjectId(post_id)})
#
#        # Renderizar la plantilla HTML y pasar la publicación como argumento
#        return render_template('inicio.html', publicacion=publicacion)
    
@app.route('/crear_comentario', methods=['POST'])
def guardar_comentario():
        if request.method == 'POST':
            comentario = request.form['comentario']

            # Insertar datos del comentario en MongoDB
            comentario_id = ObjectId()
            db.comentarios.insert_one({
                '_id': comentario_id,
                'comentario': comentario
            })

            # Redirigir a la página de inicio o a donde desees
            return render_template('inicio.html')

        # Si no se realiza una solicitud POST, redirigir a la página de inicio
        return render_template('inicio.html')

if __name__ == '_main_':
    app.run(debug=True)
