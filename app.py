from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/registro.html')
def registro():
    return render_template('registro.html')

@app.route('/process_login', methods=['POST'])
def process_login():
    correo = request.form['correo']
    contrasenia = request.form['contrasenia']

    return redirect(url_for('homepage'))

@app.route('/homepage.html')
def homepage():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)

