from pygame import *
from random import randint      

init()

#Varibles de manejo global
large = 800  
height = 600
fps =  20
speed_music = -1
clock = time.Clock()
window = display.set_mode((large,height))
display.set_caption('Shooter Game')

BkG = transform.scale(image.load('galaxy.jpg'),(large,height))

#Musica del entorno de juego
#mixer.music.load('fire.ogg')
#mixer.music.play(speed_music)
#Mensajes que apareceran en el juego
font.init()
main_Font = font.SysFont('Comic Sans',20)
font_final = font.SysFont('Comic Sans', 20)

font_winner = main_Font.render("¡GANASTE!",True,(0,255,0))
font_loser = font_final.render("¡PERDISTE!",True,(255,0,0))
# clase padre para otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # llamamos al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)

        # cada objeto debe almacenar una propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # cada objeto debe almacenar la propiedad rect en la cual está inscrito
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método que dibuja al personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    #metodo para el  movimiento del jugador
    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    #Objeto para colisionar
    def isCollision(self,object):
        return self.rect.colliderect(object.rect)

    

#listas globales
gunss = []
enemigos = []

#Metodo para determinar el disparo de los objetos
#Clase disparos
class Guns(GameSprite):
    def moveshoot(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            if self in gunss:
                gunss.remove(self)

    

class Player(GameSprite):
    
    #Calcular el moviento del cohete
    def move_rocket(self):
        
        touch = key.get_pressed()
        if (touch[K_a] or touch[K_LEFT] and self.rect.x > 0):
            self.rect.x -= self.speed
        elif (touch[K_d] or touch[K_RIGHT] and self.rect.x < large - self.rect.width):
            self.rect.x += self.speed

    #Metodo shoot
    def shoot(self):
        keys= key.get_pressed()
        if keys[K_SPACE]:
            Gun = Guns("bullet.png",self.rect.x + 20, self.rect.y - 50,60,60,5)
            gunss.append(Gun)
            mixer.music.load("fire.ogg")
            mixer.music.play()
        


class Enemy(GameSprite):
    #Metodo para que los enemigos se caigan de manera aleatoria
    def fall_enemy(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.x = randint(0,large-100)
            self.rect.y = 0
            global falls
            falls += 1

def setText(text,size,font="Comic Sans",coords=(0,0),color=(255,255,255)):
    font_text = font.SysFont(font,size)
    rend = font_text.render(text,"",color)
    window.blit(rend,coords)

#Objetos enemigos
Enemy1 = Enemy('ufo.png',200,-50,50,50,4)
Enemy2 = Enemy('ufo.png',400,-250,50,50,3)
Enemy3 = Enemy('ufo.png',600,-100,50,50,5)
enemigos = [Enemy1, Enemy2, Enemy3]
# clase del jugador principal
# clase del enemigo

Player1 = Player('rocket.png',350,480,100,100,6)


#Var del juego
falls = 0
points = 0
max_falls = 5
max_points = 10

on = True
finish = False
while on:

    for e in event.get():
        if e.type == QUIT:
            on = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                Player1.shoot()  
    #manejo del teclado, disparar enter_space 
    #Actualizacion de ciclo 
    if not finish:          
        window.blit(BkG,(0,0))
        Player1.move_rocket()
        Player1.shoot()
        
        #Iterar sobre copia
        for gu in gunss[:]:
            gu.moveshoot()
        
        for enemy in enemigos:
            enemy.fall_enemy()
        
        #Comprobación de collions

        for gu in gunss[:]:
            for enemy in enemigos[:]:
                if gu.isCollision(enemy):
                    if gu in gunss:
                        gunss.remove(gu)
                    if enemy in enemigos:
                        enemigos.remove(enemy)
                        points += 1
                        #Aparecer de nuevo 
                        new_enemy = Enemy('ufo.png', randint(0, large - 100), randint(-200,-50), 100,100, randint(3,6))
                        enemigos.append(new_enemy)
    
    Player1.reset() 
    #Dibujar en pantalla
    for enemy in enemigos:
        enemy.reset ()
    for gu in gunss[:]:
        gu.reset()
        
    #Mostrar Points y lives
    score = font_final.render(f"Puntos: {points}",True,(0,255,0))
    falls_text = font_final.render(f"Fallos: {falls}/{max_falls}",True,(0,255,0))
    window.blit(score,(20,20))
    window.blit(falls_text,(20,40))
    
    #Comprobar puntuacion
    if points >= max_points:
        finish = True
        window.blit(font_winner,(large//2 - 100,height // 2 - 50))
    
    #Comprobar derrota
    for enemy in enemigos:
        if Player1.isCollision(enemy) or falls >= max_falls:
            finish = True
            window.blit(font_loser,(large//2 - 100, height // 2 - 50))

    display.update()
    clock.tick(fps) 


#como hacer que no se agregue una bala despues de otra
#Niveles, recompesas, cambiar estilo, reiniciar el juego, que se portable para cualquier tipo de tamanio
#Crear una mini app movil del juego
#Con presentacion y fin
#usar mas funciones
#Mejorarlo porque esta muy generico
#Pensar más ideas 
#Cambiar las img que estan en el juego
#Crear mis propias librerias