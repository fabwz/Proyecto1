import pygame
import random
import os

# Clase del repartidor
class Repartidor:
    def __init__(self, posInicial, rutaBaseProyecto):
        ruta_imagen = os.path.join(rutaBaseProyecto, "Personajes", "Repartidor.png")
        try:
            self.imagen = pygame.image.load(ruta_imagen).convert_alpha()
        except pygame.error:
            self.imagen = pygame.Surface((200, 200))
            self.imagen.fill((0, 255, 0))  # Verde
        self.imagen = pygame.transform.scale(self.imagen, (200, 200))
        self.rect = self.imagen.get_rect(topleft=posInicial)
        self.velocidad = 5

    def mover(self, teclas):
        if teclas[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_d] and self.rect.right < 800:
            self.rect.x += self.velocidad
        #No mover verticalmente

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


#Grupo de objetos: Obra Vial (cono, señal, policía, etc.)
class ObraVial:
    def __init__(self, imagenesRelativas, anchoJuego, altoJuego, rutaBaseProyecto, escala=1.8):
        self.imagenes = []
        self.anchoJuego = anchoJuego
        self.altoJuego = altoJuego
        self.escala = escala
        self.grupo = []
        self.activo = False
        self.tiempoUltimoSpawn = 0
        self.spawnIntervalo = 6000  

        # Cargar y escalar imágenes
        for imgRelativa in imagenesRelativas:
            rutaCompleta = os.path.join(rutaBaseProyecto, imgRelativa)
            try:
                imagen = pygame.image.load(rutaCompleta).convert_alpha()
                tam = (int(imagen.get_width() * escala), int(imagen.get_height() * escala))
                imagen = pygame.transform.scale(imagen, tam)
                self.imagenes.append(imagen)
            except:
                imgError = pygame.Surface((50, 50))
                imgError.fill((255, 0, 0))
                self.imagenes.append(imgError)

    def actualizar(self, velocidadScroll):
        tiempoActual = pygame.time.get_ticks()

        if not self.activo and tiempoActual - self.tiempoUltimoSpawn > self.spawnIntervalo:
            self.tiempoUltimoSpawn = tiempoActual
            self.spawnGrupo()
            self.activo = True

        if self.activo:
            for img, rect in self.grupo:
                rect.y += velocidadScroll
            #Eliminar si salieron
            if self.grupo and self.grupo[0][1].y > self.altoJuego + 100:
                self.grupo.clear()
                self.activo = False

    def spawnGrupo(self):
        self.grupo.clear()
        y = -180  # Aparece arriba
        centroX = self.anchoJuego // 2
        offset = 70 * self.escala

        posiciones = [
            (-2*offset, 15),   # Cono izq
            (-1*offset, -10),  # Señal alto
            (0, 0),            # Policía
            (1*offset, 8),     # Piedra
            (2*offset, 20),    # Cono der
        ]

        for i, (ox, oy) in enumerate(posiciones):
            if i < len(self.imagenes):
                x = centroX + ox
                yPos = y + oy
                img = self.imagenes[i]
                rect = img.get_rect(center=(x, yPos))
                self.grupo.append((img, rect))

    def dibujar(self, pantalla):
        for img, rect in self.grupo:
            pantalla.blit(img, rect)


# Grupo de carros: Presa de tráfico
class PresaVehiculos:
    def __init__(self, imagenesRelativas, anchoJuego, altoJuego, rutaBaseProyecto, escala=1.4):
        self.imagenes = []
        self.anchoJuego = anchoJuego
        self.altoJuego = altoJuego
        self.escala = escala
        self.grupo = []
        self.activo = False
        self.tiempoUltimoSpawn = 0
        self.spawnIntervalo = 8000  

        for imgRelativa in imagenesRelativas:
            rutaCompleta = os.path.join(rutaBaseProyecto, imgRelativa)
            try:
                imagen = pygame.image.load(rutaCompleta).convert_alpha()
                tam = (int(imagen.get_width() * escala), int(imagen.get_height() * escala))
                imagen = pygame.transform.scale(imagen, tam)
                for _ in range(6):  
                    self.imagenes.append(imagen)
            except:
                imgError = pygame.Surface((70, 40))
                imgError.fill((0, 0, 255))
                self.imagenes.append(imgError)

    def actualizar(self, velocidadScroll):
        tiempoActual = pygame.time.get_ticks()

        if not self.activo and tiempoActual - self.tiempoUltimoSpawn > self.spawnIntervalo:
            self.tiempoUltimoSpawn = tiempoActual
            self.spawn_grupo()
            self.activo = True

        if self.activo:
            for img, rect in self.grupo:
                rect.y += velocidadScroll
            if self.grupo and self.grupo[0][1].y > self.altoJuego + 100:
                self.grupo.clear()
                self.activo = False

    def spawn_grupo(self):
        self.grupo.clear()
        y = -250
        anchoCalle = 680
        inicioX = (self.anchoJuego - anchoCalle) // 2
        filas = 2
        columnas = 3
        espacioX = anchoCalle // columnas
        espacioY = 90

        idx = 0
        for fila in range(filas):
            for col in range(columnas):
                x = inicioX + col * espacioX + espacioX // 2
                yPos = y + fila * espacioY + 30
                img = self.imagenes[idx % len(self.imagenes)]
                rect = img.get_rect(center=(x, yPos))
                self.grupo.append((img, rect))
                idx += 1

    def dibujar(self, pantalla):
        for img, rect in self.grupo:
            pantalla.blit(img, rect)