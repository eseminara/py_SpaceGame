import pygame
import random
import math
from pygame import mixer


#INICIAR JUEGO
pygame.init()


# CREAR PANTALLA
pantalla = pygame.display.set_mode((800,600))


# TITULO E ICONO PRINCIPAL

pygame.display.set_caption('Spaceship Wars')

icono = pygame.image.load("Game\spaceship.png")

# PANTALLA FONDO
fondo = pygame.image.load("Game\spaceback.png")

# AGREGAR MUSICA
mixer.music.load("Game\MusicaFondo.mp3")
mixer.music.set_volume(0.1)
mixer.music.play(-1)

########SCORE##########

    #SCORE - VARIABLES

score = 0

fuente = pygame.font.Font("Game\8bitfont.ttf",25)
texto_y = 10
texto_x = 10

    #SCORE - FUNCION
def mostrar_puntaje(x,y):
    texto = fuente.render(f'SCORE: {score}', True,(255,255,255))
    pantalla.blit(texto, (x,y))    

########GAME OVER SCREEN#########

fuente_final = pygame.font.Font("Game\8bitfont.ttf", 100)

    #GAME OVER - FUNCION
    
def texto_final():
    mi_fuente_final = fuente.render(f'- = G A M E  O V E R = -', True,(255,255,255))
    pantalla.blit(mi_fuente_final, (250,250))


#########JUGADOR###########

    #JUGADOR - VARIABLES

jugador_x = 368
jugador_y = 500
jugador_imagen = pygame.image.load("Game\player.png")
jugador_x_cambio = 0

    #JUGADOR - FUNCION

def jugador (x,y):
    pantalla.blit(jugador_imagen,(x,y))
    
    
#########ENEMY#########

    #ENEMY - VARIABLES
enemigo_x = []
enemigo_y = []
enemigo_imagen = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 6

for e in range(cantidad_enemigos):
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,300))
    enemigo_imagen.append(pygame.image.load("Game\enemy.png"))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)

    #ENEMY - FUNCION
def enemigo (x,y,ene):
    pantalla.blit(enemigo_imagen[ene],(x,y))
    
    
##########BULLET#########

    #BULLET - VARIABLES

bala_x = 0
bala_y = 500
bala_imagen = pygame.image.load("Game\\bullet_2.png")
bala_x_cambio = 0
bala_y_cambio = 1
bala_visible = False

    #BULLET - FUNCION

def disparar_bala (x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(bala_imagen,(x + 16, y + 10))



###### COLISIONES ######

    #DETECTAR COLISIONES - FUNCION

def detectar_colision (x_1,x_2,y_1,y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 25:
        return True
    else:
        return False




###### LOOP GAME ######

se_ejecuta = True

while se_ejecuta:
    
    #RGB
    pantalla.blit(fondo, (0,0))
    
    #IN GAME - EVENT INTERATION
    for evento in pygame.event.get():
    
    #QUIT GAME - EVENT
    
        if evento.type == pygame.QUIT:
            se_ejecuta = False 


    #MOVIMIENTO - EVENT
        
        #PUSH KEYS
            
        if evento.type == pygame.KEYDOWN:
            
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.3
                
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.3
                
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("Game\disparo.mp3")
                sonido_bala.set_volume(0.1)
                sonido_bala.play()
                
                if bala_visible == False:
                    bala_x = jugador_x
                    disparar_bala(bala_x,bala_y)
                
                
        #PULL KEYS  
             
        if evento.type == pygame.KEYUP:
            jugador_x_cambio = 0
    
    
        # MODIFICAR UBICACION JUGADOR
    
    jugador_x += jugador_x_cambio
    
        # DISPLAY LIMITS JUGADOR
    
    if jugador_x <= 0:
        jugador_x = 0
    if jugador_x >= 736: 
        jugador_x = 736
        
    
        # MODIFICAR UBICACION ENEMIGO
    for e in range (cantidad_enemigos):
        
        # FIN DEL JUEGO 
        if enemigo_y[e] >= 470:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        
        enemigo_x[e] += enemigo_x_cambio[e]
    
        # DISPLAY LIMITS ENEMIGO -X-
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e]+= enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736: 
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e]+= enemigo_y_cambio[e]
            
        #COLISION
        
        colision = detectar_colision(enemigo_x[e],bala_x,enemigo_y[e],bala_y)
        if colision == True:
            sonido_colision = mixer.Sound('Game\golpe.mp3')
            sonido_colision.set_volume(0.1)
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            score+= 1
            enemigo_x[e] = random.randint(0,736)
            enemigo_y[e] = random.randint(50,300)
        
        enemigo(enemigo_x[e],enemigo_y[e],e)
        
        #MODIFICAR UBICACION BALA
    
    if bala_y == -16:
        bala_y = 500
        bala_visible = False

    if bala_visible == True:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio
    
 
    
    mostrar_puntaje(texto_x,texto_y)
    jugador(jugador_x,jugador_y)
    
    
    # UPDATE
    
    pygame.display.update()