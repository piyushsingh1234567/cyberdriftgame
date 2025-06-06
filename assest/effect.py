import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color, size=5, lifetime=60, velocity=None):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.velocity = velocity or pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        
    def update(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
        self.lifetime -= 1
        self.size = max(0, self.size * 0.95)
        
    def draw(self, screen):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*self.color, alpha)
        
        # Create a surface for the particle with alpha
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(particle_surface, (self.x - self.size, self.y - self.size))


class ExplosionEffect:
    def __init__(self, x, y, color=(255, 100, 0), particles=30):
        self.particles = []
        for _ in range(particles):
            velocity = pygame.math.Vector2(random.uniform(-3, 3), random.uniform(-3, 3))
            size = random.uniform(3, 8)
            lifetime = random.randint(30, 60)
            self.particles.append(Particle(x, y, color, size, lifetime, velocity))
            
    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
                
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
            
    def is_finished(self):
        return len(self.particles) == 0


class BoostEffect:
    def __init__(self, player):
        self.player = player
        self.particles = []
        
    def update(self):
        # Add new particles if boost is active
        if self.player.velocity.length() > 5:
            # Calculate position behind the car
            angle_rad = math.radians(self.player.angle)
            exhaust_pos = (
                self.player.position.x + math.sin(angle_rad) * 35,
                self.player.position.y + math.cos(angle_rad) * 35
            )
            
            # Add particles
            for _ in range(2):
                velocity = pygame.math.Vector2(
                    random.uniform(-1, 1) + math.sin(angle_rad) * 2,
                    random.uniform(-1, 1) + math.cos(angle_rad) * 2
                )
                
                color = (255, 100, 0) if random.random() > 0.5 else (255, 200, 0)
                size = random.uniform(2, 6)
                lifetime = random.randint(10, 30)
                
                self.particles.append(Particle(exhaust_pos[0], exhaust_pos[1], color, size, lifetime, velocity))
                
        # Update existing particles
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
                
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)


class CollectEffect:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 5
        self.max_radius = 40
        self.lifetime = 30
        self.max_lifetime = 30
        
    def update(self):
        self.radius += (self.max_radius - self.radius) * 0.2
        self.lifetime -= 1
        
    def draw(self, screen):
        alpha = int(200 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*self.color, alpha)
        
        ring_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(ring_surface, color_with_alpha, (self.radius, self.radius), self.radius, 2)
        screen.blit(ring_surface, (self.x - self.radius, self.y - self.radius))
        
    def is_finished(self):
        return self.lifetime <= 0


class EffectManager:
    def __init__(self):
        self.explosions = []
        self.collect_effects = []
        self.boost_effects = {}
        
    def add_explosion(self, x, y, color=(255, 100, 0), particles=30):
        self.explosions.append(ExplosionEffect(x, y, color, particles))
        
    def add_collect_effect(self, x, y, color):
        self.collect_effects.append(CollectEffect(x, y, color))
        
    def add_boost_effect(self, player):
        if player not in self.boost_effects:
            self.boost_effects[player] = BoostEffect(player)
            
    def update(self):
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
                
        # Update collect effects
        for effect in self.collect_effects[:]:
            effect.update()
            if effect.is_finished():
                self.collect_effects.remove(effect)
                
        # Update boost effects
        for player, effect in self.boost_effects.items():
            effect.update()
            
    def draw(self, screen):
        # Draw all effects
        for explosion in self.explosions:
            explosion.draw(screen)
            
        for effect in self.collect_effects:
            effect.draw(screen)
            
        for effect in self.boost_effects.values():
            effect.draw(screen)
