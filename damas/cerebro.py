from regex import R
import modelos
from copy import deepcopy

def tomarDama(x, y, tablero):
    tablero[x, y].dama = None


DIFICULTAD = 2


def ponerDificultad(val):
    DIFICULTAD = val


class Movimiento():
    def __init__(self, dama, pieza, variante):
        self.dama = dama
        self.pieza = pieza
        self.tipo = variante
        self.distancia = 1
        self.peso = None
        self.saltado = []
        self.otraspiezas = []

    # Aplicar movimientos a un tablero dado
    def aplicar(self, tablero):
        dama_x = self.dama.x
        dama_y = self.dama.y
        nuevo_x = self.pieza.x / 62.5
        nuevo_y = self.pieza.y / 62.5
        tablero[int(dama_x), int(dama_y)].dama = None
        tablero[int(nuevo_x), int(nuevo_y)].dama = deepcopy(self.dama)
        tablero[int(nuevo_x), int(nuevo_y)].dama.x = tablero[int(
            nuevo_x), int(nuevo_y)].x / 62.5
        tablero[int(nuevo_x), int(nuevo_y)].dama.y = tablero[int(
            nuevo_x), int(nuevo_y)].y / 62.5
        for pieza in self.saltado:
            tablero[int(pieza.x / 62.5), int(pieza.y / 62.5)].dama = None
        return tablero
    

def encontrarVecino(tablero, x, y, arriba=False, abajo=False):
    vecinos = []
    if not arriba:
        if x != 7 and y != 7:
            vecinos.append(tablero[int(x + 1), int(y + 1)])
        if x != 0 and y != 7:
            vecinos.append(tablero[int(x - 1), int(y + 1)])
    if not abajo:
        if x != 7 and y != 0:
            vecinos.append(tablero[int(x + 1), int(y - 1)])
        if x != 0 and y != 0:
            vecinos.append(tablero[int(x - 1), int(y - 1)])
    return vecinos


# comprueba si 2 conjuntos de posiciones de pieza se están arrinconando entre sí
def checarVecino(x, y, px, py, arriba=False, abajo=False, dir=-1):
    resultados = []
    if not arriba:
        if (x == px + 1 and y == py + 1):
            # Suroeste
            resultados.append(0)
            if dir == 0:
                resultados = [0]
                return resultados
        if (x == px - 1 and y == py + 1):
            # Sureste
            resultados.append(1)
            if dir == 1:
                resultados = [1]
                return resultados
    if abajo:
        if resultados == []:
            resultados.append(-1)
        return resultados
    if (x == px + 1 and y == py - 1):
        # Noroeste
        resultados.append(2)
        if dir == 2:
            resultados = [2]
            return resultados
    if (x == px - 1 and y == py - 1):
        # Noreste
        resultados.append(3)
        if dir == 3:
            resultados = [3]
            return resultados
    if resultados == []:
        resultados.append(-1)
    return resultados


# Encuentra los movimientos de un paso que se pueden realizar
def encuentraMovimientos(tablero, color):
    movimientos = []
    for pieza in tablero.flat:
        if pieza.dama is None or pieza.dama.negra != color:
            continue
        opciones = []
        if pieza.dama.rey:
            pieces = encontrarVecino(tablero, pieza.x / 62.5, pieza.y / 62.5)
        elif color:
            pieces = encontrarVecino(tablero, pieza.x / 62.5,
                                  pieza.y / 62.5, abajo=True)
        elif not color:
            pieces = encontrarVecino(tablero, pieza.x / 62.5,
                                  pieza.y / 62.5, arriba=True)
        for nueva_pieza in pieces:
            direcciones = []
            if color is True or pieza.dama.rey:
                direcciones.append(checarVecino(nueva_pieza.x / 62.5, nueva_pieza.y /
                                          62.5, pieza.x / 62.5, pieza.y / 62.5, abajo=True))
            if color is False or pieza.dama.rey:
                direcciones.append(checarVecino(nueva_pieza.x / 62.5, nueva_pieza.y /
                                          62.5, pieza.x / 62.5, pieza.y / 62.5, arriba=True))
            for direccion in direcciones:
                if direccion[0] != -1:
                    opciones.append(nueva_pieza)

        for opcion in opciones:
            if opcion.dama == None:
                movimientos.append(Movimiento(pieza.dama, opcion, "Movimiento"))
    return movimientos


# Encuentra los saltos que se pueden hacer
def encuentraSaltos(tablero, color, viejo=None, profundidad=0):
    saltos = []
    for pieza in tablero.flat:
        if pieza.dama is None or pieza.dama.negra != color:
            continue
        opciones = []
        direcciones = []
        if pieza.dama.rey:
            pieces = encontrarVecino(tablero, pieza.x / 62.5, pieza.y / 62.5)
        elif color:
            pieces = encontrarVecino(tablero, pieza.x / 62.5,
                                  pieza.y / 62.5, abajo=True)
        elif not color:
            pieces = encontrarVecino(tablero, pieza.x / 62.5,
                                  pieza.y / 62.5, arriba=True)
        for nueva_pieza in pieces:
            direcciones2 = []
            if nueva_pieza.dama is None or nueva_pieza.dama.negra == color:
                continue
            if color is True or pieza.dama.rey:
                direcciones2.append(checarVecino(nueva_pieza.x / 62.5, nueva_pieza.y /
                                         62.5, pieza.x / 62.5, pieza.y / 62.5, abajo=True))
            if color is False or pieza.dama.rey:
                direcciones2.append(checarVecino(nueva_pieza.x / 62.5, nueva_pieza.y /
                                         62.5, pieza.x / 62.5, pieza.y / 62.5, arriba=True))
            for direccion in direcciones2:
                if direccion[0] != -1:
                    opciones.append(nueva_pieza)
                    direcciones.append(direccion[0])
        x = 0
        for opcion in opciones:
            nueva_pieza = None
            if opcion.x / 62.5 == 0 or opcion.x / 62.5 == 7 or opcion.y / 62.5 == 0 or opcion.y / 62.5 == 7:
                x += 1
                continue
            if direcciones[x] == 0:
                nueva_pieza = tablero[int(opcion.x / 62.5) + 1,
                                  int(opcion.y / 62.5) + 1]
                x += 1
            elif direcciones[x] == 1:
                nueva_pieza = tablero[int(opcion.x / 62.5 - 1),
                                  int(opcion.y / 62.5 + 1)]
                x += 1
            elif direcciones[x] == 2:
                nueva_pieza = tablero[int(opcion.x / 62.5 + 1),
                                  int(opcion.y / 62.5 - 1)]
                x += 1
            elif direcciones[x] == 3:
                nueva_pieza = tablero[int(opcion.x / 62.5 - 1),
                                  int(opcion.y / 62.5 - 1)]
                x += 1
            if nueva_pieza.dama is None:
                mueve = Movimiento(pieza.dama, nueva_pieza, "Salto")
                mueve.saltado.append(opcion)
                nuevo_tablero = modelos.copiarTablero(tablero)
                mueve.aplicar(nuevo_tablero)

                if profundidad < 2:
                    nuevos_saltos = encuentraSaltos(nuevo_tablero, color, opcion, profundidad + 1)
                    salto_extra = False
                    for salto in nuevos_saltos:
                        if salto.dama.id == pieza.dama.id:
                            salto_extra = True
                            salto.saltado.append(opcion)
                            salto.otraspiezas.append(nueva_pieza)
                            if viejo is not None:
                                salto.saltado.append(viejo)
                            salto.dama = pieza.dama
                            saltos.append(salto)
                    if not salto_extra:
                        saltos.append(mueve)
    return saltos


def distanciaAlRey(y, color):
    dif = None
    if color:
        dif = 7 - y
    elif not color:
        dif = y
    return dif

# Pesa al tablero en base a los movimientos disponibles
def pesaTablero(tablero, profundidad):
    movimientos_blancas = encuentraMovimientos(tablero, False) + encuentraSaltos(tablero, False)
    movimientos_negras = encuentraMovimientos(tablero, True) + encuentraSaltos(tablero, True)
    for mueve in movimientos_blancas:
        ocupaHash = True
        if modelos.movimientoAHash(mueve, tablero, profundidad) in modelos.ttable.tablahash:
            mueve.peso = modelos.ttable.buscar(mueve, tablero, profundidad)
            ocupaHash = False
        else:
            mueve.peso = 0
            if movimientoProtege(tablero, mueve, False):
                mueve.peso += 3
            if movimientoEnemigo(tablero, mueve, False):
                mueve.peso += -3
            if movimientoDesprotege(tablero, mueve, False):
                mueve.peso += -5
            if movimientoEscapa(tablero, mueve, False):
                mueve.peso += 4
            if movimientoHaceRey(tablero, mueve, False):
                mueve.peso += 6
            if len(movimientos_negras) == 3 and movimientoGana(tablero, mueve, False):
                mueve.peso += 200
            if mueve.tipo == "Salto":
                mueve.peso += 99 + len(mueve.saltado)
            if mueve.tipo != "Salto":
                modelos.ttable.insertar(mueve, tablero, profundidad)
    for mueve in movimientos_negras:
        ocupaHash = True
        if modelos.movimientoAHash(mueve, tablero, profundidad) in modelos.ttable.tablahash:
            mueve.peso = modelos.ttable.buscar(mueve, tablero, profundidad)
            ocupaHash = False
        else:
            mueve.peso = 0
            if movimientoProtege(tablero, mueve, True):
                mueve.peso += -3
            if movimientoEnemigo(tablero, mueve, True):
                mueve.peso += 3
            if movimientoDesprotege(tablero, mueve, True):
                mueve.peso += 5
            if movimientoEscapa(tablero, mueve, True):
                mueve.peso += -4
            if movimientoHaceRey(tablero, mueve, True):
                mueve.peso += -6
            if len(movimientos_blancas) == 3 and movimientoGana(tablero, mueve, True):
                mueve.peso += -200
            if mueve.tipo == "Salto":
                mueve.peso += -99 - len(mueve.saltado)
            if mueve.tipo != "Salto":
                modelos.ttable.insertar(mueve, tablero, profundidad)
    
    return (sorted(movimientos_blancas, key=lambda mueve: mueve.peso), sorted(movimientos_negras, key=lambda mueve: mueve.peso))

# Comprueba si un movimiento suicida una dama
def movimientoEnemigo(tablero, mueve, color):
    movimientos_enemigo = encuentraSaltos(mueve.aplicar(modelos.copiarTablero(tablero)), not color)
    for salto in movimientos_enemigo:
        for victima in salto.saltado:
            if victima.dama.id == mueve.dama.id:
                return True
    return False


# Comprueba si al mover protege dama
def movimientoProtege(tablero, mueve, color):
    movimientos_enemigo = encuentraSaltos(tablero, not color)
    for salto in movimientos_enemigo:
        for otrapieza in salto.otraspiezas:
            if otrapieza.x == mueve.pieza.x and otrapieza.y == mueve.pieza.y:
                return True
        if mueve.pieza.x == salto.pieza.x and mueve.pieza.y == salto.pieza.y:
            return True
    return False


# Comprueba si la dama  se hace rey
def movimientoHaceRey(tablero, mueve, color):
    if color:
        if mueve.pieza.x / 62.5 == 7:
            return True
    elif not color:
        if mueve.pieza.x / 62.5 == 0:
            return True

# Comprueba si puede hacer un salto el enemigo
def movimientoEscapa(tablero, mueve, color):
    movimientos_enemigo = encuentraSaltos(tablero, not color)
    for salto in movimientos_enemigo:
        for victima in salto.saltado:
            if victima.x / 62.5 == mueve.dama.x and victima.y / 62.5 == mueve.dama.y:
                return True
    return False


# Checa si el movimiento hace ganar

def movimientoGana(tablero, mueve, color):
    nuevo_tablero = mueve.aplicar(tablero)
    gana_val = 0
    if color:
        gana_val = -1
    else: 
        gana_val = 1
    if modelos.haGanado(tablero) == gana_val:
        return True
    else:
        return False

def movimientoDesprotege(tablero, mueve, color):
    saltos = encuentraSaltos(mueve.aplicar(modelos.copiarTablero(tablero)), not color)
    for salto in saltos:
        for otrapieza in salto.otraspiezas:
            if otrapieza.x/62.5 == mueve.dama.x and otrapieza.y/62.5 == mueve.dama.y:
                return True
        if salto.pieza.x/62.5 == mueve.dama.x and salto.pieza.y/62.5 == mueve.dama.y:
            return True

    return False

# hace el calculo para la accion MINIMAX
def minimax(profundidad, color, tablero, a, b):
    if profundidad == DIFICULTAD:
        movimientos = pesaTablero(tablero, profundidad)
        if color:
            movimientos_negras = movimientos[1]
            # Min
            # Regresa lo mejor para dama negra
            mini = None
            for mueve in movimientos_negras:
                if mini is None:
                    mini = mueve
                elif mini.peso > mueve.peso:
                    mini = mueve
                b = min(b, mini.peso)
                if b <= a:
                    break
            return mini
        else:
            movimientos_blancas = movimientos[0]
            # Max
            # Regresa lo mejor para dama blanca
            maxi = None
            for mueve in movimientos_blancas:
                if maxi is None:
                    maxi = mueve
                elif maxi.peso < mueve.peso:
                    maxi = mueve
                a = max(a, maxi.peso)
                if b <= a:
                    break
            return maxi

    mejor_movimiento = None
    if color:
        # Min
        # Evalua el movimiento futuro y las consecuencias
        movimientos_negras = encuentraMovimientos(tablero, True) + encuentraSaltos(tablero, True)
        if mejor_movimiento is not None:
            return mejor_movimiento

        for mueve in movimientos_negras:
            copy = modelos.copiarTablero(tablero)
            val = minimax(profundidad + 1, False, mueve.aplicar(copy), a, b)
            if mejor_movimiento is None or val.peso < mejor_movimiento.peso or mueve.tipo == "Salto":
                mejor_movimiento = val
            b = min(b, mejor_movimiento.peso)
            if b <= a:
                break

    else:
        # Evalua el movimiento futuro y las consecuencias
        movimientos_blancas = encuentraMovimientos(tablero, False) + encuentraSaltos(tablero, False)
        for mueve in movimientos_blancas:
            val = minimax(profundidad + 1, True,
                          mueve.aplicar(modelos.copiarTablero(tablero)), a, b)
            if mejor_movimiento is None or val.peso > mejor_movimiento.peso:
                mejor_movimiento = val
            a = max(a, mejor_movimiento.peso)
            if b <= a:
                break
    return mejor_movimiento

# hace el calculo para la accion Montercarlo
def montecarlo(profundidad, color, tablero, a, b):
    if profundidad == DIFICULTAD:
        movimientos = pesaTablero(tablero, profundidad)
        if color:
            movimientos_negras = movimientos[1]
        else:
            movimientos_blancas = movimientos[0]
    else:
        movimientos_blancas = encuentraMovimientos(tablero, False) + encuentraSaltos(tablero, False)
    mejor_movimiento = None
    return mejor_movimiento