# C
import pygame

C_ORANGE = (217, 145, 133)
C_YELLOW = (255, 255, 128)
C_WHITE = (255, 255, 255)
C_GREEN = (0, 128, 0)
C_CYAN = (0, 128, 128)

# E
EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_TIMEOUT = pygame.USEREVENT + 2
ENTITY_SPEED = {
    'Player': 3,
    'Enemy1': 1,
    'Enemy2': 2,
}

ENTITY_HEALTH = {
    'Player': 100,
    'Enemy1': 15,
    'Enemy2': 25,
}

ENTITY_DAMAGE = {
    'Player': 5,
    'Enemy1': 3,
    'Enemy2': 5,
}

ENTITY_SCORE = {
    'Player': 0,
    'Enemy1': 100,
    'Enemy2': 125,
}

ENTITY_SCALE = 0.2

ENEMY_ATTACK_RANGE_X = 20
ENEMY_ATTACK_RANGE_Y = 15

# M
MENU_OPTION = ('NEW GAME',
               'RANKING',
               'EXIT')

# P
PLAYER_KEY_UP = pygame.K_w
PLAYER_KEY_DOWN = pygame.K_s
PLAYER_KEY_LEFT = pygame.K_a
PLAYER_KEY_RIGHT = pygame.K_d
PLAYER_KEY_ATTACK = pygame.K_l

PLAYER_ATTACK_RANGE_X = 50
PLAYER_ATTACK_RANGE_Y = 20

# S
SPAWN_TIME = 5000

# T
TIMEOUT_STEP = 100  # 100ms
TIMEOUT_LEVEL = 60000  # 60s
# W
WIN_WIDTH = 600
WIN_HEIGHT = 337

# S
SCORE_POS = {'Title': (WIN_WIDTH / 2, 50),
             'EnterName': (WIN_WIDTH / 2, 80),
             'Label': (WIN_WIDTH / 2, 90),
             'Name': (WIN_WIDTH / 2, 110),
             0: (WIN_WIDTH / 2, 110),
             1: (WIN_WIDTH / 2, 130),
             2: (WIN_WIDTH / 2, 150),
             3: (WIN_WIDTH / 2, 170),
             4: (WIN_WIDTH / 2, 190),
             5: (WIN_WIDTH / 2, 210),
             6: (WIN_WIDTH / 2, 230),
             7: (WIN_WIDTH / 2, 250),
             8: (WIN_WIDTH / 2, 270),
             9: (WIN_WIDTH / 2, 290),
             }
