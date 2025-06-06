import pygame
import math
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Placeholder rectangle for the player car
        self.original_image = pygame.Surface((40, 70), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (0, 195, 255), [(20, 0), (40, 50), (30, 70), (10, 70), (0, 50)])
        pygame.draw.rect(self.original_image, (57, 255, 20), (10, 15, 20, 40))
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        
        # Movement attributes
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0.2
        self.max_speed = 10
        self.friction = 0.05
        self.angle = 0
        self.steering = 3
        
        # Game attributes
        self.health = 100
        self.shield = 0
        self.boost = 0
        self.score = 0
    
    def update(self, road_width, road_height):
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Acceleration
        if keys[K_UP] or keys[K_w]:
            self.velocity += pygame.math.Vector2(0, -self.acceleration).rotate(-self.angle)
        if keys[K_DOWN] or keys[K_s]:
            self.velocity += pygame.math.Vector2(0, self.acceleration).rotate(-self.angle)
            
        # Steering
        if keys[K_LEFT] or keys[K_a]:
            if self.velocity.length() > 0.5:
                self.angle += self.steering
        if keys[K_RIGHT] or keys[K_d]:
            if self.velocity.length() > 0.5:
                self.angle -= self.steering
                
        # Apply friction
        if self.velocity.length() > 0:
            self.velocity -= self.velocity.normalize() * self.friction
            if self.velocity.length() < 0.1:
                self.velocity = pygame.math.Vector2(0, 0)
        
        # Limit speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
            
        # Update position
        self.position += self.velocity
        
        # Keep player on the road
        road_left = (800 - road_width) // 2
        road_right = road_left + road_width
        
        if self.position.x < road_left + 20:
            self.position.x = road_left + 20
            self.velocity.x = 0
        if self.position.x > road_right - 20:
            self.position.x = road_right - 20
            self.velocity.x = 0
            
        # Update rect and rotate image
        self.rect.center = self.position
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def draw_effects(self, screen):
        # Draw engine glow
        if self.velocity.length() > 1:
            # Calculate the position behind the car
            angle_rad = math.radians(self.angle)
            exhaust_pos = (
                self.position.x + math.sin(angle_rad) * 35,
                self.position.y + math.cos(angle_rad) * 35
            )
            
            # Draw the glow
            size = int(5 + self.velocity.length())
            pygame.draw.circle(screen, (255, 100, 0, 128), exhaust_pos, size)
            pygame.draw.circle(screen, (255, 200, 0, 128), exhaust_pos, size // 2)
            
    def apply_boost(self):
        if self.boost > 0:
            self.velocity *= 1.5
            if self.velocity.length() > self.max_speed * 1.5:
                self.velocity.scale_to_length(self.max_speed * 1.5)
            self.boost -= 1
            
    def collect_powerup(self, powerup_type):
        if powerup_type == "boost":
            self.boost += 100
        elif powerup_type == "shield":
            self.shield = 100
        elif powerup_type == "repair":
            self.health = min(100, self.health + 50)
            
    def take_damage(self, amount):
        if self.shield > 0:
            self.shield -= amount
            if self.shield < 0:
                self.health += self.shield
                self.shield = 0
        else:
            self.health -= amount
        return self.health <= 0
