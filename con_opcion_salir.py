import pygame
import random
import sys
import os

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Definir dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Definir la velocidad del jugador, los corazones y los proyectiles
VEL_JUGADOR = 5
VEL_CORAZON = 3
VEL_PROYECTIL = 8

ruta_imagenes = os.path.join(os.getcwd(), "imagenes")

# Clase para el jugador


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen_original = pygame.image.load(os.path.join(
            ruta_imagenes, "xinay.png")).convert()
        self.imagen_original.set_colorkey(BLANCO)
        self.imagen = pygame.transform.scale(
            self.imagen_original, (50, 50))  # Reducir tamaño aquí
        self.rect = self.imagen.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.vel_x = 0

    def update(self):
        # Mover el jugador
        self.rect.x += self.vel_x
        # Limitar el movimiento del jugador dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > ANCHO:
            self.rect.right = ANCHO

# Clase para los corazones


class Corazon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen_original = pygame.image.load(os.path.join(
            ruta_imagenes, "abby.png")).convert()
        self.imagen_original.set_colorkey(BLANCO)
        self.imagen = pygame.transform.scale(
            self.imagen_original, (30, 30))  # Reducir tamaño aquí
        self.rect = self.imagen.get_rect()
        self.rect.x = random.randrange(
            0, max(ANCHO - self.rect.width, 1))
        self.rect.y = random.randrange(-100, -40)
        self.vel_y = VEL_CORAZON

    def update(self):
        # Mover el corazón hacia abajo
        self.rect.y += self.vel_y
        # Si el corazón sale de la pantalla, reiniciarlo en la parte superior con una nueva posición horizontal
        if self.rect.top > ALTO + 10:
            self.rect.x = random.randrange(
                0, max(ANCHO - self.rect.width, 1))
            self.rect.y = random.randrange(-100, -40)

# Clase para los proyectiles (besos)


class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.imagen_original = pygame.image.load(os.path.join(
            # Usar convert_alpha para conservar la transparencia
            ruta_imagenes, "xinay.png")).convert_alpha()
        self.imagen = pygame.transform.scale(
            # Reducir tamaño aquí si es necesario
            self.imagen_original, (30, 30))
        self.rect = self.imagen.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.vel_y = -VEL_PROYECTIL

    def update(self):
        # Mover el proyectil (beso) hacia arriba
        self.rect.y += self.vel_y
        # Eliminar el proyectil si sale de la pantalla
        if self.rect.bottom < 0:
            self.kill()

# Función para mostrar texto en pantalla


def mostrar_texto(pantalla, texto, tamaño, x, y):
    fuente = pygame.font.Font(None, tamaño)
    texto_superficie = fuente.render(texto, True, BLANCO)
    rectangulo_texto = texto_superficie.get_rect()
    rectangulo_texto.midtop = (x, y)
    pantalla.blit(texto_superficie, rectangulo_texto)

# Función principal


def main():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Demostrando Amor programando")
    reloj = pygame.time.Clock()

    # Crear sprites
    todos_los_sprites = pygame.sprite.Group()
    corazones = pygame.sprite.Group()
    proyectiles = pygame.sprite.Group()
    jugador = Jugador()
    todos_los_sprites.add(jugador)

    # Contadores de puntaje y mensajes
    puntaje = 0
    mensaje = ""

    # Bucle principal del juego
    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # Disparar al presionar la tecla de espacio
                    proyectil = Proyectil(
                        jugador.rect.centerx, jugador.rect.top)
                    todos_los_sprites.add(proyectil)
                    proyectiles.add(proyectil)
                elif evento.key == pygame.K_LEFT:
                    jugador.vel_x = -VEL_JUGADOR
                elif evento.key == pygame.K_RIGHT:
                    jugador.vel_x = VEL_JUGADOR
                elif evento.key == pygame.K_ESCAPE:  # Salir del juego
                    jugando = False
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    jugador.vel_x = 0

        # Generar corazones aleatoriamente
        if len(corazones) < 10:  # Controlar el número máximo de corazones en pantalla
            corazon = Corazon()
            todos_los_sprites.add(corazon)
            corazones.add(corazon)

        # Verificar colisiones entre proyectiles y corazones
        colisiones_proyectil_corazon = pygame.sprite.groupcollide(
            proyectiles, corazones, True, True)
        # Incrementar el puntaje por cada colisión entre proyectiles y corazones
        puntaje += len(colisiones_proyectil_corazon)

        # Actualizar mensaje según el puntaje
        if puntaje >= 20:
            mensaje = "Seras la madre de mis hijos"
        elif puntaje >= 10:
            mensaje = "Te quiero mi chiquita"
        elif puntaje >= 5:
            mensaje = "Voy por ti"

        # Actualizar
        todos_los_sprites.update()

        # Dibujar
        pantalla.fill(NEGRO)
        for sprite in todos_los_sprites:
            pantalla.blit(sprite.imagen, sprite.rect)

        # Mostrar puntaje y mensaje en pantalla
        mostrar_texto(pantalla, f"Puntaje: {puntaje}", 20, 70, 10)
        mostrar_texto(pantalla, mensaje, 30, ANCHO // 2, ALTO // 2)

        pygame.display.flip()
        reloj.tick(60)

    # Una vez que el juego termina, mostrar opción para continuar o salir
    pantalla.fill(NEGRO)
    mostrar_texto(pantalla, "¿Deseas volver a jugar? (Sí / No)",
                  30, ANCHO // 2, ALTO // 2)
    pygame.display.flip()

    esperando_respuesta = True
    while esperando_respuesta:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:  # Si el jugador presiona "S" (Sí)
                    esperando_respuesta = False
                    # Reiniciar el juego
                    puntaje = 0
                    mensaje = ""
                    corazones.empty()
                    proyectiles.empty()
                # Si el jugador presiona "N" (No)
                elif evento.key == pygame.K_n:
                    esperando_respuesta = False
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    main()
