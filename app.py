import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Definir dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Definir la velocidad del jugador y los corazones
VEL_JUGADOR = 5
VEL_CORAZON = 3

# Clase para el jugador


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen_original = pygame.image.load("compi.png").convert()
        self.imagen_original.set_colorkey(BLANCO)
        self.imagen = pygame.transform.scale(
            self.imagen_original, (50, 50))  # Reducir tamaño aquí
        self.rect = self.imagen.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10

    def update(self):
        # Mover el jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= VEL_JUGADOR
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += VEL_JUGADOR

# Clase para los corazones


class Corazon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen_original = pygame.image.load("compi.png").convert()
        self.imagen_original.set_colorkey(BLANCO)
        self.imagen = pygame.transform.scale(
            self.imagen_original, (30, 30))  # Reducir tamaño aquí
        self.rect = self.imagen.get_rect()
        self.rect.x = random.randrange(0, max(ANCHO - self.rect.width, 1))
        self.rect.y = random.randrange(-100, -40)
        self.vel_y = VEL_CORAZON

    def update(self):
        # Mover el corazón hacia abajo
        self.rect.y += self.vel_y
        # Si el corazón sale de la pantalla, reiniciarlo en la parte superior con una nueva posición horizontal
        if self.rect.top > ALTO + 10:
            self.rect.x = random.randrange(0, max(ANCHO - self.rect.width, 1))
            self.rect.y = random.randrange(-100, -40)

# Función principal


def main():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Disparador de Corazones")
    reloj = pygame.time.Clock()

    # Crear sprites
    todos_los_sprites = pygame.sprite.Group()
    corazones = pygame.sprite.Group()
    jugador = Jugador()
    todos_los_sprites.add(jugador)

    # Crear corazones
    for i in range(8):
        corazon = Corazon()
        todos_los_sprites.add(corazon)
        corazones.add(corazon)

    # Bucle principal del juego
    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        # Actualizar
        todos_los_sprites.update()

        # Dibujar
        pantalla.fill(NEGRO)
        for sprite in todos_los_sprites:
            pantalla.blit(sprite.imagen, sprite.rect)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
