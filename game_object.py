import pygame
pygame.init()

import config
import script

# background = pygame.image.load("data/image/background/background.jpg")
# background = pygame.transform.scale(background, (1280, 720))


class System:
	all_object = []

	def RestartScen(self, all_object, start_ord):
		for i in range(len(all_object)):
			all_object[i].x = start_ord[i][0]
			all_object[i].y = start_ord[i][1]

 
class Window:
	win = None
	run = True
	clock = pygame.time.Clock()

	def __init__(self, width, height):
		self.win = pygame.display.set_mode((width, height))
		pygame.display.set_caption("BulletHell")
		pygame.display.set_icon(pygame.image.load("data/image/icon.ico"))


	def update(self, all_object):
		pygame.display.update()
		self.clock.tick(120)
		#round(self.clock.get_fps())

		#BackGround
		#self.win.blit(background, (0, 0))
		self.win.fill((201, 201, 201))

		for i in all_object:
			if i.draw_type == "rect":
				pygame.draw.rect(self.win, i.color, (i.x, i.y, i.width, i.height))
			if i.draw_type == "custom":
				i.draw(self.win)
			if i.draw_type == "circle":
				pygame.draw.circle(self.win, i.color, (i.x, i.y), i.radius)
			if i.draw_type == "text":
				font = pygame.font.Font("data/font/main-font.ttf", i.font_size)
				self.win.blit(font.render(i.text, True, i.color), (i.x, i.y))

			if isinstance(i, Button):
				pos = pygame.mouse.get_pos()
				if (pos[0] >= i.x and pos[0] <= i.x + i.width) and (pos[1] >= i.y and pos[1] <= i.y + i.height):
					i.active = True
				else:
					i.active = False


class Player:
	draw_type = "custom"
	speed = 0

	width = 0
	height = 0

	x = 0
	y = 0

	def lose(self, scen):
		scen.memorize.clear()
		scen.memorize.append(scen.now_scen)
		scen.lost = 0 
		scen.now_scen = "LoseScreen"

	def draw(self, win):
		pygame.draw.rect(win, (53, 53, 53), (self.x, self.y, self.width, self.height))
		pygame.draw.rect(win, (201, 46, 46), (self.x + 5, self.y + 5, self.width - 10, self.height - 10))

	def __init__(self, system, x, y, width, height):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.speed = 5

		system.all_object.append(self)

	def control(self, all_object, scen):
		keys = pygame.key.get_pressed()
		move_left = True
		move_right = True
		move_top = True
		move_bottom = True

		for i in all_object:
			if isinstance(i, Block):
				if (self.x == i.x + i.width and self.x <= i.x + i.width + 5) and ((self.y >= i.y and self.y < i.y + i.height) or (self.y + self.height > i.y and self.y + self.height < i.y + i.height)):
					move_left = False
				if (self.x + self.width == i.x and self.x + self.width >= i.x - 5) and ((self.y >= i.y and self.y < i.y + i.height) or (self.y + self.height > i.y and self.y + self.height < i.y + i.height)):
					move_right = False

				if (self.y >= i.y + i.height and self.y <= i.y + i.height + 5) and ((self.x >= i.x and self.x <= i.x + i.width) or (self.x + self.width >= i.x and self.x + self.width <= i.x + i.width)):
					move_top = False
				if (self.y + self.height == i.y and self.y <= i.y - 5) and ((self.x >= i.x and self.x <= i.x + i.width) or (self.x + self.width >= i.x and self.x + self.width <= i.x + i.width)):
					move_bottom = False


			if isinstance(i, Enemy):
				i.enumy_colider(self, scen)
				i.enumy_move()

			if isinstance(i, Coin):
				i.coin_colider(self, scen)

			


		if keys[pygame.K_a] and move_left:
			self.x -= self.speed
		elif keys[pygame.K_d] and move_right:
			self.x += self.speed	
		elif keys[pygame.K_w] and move_top:
			self.y -= self.speed
		elif keys[pygame.K_s] and move_bottom:
			self.y += self.speed

		# if keys[pygame.K_a] and keys[pygame.K_w]:
		# 	self.x -= self.speed
		# 	self.y -= self.speed
		# if keys[pygame.K_d] and keys[pygame.K_w]:
		# 	self.x += self.speed	
		# 	self.y -= self.speed
		# if keys[pygame.K_a] and keys[pygame.K_s]:

		# 	self.y += self.speed
		# if keys[pygame.K_d] and keys[pygame.K_s]:
		# 	self.x += self.speed
		# 	self.y += self.speed


class Block:
	draw_type = "rect"
	color = None

	width = 0
	height = 0

	x = 0
	y = 0

	def __init__(self, system, x, y, width, height):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.color = [53, 50, 152]

		system.all_object.append(self)


class Enemy:
	draw_type = "circle"
	color = None

	radius = 0

	x = 0
	y = 0

	move_type = None

	speed_x = 8
	speed_y = 8

	def enumy_move(self):
		if self.move_type == "d":
			if self.x - self.radius <= 4 or self.x + self.radius >= 1917:
				self.speed_x = -self.speed_x
			if self.y - self.radius <= 4 or self.y + self.radius >= 1077:
				self.speed_y = -self.speed_y

			self.x += self.speed_x
			self.y += self.speed_y

		if self.move_type == "h":
			if self.x - self.radius <= 4 or self.x + self.radius >= 1917:
				self.speed_x = -self.speed_x
			if self.y - self.radius <= 4 or self.y + self.radius >= 1077:
				self.speed_y = -self.speed_y

			self.x += self.speed_x

		if self.move_type == "v":
			if self.x - self.radius <= 4 or self.x + self.radius >= 1917:
				self.speed_x = -self.speed_x
			if self.y - self.radius <= 4 or self.y + self.radius >= 1077:
				self.speed_y = -self.speed_y

			self.y += self.speed_y
		


	def draw(self, win):
		pygame.draw.circle(win, (53, 53, 53), (self.x, self.y), self.radius)
		pygame.draw.circle(win, (51, 51, 255), (self.x, self.y), self.radius - 5)

	def enumy_colider(self, player, scen):
		left = left = [player.x + player.width*0.5, player.y + player.height*0.5]

		if left[0] <= self.x + self.radius and left[0] >= self.x - self.radius and left[1] <= self.y + self.radius and left[1] >= self.y - self.radius:
			player.lose(scen)

	def __init__(self, system, x, y, move_type):
		self.x = x
		self.y = y
		self.radius = 13
		self.color = [51, 0, 0]

		self.move_type = move_type

		system.all_object.append(self)


class Coin:
	draw_type = "circle"
	color = None

	radius = 0

	x = 0
	y = 0

	move_type = None

	def draw(self, win):
		pygame.draw.circle(win, (53, 53, 53), (self.x, self.y), self.radius)
		pygame.draw.circle(win, (51, 51, 255), (self.x, self.y), self.radius - 5)

	def coin_colider(self, player, scen): 
		left = [player.x + player.width*0.5, player.y + player.height*0.5]

		if left[0] <= self.x + self.radius and left[0] >= self.x - self.radius and left[1] <= self.y + self.radius and left[1] >= self.y - self.radius:
			scen.all_coin += 1
			self.x = 2000
			

	def __init__(self, system, x, y):
		self.x = x
		self.y = y
		self.radius = 13
		self.color = [255, 255, 0]

		system.all_object.append(self)



class Text:
	draw_type = "text"
	text = ""
	color = None

	font_size = 0
	x = 0
	y = 0

	def __init__(self, system, font_size, x, y, text, color):
		self.font_size = font_size
		self.x = x
		self.y = y

		self.color = color
		self.text = text

		system.all_object.append(self)



class Button:
	draw_type = "custom"
	text = ""

	font_size = 0

	width = 0
	height = 0
	x = 0
	y = 0

	active = False
	onclick_function = None
	argument = None

	def draw(self, win):
		if not(self.active):
			pygame.draw.rect(win, [0, 0, 0], (self.x, self.y, self.width, self.height), round(self.font_size/10))

			font = pygame.font.Font("data/font/main-font.ttf", self.font_size)
			win.blit(font.render(self.text, True, [0, 0, 0]), (self.x + self.width / 2 - self.font_size*1.5, self.y + self.font_size*0.2))

		elif self.active:
			pygame.draw.rect(win, [0, 0, 0], (self.x, self.y, self.width, self.height))

			font = pygame.font.Font("data/font/main-font.ttf", self.font_size)
			win.blit(font.render(self.text, True, [255, 255, 255]), (self.x + self.width / 2 - self.font_size*1.5, self.y + self.font_size*0.2))


	def __init__(self, system, font_size, x, y, text, width, height, onclick_function, argument):
		self.font_size = font_size
		self.x = x
		self.y = y

		self.width = width
		self.height = height

		self.text = text
		self.onclick_function = onclick_function
		self.argument = argument

		system.all_object.append(self)



class Finish:
	draw_type = "custom"

	width = 100
	height = 50
	x = 0
	y = 0

	def draw(self, win):
		pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width*0.25, self.height*0.5))
		pygame.draw.rect(win, (255, 255, 255), (self.x + 25, self.y, self.width/4, self.height/2))
		pygame.draw.rect(win, (0, 0, 0), (self.x + 50, self.y, self.width/4, self.height/2))
		pygame.draw.rect(win, (255, 255, 255), (self.x + 75, self.y, self.width/4, self.height/2))

		pygame.draw.rect(win, (255, 255, 255), (self.x, self.y + 25, self.width/4, self.height/2))
		pygame.draw.rect(win, (0, 0, 0), (self.x + 25, self.y + 25, self.width/4, self.height/2))
		pygame.draw.rect(win, (255, 255, 255), (self.x + 50, self.y + 25, self.width/4, self.height/2))
		pygame.draw.rect(win, (0, 0, 0), (self.x + 75, self.y + 25, self.width/4, self.height/2))

	def __init__(self, system, x, y):
		self.x = x
		self.y = y

		self.width = 100
		self.height = 50

		system.all_object.append(self)


	def end_check(self, player):
		if (player.x >= self.x and player.x <= self.x + self.width) and (player.y >= self.y and player.y <= self.y + self.height):
			return True
		if (player.x + player.width >= self.x and player.x + player.width <= self.x + self.width) and (player.y >= self.y and player.y <= self.y + self.height):
			return True