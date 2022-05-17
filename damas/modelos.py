import copy
import pickle
import random
import numpy
import cerebro



# Piezas del tablero
class Pieza():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.centro = [x + 25, y + 25]
        self.dama = None

# Copias completas del tablero para minimax
def copiarTablero(origen):
    nuevo_tablero = copy.deepcopy(origen)
    for pieza in tablero.flat:
        nuevo_tablero[int(pieza.x / 62.5), int(pieza.y / 62.5)
                  ] = copy.deepcopy(pieza)
        nuevo_tablero[int(pieza.x / 62.5), int(pieza.y / 62.5)
                  ].dama = copy.deepcopy(pieza.dama)
    return nuevo_tablero

# Una dama en el tablero
class Dama():
    def __init__(self):
        self.viva = True
        self.rey = False
        self.x = None
        self.y = None
        self.negra = False
        self.circulo = None
        self.id = None
        self.indice = None


def mueveDama(dama, pieza):
    pieza.dama = dama
    dama.circulo.movimiento(pieza.centro[0], pieza.centro[1])


# El tablero principal
tablero = numpy.empty((8, 8), dtype=Pieza)
damas = []

def agregaDamas(x, y):
    if y == 3 or y == 4:
        return
    dama = Dama()
    dama.id = (x, y)
    dama.indice = x*8 + (y+1)
    if y < 4:
        dama.negra = True
    dama.x = x
    dama.y = y
    tablero[x, y].dama = dama
    damas.append(dama)


# Inicializa el tablero
for x in range(0, 8):
    if x % 2 == 1:
        movimiento_pieza = True
    else:
        movimiento_pieza = False
    for y in range(0, 8):
        pieza = Pieza(x * 62.5, y * 62.5)
        tablero[x, y] = pieza
        if (x % 2 == 0 or y % 2 == 0) and (movimiento_pieza == True):
            agregaDamas(x, y)
        elif (x % 2 == 1 or y % 2 == 1) and (movimiento_pieza == False):
            agregaDamas(x, y)


def Rey(tablero):
    for pieza in tablero.flat:
        if pieza.dama is None or pieza.dama.rey:
            continue
        if (pieza.y / 62.5 == 7 and pieza.dama.negra) or (pieza.y / 62.5 == 0 and not pieza.dama.negra):
            pieza.dama.rey = True


def getMovimientoCompleto(movimiento_parcial):
    movimientos = cerebro.encuentraSaltos(tablero, False) + cerebro.encuentraMovimientos(tablero, False)
    for movimiento in movimientos:
        if movimiento.dama.id == movimiento_parcial.dama.id and movimiento.pieza.x == movimiento_parcial.pieza.x \
                and movimiento.pieza.y == movimiento_parcial.pieza.y:
            return movimiento
    return None


def haGanado(tablero):
    acciones_blancas = cerebro.encuentraSaltos(tablero, False) + cerebro.encuentraMovimientos(tablero, False)
    acciones_negras = cerebro.encuentraSaltos(tablero, True) + cerebro.encuentraMovimientos(tablero, True)
    if len(acciones_blancas) == 0:
        return -1
    elif len(acciones_negras) == 0:
        return 1
    else:
        return 0

tabla_zobrist = numpy.zeros((8, 8, 64))

for i in range(0,8):
    for j in range(0,8):
        for k in range(0,64):
            tabla_zobrist[i,j,k] = random.randint(0, 1000000)

def movimientoAHash(movimiento, tablero, profundidad):
    hsh = 0
    for pieza in tablero.flat:
        if pieza.dama is None:
            continue
        dama = pieza.dama
        hsh = hsh ^ int(tabla_zobrist[int(pieza.x/62.5), int(pieza.y/62.5), pieza.dama.indice])
    hsh += hash(str(movimiento.dama.id) + str(movimiento.dama.x) + str(movimiento.dama.y))
    return hsh



class TablaTranspuesta():
    def __init__(self):
        self.tablahash = {}
            
    def insertar(self, movimiento, tableroN, profundidad):
        indice = movimientoAHash(movimiento, tableroN, profundidad)
        self.tablahash[indice] = movimiento.peso
    
    def buscar(self, movimiento, tableroN, profundidad):
        indice = movimientoAHash(movimiento, tableroN, profundidad)
        return self.tablahash[indice]
    def guardar(self):
        save_file = open('guardar.dat', 'wb')
        pickle.dump(self.tablahash, save_file)
        save_file.close()

ttable = TablaTranspuesta()

