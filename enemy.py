import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, difficulty=1):
        super().__init__()
        # Create enemy car image
        self.original_image = pygame.Surface((40, 70), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (255, 0, 153), [(20, 0), (40, 50), (30, 70), (10, 70), (0, 50)])
        pygame.draw.rect(self.original_image, (200, 0, 100), (10, 15, 20, 40))
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        
        # Movement attributes
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, -2 - difficulty)  # Enemies move up the screen
        self.angle = 0
        self.difficulty = difficulty
        
        # AI behavior
        self.target_lane = random.randint(0, 2)  # 0=left, 1=center, 2=right
        self.lane_change_timer = random.randint(60, 180)  # Frames until next lane change
        self.aggression = random.random() * difficulty  # How likely to target player
        
    def update(self, road_width, player_pos=None):
        # Basic movement
        self.position += self.velocity
        
        # AI lane targeting
        road_left = (800 - road_width) // 2
        lane_width = road_width / 3
        
        # Calculate target x position based on lane
        target_x = road_left + (self.target_lane + 0.5) * lane_width
        
        # Move toward target lane
        if abs(self.position.x - target_x) > 5:
            if self.position.x < target_x:
                self.position.x += 2
                self.angle = -10
            else:
                self.position.x -= 2
                self.angle = 10
        else:
            self.angle = 0
            
        # Lane changing logic
        self.lane_change_timer -= 1
        if self.lane_change_timer <= 0:
            self.target_lane = random.randint(0, 2)
            self.lane_change_timer = random.randint(60, 180)
            
        # Player targeting (if player position provided)
        if player_pos and random.random() < self.aggression:
            player_lane = 0
            if player_pos.x > road_left + lane_width:
                player_lane = 1
            if player_pos.x > road_left + 2 * lane_width:
                player_lane = 2
                
            # Chance to follow player's lane
            if random.random() < 0.3 * self.difficulty:
                self.target_lane = player_lane
                
        # Update rect and rotate image
        self.rect.center = self.position
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def draw_effects(self, screen):
        # Draw engine glow
        angle_rad = math.radians(self.angle)
        exhaust_pos = (
            self.position.x + math.sin(angle_rad) * 35,
            self.position.y + math.cos(angle_rad) * 35
        )
        
        # Draw the glow
        pygame.draw.circle(screen, (255, 0, 100, 128), exhaust_pos, 8)
        pygame.draw.circle(screen, (255, 100, 200, 128), exhaust_pos, 4)


class EnemyManager:
    def __init__(self, road_width):
        self.enemies = pygame.sprite.Group()
        self.road_width = road_width
        self.spawn_timer = 0
        self.difficulty = 1.0
        
    def update(self, player_pos=None):
        # Spawn new enemies
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = random.randint(30, 120) // self.difficulty
            
        # Update existing enemies
        for enemy in self.enemies:
            enemy.update(self.road_width, player_pos)
            
            # Remove enemies that have gone off screen
            if enemy.position.y < -100 or enemy.position.y > 700:
                enemy.kill()
                
        # Gradually increase difficulty
        self.difficulty += 0.0001
        
    def spawn_enemy(self):
        road_left = (800 - self.road_width) // 2
        lane = random.randint(0, 2)
        x = road_left + (lane + 0.5) * (self.road_width / 3)
        y = -100  # Spawn above the screen
        
        enemy = Enemy(x, y, self.difficulty)
        self.enemies.add(enemy)
        
    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw_effects(screen)
        self.enemies.draw(screen)
        
    def check_collisions(self, player):
        return pygame.sprite.spritecollide(player, self.enemies, False)
