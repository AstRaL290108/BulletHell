from game_object import *
from scen_manager import *
from config import *
from script import *

import sys
import os
import pygame
pygame.init()

system = System()
win = Window(WIDTH, HEIGHT)

scen = Scen("main-menu")
system.lost = 0

while win.run:
	win.update(system.all_object)

	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			for i in system.all_object:
				if isinstance(i, Button):
					pos = pygame.mouse.get_pos()
					if (pos[0] >= i.x and pos[0] <= i.x + i.width) and (pos[1] >= i.y and pos[1] <= i.y + i.height):
						i.active = False
						i.onclick_function(i.argument)
					else:
						i.active = True

		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()


	if scen.now_scen == "AllLevel":
		if scen.lost == 0:
			system.all_object.clear()

			s = [-300, 150]
			fileExt = []

			lost_x = 1
			lost_y = 1

			for file in os.listdir("maps"):
				if file.endswith(".txt"): 
					fileExt.append(os.path.join("maps", file).replace("maps\\", "").replace(".txt", ""))

			title = Text(system, 100, s[0] + 360, s[1], "Выберите уровень", [0, 0, 0])
			for i in range(len(fileExt)):
				button = Button(system, 36, s[0]+(320*lost_x), s[1] + 120*lost_y, f"Уровень {fileExt[i][4:]}", 300, 60, StartLvL, [scen, fileExt[i][4:]])
				lost_x += 1
				if lost_x == 6:
					lost_y += 1
					lost_x = 1

			scen.lost = 1


	if scen.now_scen == "main-menu":
		if scen.lost == 0:
			system.all_object.clear()
			
			title = Text(system, 100, 60, 150, "Bullet Hell", [0, 0, 0])
			button_start = Button(system, 36, 60, 280, "Начать", 250, 60, AllLvL, scen)
			button_exit = Button(system, 36, 60, 350, "Выйти", 250, 60, GameClose, None)

			scen.lost = 1


	if scen.now_scen[0:5] == "Level":
		if scen.lost == 0:
			scen.all_coin = 0
			system.all_object.clear()
			lvl_num = scen.now_scen[5:]

			map = open(f"maps/lvl_{lvl_num}.txt", "r")
			line_type = ''
			for line in map:
				try:
					if line == "#START\n":
						line_type = "s"

					if line == "#FINISH\n":
						line_type = "f"

					if line == "#ENUMY\n":
						line_type = "e"

					if line == "#BLOCK\n":
						line_type = "b"

					if line == "#COIN\n":
						line_type = "c"

					elif line_type == "b":
						z = line.split(";")
						block = Block(system, int(z[0]), int(z[1]), int(z[2]), int(z[3]))

					elif line_type == "e":
						z = line.split(";")
						enemy = Enemy(system, int(z[0]), int(z[1]), str(z[2][0]))

					elif line_type == "c":
						z = line.split(";")
						coin = Coin(system, int(z[0]), int(z[1]))

					elif line_type == "f":
					 	z = line.split(";")
					 	finish = Finish(system, int(z[0]), int(z[1]))

					elif line_type == "s":
						z = line.split(";")
						player = Player(system, int(z[0]), int(z[1]), 25, 25)
						

				except ValueError:
					pass

			map.close()

			scen.lost = 1

		if scen.lost == 1:
			player.control(system.all_object, scen)

			#coin render
			font = pygame.font.Font("data/font/main-font.ttf", 36)
			win.win.blit(font.render(str(scen.all_coin), True, [255, 255, 255]), (WIDTH - 200, 0))

			if finish.end_check(player) and scen.all_coin < 3:
				font = pygame.font.Font("data/font/main-font.ttf", 36)
				win.win.blit(font.render(str(scen.all_coin), True, [255, 0, 0]), (WIDTH - 200, 0))
			if finish.end_check(player) and scen.all_coin == 3:
				scen.memorize.clear()
				scen.memorize.append(scen.now_scen)
				scen.now_scen = "WinScreen"
				scen.lost = 0




	if scen.now_scen == "LoseScreen":
		if scen.lost == 0:
			system.all_object.clear()

			title = Text(system, 100, 60, 150, "Ты проиграл!", [0, 0, 0])
			button_restart = Button(system, 36, 60, 280, "Заново", 250, 60, ReStartLvL, scen)
			button_menu = Button(system, 36, 60, 350, "В меню", 250, 60, ToMenu, scen)

			scen.lost = 1


	if scen.now_scen == "WinScreen":
		if scen.lost == 0:
			system.all_object.clear()

			title = Text(system, 100, 60, 150, "Ты выиграл!", [0, 0, 0])
			button_restart = Button(system, 36, 60, 280, "Заново", 250, 60, ReStartLvL, scen)
			button_menu = Button(system, 36, 60, 350, "В меню", 250, 60, ToMenu, scen)

			scen.lost = 1