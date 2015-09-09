# -*- coding: utf-8 -*-

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

N_CADROS = 30 #POR FILA

lado_cadrado = 10

LADO_VENTANA = (N_CADROS * lado_cadrado) + (MARCO * 2)

TICKS_SEGUNDO = 60

MOVEMENTOS_SEGUNDO = 8 #MOVEMENTOS POR SEGUNDO

FRECUENCIA = TICKS_SEGUNDO / MOVEMENTOS_SEGUNDO

p_serpe = serpe(punto(MARCO+lado_cadrado*2, MARCO), "dereita")

lista_cola = [punto(MARCO+lado_cadrado,MARCO),punto(MARCO,MARCO)]

def crear_punto_comida():
	global lista_cola
	lista = lista_cola[:]
	lista.insert(0, p_serpe.punto)
	correcto = False
	while not correcto:
		p = punto(((random.randint(0,N_CADROS-1))*lado_cadrado)+MARCO,((random.randint(0,N_CADROS-1))*lado_cadrado)+MARCO)
		c = 0
		for i in lista:
			c += 1
			if p.x == i.x and p.y == i.y:
				break
			elif c == len(lista):
				correcto = True
	return p
	

punto_comida = crear_punto_comida()

pygame.init() #INICIAR PYGAME

ventana = pygame.display.set_mode([LADO_VENTANA, LADO_VENTANA],0,32)
pygame.display.set_caption("Python_Snake")

imag_rect_xogo = pygame.Rect(MARCO,MARCO,LADO_VENTANA-(MARCO*2),LADO_VENTANA-(MARCO*2))

proximo_movemento = "dereita"

ON = True

Cadricula = False

cont_frecuencia = 0

GAME_OVER = False

while ON:

	reloj = pygame.time.Clock()
	
	#LIMPIAR PANTALLA:
	
	if not GAME_OVER:
		ventana.fill((255,255,255))
	elif len(lista_cola)+1 == N_CADROS * N_CADROS:
		ventana.fill((0,0,200))
	else:
		ventana.fill((255,0,0))
	
	#DEBUXAR ELEMENTOS:
	
	pygame.draw.rect(ventana, (0,0,0), imag_rect_xogo)
	
	if Cadricula == True:
		for i in range(MARCO, LADO_VENTANA, lado_cadrado):
			pygame.draw.line(ventana, (100,100,100), (MARCO, i), (LADO_VENTANA-MARCO, i))
			pygame.draw.line(ventana, (100,100,100), (i, MARCO), (i, LADO_VENTANA-MARCO))
		
	rect_comida = pygame.Rect(punto_comida.x, punto_comida.y, lado_cadrado, lado_cadrado)
	
	pygame.draw.rect(ventana, (180,180,50), rect_comida)
	
	rect_serpe = pygame.Rect(p_serpe.punto.x, p_serpe.punto.y, lado_cadrado, lado_cadrado)
	pygame.draw.rect(ventana, (0,110,0), rect_serpe)
		
	for i in lista_cola:
		rect_cola = pygame.Rect(i.x, i.y, lado_cadrado, lado_cadrado)
		pygame.draw.rect(ventana, (0,110,0), rect_cola)
	
	#ACCIÓNS SERPE:
	
	if cont_frecuencia == FRECUENCIA and not GAME_OVER:
	
		p_serpe = serpe(p_serpe.punto, proximo_movemento)

		#GAME OVER?
	
		if p_serpe.punto.x < MARCO or p_serpe.punto.x > LADO_VENTANA-(MARCO+lado_cadrado):
			GAME_OVER = True
		if p_serpe.punto.y < MARCO or p_serpe.punto.y > LADO_VENTANA-(MARCO+lado_cadrado):
			GAME_OVER = True
		if (p_serpe.punto.x <= MARCO and p_serpe.mov == "esquerda") or (p_serpe.punto.x >= LADO_VENTANA-(MARCO+lado_cadrado) and p_serpe.mov == "dereita"):
			GAME_OVER = True
		if (p_serpe.punto.y <= MARCO and p_serpe.mov == "arriba") or (p_serpe.punto.y >= LADO_VENTANA-(MARCO+lado_cadrado) and p_serpe.mov == "abaixo"):
			GAME_OVER = True
		if len(lista_cola)+1 == N_CADROS * N_CADROS:
			GAME_OVER = True
		for i in lista_cola:
			if p_serpe.punto.x == i.x and p_serpe.punto.y == i.y:
				GAME_OVER = True
				
		#COME?
		if not GAME_OVER:
			lista_cola.insert(0, p_serpe.punto)
			if not (p_serpe.punto.x == punto_comida.x and p_serpe.punto.y == punto_comida.y):
				del lista_cola[len(lista_cola)-1]
			else:
				COME = True
				punto_comida = crear_punto_comida()
		
		#MOVEMENTO
	
			if not GAME_OVER:
				if p_serpe.mov == "dereita":
					p_serpe = serpe(punto(p_serpe.punto.x+lado_cadrado,p_serpe.punto.y), p_serpe.mov)
				elif p_serpe.mov == "esquerda":
					p_serpe = serpe(punto(p_serpe.punto.x-lado_cadrado,p_serpe.punto.y), p_serpe.mov)
				elif p_serpe.mov == "arriba":
					p_serpe = serpe(punto(p_serpe.punto.x,p_serpe.punto.y-lado_cadrado), p_serpe.mov)
				elif p_serpe.mov == "abaixo":
					p_serpe = serpe(punto(p_serpe.punto.x,p_serpe.punto.y+lado_cadrado), p_serpe.mov)
		
		cont_frecuencia = 0
		
	#UPDATE:
	
	pygame.display.update()
	
	#EVENTOS - KEYDOWN and EXIT:
	
	for eventos in pygame.event.get():
	
		if eventos.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
			
		if eventos.type == pygame.KEYDOWN:
			if eventos.key == K_c: #C -> CADRICULA
				if Cadricula:
					Cadricula = False
				else:
					Cadricula = True
			elif eventos.key == K_SPACE and GAME_OVER:
				GAME_OVER = False
				p_serpe = serpe(punto(MARCO, MARCO), "dereita")
				proximo_movemento = "dereita"
				lista_cola = []
				cont_frecuencia = 0
			elif (eventos.key == K_UP or eventos.key == K_w) and not GAME_OVER and not p_serpe.mov == "abaixo":
				proximo_movemento = "arriba"
			elif (eventos.key == K_DOWN or eventos.key == K_s) and not GAME_OVER and not p_serpe.mov == "arriba":
				proximo_movemento = "abaixo"
			elif (eventos.key == K_RIGHT or eventos.key == K_d) and not GAME_OVER and not p_serpe.mov == "esquerda":
				proximo_movemento = "dereita"
			elif (eventos.key == K_LEFT or eventos.key == K_a) and not GAME_OVER and not p_serpe.mov == "dereita":
				proximo_movemento = "esquerda"
				
	cont_frecuencia += 1
				
	reloj.tick(TICKS_SEGUNDO)