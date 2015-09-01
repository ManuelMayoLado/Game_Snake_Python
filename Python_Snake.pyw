# -*- coding: utf-8 -*-

#NON OPERATIVO

import random
import pygame
from pygame.locals import *

class punto:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class serpe:
	def __init__(self, punto, mov):
		self.punto = punto
		self.mov = mov

MARCO = 5

LADO_CADRADO = 10

VELOCIDADE_SERPE = 2

ANCHO_VENTANA = ALTO_VENTANA = 300

TICKS_SEGUNDO = 60

p_serpe = serpe(punto(MARCO, MARCO), "dereita")

lista_cola = []

pygame.init() #INICIAR PYGAME

def crear_punto_comida():
	lista_rect = []
	for i in lista_cola:
		lista_rect.append(pygame.Rect(i.x,i.y,LADO_CADRADO,LADO_CADRADO))
	while True:
		p = punto((random.randint(MARCO,ANCHO_VENTANA-(LADO_CADRADO+MARCO))),((random.randint(MARCO,ANCHO_VENTANA-(LADO_CADRADO+MARCO)))))
		rectangulo = pygame.Rect(p.x, p.y, LADO_CADRADO, LADO_CADRADO)
		if rectangulo.collidelist(lista_rect) == -1:
			break
	return p
	
punto_comida = crear_punto_comida()

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
pygame.display.set_caption("Python_Snake")

imag_rect_xogo = pygame.Rect(MARCO,MARCO,ANCHO_VENTANA-(MARCO*2),ALTO_VENTANA-(MARCO*2))

proximo_movemento = "dereita"

comeu = False

ON = True

GAME_OVER = False

bucle_on = 0

espacio_pulsado = False

while ON:

	reloj = pygame.time.Clock()
	
	#LIMPIAR PANTALLA:
	
	if not GAME_OVER:
		ventana.fill((0,0,0))
	else:
		ventana.fill((255,0,0))
	
	#DEBUXAR ELEMENTOS:
	
	pygame.draw.rect(ventana, (255,255,255), imag_rect_xogo)
		
	rect_comida = pygame.Rect(punto_comida.x, punto_comida.y, LADO_CADRADO, LADO_CADRADO)
	pygame.draw.rect(ventana, (180,180,50), rect_comida)
	
	color_verde = 170
	
	if bucle_on == 1:
		rect_serpe_ant = rect_serpe
		
	rect_serpe = pygame.Rect(p_serpe.punto.x, p_serpe.punto.y, LADO_CADRADO, LADO_CADRADO)
	pygame.draw.rect(ventana, (50,color_verde,0), rect_serpe)
	
	#for i in lista_cola:
	#	rect_cola = pygame.Rect(i.x, i.y, LADO_CADRADO, LADO_CADRADO)
	#	pygame.draw.rect(ventana, (50,color_verde,0), rect_cola)
	#	if color_verde >= 100:
	#		color_verde -= 1

	#ACCIÓNS SERPE:

	p_serpe = serpe(p_serpe.punto, proximo_movemento)

	#GAME OVER?
	
	if p_serpe.punto.x < MARCO or p_serpe.punto.x > ANCHO_VENTANA-(MARCO+LADO_CADRADO):
		GAME_OVER = True
	if p_serpe.punto.y < MARCO or p_serpe.punto.y > ANCHO_VENTANA-(MARCO+LADO_CADRADO):
		GAME_OVER = True
	if (p_serpe.punto.x <= MARCO and p_serpe.mov == "esquerda") or (p_serpe.punto.x >= ANCHO_VENTANA-(MARCO+LADO_CADRADO) and p_serpe.mov == "dereita"):
		GAME_OVER = True
	if (p_serpe.punto.y <= MARCO and p_serpe.mov == "arriba") or (p_serpe.punto.y >= ANCHO_VENTANA-(MARCO+LADO_CADRADO) and p_serpe.mov == "abaixo"):
		GAME_OVER = True
	for i in range(int((LADO_CADRADO/VELOCIDADE_SERPE)*3),len(lista_cola),1):
		if rect_serpe.colliderect(pygame.Rect(lista_cola[i].x,lista_cola[i].y,LADO_CADRADO,LADO_CADRADO)):
			GAME_OVER = True
	
	if comeu > 0:
		comeu -= 1
	
	#COME?
	
	if not GAME_OVER:
		#lista_cola.insert(0, p_serpe.punto)
		if rect_serpe.colliderect(rect_comida):
			comeu = LADO_CADRADO / VELOCIDADE_SERPE
			punto_comida = crear_punto_comida()
			pygame.display.update()
		#if comeu == 0:
		#	del lista_cola[len(lista_cola)-1]
			
		
	#MOVEMENTO
	
	p_serpe_anterior = punto(p_serpe.punto.x,p_serpe.punto.y)
	rectangulo_serpe_anterior = pygame.Rect(p_serpe_anterior.x,p_serpe_anterior.y,LADO_CADRADO,LADO_CADRADO)

	if not GAME_OVER:
		if p_serpe.mov == "dereita":
			p_serpe = serpe(punto(p_serpe.punto.x+VELOCIDADE_SERPE,p_serpe.punto.y), p_serpe.mov)
		elif p_serpe.mov == "esquerda":
			p_serpe = serpe(punto(p_serpe.punto.x-VELOCIDADE_SERPE,p_serpe.punto.y), p_serpe.mov)
		elif p_serpe.mov == "arriba":
			p_serpe = serpe(punto(p_serpe.punto.x,p_serpe.punto.y-VELOCIDADE_SERPE), p_serpe.mov)
		elif p_serpe.mov == "abaixo":
			p_serpe = serpe(punto(p_serpe.punto.x,p_serpe.punto.y+VELOCIDADE_SERPE), p_serpe.mov)
	
	#UPDATE:
	
	if not bucle_on:
		pygame.display.update()
	else:
		pygame.display.update(rectangulo_serpe_anterior)
	
	
	if espacio_pulsado:
		espacio_pulsado = False
	
	#EVENTOS - KEYDOWN and EXIT:
	
	for eventos in pygame.event.get():
	
		if eventos.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
			
		if eventos.type == pygame.KEYDOWN:
			if eventos.key == K_SPACE and GAME_OVER:
				GAME_OVER = False
				p_serpe = serpe(punto(MARCO, MARCO), "dereita")
				proximo_movemento = "dereita"
				lista_cola = []
				pygame.display.update()
				espacio_pulsado = True
			elif (eventos.key == K_UP or eventos.key == K_w) and not GAME_OVER and not p_serpe.mov == "abaixo":
				proximo_movemento = "arriba"
			elif (eventos.key == K_DOWN or eventos.key == K_s) and not GAME_OVER and not p_serpe.mov == "arriba":
				proximo_movemento = "abaixo"
			elif (eventos.key == K_RIGHT or eventos.key == K_d) and not GAME_OVER and not p_serpe.mov == "esquerda":
				proximo_movemento = "dereita"
			elif (eventos.key == K_LEFT or eventos.key == K_a) and not GAME_OVER and not p_serpe.mov == "dereita":
				proximo_movemento = "esquerda"
				
	reloj.tick(TICKS_SEGUNDO)
	
	bucle_on = 1