import pygame
import time
from random import *

pygame.init()

red = (255,0,0)
back = (255,247,0)
mw = pygame.display.set_mode((300,300))
mw.fill(back)
clock = pygame.time.Clock()


class Area():
	def __init__(self, x=0, y=0, width=5, height=5, color=None):
		self.rect = pygame.Rect(x, y, width, height)
		self.fill_color = back
		if color:
			self.fill_color = color

	def color(self, new_color):
		self.fill_color = new_color

	def fill(self):
		pygame.draw.rect(mw, self.fill_color, self.rect)

	def collidepoint(self, x, y):
		return self.rect.collidepoint(x, y)

	def colliderect(self, rect):
		return self.rect.colliderect(rect)

#класс для объектов-картинок
class Picture(Area):
	def __init__(self, filename, x=0, y=0, width=10, height=10):
		Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
		self.image = pygame.image.load(filename)

	def draw(self):
		mw.blit(self.image, (self.rect.x, self.rect.y))

class Label(Area):
	def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
		self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

	def draw(self, shift_x=0, shift_y=0):
		self.fill()
		mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

end = False

start_y = 5
start_x = 5
n = 9
monsters = list()

for i in range(3):
	y = start_y + (i*55)
	x = start_x + (i*27.5)

	for i in range(n):
		enemy = Picture('enemy_3.png', x, y, 50, 50)
		monsters.append(enemy)
		x = x + 55
	n -= 1

ball = Picture('ball_3.png',randint(0,200), 170, 50, 50)
platform = Picture('platform7.png', 150, 300, 120, 50)


total_label = Label(380,400,100,40,(134, 204,63))
total_label.set_text('Очки',40)
total_score = Label(380,450,100,40,(134, 204,63))

tab = Label(150,170,100,70,back)


move_right = False
move_left = False

speed_x = 3
speed_y = 3
total = 0


while not end :
	ball.fill()
	platform.fill()


	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				move_right = True
			if event.key == pygame.K_LEFT:
				move_left = True

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				move_right = False
			if event.key == pygame.K_LEFT:
				move_left = False

	if move_right:
		platform.rect.x += 6
	if move_left:
		platform.rect.x -= 6

	ball.rect.x += speed_x
	ball.rect.y += speed_y

	if ball.colliderect(platform.rect):
		speed_y *= -1
	if  ball.rect.y < 0:
		speed_y *= -1

	if ball.rect.x > 450 or ball.rect.x < 0:
		speed_x *= -1

	for m in monsters:
		m.draw()
		if m.rect.colliderect(ball.rect):
			monsters.remove(m)
			m.fill()
			speed_y *= -1
			total += 450

	if ball.rect.y >= 350 :
		tab.set_text("أنت مصاصة",70)
		tab.draw()
		end = True


	elif total == 10800:
		tab.set_text("أنت رائع",70)
		tab.draw()
		end = True


	ball.draw()
	platform.draw()

	total_score.set_text(total,40)
	total_score.draw(5,5)
	total_label.draw(5,5)


	pygame.display.update()
	clock.tick(40)