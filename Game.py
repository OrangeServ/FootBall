import pygame
import sys
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jeu de Football à 2 Joueurs")

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (50, 255, 0)

# Positions et dimensions des joueurs et de la balle
player_size = 50
player1_x, player1_y = width // 4, height // 2 - player_size // 2
player2_x, player2_y = 3 * width // 4, height // 2 - player_size // 2
ball_x, ball_y = width // 2, height // 2
ball_radius = 15
ball_speed_x, ball_speed_y = 5, 5

# Scores des joueurs
score1 = 0
score2 = 0

# Vitesse des joueurs
player_speed = 7

# Fonction pour dessiner le terrain de football
def draw_field():
    window.fill(green)
    pygame.draw.line(window, white, (width // 2, 0), (width // 2, height), 5)
    pygame.draw.circle(window, white, (width // 2, height // 2), 100, 5)
    pygame.draw.rect(window, white, (0, height // 2 - 100, 20, 200))  # But gauche
    pygame.draw.rect(window, white, (width - 20, height // 2 - 100, 20, 200))  # But droit

# Fonction pour réinitialiser la balle au centre avec un décompte
def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x, ball_y = width // 2, height // 2
    ball_speed_x, ball_speed_y = 5, 5
    for i in range(3, 0, -1):
        window.fill(green)
        draw_field()
        font = pygame.font.Font(None, 74)
        countdown_text = font.render(str(i), True, white)
        window.blit(countdown_text, (width // 2 - countdown_text.get_width() // 2, height // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player1_y > 0:
        player1_y -= player_speed
    if keys[pygame.K_DOWN] and player1_y < height - player_size:
        player1_y += player_speed
    if keys[pygame.K_LEFT] and player1_x > 0:
        player1_x -= player_speed
    if keys[pygame.K_RIGHT] and player1_x < width // 2 - player_size:
       player1_x += player_speed

    # Mouvement du joueur 2 avec la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x > width // 2:
        player2_x = mouse_x - player_size // 2
        player2_y = mouse_y - player_size // 2

    # Empêcher les joueurs d'entrer dans les cages
    if player1_x < 20:
        player1_x = 20
    if player2_x > width - 20 - player_size:
        player2_x = width - 20 - player_size

    # Mouvement de la balle
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision avec le haut et le bas de la fenêtre
    if ball_y - ball_radius < 0 or ball_y + ball_radius > height:
        ball_speed_y = -ball_speed_y

    # Collision avec les côtés des buts
    if (ball_x - ball_radius < 20 and not (height // 2 - 100 < ball_y < height // 2 + 100)) or \
       (ball_x + ball_radius > width - 20 and not (height // 2 - 100 < ball_y < height // 2 + 100)):
        ball_speed_x = -ball_speed_x

    # Collision avec les joueurs
    if (ball_x - ball_radius < player1_x + player_size and player1_y < ball_y < player1_y + player_size) or \
       (ball_x + ball_radius > player2_x and player2_y < ball_y < player2_y + player_size):
        ball_speed_x = -ball_speed_x

    # Buts
    if ball_x - ball_radius < 20 and height // 2 - 100 < ball_y < height // 2 + 100:
        score2 += 1
        reset_ball()
    elif ball_x + ball_radius > width - 20 and height // 2 - 100 < ball_y < height // 2 + 100:
        score1 += 1
        reset_ball()

    # Affichage
    draw_field()
    pygame.draw.rect(window, red, (player1_x, player1_y, player_size, player_size))
    pygame.draw.rect(window, blue, (player2_x, player2_y, player_size, player_size))
    pygame.draw.circle(window, black, (ball_x, ball_y), ball_radius)

    font = pygame.font.Font(None, 74)
    text1 = font.render(str(score1), True, white)
    text2 = font.render(str(score2), True, white)
    window.blit(text1, (width // 4, 50))
    window.blit(text2, (3 * width // 4, 50))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()

