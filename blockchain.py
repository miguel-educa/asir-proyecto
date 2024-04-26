import datetime
import hashlib


class Bloque:
    def __init__(self, index, timestamp, data, prev_hash):
        '''
        Iniciar un bloque.
        Índice
        TimeStamp
        Datos
        Hash del bloque anterior
        Nonce
        Hash del bloque
        '''
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.calcular_hash()

    def calcular_hash(self):
        '''
        Calcula el hash del bloque
        '''
        bloque_hash = str(self.index) + str(self.timestamp) + str(self.data) + str(self.prev_hash) + str(self.nonce)
        return hashlib.sha256(bloque_hash.encode()).hexdigest()

    def minar_bloque(self):
        '''
        Minado de un bloque para añadirlo a la cadena.
        Aumentar cant_ceros para mayor dificultad o viceversa
        '''
        cant_ceros = 3
        n_ceros = "0" * cant_ceros

        # Búsqueda del Nonce para encontrar un hash válido
        while self.hash[:cant_ceros] != n_ceros:
            self.nonce += 1
            self.timestamp = datetime.datetime.now().timestamp()
            self.hash = self.calcular_hash()
            print(f"{self.nonce}: {self.hash}") # Mostrar el Nonce y el hash generado
        print('Minado realizado con éxito')

class Blockchain:
    def __init__(self):
        '''
        Iniciar cadena con el Bloque Génesis
        '''
        self.chain = [self.crear_bloque_genesis()]

    def crear_bloque_genesis(self):
        '''
        Creación del Bloque Génesis
        '''
        return Bloque(0, datetime.datetime.now().timestamp(), {'Bloque génesis': True}, "0")

    def obtener_bloque_anterior(self):
        '''
        Devuelve el bloque anterior de la cadena
        '''
        return self.chain[-1]

    def add_bloque(self, bloque_nuevo):
        '''
        Añade un nuevo bloque a la cadena después de minar
        '''
        # Obtener hash del bloque previo y nuevo index
        bloque_nuevo.prev_hash = self.obtener_bloque_anterior().hash
        bloque_nuevo.index = self.obtener_bloque_anterior().index + 1

        # Minar y añadir
        bloque_nuevo.minar_bloque()
        self.chain.append(bloque_nuevo)

    def validar_cadena(self):
        '''
        Comprobar si la cádena es válida o ha sido modificada.
        Se comprueban todos los bloques de la cadena
        '''
        for i in range(1, len(self.chain)):
            bloque_actual = self.chain[i]
            bloque_anterior = self.chain[i - 1]

            # Comparar hash actual con el hash almacenado en el bloque actual
            if bloque_actual.hash != bloque_actual.calcular_hash():
                return False

            # Comparar hash del bloque anterior con el hash del bloque anterior almacenado en el bloque actual
            if bloque_actual.prev_hash != bloque_anterior.hash:
                return False

        return True
