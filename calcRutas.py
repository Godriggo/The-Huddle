import random
import time
import os

# CLASE MAPA
class Mapa:
    
    def __init__(self, alto, ancho):
        self.alto = alto
        self.ancho = ancho
        self.grid = [[0 for _ in range(ancho)] for _ in range(alto)]
        self.inicio = (0, 0)
        self.meta = (alto - 1, ancho - 1)

    #x = fila, y = columna
    def agregar_obstaculo(self, x, y, tipo_obstaculo=1):
        #Agrega un obstáculo: 1 = edificio, 2 = agua, 3 = bloqueo temporal.
        if (x, y) not in [self.inicio, self.meta]:
            self.grid[x][y] = tipo_obstaculo

    def quitar_obstaculo(self, x, y):
        #Elimina un obstáculo y vuelve la celda transitable.
        self.grid[x][y] = 0

    def generar_obstaculos_aleatorios(self, probabilidad=0.25):
        #Genera obstáculos aleatorios de diferentes tipos.
        tipos = [1, 2, 3]
        for x in range(self.alto):
            for y in range(self.ancho):
                if (x, y) in [self.inicio, self.meta]:
                    continue
                if random.random() < probabilidad:
                    self.grid[x][y] = random.choice(tipos)

    def mostrar_mapa(self, ruta=None):
        #Muestra el mapa con símbolos representativos.
        simbolos = {0: '.', 1: 'X', 2: '#', 3: '!'}
        for x in range(self.alto):
            linea = ''
            for y in range(self.ancho):
                if (x, y) == self.inicio:
                    linea += 'I '
                elif (x, y) == self.meta:
                    linea += 'M '
                elif ruta and (x, y) in ruta:
                    linea += '* '
                else:
                    linea += simbolos[self.grid[x][y]] + ' '
            print(linea)
        print()

    def celda_valida(self, x, y):
        #Comprueba si una celda está dentro del mapa y no es un edificio.
        if 0 <= x < self.alto and 0 <= y < self.ancho:
            return self.grid[x][y] != 1
        return False

    def vecinos(self, x, y):
        #Devuelve las celdas vecinas válidas (arriba, abajo, izquierda, derecha).
        posibles = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        vecinos_validos = []
        for dx, dy in posibles:
            if self.celda_valida(dx, dy) and self.grid[dx][dy] != 1:
                vecinos_validos.append((dx, dy))
        return vecinos_validos



# CLASE BUSCADOR DE RUTA (A*)
class BuscadorRuta:
    def __init__(self, mapa):
        self.mapa = mapa

    def heuristica(self, posicion_actual, posicion_meta):
        #Distancia Manhattan.
        return abs(posicion_actual[0] - posicion_meta[0]) + abs(posicion_actual[1] - posicion_meta[1])

    def costo_movimiento(self, x, y):
        #Costo del terreno según el tipo.
        tipo = self.mapa.grid[x][y]
        if tipo == 0:  # Camino libre
            return 1
        elif tipo == 2:  # Agua
            return 3
        elif tipo == 3:  # Bloqueo temporal
            return 5
        else:
            return float("inf")  # Edificio (intransitable)

    def encontrar_ruta(self, animar=True):
        #Aplica el algoritmo A* para encontrar la mejor ruta.
        inicio = self.mapa.inicio
        meta = self.mapa.meta
        
        lista_abierta = [self.mapa.inicio]
        lista_cerrada = []

        costos_g = {self.mapa.inicio: 0}
        origen = {self.mapa.inicio: None}

        while lista_abierta:
            # Ordenar lista por costo total estimado (g + h)
            lista_abierta.sort(key=lambda celda: costos_g[celda] + self.heuristica(celda, meta))
            celda_actual = lista_abierta.pop(0)
            lista_cerrada.append(celda_actual)

            if celda_actual == meta:
                break

            for vecino in self.mapa.vecinos(*celda_actual):
                if vecino in lista_cerrada:
                    continue

                costo_vecino = costos_g[celda_actual] + self.costo_movimiento(*vecino)

                if vecino not in lista_abierta or costo_vecino < costos_g.get(vecino, float("inf")):
                    origen[vecino] = celda_actual
                    costos_g[vecino] = costo_vecino
                    if vecino not in lista_abierta:
                        lista_abierta.append(vecino)

            # Animación en terminal
            if animar:
                os.system('clear')
                print("Calculando ruta con A*...\n")
                self.mapa.mostrar_mapa(lista_cerrada)
                time.sleep(0.03)

        # Reconstruir la ruta final
        ruta = []
        actual = meta
        while actual is not None:
            ruta.append(actual)
            actual = origen.get(actual)
        ruta.reverse()

        if ruta and ruta[0] == inicio:
            return ruta
        else:
            return None


# -----------------------------
# EJECUCIÓN PRINCIPAL
# -----------------------------
filas = 15
columnas = 20

mapa = Mapa(filas, columnas)
mapa.generar_obstaculos_aleatorios(probabilidad=0.25)

print("Mapa inicial:\n")
mapa.mostrar_mapa()

buscador = BuscadorRuta(mapa)
print("Buscando la mejor ruta con A*...\n")

ruta = buscador.encontrar_ruta(animar=True)

os.system('clear')

print(ruta, "debugueando...")
if ruta:
    print("Ruta encontrada con éxito:\n")
    mapa.mostrar_mapa(ruta)
else:
    print("No se encontró una ruta posible.\n")
    mapa.mostrar_mapa()


    """ 4 pilares
cuales use

como use
por que no use

formas de definir variables (sobre y dentro del constructor

como funciona la herencia y probar ambas formas.

probar cambios

explicar clases, flujo y conceptos basicos

atributos de instancia y de clase
diferencias, cuando usarlos

"""