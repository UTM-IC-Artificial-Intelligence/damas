# Damas
Chckers

## Definición del problema
Las damas es un juego de mesa para dos contrincantes. El juego consiste en mover las piezas en diagonal a través de los cuadros negros de un tablero de 64 cuadros. Si alguien no mata (captura), perderá esa pieza al jugar contrario a la intención obligatoria de capturar (comer) las piezas del jugador contrario, pasando por encima de dichas piezas.

## Complejidad. 

| *Caracteriscias*    |  *Tamaño*      |
|--------|--------------|
| Tamaño del Tablero      |  64           |
| Tamaño de estados      |  40           |
| Duración de partida    |  70           |
| Factor de ramifiacion     |  2.8           |


## Ejemplo
Aqui se muestra un ejemplo del tableros de las Damas y como se juega.
![Juego de Damas](https://upload.wikimedia.org/wikipedia/commons/4/44/Column_draughts_game.gif)

## Modelo
Las damas es un juego para dos personas en un tablero de 64 casillas de 8×8 celdas (el mismo que se utiliza para jugar al ajedrez). El tablero se coloca de manera que cada jugador tenga una casilla blanca en su parte inferior derecha.

Cada jugador dispone de 12 piezas de un mismo color (unas blancas y las otras negras) que al principio de la partida se colocan en las casillas negras de las tres filas más próximas a él. El objetivo del juego de damas es capturar las fichas del oponente o acorralarlas para que los únicos movimientos que puedan realizar sean los que lleven a su captura (excepto las damas rusas, la variante poddavki, en la que gana quién se queda sin fichas o las que tiene están bloqueadas).
Se juega por turnos alternos. Empieza a jugar quien tiene las fichas claras (blancas). En su turno cada jugador mueve una pieza propia.
Las piezas se mueven (cuando no comen) una posición hacia delante hacia atrás en diagonal a la derecha o a la izquierda, a una posición adyacente vacía.
Al momento de comer piezas del oponente, se pueden comer varias en un mismo turno de forma diagonal hacia la derecha e izquierda, adelante y atrás. Soplar (o comer) no es obligatorio, es una decisión del jugador de turno. 

**Formas de ganar**
    Gana cuando el rival se queda sin fichas.
    Se gana cuando el rival no pueda hacer un movimiento de comer.


## Representación del espacio de búsquedas

- Espacio de estados : Movimiento de las fichas en diagonal hacia izquierda o derecha
- Estado inicial: 12 fichas negras y 12 fichas blancas
- Estado final: Ninguna ficha del rival en el tablero
- Operadores: Mover una ficha en diagonal izquierda o derecha
    - Condiciones: Si se mueve solo es salto de 1 casillas y si come pueden ser 2 casillas y quitar un ficha.
    - Transformación: Alterar las fichas del tablero.
 
##Representacion del arbol.
![Arbol de damas](https://raw.githubusercontent.com/AboorvaDevarajan/Parallel-Checkers-Game/master/images/1.png)
