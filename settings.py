from random import choice

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (1, 1, 1)
LIGHTGREY = (200, 200, 200)
LIGHTBLUE = (0, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

# TEXTURE_WALL =
CHARACTER = choice(('25', '87', '56', '6', '113', '40', '134', '135', '136'))

# Maps:
MAPNAMES = ['Amp Plains.png', 'AppleWoods.png', 'Beach Cave.png', 'Blank Desert.png',
            'Bottomless Sea.png', 'Brine Cave.png',
            'Concealed Ruins.png', 'Craggy Coast.png', 'Crystal Cave Lower.png',
            'Crystal Cave Upper.png', 'Dark Hill Lower.png',
            'Dark Hill Upper.png', 'Deep Dark Crater.png', 'Deep Dusk Forest Upper.png',
            'Deep Dusk Forest Lower.png', 'Deep Grove.png',
            'Deep Sealed Ruin.png', 'Drenched Bluff.png', 'Dusk Forest Lower.png',
            'Dusk Forest Upper.png', 'Far Amp Plains.png',
            'Final Maze.png', 'Foggy Forest.png', 'Forest Path.png', 'Golden Chamber.png',
            'Hidden Highland.png',
            'Hidden Land.png', 'Ice Aegis Cave.png', 'Lower Brine Cave.png', 'Miracle Sea.png',
            'Mt Bristle.png', 'Mt Horn.png', 'Mt Travail.png',
            'Mystery Jungle Lower.png', 'Mystery Jungle Upper.png',
            'Mystifying Forest.png', 'Northern Desert Lower.png',
            'Northern Desert Upper.png', 'Quicksand Cave.png', 'Quicksand Pit.png',
            'Rock Aegis Cave.png', 'Rock Path.png', 'Shimmer Desert.png', 'Side Path.png',
            'Spacial Rift Lower.png', 'Spacial Rift Upper.png', 'Steam Cave.png',
            'Steel Aegis Cave.png', 'Surrounded Sea.png', 'Temporal Spire.png',
            'Temporal Tower.png', 'The Nightmare.png', 'Tiny Meadow.png',
            'Treeshroud Forest Lower.png',
            'Treeshroud Forest Upper.png', 'Waterfall Cave.png', 'World Abyss.png',
            'Zero Isle East.png', 'Zero Isle West.png', 'Zero Isle South.png',
            'Zero Isle North.png']

# game settings

TILESIZE = 24

WIDTH = int(512)  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = int(384)  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "DungeonCrawler"
BGCOLOR = 255, 0, 255

GRIDWIDTH = WIDTH / TILESIZE

GRIDHEIGHT = HEIGHT / TILESIZE

# player Settings
