from pydoc import visiblename
import numpy as np
import copy
import collections

from sympy import re, root

tablero0 = [
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]]
listT = [[]]
listT.append([tablero0])

class nodo:
  def __init__(self, data):
    self.hijos = []
    self.data = data

root = nodo(tablero0)


def movPosibles(root):
  limite = -1
  for x in range(8):
    for y in range(8):
      if root.data[x][y] == 2:
        if y == 0:
          if root.data[x+1][y+1] == 0:
            tableroCopy = copy.deepcopy(root.data)  
            tableroCopy[x+1][y+1] = 2
            tableroCopy[x][y] = 0
            root.hijos.append(nodo(tableroCopy))
        if y == 7:
          if root.data[x+1][y-1] == 0:
            tableroCopy = copy.deepcopy(root.data) 
            tableroCopy[x+1][y-1] = 2
            tableroCopy[x][y] = 0
            root.hijos.append(nodo(tableroCopy))
        else:
          if root.data[x+1][y+1] == 0:
            tableroCopy = copy.deepcopy(root.data) 
            tableroCopy[x+1][y+1] = 2
            tableroCopy[x][y] = 0
            root.hijos.append(nodo(tableroCopy))

          if root.data[x+1][y-1] == 0:
            tableroCopy = copy.deepcopy(root.data) 
            tableroCopy[x+1][y-1] = 2
            tableroCopy[x][y] = 0
            root.hijos.append(nodo(tableroCopy))
  return root


root = movPosibles(root)


#for x in range(len(root.hijos)):
#  root.hijos[x] = movPosibles(root.hijos[x])

# print("Soy padre y tengo ", len(root.hijos), " hijos")
# for y in range(8):
#     for z in range(8):
#       print(root.data[y][z], end=" ")
#     print()

# for x in range(len(root.hijos)):
#   print("Hijo numero: ", x,  "Y padre de: ",len(root.hijos[x].hijos))
#   for y in range(8):
#     for z in range(8):
#       print(root.hijos[x].data[y][z], end=" ")
#     print()
#   for t in range(len(root.hijos[x].hijos)):
#     print("Hijo numero: ", t, "de ", x)
#     for o in range(8):
#       for k in range(8):
#         print(root.hijos[x].hijos[t].data[o][k], end=" ")
#       print()

def convertir(nodoC):
  tablerMx = []
  band = 0
  tableroRow = []
  for x in range(len(nodoC)):
    if band < 8:
      if nodoC[x] == "0" or  nodoC[x] == "1" or nodoC[x] == "2":
        tableroRow.append(int(nodoC[x]))
        band = band + 1
    else:
      band = 0
      tablerMx.append(tableroRow)
      tableroRow = []
  
  return tablerMx

def encuentraEmpate(tablero):
  for x in range(8):
    for y in range(8):
      if tablero[x][y] == 2:
        if y == 0:
          if tablero[x+1][y+1] == 1:
            return True
        if y == 7:
          if tablero[x+1][y-1] == 1:
            return True
        else:
          if root.data[x+1][y+1] == 1:
            return True

          if root.data[x+1][y-1] == 1:
            return True
  return False 

def extrerHijos(root):
  hijos = []
  for x in range(len(root.hijos)):
    hijos.append(str(root.hijos[x].data))
  return hijos

grafo = {
   str(root.data) : extrerHijos(root),
   str(root.hijos[0].data) : extrerHijos(root.hijos[0]),
   str(root.hijos[1].data) : extrerHijos(root.hijos[1]),
   str(root.hijos[2].data) : extrerHijos(root.hijos[2]),
   str(root.hijos[3].data) : extrerHijos(root.hijos[3]),
   str(root.hijos[4].data) : extrerHijos(root.hijos[4]),
   str(root.hijos[5].data) : extrerHijos(root.hijos[5]),
   str(root.hijos[6].data) : extrerHijos(root.hijos[6]),
 } 

def dfs(visitado, grafo, nodo):
  if nodo not in visitado:
    if encuentraEmpate(convertir(nodo)) == True:
      print(nodo)
      return 
        
    visitado.add(nodo)
    print("visitado")
    for vecino in grafo[nodo]:
      dfs(visitado, grafo, vecino)


visitado = set()

dfs(visitado, grafo, str(root.data))
   