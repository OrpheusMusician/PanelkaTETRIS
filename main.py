import pygame
from copy import deepcopy # для изменения элементов списка (в виде экземпляров)
from random import choice, randrange
import panel


W, H = 10 ,20
TILE = 48
GAME_RES = W * TILE, H * TILE
RES = W * TILE * 2 + 10, H * TILE + 10

FPS = 60


pygame.init()

sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES) 
pygame.display.set_caption('Doomer\'s Panelka Simulator')
clock = pygame.time.Clock()

bg = pygame.image.load('assets/window_bg.jpg').convert()
game_bg = pygame.image.load('assets/surface_bg.jpg').convert()

flat_textures = [pygame.image.load('assets/textures/bars.jpg'), 
				 pygame.image.load('assets/textures/neon.jpg'), 
				 pygame.image.load('assets/textures/rostelekom.jpg'), 
				 pygame.image.load('assets/textures/red.jpg')]

# заготовка пустого поля
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

# фигуры на координатных осях в виде плиток
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],   # 0
               [(0, -1), (-1, -1), (-1, 0), (0, 0)], # 1
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],  # 2
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],  # 3
               [(0, 0), (0, -1), (0, 1), (-1, -1)],  # 4
               [(0, 0), (0, -1), (0, 1), (1, -1)],   # 5
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]   # 6

# фигуры в виде связных плиток
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
# для составляющих частей конкретной фигуры
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
# заполняемость поля
field = [[0 for i in range(W)] for j in range(H)]



# анимация
animation_count, animation_speed, animation_limit = 0, 60, 2000

# текущая фигура
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
current_textures = [choice(flat_textures), choice(flat_textures), choice(flat_textures), choice(flat_textures)]
next_textures = [choice(flat_textures), choice(flat_textures), choice(flat_textures), choice(flat_textures)]


# score | счет
score, lines = 0, 0
scores_in_a_row = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False

    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    
    return True

def get_record():
    try:
        with open('assets/record') as f:
            return f.readline()

    except FileNotFoundError:
        with open('assets/record', 'w') as f:
            f.write('0')
            return '0'

def set_record(record, score):
    rec = max(int(record), score)
    with open('assets/record', 'w') as f:
        f.write(str(rec))

while True:
	record = get_record()

	dx = 0 # изменение координаты по х
	rotate = False

	sc.blit(bg, (0, 0))
	sc.blit(game_sc, (121, 6))
	game_sc.blit(game_bg, (0, 0))

	# delay
	for i in range(lines):
		pygame.time.wait(200)

	# control | управление
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			exit()

		if (event.type == pygame.KEYDOWN):
			if (event.key == pygame.K_LEFT):
				dx = -1

			elif (event.key == pygame.K_RIGHT):
				dx = 1

			elif (event.key == pygame.K_DOWN):
				animation_limit = 100

			elif (event.key == pygame.K_UP):
				rotate = True

	# move x | движение по горизонтали
	figure_old = deepcopy(figure)
	for i in range(4):
		figure[i].x += dx
		
		# если выход за границы поля, то копируем обратно и обрываем перемещение
		if (not check_borders()):
			figure = deepcopy(figure_old)
			break

	# move y | движение по вертикали
	animation_count += animation_speed
	if (animation_count > animation_limit):
		animation_count = 0

		figure_old = deepcopy(figure)
		for i in range(4):
			figure[i].y += 1
			
			# если выход за границы поля, то копируем обратно и обрываем перемещение
			if (not check_borders()):

				for j in range(4):
					field[figure_old[j].y][figure_old[j].x] = current_textures[j]

				figure = deepcopy(next_figure)
				current_textures = next_textures

				next_figure = deepcopy(choice(figures))
				next_textures = [choice(flat_textures), choice(flat_textures), choice(flat_textures), choice(flat_textures)]

				animation_limit = 2000
				break

	# rotation | вращение
	center = figure[0]
	figure_old = deepcopy(figure)
	if (rotate):
		for i in range(4):
			x = figure[i].y - center.y
			y = figure[i].x - center.x

			figure[i].x = center.x - x
			figure[i].y = center.y + y

			if not check_borders():
				figure = deepcopy(figure_old)
				break

	# check full lines | проверка заполненных линий
	line, lines = H - 1, 0
	for row in range(H - 1, -1, -1):
		count = 0
		for i in range(W):
			if field[row][i]:
				count += 1

			field[line][i] = field[row][i]

		if (count < W):
			line -= 1

		else:
			animation_speed += 3
			lines += 1


	# checking score | проверка счёта
	score += scores_in_a_row[lines]

	# draiwing grid | отрисовка поля
	[pygame.draw.rect(game_sc, (108, 119, 139), i_rect, 1) for i_rect in grid]

	# drawing figure | отрисовка фигуры
	for i in range(4):

		x, y = figure[i].x * TILE, figure[i].y * TILE
		figure_rect.x = figure[i].x * TILE
		figure_rect.y = figure[i].y * TILE

		pygame.draw.rect(game_sc, pygame.Color('white'), figure_rect)
		game_sc.blit(current_textures[i], (x, y))

	# drawing field | отрисовка заполненной части игрового поля
	for y, raw in enumerate(field):
		for x, col in enumerate(raw):
			if (col):
				figure_rect.x, figure_rect.y = x * TILE, y * TILE
				pygame.draw.rect(game_sc, (40, 40, 40), figure_rect)
				game_sc.blit(col, (x * TILE, y * TILE))

	# отрисовка следующей фигуры


	# menu | отрисовка меню
	sc.blit(panel.title_tetris1, (680, 5))
	sc.blit(panel.title_tetris2, (680, 50))

	sc.blit(panel.title_score, (680, 375))
	sc.blit(panel.font_sml.render(str(score), True, pygame.Color('white')), (680, 455))

	sc.blit(panel.title_record, (680, 575))
	sc.blit(panel.font_sml.render(str(record), True, pygame.Color('white')), (680, 655))

	# game over check | проверка на конец игры
	for i in range(W):
		if field[0][i]:

			set_record(record, score)
			print(record, score)
            
			field = [[0 for i in range(W)] for i in range(H)]
			animation_count, animation_speed, animation_limit = 0, 60, 2000
			score = 0

			for i_rect in grid:
				pygame.draw.rect(game_sc, pygame.Color('white'), i_rect)
				sc.blit(game_sc, (121, 6))
				pygame.display.flip()
				clock.tick(200)

	pygame.display.flip()
	clock.tick(FPS)