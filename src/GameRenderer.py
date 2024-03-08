# GameRenderer.py
import pygame


class GameRenderer:
    def __init__(self, screen):
        self.screen = screen

    def draw_players(self, players):
        for player in players:
            if player.is_active:  # Малювання лише активних гравців
                player.draw()

    def draw_road(self, road1, road2):
        self.screen.blit(road1.image, road1.rect)
        self.screen.blit(road2.image, road2.rect)

    def draw_bots(self, obstacles):
        for bot in obstacles:
            bot.draw()

    def draw_explosions(self, players):
        for player in players:
            if player._is_explosion_anim_playing:
                player.draw_explosion()