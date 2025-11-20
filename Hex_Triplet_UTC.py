import pygame
import datetime
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexadecimal UTC Clock")

# Font setup
font = pygame.font.SysFont('monospace', 72, bold=True)

# Time conversion factors
SECONDS_PER_HEX_SECOND = 1.318359375
SECONDS_PER_HEX_MINUTE = 21.09375
SECONDS_PER_HEX_HOUR = 90 * 60  # 1 hour 30 minutes in seconds
SECONDS_PER_HEX_DAY = 24 * 60 * 60  # 24 hours in seconds

def get_hex_time():
    """Calculate the current hex time based on UTC"""
    now = datetime.datetime.utcnow()
    
    # Total seconds since midnight UTC
    total_seconds = now.hour * 3600 + now.minute * 60 + now.second + now.microsecond / 1e6
    
    # Calculate hex time components
    hex_day = int((total_seconds / SECONDS_PER_HEX_DAY) * 256) % 256
    hex_hour = int((total_seconds / SECONDS_PER_HEX_HOUR) * 256) % 256
    hex_minute = int((total_seconds / SECONDS_PER_HEX_MINUTE) * 256) % 256
    hex_second = int((total_seconds / SECONDS_PER_HEX_SECOND) * 256) % 256
    
    return hex_day, hex_hour, hex_minute, hex_second

def hex_to_rgb(hex_day, hex_hour, hex_minute):
    """Convert hex time components to RGB color"""
    # Use the three components to create an RGB color
    r = int((hex_day / 255) * 255)
    g = int((hex_hour / 255) * 255)
    b = int((hex_minute / 255) * 255)
    
    return (r, g, b)

def main():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Get current hex time
        hex_day, hex_hour, hex_minute, hex_second = get_hex_time()
        
        # Format time as hex triplet
        time_str = f"{hex_day:02X}_{hex_hour:02X}_{hex_minute:02X}"
        
        # Calculate background color
        bg_color = hex_to_rgb(hex_day, hex_hour, hex_minute)
        
        # Fill screen with background color
        screen.fill(bg_color)
        
        # Render time text
        text_surface = font.render(time_str, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        
        # Draw a semi-transparent box behind the text
        box_rect = text_rect.inflate(40, 20)
        box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(box_surface, box_rect)
        
        # Draw the text
        screen.blit(text_surface, text_rect)
        
        # Update display
        pygame.display.flip()
        
        # Cap at 60 FPS
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()