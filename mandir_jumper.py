import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
DARK_BROWN = (101, 67, 33)
ORANGE = (255, 165, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.on_left_wall = True
        self.jumping = False
        self.jump_progress = 0
        self.jump_duration = 20
        self.jump_height = 60
        self.climb_speed = 2
        
        # Power-up states
        self.speed_boost = False
        self.speed_boost_timer = 0
        self.invincible = False
        self.invincible_timer = 0
        
    def update(self):
        # Handle power-up timers
        if self.speed_boost:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost = False
        
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # Automatic climbing
        if not self.jumping:
            climb_speed = self.climb_speed * (2 if self.speed_boost else 1)
            self.y -= climb_speed
        
        # Handle jumping animation
        if self.jumping:
            self.jump_progress += 1
            progress = self.jump_progress / self.jump_duration
            
            if progress >= 1.0:
                self.x = self.jump_target_x
                self.y = self.jump_start_y
                self.on_left_wall = not self.on_left_wall
                self.jumping = False
                self.jump_progress = 0
            else:
                # Animate jump with parabolic arc
                self.x = self.jump_start_x + (self.jump_target_x - self.jump_start_x) * progress
                arc_offset = self.jump_height * 4 * progress * (1 - progress)
                self.y = self.jump_start_y - arc_offset
    
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_progress = 0
            self.jump_start_x = self.x
            self.jump_start_y = self.y
            
            if self.on_left_wall:
                self.jump_target_x = SCREEN_WIDTH - 80 - self.width
            else:
                self.jump_target_x = 80
    
    def activate_speed_boost(self):
        self.speed_boost = True
        self.speed_boost_timer = 300
    
    def activate_invincibility(self):
        self.invincible = True
        self.invincible_timer = 180
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        center_x = self.x + self.width // 2
        
        # Flash effect when invincible
        flash = self.invincible and self.invincible_timer % 10 < 5
        
        # Draw head
        head_color = WHITE if flash else (255, 220, 177)
        pygame.draw.circle(screen, head_color, (center_x, int(self.y + 8)), 8)
        
        # Draw hair
        pygame.draw.arc(screen, BLACK, (center_x - 10, self.y - 2, 20, 16), 0, math.pi, 3)
        
        # Draw eyes
        pygame.draw.circle(screen, BLACK, (center_x - 3, int(self.y + 6)), 1)
        pygame.draw.circle(screen, BLACK, (center_x + 3, int(self.y + 6)), 1)
        
        # Draw body
        body_color = WHITE if flash else GOLD
        pygame.draw.rect(screen, body_color, (self.x + 8, self.y + 16, 14, 16))
        
        # Draw arms
        arm_color = WHITE if flash else (255, 220, 177)
        pygame.draw.rect(screen, arm_color, (self.x + 4, self.y + 18, 4, 12))
        pygame.draw.rect(screen, arm_color, (self.x + 22, self.y + 18, 4, 12))
        
        # Draw pants
        pygame.draw.rect(screen, BROWN, (self.x + 8, self.y + 32, 14, 8))
        
        # Draw khukuri weapon
        weapon_x = self.x + self.width - 2
        weapon_y = self.y + 20
        pygame.draw.rect(screen, DARK_BROWN, (weapon_x, weapon_y, 3, 8))
        pygame.draw.polygon(screen, GRAY, [
            (weapon_x + 3, weapon_y),
            (weapon_x + 8, weapon_y - 2),
            (weapon_x + 10, weapon_y + 3),
            (weapon_x + 6, weapon_y + 6),
            (weapon_x + 3, weapon_y + 4)
        ])

class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.speed = random.uniform(1, 3)
        self.direction = random.choice([-1, 1])
        self.rotation = 0
        self.fall_speed = random.uniform(0.5, 1.5)
        
        if enemy_type == "crow":
            self.width = 25
            self.height = 20
        else:  # khukuri
            self.width = 30
            self.height = 30
    
    def update(self):
        # Horizontal movement
        self.x += self.speed * self.direction
        
        # Vertical movement (falling)
        self.y += self.fall_speed
        
        # Bounce off walls
        if self.x <= 80 or self.x >= SCREEN_WIDTH - 80 - self.width:
            self.direction *= -1
        
        # Rotation for spinning khukuri
        if self.type == "khukuri":
            self.rotation += 5
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        if self.type == "crow":
            # Draw crow body
            pygame.draw.ellipse(screen, BLACK, (self.x + 3, self.y + 5, self.width - 6, self.height - 8))
            # Draw head
            pygame.draw.circle(screen, BLACK, (center_x + 8, center_y - 3), 6)
            # Draw beak
            pygame.draw.polygon(screen, ORANGE, [
                (center_x + 13, center_y - 3),
                (center_x + 18, center_y - 1),
                (center_x + 13, center_y + 1)
            ])
            # Draw eye
            pygame.draw.circle(screen, WHITE, (center_x + 10, center_y - 5), 2)
            pygame.draw.circle(screen, BLACK, (center_x + 10, center_y - 5), 1)
            
        else:  # khukuri
            # Draw spinning knife
            angle_rad = math.radians(self.rotation)
            blade_length = 12
            blade_width = 3
            
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            
            # Blade tip
            tip_x = center_x + blade_length * cos_a
            tip_y = center_y + blade_length * sin_a
            
            # Blade base
            base_x1 = center_x - blade_width * sin_a
            base_y1 = center_y + blade_width * cos_a
            base_x2 = center_x + blade_width * sin_a
            base_y2 = center_y - blade_width * cos_a
            
            # Draw blade
            pygame.draw.polygon(screen, (200, 200, 200), [(tip_x, tip_y), (base_x1, base_y1), (base_x2, base_y2)])
            
            # Draw handle
            handle_tip_x = center_x - 6 * cos_a
            handle_tip_y = center_y - 6 * sin_a
            pygame.draw.line(screen, DARK_BROWN, (center_x, center_y), (handle_tip_x, handle_tip_y), 4)

class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.type = powerup_type
        self.width = 20
        self.height = 20
        self.bob_offset = 0
    
    def update(self):
        self.bob_offset += 0.2
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y + math.sin(self.bob_offset) * 3, self.width, self.height)
    
    def draw(self, screen):
        y_pos = self.y + math.sin(self.bob_offset) * 3
        center_x = self.x + self.width // 2
        center_y = y_pos + self.height // 2
        
        if self.type == "chiyaa":
            # Draw tea cup
            pygame.draw.ellipse(screen, BROWN, (self.x + 2, y_pos + 8, self.width - 4, self.height - 8))
            pygame.draw.ellipse(screen, DARK_BROWN, (self.x + 4, y_pos + 9, self.width - 8, 6))
            pygame.draw.arc(screen, BROWN, (self.x + self.width - 4, y_pos + 10, 6, 8), 0, math.pi, 2)
            # Steam
            for i in range(3):
                steam_x = center_x - 2 + i * 2
                steam_y = y_pos + 2 - i * 2
                pygame.draw.circle(screen, (200, 200, 200), (int(steam_x), int(steam_y)), 1)
        else:  # prayer_wheel
            # Draw prayer wheel
            pygame.draw.circle(screen, GOLD, (int(center_x), int(center_y)), self.width//2)
            pygame.draw.circle(screen, RED, (int(center_x), int(center_y)), self.width//3)
            pygame.draw.circle(screen, WHITE, (int(center_x), int(center_y)), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mandir Jumper")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.player = Player(80, SCREEN_HEIGHT - 100)
        self.enemies = []
        self.powerups = []
        self.score = 0
        self.highscore = 0
        self.camera_y = 0
        self.spawn_timer = 0
        self.powerup_spawn_timer = 0
        self.game_start_timer = 0
        self.game_over = False
        
        # UI Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def spawn_enemy(self):
        enemy_type = random.choice(["crow", "khukuri"])
        x = random.randint(100, SCREEN_WIDTH - 120)
        y = self.camera_y - random.randint(100, 300)
        self.enemies.append(Enemy(x, y, enemy_type))
    
    def spawn_powerup(self):
        powerup_type = random.choice(["chiyaa", "prayer_wheel"])
        x = random.randint(100, SCREEN_WIDTH - 120)
        y = self.camera_y - random.randint(50, 200)
        self.powerups.append(PowerUp(x, y, powerup_type))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over:
                        self.player.jump()
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_over:
                    self.player.jump()
                elif self.game_over:
                    self.restart_game()
        return True
    
    def restart_game(self):
        self.player = Player(80, SCREEN_HEIGHT - 100)
        self.enemies = []
        self.powerups = []
        self.score = 0
        self.camera_y = 0
        self.spawn_timer = 0
        self.powerup_spawn_timer = 0
        self.game_start_timer = 0
        self.game_over = False
    
    def update(self):
        if self.game_over:
            return
        
        self.game_start_timer += 1
        
        # Update player
        self.player.update()
        
        # Update camera
        self.camera_y = self.player.y - SCREEN_HEIGHT + 200
        
        # Update score
        if self.game_start_timer > 60:
            if (self.game_start_timer - 60) % 6 == 0:
                self.score += 1
                # Check for new highscore (session only)
                if self.score > self.highscore:
                    self.highscore = self.score
        
        # Spawn enemies
        if self.game_start_timer > 120:
            self.spawn_timer += 1
            spawn_rate = max(30, 90 - self.score // 50)
            
            if self.spawn_timer > spawn_rate:
                self.spawn_enemy()
                self.spawn_timer = 0
        
        # Spawn power-ups
        self.powerup_spawn_timer += 1
        if self.powerup_spawn_timer > 600:
            self.spawn_powerup()
            self.powerup_spawn_timer = 0
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.y > self.camera_y + SCREEN_HEIGHT + 100:
                self.enemies.remove(enemy)
        
        # Update power-ups
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.y > self.camera_y + SCREEN_HEIGHT + 100:
                self.powerups.remove(powerup)
        
        # Check collisions with enemies
        if not self.player.invincible:
            player_rect = self.player.get_rect()
            for enemy in self.enemies:
                if player_rect.colliderect(enemy.get_rect()):
                    self.game_over = True
                    return
        
        # Check collisions with power-ups
        player_rect = self.player.get_rect()
        for powerup in self.powerups[:]:
            if player_rect.colliderect(powerup.get_rect()):
                if powerup.type == "chiyaa":
                    self.player.activate_speed_boost()
                else:
                    self.player.activate_invincibility()
                self.powerups.remove(powerup)
    
    def draw_background(self):
        # Sky gradient (dawn/dusk colors for Himalayan atmosphere)
        for y in range(SCREEN_HEIGHT):
            # Create a more dramatic sky gradient
            progress = y / SCREEN_HEIGHT
            if progress < 0.3:  # Upper sky - deep blue
                r = int(70 + progress * 100)
                g = int(130 + progress * 80)
                b = int(200 + progress * 55)
            elif progress < 0.7:  # Middle sky - lighter blue
                r = int(120 + (progress - 0.3) * 150)
                g = int(170 + (progress - 0.3) * 100)
                b = int(220 + (progress - 0.3) * 35)
            else:  # Lower sky - warm horizon
                r = int(200 + (progress - 0.7) * 55)
                g = int(210 + (progress - 0.7) * 45)
                b = int(240 + (progress - 0.7) * 15)
            
            sky_color = (min(255, r), min(255, g), min(255, b))
            pygame.draw.line(self.screen, sky_color, (80, y), (SCREEN_WIDTH - 80, y))
        
        # Himalayan mountain range with multiple layers
        camera_offset = self.camera_y * 0.05  # Slower parallax for distant mountains
        
        # Layer 1: Distant peaks (lightest, furthest)
        distant_points = []
        # Extend range to cover full width plus extra to prevent gaps
        for x in range(70, SCREEN_WIDTH - 70, 12):
            # Create jagged, tall peaks like Himalayas
            base_height = 200 + math.sin((x + camera_offset * 0.3) * 0.008) * 40
            # Add sharp peaks
            peak_variation = math.sin((x + camera_offset * 0.3) * 0.03) * 60
            jagged_variation = math.sin((x + camera_offset * 0.3) * 0.1) * 20
            height = base_height + peak_variation + jagged_variation
            distant_points.append((x, SCREEN_HEIGHT - height))
        # Ensure full coverage by adding corner points
        distant_points.extend([(SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
        pygame.draw.polygon(self.screen, (190, 200, 220), distant_points)
        
        # Layer 2: Middle range (medium tone)
        middle_points = []
        for x in range(70, SCREEN_WIDTH - 70, 10):
            base_height = 160 + math.sin((x + camera_offset * 0.5) * 0.012) * 50
            # Different peak pattern
            peak_variation = math.sin((x + camera_offset * 0.5) * 0.025) * 45
            jagged_variation = math.sin((x + camera_offset * 0.5) * 0.08) * 15
            height = base_height + peak_variation + jagged_variation
            middle_points.append((x, SCREEN_HEIGHT - height))
        middle_points.extend([(SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
        pygame.draw.polygon(self.screen, (150, 160, 180), middle_points)
        
        # Layer 3: Near mountains (darkest, closest)
        near_points = []
        for x in range(70, SCREEN_WIDTH - 70, 8):
            base_height = 120 + math.sin((x + camera_offset * 0.7) * 0.015) * 35
            # Sharp, dramatic peaks
            peak_variation = math.sin((x + camera_offset * 0.7) * 0.04) * 40
            jagged_variation = math.sin((x + camera_offset * 0.7) * 0.12) * 12
            height = base_height + peak_variation + jagged_variation
            near_points.append((x, SCREEN_HEIGHT - height))
        near_points.extend([(SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
        pygame.draw.polygon(self.screen, (110, 120, 140), near_points)
        
        # Add some clouds drifting between mountains
        self.draw_mountain_clouds(camera_offset)
    
    def draw_mountain_clouds(self, camera_offset):
        # Draw wispy clouds between mountain layers
        cloud_offset = camera_offset * 0.02  # Very slow movement
        for i in range(2):
            cloud_x = 120 + i * 120 + (cloud_offset % 300)
            cloud_y = SCREEN_HEIGHT - 180 + i * 40
            
            # Draw wispy cloud shape
            for j in range(4):
                circle_x = cloud_x + j * 12 - 18
                circle_y = cloud_y + math.sin(j + cloud_offset * 0.1) * 3
                radius = 8 - abs(j - 1.5) * 2
                # Semi-transparent white clouds
                cloud_surface = pygame.Surface((radius * 2, radius * 2))
                cloud_surface.set_alpha(120)
                cloud_surface.fill((255, 255, 255))
                pygame.draw.circle(cloud_surface, (255, 255, 255), (radius, radius), radius)
                self.screen.blit(cloud_surface, (circle_x - radius, circle_y - radius))
    
    def draw_walls(self):
        # Left wall
        pygame.draw.rect(self.screen, DARK_BROWN, (0, 0, 80, SCREEN_HEIGHT))
        # Right wall
        pygame.draw.rect(self.screen, DARK_BROWN, (SCREEN_WIDTH - 80, 0, 80, SCREEN_HEIGHT))
        
        # Wall decorations
        for i in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.rect(self.screen, BROWN, (10, i, 60, 10))
            pygame.draw.rect(self.screen, BROWN, (SCREEN_WIDTH - 70, i, 60, 10))
    
    def draw(self):
        self.draw_background()
        self.draw_walls()
        
        # Draw game objects (adjusted for camera)
        camera_offset = self.camera_y
        
        # Draw enemies
        for enemy in self.enemies:
            if -50 < enemy.y - camera_offset < SCREEN_HEIGHT + 50:
                enemy_copy = Enemy(enemy.x, enemy.y - camera_offset, enemy.type)
                enemy_copy.rotation = enemy.rotation
                enemy_copy.draw(self.screen)
        
        # Draw power-ups
        for powerup in self.powerups:
            if -50 < powerup.y - camera_offset < SCREEN_HEIGHT + 50:
                powerup_copy = PowerUp(powerup.x, powerup.y - camera_offset, powerup.type)
                powerup_copy.bob_offset = powerup.bob_offset
                powerup_copy.draw(self.screen)
        
        # Draw player
        player_copy = Player(self.player.x, self.player.y - camera_offset)
        player_copy.invincible = self.player.invincible
        player_copy.invincible_timer = self.player.invincible_timer
        player_copy.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # Highscore
        highscore_text = self.font.render(f"High Score: {self.highscore}", True, BLACK)
        self.screen.blit(highscore_text, (10, 10))
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 50))
        
        # Power-up status
        y_offset = 50
        if self.player.speed_boost:
            boost_text = self.small_font.render(f"Chiyaa: {self.player.speed_boost_timer//60 + 1}s", True, ORANGE)
            self.screen.blit(boost_text, (10, y_offset))
            y_offset += 25
        
        if self.player.invincible:
            invincible_text = self.small_font.render(f"Prayer Wheel: {self.player.invincible_timer//60 + 1}s", True, GOLD)
            self.screen.blit(invincible_text, (10, y_offset))
        
        # Instructions
        instruction_text = self.small_font.render("SPACE/Click to jump", True, (100, 100, 100))
        self.screen.blit(instruction_text, (10, SCREEN_HEIGHT - 30))
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font.render("Game Over!", True, WHITE)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        highscore_text = self.font.render(f"High Score: {self.highscore}", True, GOLD)
        restart_text = self.small_font.render("Press R or Click to restart", True, WHITE)
        
        # Center the text
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 70)))
        self.screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30)))
        self.screen.blit(highscore_text, highscore_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60)))
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
