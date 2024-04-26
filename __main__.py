from flask import Flask, jsonify, request, render_template
from blockchain import Bloque, Blockchain
import random


# Creación de una app Flask
app = Flask(__name__)

# Inicio de la cadena
miguel_chain = Blockchain()

# Primeros 24 votos aleatorios
candidatos = ['A','B','C','D']
for i in range(1,25):
    candidato_votado = candidatos[random.randint(0,3)]
    miguel_chain.add_bloque(
        Bloque(0, 0, {'usuario': f'U_{str(i)}', 'voto': f'Candidato {candidato_votado}'}, '')
    )

# Rutas html
@app.route('/')
def index_html():
    return render_template('index.html')

@app.route('/editar')
def editar_html():
    return render_template('editar.html')

@app.route('/login')
def login_html():
    return render_template('login.html')

@app.route('/resultado')
def resultado_html():
    return render_template('resultado.html')

@app.route('/votar/<dni>')
def votar_html(dni):
    return render_template('votar.html', dni=dni)


# Rutas API
@app.route('/add_bloque', methods=['POST'])
def add_bloque():
    '''
    Añade un bloque a la cadena
    '''
    data_api = request.get_json()

    # Comprueba si el votante ha votado
    usuario = data_api['usuario']
    for bloque in miguel_chain.chain:
        if usuario in bloque.data.values():
            return jsonify({'message': 'El usuario ya ha votado'})

    # Crea, mina y añade un bloque a la cadena
    data = {
        'usuario': usuario,
        'voto': data_api['voto']
    }
    miguel_chain.add_bloque(Bloque(0, 0, data, ""))

    return jsonify({'message': 'El bloque se ha añadido correctamente'})


@app.route('/get_chain', methods=['GET'])
def get_chain():
    '''
    Devuelve el contenido de la cadena y comprueba si es válida
    '''
    data = []

    # Comprobar validez de la cadena
    if not miguel_chain.validar_cadena():
        data.append(
            {
                'error': 'cadena modificada!'
            }
        )

    # Devolver cadena excepto el bloque génesis
    for bloque in miguel_chain.chain[1:]:
        data.append(bloque.data)

    return jsonify(data)


@app.route('/modify/<index>/<voto>')
def modificar(index, voto):
    '''
    Modifica el contenido de un bloque cuyo índice es un parámetro
    '''
    # Modificación de un bloque
    modificar_index = int(index)
    modificar_data = {
        'usuario': 'Editado',
        'voto': 'Candidato '+voto.upper()
    }
    bloque_modificar = miguel_chain.chain[modificar_index]
    bloque_modificado = Bloque(
        bloque_modificar.index, 0, modificar_data, bloque_modificar.prev_hash
    )

    # Minar bloque modificado
    bloque_modificado.minar_bloque()
    miguel_chain.chain[modificar_index] = bloque_modificado

    return jsonify(['Editado con éxito'])


# Programa
if __name__ == '__main__':
    app.run()
