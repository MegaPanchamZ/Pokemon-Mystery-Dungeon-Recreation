import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from TileMap import *
from random import choice
from pygame.locals import *


class Town:
    def __init__(self):
        pg.init()
        # Added pg.FULLSCREEN for fullscreen drawing, upscaled
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat()
        #self.mapname =
        self.playerID = CHARACTER
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def load_data(self, map_name):
        game_folder = path.dirname(__file__)

        self.title_font = game_folder + '/Assets/Font/PKMN-Mystery-Dungeon.ttf'

        Sprite_Folder = game_folder + '/Assets/Sprite/'

        self.base_map = open(map_name, 'r')

        self.spritesheet_player = SpriteSheet(Sprite_Folder + 'Sprite' +
                                              self.playerID + '/' + 'sprites.png', Sprite_Folder + 'Sprite' +
                                              self.playerID + '/' + 'sprites.xml')


    def new(self):
        # initialize all variables and do all the setup for a map
        self.all_sprites = pg.sprite.Group()

        # for row, tiles in enumerate(self.base_map):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)

        self.player = Player(self, 5, 5)

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:

            self.dt = self.clock.tick(FPS) / 1000

            self.events()

            self.update()

            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)

        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        pg.display.flip()


    def events(self):
        # catch all events here
        self.state = str('I')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT or event.key == ord('a'):
                    self.player.move(dx=-1)
                    self.state = 'L'
                    self.player.walking = True
                    self.player.last_dir = 'L'
                if event.key == pg.K_RIGHT or event.key == ord('d'):
                    self.player.move(dx=1)
                    self.state = 'R'
                    self.player.walking = True
                    self.player.last_dir = 'R'
                if event.key == pg.K_UP or event.key == ord('w'):
                    self.player.move(dy=-1)
                    self.state = 'U'
                    self.player.walking = True
                    self.player.last_dir = 'U'
                if event.key == pg.K_DOWN or event.key == ord('s'):
                    self.player.move(dy=1)
                    self.state = 'D'
                    self.player.walking = True
                    self.player.last_dir = 'D'
            if event.type == pg.KEYUP:
                # after 500 milliseconds do:
                self.state = 'I'
                self.player.walking = False
                self.idle = True


    def time_wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    waiting = False  # create the game object
                    self.quit()

    def world_map_start(self):
        self.load_data()
        self.new()
        self.run()

t = Town()

# t.world_map_start()

