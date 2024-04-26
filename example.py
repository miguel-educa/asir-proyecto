from blockchain import Bloque, Blockchain


# Generar cadena
miguel_chain = Blockchain()

# Agregar bloques
miguel_chain.add_bloque(Bloque(0, 0, {'usuario': 'U_001', 'voto': 'Candidato A'}, ""))
miguel_chain.add_bloque(Bloque(0, 0, {'usuario': 'U_002', 'voto': 'Candidato A'}, ""))
miguel_chain.add_bloque(Bloque(0, 0, {'usuario': 'U_003', 'voto': 'Candidato B'}, ""))
miguel_chain.add_bloque(Bloque(0, 0, {'usuario': 'U_004', 'voto': 'Candidato B'}, ""))
miguel_chain.add_bloque(Bloque(0, 0, {'usuario': 'U_005', 'voto': 'Candidato A'}, ""))

# Mostrar bloques
print()
print("Miguel Chain:")
print("--------------------")
for block in miguel_chain.chain:
    print("Index:", block.index)
    print("Timestamp:", block.timestamp)
    print("Data:", block.data)
    print("Previous Hash:", block.prev_hash)
    print("Hash:", block.hash)
    print("--------------------")

# Verificar cadena
print()
print("¿La cadena es válida?", miguel_chain.validar_cadena())
input('Pulsa ENTER para continuar')

# Modificación de un bloque
print()
print("********************************************************")
print("¿Qué ocurre si se modifica el valor de un dato?")
modificar_index = int(input("Index del bloque a modificar: "))
modificar_dato = input("Dato modificado: ")
print("********************************************************")
print()

# Modificación y minado de un bloque
bloque_modificar = miguel_chain.chain[modificar_index]
bloque_modificado = Bloque(bloque_modificar.index, 0, modificar_dato, bloque_modificar.prev_hash)
bloque_modificado.minar_bloque()
miguel_chain.chain[modificar_index] = bloque_modificado

# Mostrar bloques de la cadena modificada
print()
for block in miguel_chain.chain:
    print("Index:", block.index)
    print("Timestamp:", block.timestamp)
    print("Data:", block.data)
    print("Previous Hash:", block.prev_hash)
    print("Hash:", block.hash)
    print("--------------------")

# Verificar cadena modificada
print()
print("¿La cadena es válida?", miguel_chain.validar_cadena())
