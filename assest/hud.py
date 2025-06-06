import pygame
import math

class HUD:
    def __init__(self):
        self.width = 800
        self.height = 600
        
        # Fonts
        self.font_large = pygame.font.SysFont('Arial', 36)
        self.font_medium = pygame.font.SysFont('Arial', 24)
        self.font_small = pygame.font.SysFont('Arial', 18)
        
        # Colors
        self.neon_blue = (0, 195, 255)
        self.neon_pink = (255, 0, 153)
        self.neon_green = (57, 255, 20)
        self.neon_yellow = (255, 230, 0)
        
        # Animation variables
        self.pulse = 0
        self.score_flash = 0
        self.damage_flash = 0
        
    def update(self, score_change=0, damage_taken=0):
        # Update animations
        self.pulse = (self.pulse + 0.05) % (2 * math.pi)
        
        # Flash effects
        if score_change > 0:
            self.score_flash = 1.0
        else:
            self.score_flash = max(0, self.score_flash - 0.05)
            
        if damage_taken > 0:
            self.damage_flash = 1.0
        else:
            self.damage_flash = max(0, self.damage_flash - 0.05)
            
    def draw(self, screen, player, score, speed, time_left=None):
        # Draw speed indicator
        speed_text = self.font_medium.render(f"SPEED: {int(speed * 10)} KM/H", True, self.neon_green)
        screen.blit(speed_text, (20, 20))
        
        # Draw score with flash effect
        score_color = self.neon_yellow
        if self.score_flash > 0:
            score_color = (255, 255, 255)
        score_text = self.font_large.render(f"SCORE: {score}", True, score_color)
        screen.blit(score_text, (self.width - score_text.get_width() - 20, 20))
        
        # Draw health bar
        health_width = 200
        health_height = 15
        health_x = 20
        health_y = self.height - 40
        
        # Health background
        pygame.draw.rect(screen, (50, 50, 50), (health_x, health_y, health_width, health_height))
        
        # Health fill
        health_fill = max(0, min(health_width * player.health / 100, health_width))
        health_color = self.neon_green
        if player.health < 30:
            health_color = self.neon_pink
        elif player.health < 60:
            health_color = self.neon_yellow
            
        # Flash effect for damage
        if self.damage_flash > 0:
            health_color = (255, 255, 255)
            
        pygame.draw.rect(screen, health_color, (health_x, health_y, health_fill, health_height))
        
        # Health text
        health_text = self.font_small.render(f"HEALTH: {int(player.health)}%", True, (255, 255, 255))
        screen.blit(health_text, (health_x + 5, health_y - 3))
        
        # Draw shield bar if active
        if player.shield > 0:
            shield_width = 200
            shield_height = 10
            shield_x = 20
            shield_y = self.height - 55
            
            # Shield background
            pygame.draw.rect(screen, (50, 50, 50), (shield_x, shield_y, shield_width, shield_height))
            
            # Shield fill
            shield_fill = max(0, min(shield_width * player.shield / 100, shield_width))
            pygame.draw.rect(screen, self.neon_blue, (shield_x, shield_y, shield_fill, shield_height))
            
            # Shield text
            shield_text = self.font_small.render(f"SHIELD: {int(player.shield)}%", True, (255, 255, 255))
            screen.blit(shield_text, (shield_x + 5, shield_y - 3))
            
        # Draw boost meter
        if player.boost > 0:
            boost_width = 150
            boost_height = 10
            boost_x = self.width - boost_width - 20
            boost_y = self.height - 40
            
            # Boost background
            pygame.draw.rect(screen, (50, 50, 50), (boost_x, boost_y, boost_width, boost_height))
            
            # Boost fill
            boost_fill = max(0, min(boost_width * player.boost / 100, boost_width))
            
            # Pulsing effect
            boost_color = self.neon_yellow
            pulse_value = abs(math.sin(self.pulse))
            if pulse_value > 0.7:
                boost_color = (255, 255, 255)
                
            pygame.draw.rect(screen, boost_color, (boost_x, boost_y, boost_fill, boost_height))
            
            # Boost text
            boost_text = self.font_small.render(f"BOOST: {int(player.boost)}%", True, (255, 255, 255))
            screen.blit(boost_text, (boost_x + 5, boost_y - 3))
            
        # Draw time left if provided (for time trial mode)
        if time_left is not None:
            minutes = int(time_left / 60)
            seconds = int(time_left % 60)
            time_text = self.font_medium.render(f"TIME: {minutes:02d}:{seconds:02d}", True, self.neon_blue)
            screen.blit(time_text, (self.width // 2 - time_text.get_width() // 2, 20))
            
    def draw_game_over(self, screen, final_score):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over = self.font_large.render("GAME OVER", True, self.neon_pink)
        screen.blit(game_over, (self.width // 2 - game_over.get_width() // 2, self.height // 2 - 50))
        
        # Final score
        score_text = self.font_medium.render(f"FINAL SCORE: {final_score}", True, self.neon_yellow)
        screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, self.height // 2))
        
        # Restart prompt
        restart = self.font_small.render("PRESS SPACE TO RESTART", True, self.neon_green)
        screen.blit(restart, (self.width // 2 - restart.get_width() // 2, self.height // 2 + 50))
        
    def draw_pause_menu(self, screen):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Paused text
        paused = self.font_large.render("PAUSED", True, self.neon_blue)
        screen.blit(paused, (self.width // 2 - paused.get_width() // 2, self.height // 2 - 50))
        
        # Resume prompt
        resume = self.font_small.render("PRESS P TO RESUME", True, self.neon_green)
        screen.blit(resume, (self.width // 2 - resume.get_width() // 2, self.height // 2))
        
        # Quit prompt
        quit_text = self.font_small.render("PRESS ESC TO QUIT", True, self.neon_pink)
        screen.blit(quit_text, (self.width // 2 - quit_text.get_width() // 2, self.height // 2 + 30))
