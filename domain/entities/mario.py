import uuid
import pygame
import random

from domain.valueble.commons import SCREEN_HEIGHT


class Mario:
    def __init__(self, genome, genome_output):
        self.id = uuid.uuid4()
        self.x = 50
        self.y = SCREEN_HEIGHT - 100
        self.width = 50
        self.height = 50
        self.velocity = 0
        self.is_jumping = False
        self.distance_to_pipe = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.genome = genome
        self.genomeOutput = genome_output
        self.fitness = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = -15

    def lower(self):
        self.is_jumping = True
        self.velocity = 100  # Adjust the velocity value as needed

    def update(self):
        if self.is_jumping:
            self.velocity += 1
            self.y += self.velocity
            if self.y >= SCREEN_HEIGHT - self.height:
                self.y = SCREEN_HEIGHT - self.height
                self.is_jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
