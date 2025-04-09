import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True

phineas_image = pygame.image.load("assets/images/phineas_flipped.png")

phineas_x = 0
phineas_y = 0

phineas_vx = 20
phineas_vy = 0

gravity = 500

p_width = phineas_image.get_width()
p_height = phineas_image.get_height()

clock = pygame.time.Clock()

rects = []

score = 0

while running:

    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        phineas_vy = -400

    if keys[pygame.K_RIGHT]:
        phineas_x += phineas_vx
    if keys[pygame.K_LEFT]:
        phineas_x -= phineas_vx

    screen.fill((0, 0, 0))

    if random.randint(0, 2000) > 1897:
        rects.append(pygame.rect.Rect(WIDTH, random.randint(0, HEIGHT), 10, 100))
    
    for rect in rects[:]:
        pygame.draw.rect(screen, (0, 255, 0), rect)

    phineas_rect = pygame.rect.Rect(phineas_x, phineas_y, p_width, p_height)

    for rect in rects:
        if phineas_rect.colliderect(rect):
            # pygame.draw.rect(screen, (255, 0, 0), rect)
            # print("collided")
            rects.remove(rect)
            score += 1
            
        rect.x -= 5

    screen.blit(phineas_image, (phineas_x, phineas_y))

    phineas_vy += gravity * dt

    phineas_y += phineas_vy * dt

    if phineas_y > HEIGHT - p_height:
        phineas_y = HEIGHT - p_height
        phineas_vy = 0

    pygame.display.flip()

print(f"Your score: {score}")

pygame.quit()