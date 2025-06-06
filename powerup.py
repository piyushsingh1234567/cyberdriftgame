import pygame
import random
import math

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.type = powerup_type
        
        # Set color based on type
        if powerup_type == "boost":
            self.color = (255, 230, 0)  # Yellow
        elif powerup_type == "shield":
            self.color = (0, 195, 255)  # Blue
        elif powerup_type == "repair":
            self.color = (57, 255, 20)  # Green
            
        # Create image
        self.original_image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.original_image, self.color, (15, 15), 15)
        
        # Add icon based on type
        if powerup_type == "boost":
            pygame.draw.polygon(self.original_image, (0, 0, 0), [(10, 5), (20, 15), (10, 25)])
        elif powerup_type == "shield":
            pygame.draw.circle(self.original_image, (0, 0, 0), (15, 15), 10, 3)
        elif powerup_type == "repair":
            pygame.draw.rect(self.original_image, (0, 0, 0), (10, 5, 10, 20))
            pygame.draw.rect(self.original_image, (0, 0, 0), (5, 10, 20, 10))
            
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        
        # Movement attributes
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 2)  # Move down the screen
        self.angle = 0
        self.rotation_speed = random.uniform(-3, 3)
        
        # Animation
        self.pulse = random.random() * 10
        self.pulse_speed = 0.1
        
    def update(self):
        # Move down
        self.position += self.velocity
        self.rect.center = self.position
        
        # Rotate
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Pulse animation
        self.pulse += self.pulse_speed
        
    def draw_effects(self, screen):
        # Draw glow effect
        pulse_value = abs(math.sin(self.pulse)) * 0.5 + 0.5
        glow_size = int(20 + 10 * pulse_value)
        
        glow_surface = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
        glow_color = (*self.color, 100)  # Add alpha
        pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), glow_size)
        screen.blit(glow_surface, (self.position.x - glow_size, self.position.y - glow_size))


class PowerUpManager:
    def __init__(self, road_width):
        self.powerups = pygame.sprite.Group()
        self.road_width = road_width
        self.spawn_timer = 300  # Initial delay
        self.types = ["boost", "shield", "repair"]
        
    def update(self):
        # Spawn new powerups
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_powerup()
            self.spawn_timer = random.randint(300, 600)  # 5-10 seconds at 60 FPS
            
        # Update existing powerups
        for powerup in self.powerups:
            powerup.update()
            
            # Remove powerups that have gone off screen
            if powerup.position.y > 700:
                powerup.kill()
                
    def spawn_powerup(self):
        road_left = (800 - self.road_width) // 2
        lane = random.randint(0, 2)
        x = road_left + (lane + 0.5) * (self.road_width / 3)
        y = -50  # Spawn above the screen
        
        powerup_type = random.choice(self.types)
        powerup = PowerUp(x, y, powerup_type)
        self.powerups.add(powerup)
        
    def draw(self, screen):
        for powerup in self.powerups:
            powerup.draw_effects(screen)
        self.powerups.draw(screen)
        
    def check_collisions(self, player):
        collisions = pygame.sprite.spritecollide(player, self.powerups, True)
        for powerup in collisions:
            player.collect_powerup(powerup.type)
        return len(collisions) > 0
