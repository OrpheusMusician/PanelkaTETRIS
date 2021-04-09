import pygame

pygame.init()

font_big= pygame.font.Font('assets/fonts/piksel_font.ttf', 60)
font_sml = pygame.font.Font('assets/fonts/piksel_font.ttf', 40)

title_tetris1 = font_sml.render('Панелька', True, pygame.Color('white'))
title_tetris2 = font_big.render('TETRIS', True, pygame.Color('white'))

title_score = font_sml.render('Счёт:', True, pygame.Color('white'))
title_record = font_sml.render('Рекорд:', True, pygame.Color('white'))