from time import sleep
import cerebro
import time
import graphics
from graphics import Point
import modelos


ancho = 500
alto = 500
desp_x = ancho / 8
desp_y = alto / 8
ganar = graphics.GraphWin("Damas", ancho, alto)


def dibujarTablero():
    desp_color = False
    for x in range(0, 8):
        if x % 2 == 1:
            desp_color = True
        else:
            desp_color = False
        for y in range(0, 8):
            punto = Point(x * desp_x, y * desp_y)
            caja = graphics.Rectangle(punto, Point(punto.x + desp_x, punto.y + desp_y))
            caja.setFill("Gray")
            if desp_color:
                if x % 2 == 0 or y % 2 == 0:
                    caja.setFill("#c2ab56")
            elif x % 2 == 1 or y % 2 == 1:
                caja.setFill("#c2ab56")
            caja.draw(ganar)


def dibujarDamas():
    for pieza in modelos.tablero.flat:
        if pieza.dama is not None:
            circulo = graphics.Circle(Point(pieza.centro[0], pieza.centro[1]), 15)
            if pieza.dama.negra:
                circulo.setFill("Black")
            else:
                circulo.setFill("White")
            circulo.draw(ganar)


def encontrarPieza(click):
    click_x = click.x/62.5
    click_y = click.y/62.5
    for x in range(0, 8):
        for y in range(0, 8):
            if (click_x > x and click_y > y) and (click_x < x+1 and click_y < y+1):
                return (x, y)
    return None





def redibujar():
    for hijo in ganar.children:
        hijo.undraw()
    dibujarTablero()
    dibujarDamas()


def correrMinimax(color):
    t1 = time.time()
    movimiento_minimax = cerebro.minimax(0, color, modelos.tablero, float("-inf"), float("inf"))
    print(movimiento_minimax.peso)
    t2 = time.time()
    print(t2-t1)
    #modelos.ttable.guardar()
    modelos.ttable.tablahash = {}
    movimiento_minimax.aplicar(modelos.tablero)
    redibujar()
    return movimiento_minimax


def escojerDiferencia():
    diferenciaGanar = graphics.GraphWin("Escoger dificultad")
    diferenciaGanar.focus()
    entrada = graphics.Entry(Point(100, 100), 20)
    entrada.setText("2")
    entrada.draw(diferenciaGanar)
    diferenciaGanar.getMouse()
    cerebro.DIFFICULTY = int(entrada.getText())
    diferenciaGanar.close()

def turnoJugador(color):
    while True:
        click1 = ganar.getMouse()
        dama = encontrarPieza(click1)
        if dama is None or modelos.tablero[int(dama[0]), int(dama[1])].dama is None or modelos.tablero[int(dama[0]), int(dama[1])].dama.negra is not color:
            continue
        click2 = ganar.getMouse()
        pieza = encontrarPieza(click2)
        if pieza is None or (pieza[0] == dama[0] and pieza[1] == dama[1]):
            continue
        movimiento_parcial = cerebro.Movimiento(modelos.tablero[int(dama[0]), int(dama[1])].dama, modelos.tablero[int(pieza[0]), int(pieza[1])],"?")
        movimiento_parcial.dama.x = dama[0]
        movimiento_parcial.dama.y = dama[1]
        move = modelos.getMovimientoCompleto(movimiento_parcial)
        if move is None:
            continue
        else:
            move.aplicar(modelos.tablero)
            redibujar()
            return

def dibujar():
    escojerDiferencia()
    dibujarTablero()
    dibujarDamas()
    while modelos.haGanado(modelos.tablero) == 0:
        sleep(0.01)
        modelos.Rey(modelos.tablero)
        turnoJugador(False)
        modelos.Rey(modelos.tablero)
        ganar.update()
        correrMinimax(True)
    ventanaGanar = graphics.GraphWin("Terminado")
    if modelos.haGanado(modelos.tablero) == 1:
        text = graphics.Text(Point(ventanaGanar.ancho/2, ventanaGanar.alto/2), "Ganaste")
        text.draw(ventanaGanar)
        sleep(3)
    elif modelos.haGanado(modelos.tablero) == -1:
        text = graphics.Text(Point(ventanaGanar.ancho / 2, ventanaGanar.alto / 2), "Perdiste")
        text.draw(ventanaGanar)
        sleep(3)
    return




