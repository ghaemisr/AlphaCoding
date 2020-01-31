# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window. The size can either be a tuple or a list
# A surface defines a rectangular area on which you can draw.
# set_mode returns a surface representing the visible part of the window.
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue square in the center
    # The surfaces can be passed as inputs to draw functions.
    pygame.draw.rect(screen, (0, 0, 255), (250, 250, 50, 50))

    # With surface
    # image = pygame.Surface((50, 50))
    # image.fill((0, 0, 255))
    # rect = image.get_rect()
    # screen.blit(image, (250, 250))

    # Flip the display
    # Contents of that surface are pushed to the display when we call flip. The entire display is updated.
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()