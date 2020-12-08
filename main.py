import pygame 
from pygame import mixer
from pygame import font
import glob, os 
from mutagen.mp3 import MP3
from tkinter import Tk
from tkinter.filedialog import askdirectory # для открытия файла

pygame.init()
font.init()
mixer.init()

clock = pygame.time.Clock()
FPS = 30
sc = ''
scW = 400
scH = 400
def updateDisplay(i): # обновление дисплея
    global sc
    sc = pygame.display.set_mode((scW + i, scH)) 

updateDisplay(0)

pygame.display.set_caption('Плейер')
pygame.display.set_icon(pygame.image.load("play.png"))

loadsImage = [
                pygame.image.load('left.png'), pygame.image.load('play.png'), 
                pygame.image.load('pause.png'), pygame.image.load('right.png'), ]

papka = pygame.image.load('papka.png')
musiclist = pygame.image.load('music.png')

leftList = pygame.image.load('leftList.png')
rightList = pygame.image.load('rightList.png')

name = []
def newPapka():
    global name, player
    Tk().withdraw()    
    direct = askdirectory() # директория выбранной папки
    name = []
    if direct:
        os.chdir(direct)
        for file in glob.glob("*.mp3"): # поиск файлов с расширением 'mp3'
            name.append(file)

# создание и вывод текста
class Text():
    def __init__(self, font, text, x, y, center):
        self.font = font
        self.text = text
        self.x = x
        self.y = y
        self.center = center
        self.init()

    def init(self):
        f1 = font.Font(None, self.font)
        text = f1.render(self.text, True, (0, 0, 0))
        if self.center:   
            text_rect = text.get_rect(center=(self.x, self.y))
            sc.blit(text, text_rect )
        else:
            sc.blit(text, (self.x, self.y))



listMysical = False # лист с музыкой False - закрыть True - открыть
lists = 1 # номер листа
maxMusic = 20 # максимальное количисво аудио на листе

def listMysic():
    for i in range(len(name)):
        if i < maxMusic and lists >= 1 and len(name) > (i + ((lists * 20) - 20) + 1):
            Text(20, name[i + ((lists * 20) - 20) + 1].split('.')[0], 420,  (i*2) * 10, False) # вывод названий в лист
        else:
            break        

def leftRighList(options):
    global lists
    if options == 'left': # листание списка с музыков в лево
        if lists == 1:
            lists = (len(name) // 20) + 1
        else:
            lists-=1
    elif options == 'right': # листание списка с музыков в право
        if lists == (len(name) // 20) + 1:
            lists = 1
        else:
            lists+=1



songLength = 0

player = False # проигрывания музыки
i = 0
def playMusik(): 
    global player, songLength, circleX

    if not player and len(name) != 0:
        mixer.music.load(name[i])  # загруска аудио
        songLength = MP3(name[i]).info.length # длинна музыки
        mixer.music.play() # запуск музыки
        player = True
        circleX = 50

    

def leftRigh(option):
    global i, player
    if option == 'left': # перелистывает предыдущую музыку
        if i == 0:
            i = len(name) - 1
        else:
            i-=1
    elif option == 'right': # перелистывает следущую музыку 
        if i == len(name) - 1:
            i = 0
        else:
            i+=1
    player = False
    
    playMusik()
        

def pauseMusik():
    global player
    mixer.music.pause() # пауза
    player = False


# выводит название, автора и длинну музыки 
def generText():
    if len(name) != 0:
        Text(30, name[i].split(' - ')[-1].split('.')[0], 400/2, 220, True)
        Text(20, name[i].split(' - ')[0], 400/2, 250, True)
        Text(18, str(round(songLength / 60, 1)), 350, 285, False )    
    else:
        Text(30, 'Папка не выбрана!', 400/2, 250, True)

BarX = 50 # 
BarY = 290 # расположение прогресс бара
BarW = 300 # длинна прогресс бара
circleX = 50

x = 100 #
y = 300 # координаты изабражений
w = 48  
h = 48
a = 0


def renderBlock():
    global x, y, a, circleX
    for i in loadsImage:
        sc.blit(i, (x, y)) # отрисовка кнопок контроля музыки
        x += 50
    x = 100
    pygame.draw.rect(sc, (0,0,0), (75, 20, 250, 250), 3) 
    pygame.draw.rect(sc, (0,0,0), (0, 0, 400, 400), 3)

    pygame.draw.line(sc, (0,0,0), [BarX, BarY], [BarX + BarW, BarY], 2) # прогресс бар

    sc.blit(papka, (350, 10)) # отрисовка кнопоки выбора папки
    sc.blit(musiclist, (10, 10)) # отрисовка кнопоки открывание листа 

    if player:
        a += 1
        if a == FPS: 
            circleX += BarW / songLength # движение прогресс бара
            a = 0

    pygame.draw.circle(sc, (0,0,0), (circleX, BarY+1), 5) 



while True:
    STOPPED_PLAYING = pygame.USEREVENT + 1 
    pygame.mixer.music.set_endevent(STOPPED_PLAYING)

    # [exit() for i in pygame.event.get()  if i.type == pygame.QUIT]
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        elif e.type == pygame.MOUSEBUTTONDOWN: # событие кнопки мыши
            if e.button == 1:
                _x, _y = e.pos # Координаты мыши
                # проверка на нажатие кнопок
                if (_x >= x and _x <= x + w) and (_y >= y and _y <= y + h):
                    leftRigh('left') 
                elif (_x >= x+50 and _x <= x+50 + w) and (_y >= y and _y <= y + h):
                    playMusik()
                elif (_x >= x+100 and _x <= x+100 + w) and (_y >= y and _y <= y + h):
                    pauseMusik()
                elif (_x >= x+150 and _x <= x+150 + w) and (_y >= y and _y <= y + h):
                    leftRigh('right')
                elif (_x >= 350 and _x <= 350 + 32) and (_y >= 10 and _y <= 10 + 32):
                    newPapka()
                elif (_x >= 10 and _x <= 10 + 32) and (_y >= 10 and _y <= 10 + 32):
                    listMysical = not listMysical
                elif (_x >= 700 and _x <= 700 + 32) and (_y >= 360 and _y <= 360 + 32): 
                    leftRighList('left')
                elif (_x >= 740 and _x <= 740 + 32) and (_y >= 360 and _y <= 360 + 32): 
                    leftRighList('right')
                for k in range(20):
                    if (_x >= 420 and _x <= 420 + 290) and (_y >= ((k*2) * 10) and _y <= ((k*2) * 10) + 15):
                        i = k + ((lists * 20) - 20) + 1
                        if i > len(name):
                            i = len(name)-1
                        player = False
                        playMusik()
                    
        elif e.type == STOPPED_PLAYING: # событие для проигрывание следущей музыки
            i+=1
            player = False
            playMusik()
            circleX = 50 


    if listMysical:
        updateDisplay(370)
        sc.fill('white')

        # кнопки для перелистывания листа
        sc.blit(leftList, (700, 360)) 
        sc.blit(rightList, (740, 360))

 
        listMysic()
    else:
        updateDisplay(0)
        sc.fill('white')

    
    generText()
    renderBlock()


    clock.tick(FPS)
    pygame.display.update()