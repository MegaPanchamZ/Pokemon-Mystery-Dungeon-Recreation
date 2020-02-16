import pygame as pg
from settings import *
from random import choice
from os import listdir
import pathfinder as pf
import numpy as np
import xml.etree.ElementTree as ET


class SpriteSheet:
    # load an atlas image
    def __init__(self, img_file, data_file=None):
        self.spritesheet = pg.image.load(img_file).convert()
        self.map = {}
        if data_file:
            tree = ET.parse(data_file)
            for node in tree.iter():
                if node.attrib.get('name'):
                    name = node.attrib.get('name')
                    self.map[name] = {}
                    self.map[name]['x'] = int(node.attrib.get('x'))
                    self.map[name]['y'] = int(node.attrib.get('y'))
                    self.map[name]['width'] = int(node.attrib.get('width'))
                    self.map[name]['height'] = int(node.attrib.get('height'))

    def get_image_rect(self, x, y, w, h):
        return self.spritesheet.subsurface(pg.Rect(x, y, w, h))

    def get_image_name(self, name):
        rect = pg.Rect(self.map[name]['x'], self.map[name]['y'],
                       self.map[name]['width'], self.map[name]['height'])
        return self.spritesheet.subsurface(rect)


class SpriteAnim:
    # Standard __init__ function, declares variables
    def __init__(self, Sheet, DataFile):
        self.Sheet = pg.image.load(Sheet).convert_alpha()
        self.XML = DataFile
        self.tree = ET.parse(self.XML)
        self.root = self.tree.getroot()
        for item in self.root:
            if item.tag == "FrameWidth":
                self.framewidth = int(item.text)
            if item.tag == "FrameHeight":
                self.frameheight = int(item.text)
        # print(self.framewidth, self.frameheight)
        self.width = int(self.Sheet.get_rect().size[0] / self.framewidth)
        # print(self.width)

        # This function Parses the Unreadable XML
        # def ParseXml(self):

        tree = self.tree
        root = self.root

        for item in root:
            if item.tag == "AnimGroupTable":
                AnimGroupTable = []
                for group in item:
                    AnimGroup = []
                    for seq_index in group:
                        AnimGroup.append(seq_index.text)
                    AnimGroupTable.append(AnimGroup)

            if item.tag == "AnimSequenceTable":
                AnimSequenceTable = []
                for Sequence in item:
                    AnimSequence = []
                    for Frame in Sequence:
                        AnimFrame = []
                        if Frame.tag == "AnimFrame":
                            FrameData = []
                            DurationData = []
                            FrameIndex = []
                            HFlipStatus = []
                            for Data in Frame:
                                if Data.tag == "Duration":
                                    DurationData.append(Data.text)
                                elif Data.tag == "MetaFrameGroupIndex":
                                    FrameIndex.append(Data.text)
                                elif Data.tag == "HFlip":
                                    HFlipStatus.append(Data.text)
                            FrameData = (FrameIndex, DurationData, HFlipStatus)
                            AnimFrame.append(FrameData)
                            # print("Frame Data")
                            # print(AnimFrame)
                        if AnimFrame:
                            AnimSequence.append(AnimFrame)
                        # print("Sequence")
                        # print(AnimSequence)
                    AnimSequenceTable.append(AnimSequence)

        self.AnimGroupTable, self.AnimSequenceTable = list(enumerate(AnimGroupTable)) \
            , list(enumerate(AnimSequenceTable))

        # print(self.AnimGroupTable)
        # print(self.AnimSequenceTable)

    def cropbox(self, Surface):

        image_data = pg.surfarray.array3d(Surface)
        image_data_bw = image_data.max(axis=2)
        non_empty_columns = np.where(image_data_bw.max(axis=0) > 0)[0]
        non_empty_rows = np.where(image_data_bw.max(axis=1) > 0)[0]
        cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
        # print(cropBox)
        x, y = cropBox[0] - 1, cropBox[2] - 1
        w, h = cropBox[1] - x + 2, cropBox[3] - y + 2
        # print(x, y, w, h)
        return (x, y, w, h)

    def get_image_rect(self, x, y, w, h):
        # print(x,y,w,h)
        return self.Sheet.subsurface(pg.Rect(x, y, w, h))

    def get_image_list(self, state):
        anim_index = {'None': 0, 'Idle': 1, 'Walk': 2, 'Sleep': 3,
                      'Hurt': 4, 'Attack': 5, 'Charge': 6, 'Shoot': 7,
                      'Strike': 8, 'Chop': 9, 'Scratch': 10, 'Punch': 11,
                      'Slap': 12, 'Slice': 13, 'MultiScratch': 14, 'MultiStrike': 15,
                      'Uppercut': 16, 'Ricochet': 17, 'Bite': 18,
                      'Shake': 19, 'Jab': 20, 'Kick': 21, 'Lick': 22,
                      'Slam': 23, 'Stomp': 24, 'Appeal': 25, 'Dance': 26,
                      'Twirl': 27, 'TailWhip': 28, 'Sing': 29, 'Sound': 30,
                      'Rumble': 31, 'FlapAround': 32, 'Gas': 33, 'Shock': 34,
                      'Emit': 35, 'Special': 36, 'Withdraw': 37, 'RearUp': 38,
                      'Swell': 39, 'Swing': 40, 'Double': 41, 'Rotate': 42,
                      'Spin': 43, 'Jump': 44, 'HighJump': 45}

        anim_to_grab = anim_index[state]

        list_anims = []

        for item in self.AnimGroupTable:
            if anim_to_grab == item[0]:
                for i in list(enumerate(item[1])):
                    for ele in self.AnimSequenceTable:

                        # print(ele)
                        if i[1] == str(ele[0]):
                            for pack in ele[1]:
                                imgindex = int(pack[0][0][0])
                                row = int(imgindex / self.width)
                                col = imgindex % self.width
                                y, x = row * self.frameheight, col * self.framewidth
                                # print((x,y) ,pack)
                                # print((x,col), (y,row), self.framewidth, self.frameheight)
                                flip = int(pack[0][2][0])
                                if flip:
                                    bounds = self.cropbox(self.get_image_rect(x, y, self.framewidth, self.frameheight))
                                    list_anims.append(pg.transform.flip(
                                        self.get_image_rect(x + bounds[0], y + bounds[1], bounds[2], bounds[3]),
                                        True, False)
                                    )
                                if not flip:
                                    bounds = self.cropbox(self.get_image_rect(x, y, self.framewidth, self.frameheight))
                                    list_anims.append(
                                        self.get_image_rect(x + bounds[0], y + bounds[1], bounds[2], bounds[3]))

        return list_anims


class PKN_DEX_Load:
    def __init__(self, DataFile):
        self.XML = DataFile
        self.tree = ET.parse(self.XML)
        self.root = self.tree.getroot()

        self.base_info = []
        self.move_info = []
        self.stat_info = []

        tree = self.tree
        root = self.root
        for i in root:
            if i.tag == "GenderedEntity":
                for e in i:
                    if e.tag == "BaseStats":
                        for s in e:
                            if (s.tag, int(s.text)) not in self.base_info:
                                self.base_info.append((s.tag, int(s.text)))

            if i.tag == "Moveset":
                for e in i:
                    if e.tag == "LevelUpMoves":
                        for s in e:
                            if s.tag == "Learn":
                                gloss = []
                                for v in s:
                                    gloss.append((v.tag, v.text))
                                if gloss not in self.move_info:
                                    self.move_info.append(gloss)

            if i.tag == "StatsGrowth":
                for e in i:
                    if e.tag == "Level":
                        additions = []
                        for s in e:
                            additions.append((s.tag, int(s.text)))
                        self.stat_info.append(additions)

    def get_base_data(self, level):
        if level == 1:
            return self.base_info

    def get_check_new(self, level):

        return


class MoveData:
    def __init__(self, datafolder):
        move_data = [f for f in listdir(datafolder)]
        xml = []
        self.movedict = {}
        movetypedict = {'Normal': '1', 'Fight': '7', 'Flying': '10', 'Poison': '8', 'Ground': '9',
                        'Rock': '13', 'Bug': '12', 'Ghost': '14', 'Steel': '17', 'Fire': '2',
                        'Water': '3', 'Grass': '4', 'Electric': '5', 'Psychic': '11',
                        'Ice': '6', 'Dragon': '15', 'Dark': '16'}
        for i in move_data:
            self.XML = datafolder + "/" + i
            self.tree = ET.parse(self.XML)
            self.root = self.tree.getroot()
            move = []
            moveid = ''
            for line in self.root:
                if line.tag == "Strings":
                    # print(line[0][0].text)
                    move.append(line[0][0].text)
                if line.tag == "Data":

                    lmovetype = line[1].text
                    for name, val in movetypedict.items():
                        if val == lmovetype:
                            movetype = name

                    if [line[0].text, movetype, line[2].text, line[5].text, line[8].text] not in move:
                        move.append([line[0].text, movetype, line[2].text, line[5].text, line[8].text])

                    moveid = line[19].text

            self.movedict[moveid] = move

    def get_movedata(self, moveid):
        return self.movedict[moveid]


# print(MoveData('Assets/Base/Dex/move_data/edited').get_movedata("129"))

player_level = 5
player_stats = {}
player_moves = {}
updated_to_level = 1


def status_update(datum):
    global updated_to_level
    if not player_stats:
        for i in datum.base_info:
            player_stats[i[0]] = i[1]

    for lvl in range(updated_to_level - 1, player_level):
        for stat in datum.stat_info[lvl]:
            if stat[0] != 'RequiredExp':
                player_stats[stat[0]] = player_stats[stat[0]] + stat[1]

        for movedata in datum.move_info:
            if movedata[0][1] == str(updated_to_level):
                if len(player_moves) <= 3:
                    if len(player_moves) == 0:
                        player_moves["1"] = movedata[1][1]
                        continue
                    if len(player_moves) == 1:
                        player_moves["2"] = movedata[1][1]
                        continue
                    if len(player_moves) == 2:
                        player_moves["3"] = movedata[1][1]
                        continue
                    if len(player_moves) == 3:
                        player_moves["4"] = movedata[1][1]
                        continue

        print(player_moves)
        updated_to_level += 1


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, data):
        self.groups = game.all_sprites, game.playersprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames_d[0]
        self.rect = pg.Rect(0, 0, 24, 24)
        self.walking = True
        self.idle = True
        self.level = player_level
        self.player_growthData = PKN_DEX_Load(data)
        status_update(self.player_growthData)
        self.max_health = player_stats["HP"]
        self.current_health = 0
        self.last_dir = 'D'
        self.x = x
        self.y = y
        self.idle = True
        self.attacking = False

    def load_images(self):
        walk_frames = self.game.spritesheet_player.get_image_list("Walk")
        idle_frames = self.game.spritesheet_player.get_image_list("Idle")
        attack_frames = self.game.spritesheet_player.get_image_list('Scratch')
        attack_per = int(len(attack_frames) / 8)
        idle_per = int(len(idle_frames) / 8)
        walk_per = int(len(walk_frames) / 8)
        self.dim = int(idle_frames[0].get_rect()[2] * 0.5), int(idle_frames[0].get_rect()[3] * 5)
        # print(self.dim)

        self.idle_frames_d = idle_frames[:idle_per * 1]

        self.idle_frames_dl = idle_frames[idle_per * 1:idle_per * 2]

        self.idle_frames_l = idle_frames[idle_per * 2:idle_per * 3]

        self.idle_frames_ul = idle_frames[idle_per * 3:idle_per * 4]

        self.idle_frames_u = idle_frames[idle_per * 4:idle_per * 5]

        self.idle_frames_ur = idle_frames[idle_per * 5:idle_per * 6]

        self.idle_frames_r = idle_frames[idle_per * 6:idle_per * 7]

        self.idle_frames_dr = idle_frames[idle_per * 7:idle_per * 8]

        self.walk_frames_d = walk_frames[:walk_per * 1]

        self.walk_frames_dl = walk_frames[walk_per * 1:walk_per * 2]

        self.walk_frames_l = walk_frames[walk_per * 2:walk_per * 3]

        self.walk_frames_ul = walk_frames[walk_per * 3:walk_per * 4]

        self.walk_frames_u = walk_frames[walk_per * 4:walk_per * 5]

        self.walk_frames_ur = walk_frames[walk_per * 5:walk_per * 6]

        self.walk_frames_r = walk_frames[walk_per * 6:walk_per * 7]

        self.walk_frames_dr = walk_frames[walk_per * 7:walk_per * 8]

        self.attack_frames_d = attack_frames[:attack_per * 1]

        self.attack_frames_dl = attack_frames[attack_per * 1:attack_per * 2]

        self.attack_frames_l = attack_frames[attack_per * 2:attack_per * 3]

        self.attack_frames_ul = attack_frames[attack_per * 3:attack_per * 4]

        self.attack_frames_u = attack_frames[attack_per * 4:attack_per * 5]

        self.attack_frames_ur = attack_frames[attack_per * 5:attack_per * 6]

        self.attack_frames_r = attack_frames[attack_per * 6:attack_per * 7]

        self.attack_frames_dr = attack_frames[attack_per * 7:attack_per * 8]

    def move(self, dx=0, dy=0):
        if self.collide_with_walls(dx, dy) == "Exit":
            self.game.show_go_screen()

        elif not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def attack(self):
        self.attacking = True
        for entity in self.game.all_sprites:
            if entity.x == self.x + 1:
                entity.current_health  -= player_stats['Attack']

            elif entity.x == self.x - 1:
                entity.current_health -= player_stats['Attack']

            elif entity.y == self.y + 1:
                entity.current_health  -= player_stats['Attack']

            elif entity.y == self.y - 1:
                entity.current_health  -= player_stats['Attack']


    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        for entity in self.game.all_sprites:
            if entity.x == self.x + dx and entity.y == self.y + dy:
                return True
        for exit in self.game.exit:
            if exit.x == self.x + dx and exit.y == self.y + dy:
                return "Exit"
        return False

    def update(self):
        self.animate(self.game.state)
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


        # print(self.rect.x, self.rect.y)

    def animate(self, state):
        now = pg.time.get_ticks()
        # print(state)
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if state == 'R':
                    self.image = self.walk_frames_r[self.current_frame]

                elif state == 'L':
                    self.image = self.walk_frames_l[self.current_frame]

                elif state == 'U':
                    self.image = self.walk_frames_u[self.current_frame]

                elif state == 'D':
                    self.image = self.walk_frames_d[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.idle:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_d)
                bottom = self.rect.bottom

                if self.last_dir == 'D':
                    self.image = self.idle_frames_d[self.current_frame]
                elif self.last_dir == 'U':
                    self.image = self.idle_frames_u[self.current_frame]
                elif self.last_dir == 'R':
                    self.image = self.idle_frames_r[self.current_frame]
                elif self.last_dir == 'L':
                    self.image = self.idle_frames_l[self.current_frame]

                # self.rect = self.image.get_rect()
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.attacking:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames_d)
                bottom = self.rect.bottom
                print("attack")
                if self.last_dir == 'D':
                    self.image = self.attack_frames_d[self.current_frame]
                elif self.last_dir == 'U':
                    self.image = self.attack_frames_u[self.current_frame]
                elif self.last_dir == 'R':
                    self.image = self.attack_frames_r[self.current_frame]
                elif self.last_dir == 'L':
                    self.image = self.attack_frames_l[self.current_frame]

                # self.rect = self.image.get_rect()
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames_d[0]
        self.rect = pg.Rect(0, 0, 24, 24)
        self.walking = False
        self.idle = True
        self.current_health = 20
        self.last_dir = 'D'
        self.x = x
        self.y = y
        self.state = "D"

    def load_images(self):
        walk_frames = self.game.spritesheet_enemy.get_image_list("Walk")
        idle_frames = self.game.spritesheet_enemy.get_image_list("Idle")
        idle_per = int(len(idle_frames) / 8)
        walk_per = int(len(walk_frames) / 8)
        self.dim = int(idle_frames[0].get_rect()[2] * 0.5), int(idle_frames[0].get_rect()[3] * 5)
        # print(self.dim)

        self.idle_frames_d = idle_frames[:idle_per * 1]

        self.idle_frames_dl = idle_frames[idle_per * 1:idle_per * 2]

        self.idle_frames_l = idle_frames[idle_per * 2:idle_per * 3]

        self.idle_frames_ul = idle_frames[idle_per * 3:idle_per * 4]

        self.idle_frames_u = idle_frames[idle_per * 4:idle_per * 5]

        self.idle_frames_ur = idle_frames[idle_per * 5:idle_per * 6]

        self.idle_frames_r = idle_frames[idle_per * 6:idle_per * 7]

        self.idle_frames_dr = idle_frames[idle_per * 7:idle_per * 8]

        self.walk_frames_d = walk_frames[:walk_per * 1]

        self.walk_frames_dl = walk_frames[walk_per * 1:walk_per * 2]

        self.walk_frames_l = walk_frames[walk_per * 2:walk_per * 3]

        self.walk_frames_ul = walk_frames[walk_per * 3:walk_per * 4]

        self.walk_frames_u = walk_frames[walk_per * 4:walk_per * 5]

        self.walk_frames_ur = walk_frames[walk_per * 5:walk_per * 6]

        self.walk_frames_r = walk_frames[walk_per * 6:walk_per * 7]

        self.walk_frames_dr = walk_frames[walk_per * 7:walk_per * 8]

    def AI(self):
        room_bounds = self.game.current_room
        direction = choice((0, 1))
        dx = 0
        dy = 0
        move = self.goto()

        if self.y in range(self.game.current_room[1] - 2, self.game.current_room[1] + self.game.current_room[3] + 2):
            if self.x in range(self.game.current_room[0] - 2,
                               self.game.current_room[0] + self.game.current_room[2] + 2):
                if move:
                    dx = move[0]
                    dy = move[1]
                    if dx == -1:
                        if dy == 0:
                            self.state = "L"
                            self.last_dir = "L"
                        if dy == -1:
                            self.state = "UL"
                            self.last_dir = "UL"
                        if dy == 1:
                            self.state = "DL"
                            self.last_dir = "DL"

                    if dx == 1:
                        if dy == 0:
                            self.state = "R"
                            self.last_dir = "R"
                        if dy == -1:
                            self.state = "UR"
                            self.last_dir = "UR"
                        if dy == 1:
                            self.state = "DR"
                            self.last_dir = "DR"

                    if dx == 0:
                        if dy == 0:
                            self.last_dir = self.last_dir
                        if dy == -1:
                            self.state = "U"
                            self.last_dir = "U"
                        if dy == 1:
                            self.state = "D"
                            self.last_dir = "D"

        if not move:
            if direction:
                dx = choice((-1, 1))
                if dx == -1:
                    self.state = "L"
                    self.last_dir = "L"
                if dx == 1:
                    self.state = "R"
                    self.last_dir = "R"
            if not direction:
                dy = choice((-1, 1))
                if dy == -1:
                    self.state = "U"
                    self.last_dir = "U"
                if dy == 1:
                    self.state = "D"
                    self.last_dir = "D"

        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

        for entity in self.game.playersprite:
            if entity.x == self.x:
                self.game.playerhealth -= 2

            elif entity.x == self.x:
                self.game.playerhealth -= 2

            elif entity.y == self.y:
                self.game.playerhealth -= 2

            elif entity.y == self.y:
                self.game.playerhealth -= 1

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        for entity in self.game.all_sprites:
            if entity.x == self.x + dx and entity.y == self.y + dy:
                return True
        return False

    def update(self):
        self.animate()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        if self.current_health <= 0:
            pg.sprite.Sprite.remove(self, (self.game.all_sprites, self.game.mobs))

    def animate(self):

        state = self.state
        # print(state)

        now = pg.time.get_ticks()
        if self.walking:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if state == 'R':
                    self.image = self.walk_frames_r[self.current_frame]

                elif state == 'L':
                    self.image = self.walk_frames_l[self.current_frame]

                elif state == 'U':
                    self.image = self.walk_frames_u[self.current_frame]

                elif state == 'D':
                    self.image = self.walk_frames_d[self.current_frame]

                elif state == 'DR':
                    self.image = self.walk_frames_dr[self.current_frame]

                elif state == 'DL':
                    self.image = self.walk_frames_dl[self.current_frame]

                elif state == 'UR':
                    self.image = self.walk_frames_ur[self.current_frame]

                elif state == 'DR':
                    self.image = self.walk_frames_dr[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.idle:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_d)
                bottom = self.rect.bottom

                if state == 'R':
                    self.image = self.idle_frames_r[self.current_frame]

                elif state == 'L':
                    self.image = self.idle_frames_l[self.current_frame]

                elif state == 'U':
                    self.image = self.idle_frames_u[self.current_frame]

                elif state == 'D':
                    self.image = self.idle_frames_d[self.current_frame]

                elif state == 'DR':
                    self.image = self.idle_frames_dr[self.current_frame]

                elif state == 'DL':
                    self.image = self.idle_frames_dl[self.current_frame]

                elif state == 'UR':
                    self.image = self.idle_frames_ur[self.current_frame]

                elif state == 'DR':
                    self.image = selfidle_frames_dr[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def goto(self):
        path = self.pathfound()
        if path:
            return path[0][0] - self.x, path[0][1] - self.y

    def pathfound(self):

        dun = self.game.map.original_map
        rev = {}
        tmp_terrain = []

        for tile in pf.config.TERRAIN_CHARACTERS:
            tmp = pf.config.TERRAIN_CHARACTERS[tile]
            rev[tmp] = tile

        for y in range(len(dun)):
            tmp_terrain.append([])
            for x in range(len(dun[y])):
                tmp_terrain[y].append(rev[dun[y][x]])

        test_area = pf.Area()
        test_area.terrain = tmp_terrain
        test_area.width = len(tmp_terrain[0])
        test_area.height = len(tmp_terrain)

        # An instance of the pathfinder.
        pathfinder = pf.Pathfinder(test_area)

        # The goal and player x and y.
        gx, gy = self.game.player_coords
        px, py = self.x, self.y

        # Find the Goal
        r1 = pathfinder.is_point_findable(px, py, gx, gy,
                                          use_diagonals=True,
                                          abort=False)

        r2 = pathfinder.find_point(px, py, gx, gy,
                                   best_path=True,
                                   use_diagonals=True,
                                   abort=False)

        # print(self.game.player_coords, r2)

        return r2


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.w = 24
        self.h = 24
        self.rect = pg.Rect(x, y, self.w, self.h)
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Stairs(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.exit
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.w = 24
        self.h = 24
        self.x = x
        self.y = y
