import pygame
import sys
import random
import math
from pygame.locals import *

# Import game modules
from scripts.player import Player
from scripts.enemy import EnemyManager
from scripts.road import Road
from scripts.powerup import PowerUpManager
from scripts.hud import HUD
from scripts.effects import EffectManager

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 195, 255)
NEON_PINK = (255, 0, 153)
NEON_GREEN = (57, 255, 20)

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyber Drift: Neon Chase")
clock = pygame.time.Clock()

# Game state
game_active = False
game_over = False
score = 0
high_score = 0
paused = False

def main_menu():
    """Display the main menu"""
    global game_active
    
    # Create animated background
    road = Road(400, SCREEN_HEIGHT)
    
    while not game_active:
        screen.fill(BLACK)
        
        # Update and draw road for background effect
        road.update(2)
        road.draw(screen)
        
        # Draw title
        title_font = pygame.font.SysFont('Arial', 64)
        subtitle_font = pygame.font.SysFont('Arial', 24)
        
        title = title_font.render("CYBER DRIFT", True, NEON_PINK)
        subtitle = subtitle_font.render("NEON CHASE", True, NEON_BLUE)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 220))
        
        # Draw start prompt
        start_text = subtitle_font.render("Press SPACE to start", True, NEON_GREEN)
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 400))
        
        # Draw high score
        if high_score > 0:
            high_score_text = subtitle_font.render(f"HIGH SCORE: {high_score}", True, NEON_BLUE)
            screen.blit(high_score_text, (SCREEN_WIDTH//2 - high_score_text.get_width()//2, 450))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game_active = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        clock.tick(FPS)

def game_loop():
    """Main game loop"""
    global game_active, game_over, score, high_score, paused
    
    # Reset game state
    game_over = False
    score = 0
    paused = False
    
    # Create game objects
    road = Road(400, SCREEN_HEIGHT)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    enemy_manager = EnemyManager(road.get_width())
    powerup_manager = PowerUpManager(road.get_width())
    hud = HUD()
    effect_manager = EffectManager()
    
    # Add boost effect to player
    effect_manager.add_boost_effect(player)
    
    # Game loop
    while game_active:
        # Handle pause
        if paused:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        paused = False
                    if event.key == K_ESCAPE:
                        game_active = False
                        
            # Draw paused screen
            hud.draw_pause_menu(screen)
            pygame.display.flip()
            clock.tick(FPS)
            continue
        
        # Process events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if game_over:
                        game_active = False
                    else:
                        paused = True
                if event.key == K_SPACE:
                    if game_over:
                        game_active = False
                    else:
                        player.apply_boost()
                if event.key == K_p:
                    paused = not paused
        
        # Skip updates if game over
        if game_over:
            hud.draw_game_over(screen, score)
            pygame.display.flip()
            clock.tick(FPS)
            continue
        
        # Update game objects
        road_speed = 5 + player.velocity.length()
        road.update(road_speed)
        
        player.update(road.get_width(), SCREEN_HEIGHT)
        
        enemy_manager.update(player.position)
        powerup_manager.update()
        
        effect_manager.update()
        
        # Check collisions
        collisions = enemy_manager.check_collisions(player)
        if collisions:
            damage = 10
            if player.take_damage(damage):
                # Player died
                game_over = True
                if score > high_score:
                    high_score = score
                
                # Create explosion effect
                effect_manager.add_explosion(player.position.x, player.position.y, (255, 100, 0), 50)
            else:
                # Player hit but survived
                hud.update(0, damage)
                
                # Create small explosion effect
                effect_manager.add_explosion(player.position.x, player.position.y, (255, 100, 0), 20)
        
        # Check powerup collisions
        if powerup_manager.check_collisions(player):
            # Create collect effect
            effect_manager.add_collect_effect(player.position.x, player.position.y, (0, 195, 255))
            
            # Update score
            score += 50
            hud.update(50, 0)
        
        # Update score based on distance traveled
        score_increment = int(road_speed * 0.1)
        if score_increment > 0:
            score += score_increment
            hud.update(score_increment, 0)
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw road
        road.draw(screen)
        
        # Draw player effects
        player.draw_effects(screen)
        
        # Draw player
        screen.blit(player.image, player.rect)
        
        # Draw enemies
        enemy_manager.draw(screen)
        
        # Draw powerups
        powerup_manager.draw(screen)
        
        # Draw effects
        effect_manager.draw(screen)
        
        # Draw HUD
        hud.draw(screen, player, score, player.velocity.length())
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

# Main game execution
if __name__ == "__main__":
    while True:
        main_menu()
        game_loop()
