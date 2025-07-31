import pygame
import sys
import os
from Entidades import Repartidor, ObraVial, PresaVehiculos
from Menu import cargarMenu

#Inicializacion
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego del Repartidor - Calle Infinita")
clock = pygame.time.Clock()

rutaBaseProyecto = os.path.dirname(os.path.abspath(__file__))

#Cargar menu
fondoMenu, botonJugar, rectJugar, botonSalir, rectSalir = cargarMenu(ANCHO, ALTO, rutaBaseProyecto)

#Fondo para scroll infinito
rutaFondo = os.path.join(rutaBaseProyecto, "Fondos", "FondoCalleV.png")
try:
    fondoImg = pygame.image.load(rutaFondo).convert()
    fondoImg = pygame.transform.scale(fondoImg, (ANCHO, ALTO))
except:
    fondoImg = pygame.Surface((ANCHO, ALTO))
    fondoImg.fill((100, 100, 100))

#Variables de scroll
yFondo1 = 0
yFondo2 = -ALTO
velocidadFondo = 5

#Listas de imagenes
imagenesObras = [
    os.path.join("Objetos", "Cono.png"),
    os.path.join("Objetos", "SeñalAlto.png"),
    os.path.join("Personajes", "PoliciaTransito.png"),
    os.path.join("Objetos", "Piedra.png"),
    os.path.join("Objetos", "Cono.png")  
]

imagenesCarros = [
    os.path.join("Objetos", "Carro.png")
]

#Crear entidades
repartidor = Repartidor((100, 400), rutaBaseProyecto)
obras = ObraVial(imagenesObras, ANCHO, ALTO, rutaBaseProyecto)
presa = PresaVehiculos(imagenesCarros, ANCHO, ALTO, rutaBaseProyecto)

#Estado del juego
estado = "menu"


def mostrar_menu():
    pantalla.blit(fondoMenu, (0, 0))
    pantalla.blit(botonJugar, rectJugar)
    pantalla.blit(botonSalir, rectSalir)


def jugar():
    global yFondo1, yFondo2

    #Scroll del fondo
    yFondo1 += velocidadFondo
    yFondo2 += velocidadFondo

    if yFondo1 >= ALTO:
        yFondo1 = yFondo2 - ALTO
    if yFondo2 >= ALTO:
        yFondo2 = yFondo1 - ALTO

    pantalla.blit(fondoImg, (0, yFondo1))
    pantalla.blit(fondoImg, (0, yFondo2))

    #Jugador
    teclas = pygame.key.get_pressed()
    repartidor.mover(teclas)
    repartidor.dibujar(pantalla)

    #Obstaculos
    obras.actualizar(velocidadFondo)
    obras.dibujar(pantalla)

    presa.actualizar(velocidadFondo)
    presa.dibujar(pantalla)


#Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rectJugar.collidepoint(evento.pos):
                    estado = "juego"
                elif rectSalir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

    if estado == "menu":
        mostrar_menu()
    elif estado == "juego":
        jugar()

    pygame.display.flip()
    clock.tick(60)