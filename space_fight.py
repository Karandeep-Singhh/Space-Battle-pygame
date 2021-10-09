import pygame
import os

pygame.font.init()

WIDTH, HEIGHT = 900,500

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("game")

WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)

FPS = 60
S_WIDTH, S_HEIGHT = 45,48
VEL = 5
MAX_BULLETS = 3
BULLET_VEL = 7

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


RED_HIT = pygame.USEREVENT + 2
YELLOW_HIT = pygame.USEREVENT + 1

YELLOW__SPACESHIP_IMAGE = pygame.transform.rotate(pygame.image.load(
		os.path.join('Assets', 'spaceship_yellow.png')), 90)
YELLOW_SPACESHIP = pygame.transform.scale(
		YELLOW__SPACESHIP_IMAGE, (S_WIDTH,S_HEIGHT))

RED__SPACESHIP_IMAGE = pygame.transform.rotate(pygame.image.load(
		os.path.join('Assets', 'spaceship_red.png')), 270)
RED_SPACESHIP = pygame.transform.scale(
		RED__SPACESHIP_IMAGE, (S_WIDTH,S_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')), (WIDTH,HEIGHT))

def draw(red,yellow,yellow_bullets,red_bullets, yellow_health, red_health):
	WIN.blit(SPACE, (0,0))

	red_health_text = HEALTH_FONT.render("Health: "+str(red_health), 1, WHITE)
	yellow_health_text = HEALTH_FONT.render("Health: "+str(yellow_health), 1, WHITE)

	WIN.blit(red_health_text, (WIDTH-red_health_text.get_width() - 5, 5))
	WIN.blit(yellow_health_text, (5, 5))

	WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
	WIN.blit(RED_SPACESHIP,(red.x,red.y))



	for bullet in yellow_bullets:
		pygame.draw.rect(WIN, YELLOW, bullet)
	
	for bullet in red_bullets:
		pygame.draw.rect(WIN, RED, bullet)
	
	pygame.display.update()

def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()//2 - 2, HEIGHT/2 - draw_text.get_height()//2))

	pygame.display.update()
	pygame.time.delay(3000)

def yellow_movement(keys_pressed,yellow):
	if keys_pressed[pygame.K_a]:
		yellow.x -= VEL
		if yellow.x<0:
			yellow.x = 0
	if keys_pressed[pygame.K_w]:
		yellow.y -= VEL
		if yellow.y<0:
			yellow.y = 0
	if keys_pressed[pygame.K_d]:
		yellow.x += VEL
		if yellow.x > (WIDTH/2)-S_WIDTH-5:
			yellow.x = (WIDTH/2)-S_WIDTH-5
	if keys_pressed[pygame.K_s]:
		yellow.y += VEL
		if yellow.y>HEIGHT-S_HEIGHT:
			yellow.y = HEIGHT-S_HEIGHT

def red_movement(keys_pressed,red):
	if keys_pressed[pygame.K_LEFT]:
		red.x -= VEL
		if red.x<(WIDTH/2)+5:
			red.x = (WIDTH/2)+5

	if keys_pressed[pygame.K_UP]:
		red.y -= VEL
		if red.y<0:
			red.y = 0

	if keys_pressed[pygame.K_RIGHT]:
		red.x += VEL
		if red.x > WIDTH-S_WIDTH:
			red.x = WIDTH-S_WIDTH

	if keys_pressed[pygame.K_DOWN]:
		red.y += VEL
		if red.y>HEIGHT-S_HEIGHT:
			red.y = HEIGHT-S_HEIGHT

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
	for bullet in yellow_bullets:
		bullet.x += BULLET_VEL
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)

		elif bullet.x > WIDTH-bullet.width:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= BULLET_VEL
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		elif bullet.x < 0:
			red_bullets.remove(bullet)


def main():

	red = pygame.Rect(750,200,S_WIDTH,S_HEIGHT)
	yellow = pygame.Rect(100,200,S_WIDTH,S_HEIGHT)

	red_bullets = []
	yellow_bullets = []

	red_health = 5
	yellow_health = 5

	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
					bullet = pygame.Rect(yellow.x+yellow.width, yellow.y+yellow.height//2 - 2, 10, 4)
					yellow_bullets.append(bullet)

				if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
					bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 4)
					red_bullets.append(bullet)

			if event.type == RED_HIT:
				red_health -= 1
			
			if event.type == YELLOW_HIT:
				yellow_health -= 1

		winner_text = ""
		
		if red_health <= 0:
			winner_text = "YELLOW WINS!!"

		if yellow_health <= 0:
			winner_text = "RED WINS!!"

		if winner_text != "":
			draw_winner(winner_text)
			break
		

		keys_pressed = pygame.key.get_pressed()

		yellow_movement(keys_pressed, yellow)
		red_movement(keys_pressed, red)

		handle_bullets(yellow_bullets, red_bullets, yellow, red)
		
		draw(red,yellow,yellow_bullets,red_bullets, yellow_health, red_health)

	main()

main()