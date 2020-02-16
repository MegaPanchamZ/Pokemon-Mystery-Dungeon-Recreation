import pygame as pg
import sys
import Question_Lib as QL
import ptext as pt
import DamageCalculator as DC
from os import path
from os import listdir
from os import walk
from os.path import isfile, join
from settings import *
from sprites import *
from TileMap import *
from random import choice, randint
from PIL import Image
import time
from pygame.locals import *

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)


class GIFImage(object):

    def __init__(self, filename):
        self.filename = filename
        self.image = Image.open(filename)
        self.frames = []
        self.get_frames()

        self.cur = 0
        self.ptime = time.time()

        self.running = True
        self.breakpoint = len(self.frames) - 1
        self.startpoint = 0
        self.reversed = False

    def get_frames(self):
        image = self.image

        pal = image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i + 3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not image.tile:
                    image.seek(0)
                if image.tile:
                    all_tiles.append(image.tile[0][3][0])
                image.seek(image.tell() + 1)
        except EOFError:
            image.seek(0)

        all_tiles = tuple(set(all_tiles))

        try:
            while 1:
                try:
                    duration = image.info["duration"]
                except:
                    duration = 100

                duration *= .001  # convert to milliseconds!
                cons = False

                x0, y0, x1, y1 = (0, 0) + image.size
                if image.tile:
                    tile = image.tile
                else:
                    image.seek(0)
                    tile = image.tile
                if len(tile) > 0:
                    x0, y0, x1, y1 = tile[0][1]

                if all_tiles:
                    if all_tiles in ((6,), (7,)):
                        cons = True
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i + 3]
                            palette.append(rgb)
                    elif all_tiles in ((7, 8), (8, 7)):
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i + 3]
                            palette.append(rgb)
                    else:
                        palette = base_palette
                else:
                    palette = base_palette

                pi = pg.image.fromstring(image.tobytes(), image.size, image.mode)
                pi.set_palette(palette)
                if "transparency" in image.info:
                    pass
                pi2 = pg.Surface(image.size)
                pi2.blit(pi, (0, 0))

                self.frames.append([pi2, duration])
                image.seek(image.tell() + 1)
        except EOFError:
            pass

    def render(self, screen, pos):
        if self.running:
            if time.time() - self.ptime > self.frames[self.cur][1]:
                if self.reversed:
                    self.cur -= 1
                    if self.cur < self.startpoint:
                        self.cur = self.breakpoint
                else:
                    self.cur += 1
                    if self.cur >= self.breakpoint:
                        self.cur = self.startpoint

                self.ptime = time.time()

        screen.blit(self.frames[self.cur][0], pos)

    def seek(self, num):
        self.cur = num
        if self.cur < 0:
            self.cur = 0
        if self.cur >= len(self.frames):
            self.cur = len(self.frames) - 1

    def set_bounds(self, start, end):
        if start < 0:
            start = 0
        if start >= len(self.frames):
            start = len(self.frames) - 1
        if end < 0:
            end = 0
        if end >= len(self.frames):
            end = len(self.frames) - 1
        if end < start:
            end = start
        self.startpoint = start
        self.breakpoint = end

    def pause(self):
        self.running = False

    def play(self):
        self.running = True

    def rewind(self):
        self.seek(0)

    def fastforward(self):
        self.seek(self.length() - 1)

    def get_height(self):
        return self.image.size[1]

    def get_width(self):
        return self.image.size[0]

    def get_size(self):
        return self.image.size

    def length(self):
        return len(self.frames)

    def reverse(self):
        self.reversed = not self.reversed

    def reset(self):
        self.cur = 0
        self.ptime = time.time()
        self.reversed = False

    def copy(self):
        new = GIFImage(self.filename)
        new.running = self.running
        new.breakpoint = self.breakpoint
        new.startpoint = self.startpoint
        new.cur = self.cur
        new.ptime = self.ptime
        new.reversed = self.reversed
        return new


def Random_Loc(rooms):
    room_choice = choice(rooms)
    x, y = randint(room_choice[0] + 1, room_choice[0] + room_choice[2] - 1), \
           randint(room_choice[1] + 1, room_choice[1] + room_choice[3] - 1)
    return x, y


def quit():
    pg.quit()
    sys.exit()


class Game:
    def __init__(self, dungeon_size, dungeon_floors, PKMN=None):
        # Added pg.FULLSCREEN for fullscreen drawing, upscaled
        self.screen = screen
        self.clock = pg.time.Clock()
        pg.key.set_repeat()
        self.playing = True
        self.dungeon_size = dungeon_size
        self.floor_cap = dungeon_floors
        self.mapname = choice(MAPNAMES)
        self.exit_visible = False
        self.coordsvisited = []
        self.current_room = []
        self.dungeon_elements = []
        self.mini_map_drawn = []
        self.visible_entities = []
        self.player = None
        if PKMN:
            self.spritename = PKMN
        else:
            self.spritename = "000"
        self.player_level = 1
        # Below Statement only for debugging maps
        # self.mapname = "Bottomless Sea" + ".png"

        self.music_path = path.dirname(__file__) + '/Assets/Music/'
        self.current_floor = 0
        self.playerID = CHARACTER
        self.menuflag = False
        self.movemenuflag = False
        self.selected_index = 0
        # Mob related variables
        self.enemy_1ID = '41'

        self.playerhealth = None

        if dungeon_size == 'S':
            self.mobcap = 3
        elif dungeon_size == 'M':
            self.mobcap = 5
        elif dungeon_size == 'L':
            self.mobcap = 10
        elif dungeon_size == 'H':
            self.mobcap = 15

        self.mob_count = 0
        self.mob_container = []

        self.load_data()

        mapVsound = {'Amp Plains.png': '036', 'AppleWoods.png': '029', 'Beach Cave.png': '005',
                     'Blank Desert.png': '040', 'Bottomless Sea.png': '088', 'Brine Cave.png': '056',
                     'Concealed Ruins.png': '092', 'Craggy Coast.png': '030', 'Crystal Cave Lower.png': '043',
                     'Crystal Cave Upper.png': '044', 'Dark Hill Lower.png': '049', 'Dark Hill Upper.png': '049',
                     'Deep Dark Crater.png': '097', 'Deep Dusk Forest Upper.png': '053',
                     'Deep Dusk Forest Lower.png': '053',
                     'Deep Grove.png': '052', 'Deep Sealed Ruin.png': '051', 'Drenched Bluff.png': '012',
                     'Dusk Forest Lower.png': '052', 'Dusk Forest Upper.png': '053', 'Far Amp Plains.png': '037',
                     'Final Maze.png': '101', 'Foggy Forest.png': '033', 'Forest Path.png': '033',
                     'Golden Chamber.png': '111', 'Hidden Highland.png': '059', 'Hidden Land.png': '058',
                     'Ice Aegis Cave.png': '090', 'Lower Brine Cave.png': '057', 'Miracle Sea.png': '089',
                     'Mt Bristle.png': '018', 'Mt Horn.png': '032', 'Mt Travail.png': '093',
                     'Mystery Jungle Lower.png': '120', 'Mystery Jungle Upper.png': '120',
                     'Mystifying Forest.png': '078',
                     'Northern Desert Lower.png': '040', 'Northern Desert Upper.png': '040',
                     'Quicksand Cave.png': '041',
                     'Quicksand Pit.png': '042', 'Rock Aegis Cave.png': '090', 'Rock Path.png': '031',
                     'Shimmer Desert.png': '040', 'Side Path.png': '031', 'Spacial Rift Lower.png': '129',
                     'Spacial Rift Upper.png': '129', 'Steam Cave.png': '034', 'Steel Aegis Cave.png': '090',
                     'Surrounded Sea.png': '088', 'Temporal Spire.png': '065', 'Temporal Tower.png': '064',
                     'The Nightmare.png': '094', 'Tiny Meadow.png': '029', 'Treeshroud Forest Lower.png': '055',
                     'Treeshroud Forest Upper.png': '055', 'Waterfall Cave.png': '024', 'World Abyss.png': '095',
                     'Zero Isle East.png': '131', 'Zero Isle West.png': '131', 'Zero Isle South.png': '131',
                     'Zero Isle North.png': '131'}

        mapname = self.mapname

        onlyfiles = [f for f in listdir(self.music_path) if isfile(join(self.music_path, f))]

        for sound in onlyfiles:
            if sound[:3] == mapVsound[mapname]:
                pg.mixer.music.load(path.dirname(__file__) + '/Assets/Music/' + sound)

        pg.mixer.music.play(-1)

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.title_font = game_folder + '/Assets/Font/PKMN-Mystery-Dungeon.ttf'

        tileset = game_folder + '/Assets/Tiles_Appropriated/ready/' + self.mapname

        Sprite_Folder = game_folder + '/Assets/PKMN_Sprites/'

        self.spritesheet_util = SpriteSheet(game_folder + '/Assets/Tile/Separated_Tiles/' + 'sprites.png',
                                            game_folder + '/Assets/Tile/Separated_Tiles/' + 'sprites.xml')

        self.map = TiledMap(self.dungeon_size, tileset, self)
        self.rooms = self.map.rooms
        self.player_location = Random_Loc(self.rooms)
        self.exit_location = Random_Loc(self.rooms)
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()

        # load in all xml files into MoveData class
        self.movedata = MoveData(game_folder + '/Assets/Base/Dex/move_data/edited')

        # print(self.map_rect)

        onlyfiles = [f for f in listdir(Sprite_Folder)]
        self.spritefiledict = {}

        for sprite in onlyfiles:
            if sprite[:3] != "000" and sprite[:3] != "zdu" and sprite[:3] != "spr":
                self.spritefiledict[sprite[:3]] = sprite

        self.spritesheet_player = SpriteAnim(Sprite_Folder + self.spritefiledict[self.spritename] + "/sheet.png",
                                             Sprite_Folder + self.spritefiledict[self.spritename] + "/animations.xml")

        # random enemy is chosen from the dictionary keys.

        #randomEnemy = choice(list(self.spritefiledict.keys())) <----- Disabled

        self.spritesheet_enemy = SpriteAnim(Sprite_Folder + self.spritefiledict["041"] + "/sheet.png",
                                            Sprite_Folder + self.spritefiledict["041"] + "/animations.xml")

        dataloc = path.dirname(__file__) + '/Assets/Base/Dex/pokemon_data'

        onlyfiles = [f for f in listdir(dataloc)]
        for XMLFile in onlyfiles:
            file = XMLFile[5:-4].upper()
            compare = self.spritefiledict[self.spritename][4:].upper()
            if file == compare:
                self.player_pkmnData = dataloc + "/" + XMLFile

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.exit_visible = False
        self.coordsvisited = []
        self.current_room = []
        self.dungeon_elements = []
        self.mini_map_drawn = []
        # Collating sprites into groups, inheriting from pg.sprite.Group() class
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.exit = pg.sprite.Group()
        self.playersprite = pg.sprite.Group()
        # Init mini map surface
        self.mini_map_surface = pg.Surface((self.map_rect[2], self.map_rect[3]))

        for row, tiles in enumerate(self.map.original_map):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)

        self.stairs = Stairs(self, self.map.exit_location[0], self.map.exit_location[1])

        self.player = Player(self, self.map.player_location[0], self.map.player_location[1], self.player_pkmnData)

        if not self.playerhealth:
            self.playerhealth = self.player.max_health
            self.player.current_health = self.playerhealth
        else:
            self.player.current_health = self.playerhealth

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000

            self.events()

            # Creating Co-ordinates for Simple FOV

            for room in self.rooms:
                # print(room)
                if self.player.y in range(room[1], room[1] + room[3] + 2):
                    if self.player.x in range(room[0], room[0] + room[2] + 2):
                        self.current_room = [room[0], room[1], room[2] + 2, room[3] + 2]
                        break
                else:
                    self.current_room = self.player.x - 1, self.player.y - 1, 3, 3
                # print('not in room')

            for y in range(self.current_room[1], self.current_room[1] + self.current_room[3]):
                for x in range(self.current_room[0], self.current_room[0] + self.current_room[2]):
                    if (x, y) not in self.coordsvisited:
                        self.coordsvisited.append((x, y))
                    if (x, y) == (self.map.exit_location[0], self.map.exit_location[1]):
                        self.exit_visible = True
            if self.mob_count < self.mobcap:
                location = Random_Loc(self.rooms)
                if location != (self.player.x, self.player.y):
                    self.mob_container.append(Enemy(self, location[0], location[1]))
                    self.mob_count += 1


            self.player.current_health = self.playerhealth
            if self.playerhealth <= 0:
                DungeonFailed(self.spritename)

            self.update()
            self.draw()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def calculate_damage(self, moveid,  target, dealer, special=False):

        level = 1
        Power = 0

        if special:
            Atk_user = player_stats['SpAttack']
            Def_target = 0
        else:
            Atk_user = player_stats['Attack']
            Def_target = 0

        movedata = self.movedata.get_movedata(moveid)

        target_type = target.type
        movetype = movedata[1][1]
        usertype = dealer.type

        damage_dealt = DC.Calculate_Damage(level, Power, Atk_user, Def_target, target_type, movetype, usertype)

        return damage_dealt

    def mini_map(self):

        for row, tiles in enumerate(self.map.original_map):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    if (col, row) in self.coordsvisited:
                        if (col, row) not in self.mini_map_drawn:
                            pg.draw.rect(self.mini_map_surface,
                                         WHITE, (col * TILESIZE, row * TILESIZE,
                                                 TILESIZE, TILESIZE))
                            self.mini_map_drawn.append((col, row))

        minimap = self.mini_map_surface
        minimap.set_colorkey(BLACK)
        minimaprect = minimap.get_rect()

        if self.exit_visible:
            pg.draw.rect(minimap, LIGHTBLUE, (int((self.map.exit_location[0] * TILESIZE)),
                                              int((self.map.exit_location[1] * TILESIZE)),
                                              int(TILESIZE),
                                              int(TILESIZE)))
        minimap = pg.transform.scale(minimap, (int(minimaprect[2] / 8), int(minimaprect[3] / 8)))

        return minimap, minimaprect

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def widget(self):
        font = path.dirname(__file__) + '/Assets/Font/PPMD.ttf'
        widget_surf = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        HP_percent = self.player.current_health / self.player.max_health
        bar_col = RED if HP_percent < 0.30 else GREEN
        HP_BarWidth = int(WIDTH * 0.45)
        pg.draw.rect(widget_surf, (210, 180, 140), pg.Rect(WIDTH - HP_BarWidth, 3, HP_BarWidth - 8, 20))
        pg.draw.rect(widget_surf, bar_col, pg.Rect(WIDTH - HP_BarWidth + 3, 6, ((HP_BarWidth - 12) * HP_percent), 16))
        pg.draw.rect(widget_surf, WHITE, pg.Rect(WIDTH - HP_BarWidth, 3, HP_BarWidth - 8, 20), 4)
        Floor_text = draw_text(str(self.current_floor) + "F", self.title_font, 30, WHITE, 10, 3)
        Lvl_Text = draw_text("LVL " + str(self.player.level), self.title_font, 30, WHITE, Floor_text[1][2] + 30, 3)

        bounding = draw_text("HP " + str(self.player.current_health) + " / " + str(self.player.max_health),
                             self.title_font, 30, WHITE, WIDTH - HP_BarWidth, 3)

        HP_Text = draw_text("HP " + str(self.player.current_health) + " / " + str(self.player.max_health),
                            font, 30, WHITE, bounding[1][0] - bounding[1][2] - 10, 3)

        widget_surf.blit(Floor_text[0], Floor_text[1])
        widget_surf.blit(Lvl_Text[0], Lvl_Text[1])
        widget_surf.blit(HP_Text[0], HP_Text[1])
        return widget_surf

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.fov_surface = pg.Surface((self.map_rect[2], self.map_rect[3]))
        self.fov_surface.set_colorkey(BLACK)

        self.screen.blit(self.map_image, self.camera.apply_rect(self.map_rect))

        self.visible_entities = []

        # Rendering Sprites onto screen
        for sprite in self.all_sprites:
            if sprite not in self.mobs:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            if sprite in self.mobs:
                if sprite.y in range(self.current_room[1] - 2, self.current_room[1] + self.current_room[3] + 2):
                    if sprite.x in range(self.current_room[0] - 2, self.current_room[0] + self.current_room[2] + 2):
                        self.screen.blit(sprite.image, self.camera.apply(sprite))
                        self.visible_entities.append(("enemy", sprite.x, sprite.y))

        for row, tiles in enumerate(self.map.original_map):
            for col, tile in enumerate(tiles):
                if col not in range(self.current_room[0], self.current_room[0] + self.current_room[2]):
                    pg.draw.rect(self.fov_surface, DARKGREY, (col * TILESIZE, row * TILESIZE,
                                                              TILESIZE, TILESIZE))
                if row not in range(self.current_room[1], self.current_room[1] + self.current_room[3]):
                    pg.draw.rect(self.fov_surface, DARKGREY, (col * TILESIZE, row * TILESIZE,
                                                              TILESIZE, TILESIZE))

        self.fov_surface.set_alpha(200)
        # Adding Field of View to screen
        self.screen.blit(self.fov_surface, (self.camera.apply_rect(self.map_rect)))
        # Adding Player MipMap location
        pg.draw.circle(self.screen, LIGHTGREY, (int((self.player.x * TILESIZE) / 8),
                                                int((self.player.y * TILESIZE) / 8) + 32), int(TILESIZE / 12))
        if self.visible_entities:
            for entity in self.visible_entities:
                if entity[0] == "enemy":
                    pg.draw.circle(self.screen, RED, (int((entity[1] * TILESIZE) / 8),
                                                      int((entity[2] * TILESIZE) / 8) + 32), int(TILESIZE / 12))

        self.screen.blit(self.mini_map()[0], (0, 32))

        # Preliminary, health bar
        # pg.draw.rect(self.screen, (GREEN), pg.Rect(3, 3, ((WIDTH - 4) * progress), 16))
        # pg.draw.rect(self.screen, (WHITE), pg.Rect(0, 0, WIDTH, 20), 4)
        # Changed to:
        self.screen.blit(self.widget(), (0, 0))

        if self.menuflag:
            self.draw_menu()

        pg.display.flip()

    def draw_menu(self):
        items = ["Moves", "Exit"]
        menu = message_box(50, len(items) * 25)

        self.screen.blit(menu, (10, 30))
        for i in range(len(items)):
            self.selected = self.selected_index % len(items)
            if i == self.selected:
                pt.draw(items[i], (20, (i * 25) + 40), fontname=self.title_font,
                        antialias=False,
                        fontsize=24,
                        color=LIGHTBLUE)

            else:
                pt.draw(items[i], (20, (i * 25) + 40), fontname=self.title_font,
                        antialias=False,
                        fontsize=24,
                        color=WHITE)

        for event in pg.event.get():
                if event.key == pg.K_DOWN:
                    self.selected_index += 1

                if event.key == pg.K_UP:
                    self.selected_index -= 1

                if event.key == pg.K_RETURN:
                    if items[self.selected] == "Exit":
                        self.menuflag = False
                    if items[self.selected] == "Moves":
                        self.movemenuflag = True

    def Mob_ai_on(self):
        # print(self.mobs)
        for mob in self.mob_container:
            mob.walking = True
            mob.AI()

    def Mob_ai_off(self):
        # print(self.mobs)
        for mob in self.mob_container:
            mob.walking = False
            mob.idle = True

    def events(self):
        # catch all events here
        self.state = str('I')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit()

                if not self.menuflag:
                    if event.key == pg.K_LEFT or event.key == ord('a'):
                        self.old_player_coords = self.player.x, self.player.y
                        self.player.move(dx=-1)
                        self.player_coords = self.player.x, self.player.y
                        # print(self.player_coords)
                        self.state = 'L'
                        self.player.walking = True
                        self.player.last_dir = 'L'
                        if self.old_player_coords == (self.player.x, self.player.y):
                            break
                        self.Mob_ai_on()
                    # self.enemy.AI() # legacy
                    # self.moved = True
                    if event.key == pg.K_RIGHT or event.key == ord('d'):
                        self.old_player_coords = self.player.x, self.player.y
                        self.player.move(dx=1)
                        self.player_coords = self.player.x, self.player.y
                        # print(self.player_coords)
                        self.state = 'R'
                        self.player.walking = True
                        self.player.last_dir = 'R'
                        if self.old_player_coords == (self.player.x, self.player.y):
                            break
                        self.Mob_ai_on()

                    # self.enemy.AI() # legacy
                    # self.moved = True
                    if event.key == pg.K_UP or event.key == ord('w'):
                        self.old_player_coords = self.player.x, self.player.y
                        self.player.move(dy=-1)
                        self.player_coords = self.player.x, self.player.y
                        # print(self.player_coords)
                        self.state = 'U'
                        self.player.walking = True
                        self.player.last_dir = 'U'
                        if self.old_player_coords == (self.player.x, self.player.y):
                            break

                        self.Mob_ai_on()
                    # self.enemy.AI() # legacy
                    # self.moved = True
                    if event.key == pg.K_DOWN or event.key == ord('s'):
                        self.old_player_coords = self.player.x, self.player.y
                        self.player.move(dy=1)
                        self.player_coords = self.player.x, self.player.y
                        # print(self.player_coords)
                        self.state = 'D'
                        self.player.walking = True
                        self.player.last_dir = 'D'
                        if self.old_player_coords == (self.player.x, self.player.y):
                            break
                        self.Mob_ai_on()
                    # self.enemy.AI() # legacy
                    # self.moved = True
                    if event.key == pg.K_v:
                        self.menuflag = True

                    if event.key == K_SPACE:
                        self.player.walking = False
                        self.player.idle = False
                        self.player.attacking = True
                        self.player.attack()
                        self.Mob_ai_on()

            if event.type == pg.KEYUP:
                # after 500 milliseconds do:
                self.state = 'I'
                self.player.walking = False
                self.player.idle = True
                self.Mob_ai_off()
            # self.moved = False

    def show_go_screen(self):
        self.current_floor += 1
        # self.screen.blit(self.intro, [0, 0])
        if self.current_floor >= self.floor_cap:
            try:
                DungeonClear()
            except pg.error as message:
                raise SystemExit("End")

        self.screen.fill(BLACK)
        self.draw_text(self.mapname[:-4] + " " + str(self.current_floor) + "F", self.title_font, 60, WHITE,
                       WIDTH / 2, int(HEIGHT * 0.4), align="center")

        self.draw_text("Enjoy the Demo!", self.title_font, 25, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")

        pg.display.flip()
        pg.time.delay(1500)

        self.floor_start()

    def first_floor_screen(self):
        self.current_floor += 1
        self.screen.fill(BLACK)
        self.draw_text(self.mapname[:-4] + " " + str(self.current_floor) + "F", self.title_font, 60, WHITE,
                       WIDTH / 2, int(HEIGHT * 0.4), align="center")

        self.draw_text("Enjoy the Demo!", self.title_font, 25, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")

        pg.display.flip()
        pg.time.delay(1500)

    def floor_start(self):
        self.mob_count = 0
        self.mob_container = []
        self.load_data()
        self.moved = False
        self.new()
        self.run()


def Dungeon_Begin(Size, Floor_Num, PKMN):
    g = Game(Size, Floor_Num, PKMN=PKMN)
    # g.show_start_screen()
    g.first_floor_screen()
    while True:
        g.new()
        g.run()


def draw_text(text, font_name, size, color, x, y, align="topleft"):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    return text_surface, text_rect


def message_box(width, height):
    box_pieces = path.dirname(__file__) + '/Assets/Base/Graphics/UI/parts.png'
    box_sch = path.dirname(__file__) + '/Assets/Base/Graphics/UI/parts.xml'
    box_parts = SpriteSheet(box_pieces, box_sch)
    width = int(width)
    height = int(height)
    board = pg.Surface((width, height))

    for x in range(2, width - 3):
        board.blit(box_parts.get_image_name('Length'), (x, 0))

    for x in range(2, width - 3):
        board.blit(box_parts.get_image_name('Length'), (x, height - 3))

    for y in range(2, height - 3):
        board.blit(box_parts.get_image_name('Height'), (0, y))

    for y in range(2, height - 3):
        board.blit(box_parts.get_image_name('Height'), (width - 3, y))

    board.blit(box_parts.get_image_name("TopLeft"), (0, 0))
    board.blit(box_parts.get_image_name("TopRight"), (width - 3, 0))
    board.blit(box_parts.get_image_name("BottomLeft"), (0, height - 3))
    board.blit(box_parts.get_image_name("BottomRight"), (width - 3, height - 3))

    for y in range(3, height - 3):
        for x in range(3, width - 3):
            board.blit(box_parts.get_image_name("Fill"), (x, y))
    board.set_colorkey(MAGENTA)
    return pg.transform.scale2x(board)


def show_start_screen():
    clock = pg.time.Clock()

    intro = GIFImage(path.dirname(__file__) +
                     '/Assets/Base/Graphics/UI/PMDExplorersofTimeDarknessIntro.gif')
    pg.mixer.music.load(path.dirname(__file__) + '/Assets/Music/PMD_Intro.ogg')

    pg.mixer.music.play(-1)

    UI_font = path.dirname(__file__) + '/Assets/Font/PKMN-Mystery-Dungeon.ttf'

    timer = pg.time.get_ticks()
    text_col = WHITE
    last = True
    l = True
    while l:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                pg.mixer.music.fadeout(500)
                intro.image.close()
                l = False
                # return

        screen.fill((255, 255, 255))
        intro.render(screen, (0, 0))

        if pg.time.get_ticks() - timer > 1000:
            timer = pg.time.get_ticks()
            if last:
                text_col = BLACK
                last = False
            elif not last:
                text_col = WHITE
                last = True

        message = draw_text("Press A Key To Begin", UI_font, 30, text_col,
                            WIDTH / 2, HEIGHT - HEIGHT / 6, align="center")

        screen.blit(message[0], message[1])

        pg.display.flip()


def choose_character():
    bg = GIFImage(path.dirname(__file__) + '/Assets/Base/Graphics/UI/Personality Test Background.gif')

    pg.mixer.music.load(path.dirname(__file__) + '/Assets/Music/003 Welcome To the World of Pokemon!.ogg')

    pg.mixer.music.play(-1)

    UI_font = path.dirname(__file__) + '/Assets/Font/PKMN-Mystery-Dungeon.ttf'

    d = True
    msg = message_box(252, 50)
    questions = QL.getQuestions()
    x = 0
    Nature_attrib = {'Bold': 0, 'Brave': 0, 'Calm': 0,
                     'Docile': 0, 'Hardy': 0, 'Hasty': 0,
                     'Impish': 0, 'Jolly': 0, 'Lonely': 0,
                     'Quiet': 0, 'Quirky': 0, 'Rash': 0,
                     'Relaxed': 0, 'Sassy': 0, 'Timid': 0,
                     'Naive': 0}
    index = 0
    gender = "Male"
    line = 0
    PKMNName = "Default"
    name = ''
    portraitBorder = message_box(26, 26)
    portrait = False
    pic = 0
    leave = False
    while d:
        bg.render(screen, (0, 0))
        screen.blit(msg, (4, HEIGHT - 100 - 3))

        if x >= 9:
            nature = max(Nature_attrib, key=lambda key: Nature_attrib[key])
            PKMN = QL.getPokemon(gender, nature)
            nature_txt = QL.getNatureText(nature)
            print(nature)
            onlyfiles = [f for f in listdir(path.dirname(__file__) + '/Assets/PKMN_Sprites/')]
            for sprite in onlyfiles:
                # print(sprite[:3])
                if PKMN == sprite[:3]:
                    PKMNName = sprite[4:]

            port_dir = [f for f in listdir(path.dirname(__file__) + '/Assets/Portraits')]

            for por in port_dir:
                if PKMNName == por[5:]:
                    pic = pg.image.load(path.dirname(__file__) + '/Assets/Portraits/' + por + "/0002_GRIN.png")

            try:
                pt.draw(nature_txt[line][0], (12, HEIGHT - 88), fontname=UI_font, antialias=False, width=WIDTH - 12,
                        shadow=(1.0, 1.0), scolor="black")
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                            line += 1
            except IndexError:
                pt.draw("Will be a.. " + name, (12, HEIGHT - 88), fontname=UI_font, antialias=False, width=WIDTH - 12,
                        shadow=(1.0, 1.0), scolor="black"
                        )
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        name = PKMNName
                        portrait = True
                    if leave:
                        screen.fill(BLACK)
                        pt.draw("Your Journey Awaits!", (int(WIDTH / 2), int(HEIGHT / 2)), fontname=UI_font,
                                antialias=False,
                                align="center", shadow=(1.0, 1.0), scolor="blue", anchor=(0.5, 0.5), fontsize=50)
                        pg.display.flip()
                        pg.time.delay(3000)
                        return PKMN
                if portrait:
                    screen.blit(portraitBorder, (int(WIDTH / 2) - 26, int(HEIGHT / 2) - 26))
                    screen.blit(pic, (int(WIDTH / 2) - 20, int(HEIGHT / 2) - 20))
                    pg.display.flip()
                    pg.time.delay(2000)
                    leave = True


        else:
            pt.draw(questions[x][0], (12, HEIGHT - 88), fontname=UI_font, antialias=False, width=WIDTH - 12,
                    shadow=(1.0, 1.0), scolor="black")
            box_w, box_h = 150, 15 * (len(questions[x]) - 1)
            ansBox = message_box(box_w, box_h)
            boxlocx, boxlocy = WIDTH - (box_w * 2) - 4, HEIGHT - (box_h * 2) - 102
            screen.blit(ansBox, (boxlocx, boxlocy))

            for i in range(len(questions[x]) - 1):
                i += 1
                if i == index + 1:
                    pt.draw(questions[x][i][0], (boxlocx + 12, boxlocy + 8 + ((i - 1) * 25)), fontname=UI_font,
                            antialias=False,
                            width=WIDTH - (boxlocx + 8),
                            fontsize=25,
                            color=LIGHTBLUE,
                            shadow=(1.0, 1.0), scolor="black")
                else:
                    pt.draw(questions[x][i][0], (boxlocx + 12, boxlocy + 8 + ((i - 1) * 25)), fontname=UI_font,
                            antialias=False,
                            width=WIDTH - (boxlocx + 8),
                            fontsize=25,
                            color=WHITE,
                            shadow=(1.0, 1.0), scolor="black")

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        index -= 1
                        index = index % (len(questions[x]) - 1)
                        # print(index + 1)
                    if event.key == pg.K_DOWN:
                        index += 1
                        index = index % (len(questions[x]) - 1)
                        # print(index + 1)
                    if event.key == pg.K_RETURN:
                        addition = questions[x][index + 1]

                        if x == 8:
                            gender = questions[x][index + 1][0]
                            # print(gender[0])
                        index = 0
                        vals = addition[1:][0]
                        to_add = vals.split("; ")
                        for i in to_add:
                            Nature_attrib[i[:-3]] = Nature_attrib[i[:-3]] + int(i[-1:])

                        # print(max(Nature_attrib, key=lambda key: Nature_attrib[key]))
                        x += 1

        pg.display.flip()


def Menu():
    bg = pg.image.load(path.dirname(__file__) +
                       '/Assets/Base/Graphics/UI/menu_06.png')

    pg.mixer.music.load(path.dirname(__file__) + '/Assets/Music/002 Top Menu Theme.ogg')

    pg.mixer.music.play(-1)

    UI_font = path.dirname(__file__) + '/Assets/Font/PKMN-Mystery-Dungeon.ttf'

    selected = 'start'

    l = True
    while l:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    selected = "start"

                elif event.key == pg.K_DOWN:
                    selected = "quit"

                if event.key == pg.K_RETURN:

                    if selected == "start":
                        l = False
                    if selected == "quit":
                        pg.quit()

            screen.blit(bg, (0, 0))
            if selected == "start":
                text_start = draw_text("Start Demo", UI_font, 30, LIGHTGREY,
                                       WIDTH / 6, HEIGHT / 8, align="center")

            else:
                text_start = draw_text("Start Demo", UI_font, 30, WHITE,
                                       WIDTH / 6, HEIGHT / 8, align="center")

            if selected == "quit":
                text_quit = draw_text("Quit", UI_font, 30, LIGHTGREY,
                                      WIDTH / 6, HEIGHT / 5, align="center")

            else:
                text_quit = draw_text("Quit", UI_font, 30, WHITE,
                                      WIDTH / 6, HEIGHT / 5, align="center")

            box = message_box(80, 60)
            box.set_colorkey(MAGENTA)
            screen.blit(box, (10, 10))
            screen.blit(text_start[0], text_start[1])
            screen.blit(text_quit[0], text_quit[1])

            pg.display.flip()


def DungeonClear():
    pg.mixer.init()

    pg.mixer.music.load(path.dirname(__file__) + '/Assets/Music/013 Job Clear!.ogg')

    pg.mixer.music.play(-1)

    UI_font = path.dirname(__file__) + '/Assets/Font/PKMN-Mystery-Dungeon.ttf'
    h = True
    while h:
        screen.fill(BLACK)
        pt.draw("Congratulations of Clearing the Dungeon.\n Thankyou For playing the demo!",
                (int(WIDTH / 2), int(HEIGHT / 2)), fontname=UI_font,
                antialias=False,
                align="center", shadow=(1.0, 1.0), scolor="blue", anchor=(0.5, 0.5), fontsize=40
                )

        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                pg.mixer_music.fadeout(1000)
                pg.time.delay(2500)
                h = False


def DungeonFailed(pokemon):
    pg.mixer.init()

    pg.mixer.music.load(path.dirname(__file__) + '/Assets/Music/017 Oh No!.ogg')

    pg.mixer.music.play(-1)

    UI_font = path.dirname(__file__) + '/Assets/Font/PKMN-Mystery-Dungeon.ttf'
    h = True
    while h:
        screen.fill(BLACK)
        pt.draw("You Died!\n press 'R' to restart \n press 'Q' to quit",
                (int(WIDTH / 2), int(HEIGHT / 2)), fontname=UI_font,
                antialias=False,
                align="center", shadow=(1.0, 1.0), scolor="blue", anchor=(0.5, 0.5), fontsize=40
                )

        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.mixer_music.fadeout(1000)
                    pg.time.delay(500)
                    h = False
                    pg.quit()
                if event.key == pg.K_r:
                    StartGame(newstart=pokemon)





def Base(PKMN):
    # TODO Implement a home base.
    # FIXME Currently Generates Dungeon Automatically
    # TODO Create select box for dungeons?
    try:
        Dungeon_Begin("S", 5, PKMN)
    except pg.error as message:
        DungeonClear()
        pass


def StartGame(newstart = None):
    if not newstart:
        show_start_screen()
        try:
            Menu()
        except pg.error as message:
            raise SystemExit("Game Exit!")
        poke = choose_character()
        Base(poke)
    if newstart:
        Base(newstart)


StartGame()
