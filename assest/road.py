import pygame
import random
import math

class Road:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen_width = 800
        self.screen_height = 600
        
        # Road position
        self.x = (self.screen_width - self.width) // 2
        
        # Road markings
        self.stripe_width = 10
        self.stripe_height = 50
        self.stripe_gap = 30
        self.stripes = []
        
        # Initialize stripes
        for y in range(-self.stripe_height, self.screen_height + self.stripe_height, self.stripe_height + self.stripe_gap):
            self.stripes.append(y)
            
        # Neon decorations
        self.decorations = []
        for _ in range(20):
            side = random.choice(["left", "right"])
            y = random.randint(0, self.screen_height)
            size = random.randint(5, 15)
            color = random.choice([
                (0, 195, 255),  # Neon blue
                (255, 0, 153),  # Neon pink
                (57, 255, 20),  # Neon green
                (255, 230, 0)   # Neon yellow
            ])
            self.decorations.append({
                "side": side,
                "y": y,
                "size": size,
                "color": color,
                "pulse": random.random() * 10
            })
            
    def update(self, speed):
        # Move stripes down
        for i in range(len(self.stripes)):
            self.stripes[i] += speed
            if self.stripes[i] > self.screen_height:
                self.stripes[i] = -self.stripe_height
                
        # Move decorations
        for dec in self.decorations:
            dec["y"] += speed
            dec["pulse"] += 0.1
            if dec["y"] > self.screen_height:
                dec["y"] = -20
                dec["side"] = random.choice(["left", "right"])
                
    def draw(self, screen):
        # Draw road background
        pygame.draw.rect(screen, (20, 20, 30), (self.x, 0, self.width, self.screen_height))
        
        # Draw center line
        center_x = self.screen_width // 2
        for y in self.stripes:
            pygame.draw.rect(screen, (255, 255, 0), (center_x - self.stripe_width//2, y, self.stripe_width, self.stripe_height))
            
        # Draw lane dividers
        lane_width = self.width // 3
        left_lane_x = self.x + lane_width
        right_lane_x = self.x + 2 * lane_width
        
        for y in self.stripes:
            pygame.draw.rect(screen, (255, 255, 255), (left_lane_x - self.stripe_width//2, y, self.stripe_width, self.stripe_height))
            pygame.draw.rect(screen, (255, 255, 255), (right_lane_x - self.stripe_width//2, y, self.stripe_width, self.stripe_height))
            
        # Draw road edges
        pygame.draw.rect(screen, (255, 0, 0), (self.x - 5, 0, 5, self.screen_height))
        pygame.draw.rect(screen, (255, 0, 0), (self.x + self.width, 0, 5, self.screen_height))
        
        # Draw neon decorations
        for dec in self.decorations:
            pulse = abs(math.sin(dec["pulse"])) * 0.5 + 0.5
            color = dec["color"]
            glow_color = (color[0], color[1], color[2], int(128 * pulse))
            
            if dec["side"] == "left":
                x = self.x - 20
            else:
                x = self.x + self.width + 15
                
            # Draw decoration
            pygame.draw.circle(screen, color, (x, dec["y"]), dec["size"])
            
            # Draw glow (would need a surface with alpha for proper glow)
            glow_surface = pygame.Surface((dec["size"]*4, dec["size"]*4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (dec["size"]*2, dec["size"]*2), dec["size"]*2)
            screen.blit(glow_surface, (x - dec["size"]*2, dec["y"] - dec["size"]*2))
            
    def get_width(self):
        return self.width
