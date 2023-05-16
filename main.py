import pygame
import sys
import random

# Definindo as dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Definindo as cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Mario:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT - 100
        self.width = 50
        self.height = 50
        self.velocity = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -15

    def update(self):
        if self.is_jumping:
            self.velocity += 1
            self.y += self.velocity
            if self.y >= SCREEN_HEIGHT - self.height:
                self.y = SCREEN_HEIGHT - self.height
                self.is_jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))


class Pipe:
    def __init__(self, height):
        self.x = SCREEN_WIDTH
        self.width = 50
        self.height = height
        self.y = SCREEN_HEIGHT - self.height

    def update(self):
        self.x -= 5

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))


def create_pipe():
    height = random.randint(15, 30)  # Altura aleatória entre 15 e 30
    return Pipe(height)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jump Mario")

        self.clock = pygame.time.Clock()
        self.mario = Mario()
        self.pipe = create_pipe()
        self.start_time = pygame.time.get_ticks()

    def print_distance(self):
        distance = abs(self.mario.x - self.pipe.x)
        print("Distância do Mario para o Pipe:", distance - 45)

    def run(self):
        running = True

        while running:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.mario.jump()

            self.mario.update()
            self.pipe.update()

            if self.pipe.x + self.pipe.width < 0:
                self.pipe = create_pipe()

            if self.mario.x + self.mario.width > self.pipe.x and \
                    self.mario.x < self.pipe.x + self.pipe.width and \
                    self.mario.y + self.mario.height > self.pipe.y:
                print("Game Over")
                running = False

            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            self.screen.fill((0, 0, 0))
            self.mario.draw(self.screen)
            self.pipe.draw(self.screen)

            self.print_distance()  # Chama a função para exibir a distância

            # Renderiza o texto na tela
            font = pygame.font.Font(None, 36)
            text = font.render("Tempo: {}s".format(elapsed_time), True, WHITE)
            text_rect = text.get_rect()
            text_rect.topleft = (10, 10)
            self.screen.blit(text, text_rect)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
