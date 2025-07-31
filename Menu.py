import pygame
import os


def cargarMenu(ancho, alto, rutaBaseProyecto):
    #Fondo del menu
    rutaFondo = os.path.join(rutaBaseProyecto, "Fondos", "FondoCielo.jpg")
    try:
        fondo = pygame.image.load(rutaFondo).convert()
    except pygame.error as e:
        print(f"No se pudo cargar el fondo del menú: {rutaFondo}")
        fondo = pygame.Surface((ancho, alto))
        fondo.fill((135, 206, 235)) 
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    #Boton jugar
    rutaBotonJugar = os.path.join(rutaBaseProyecto, "Botones", "BotonJUGAR.png")
    try:
        botonJugar = pygame.image.load(rutaBotonJugar).convert_alpha()
    except pygame.error as e:
        print(f"No se pudo cargar BotonJUGAR.png")
        botonJugar = pygame.Surface((350, 300))
        botonJugar.fill((0, 255, 0))
    botonJugar = pygame.transform.scale(botonJugar, (350, 300))
    rectJugar = botonJugar.get_rect(center=(ancho // 2, 250))

    #Boton salir
    rutaBotonSalir = os.path.join(rutaBaseProyecto, "Botones", "BotonSALIR.png")
    try:
        botonSalir = pygame.image.load(rutaBotonSalir).convert_alpha()
    except pygame.error as e:
        print(f"No se pudo cargar BotonSALIR.png")
        botonSalir = pygame.Surface((350, 300))
        botonSalir.fill((255, 0, 0))
    botonSalir = pygame.transform.scale(botonSalir, (350, 300))
    rectSalir = botonSalir.get_rect(center=(ancho // 2, 390))

    return fondo, botonJugar, rectJugar, botonSalir, rectSalir

 



