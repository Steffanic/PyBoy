#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#
__pdoc__ = {
    "GameWrapperPacMan.cartridge_title": False,
    "GameWrapperPacMan.post_tick": False,
}

import logging

import numpy as np
from pyboy.utils import WindowEvent

from .base_plugin import PyBoyGameWrapper

logger = logging.getLogger(__name__)

try:
    from cython import compiled
    cythonmode = compiled
except ImportError:
    cythonmode = False

# Define the tiles that are used in the game
# for four tile sprites and "tile groups" the order is 
# top left, top right, bottom left, bottom right

# Pacman Alive
left_facing_neutral = [66, 67, 82, 83] 
right_facing_neutral = [67, 66, 83, 82] # right facing is left facing mirrored, one of the sprite attributes
up_facing_neutral = [74, 75, 90, 91]
down_facing_neutral = [90, 91, 74, 75] # down facing is up facing mirrored, one of the sprite attributes

left_facing_open = [68, 69, 84, 85]
right_facing_open = [69, 68, 85, 84] # right facing is left facing mirrored, one of the sprite attributes

up_facing_open = [76, 77, 92, 93]
down_facing_open = [92, 93, 76, 77] # down facing is up facing mirrored, one of the sprite attributes

left_facing_closed = [64, 65, 80, 81]
right_facing_closed = [65, 64, 81, 80] # right facing is left facing mirrored, one of the sprite attributes
up_facing_closed = [72, 73, 88, 89]
down_facing_closed = [88, 89, 72, 73] # down facing is up facing mirrored, one of the sprite attributes


# Pacman Dead
dead_1 = [0,1,16,17]
dead_2 = [2,3,18,19]
dead_3 = [4,5,20,21]
dead_4 = [6,7,22,23]
dead_5 = [8,9,24,25]
dead_6 = [10,11,26,27]
dead_7 = [12,13,28,29]
dead_8 = [14,15,30,31]
dead_poof = [32,33,48,49]

pacman_neutral = [left_facing_neutral+right_facing_neutral+up_facing_neutral+down_facing_neutral]
pacman_open = [left_facing_open+right_facing_open+up_facing_open+down_facing_open]
pacman_closed = [left_facing_closed+right_facing_closed+up_facing_closed+down_facing_closed]
pacman_alive = [pacman_neutral+pacman_open+pacman_closed]

pacman_dead = [dead_1+dead_2+dead_3+dead_4+dead_5+dead_6+dead_7+dead_8+dead_poof]

# Ghosts
left_looking_ghost = [104, 105, 120, 121]
right_looking_ghost = [105, 104, 121, 120] # right facing is left facing mirrored, one of the sprite attributes
up_looking_ghost = [100, 101, 116, 117]
down_looking_ghost = [96, 97, 112, 113]
scared_ghost = [108, 109, 124, 125]
left_looking_ghost_eyes = [44, 45, 54, 55]
right_looking_ghost_eyes = [45, 44, 55, 54] # right facing is left facing mirrored, one of the sprite attributes
up_looking_ghost_eyes = [42, 43]
down_looking_ghost_eyes = [40, 41, 50, 51]

ghosts_danger = [left_looking_ghost+right_looking_ghost+up_looking_ghost+down_looking_ghost]
ghosts_scared = [scared_ghost]
ghosts_eyes = [left_looking_ghost_eyes+right_looking_ghost_eyes+up_looking_ghost_eyes+down_looking_ghost_eyes]



# Pellets and Power Pellets
pellet = [260, 262]
power_pellet = [261]

pellets = [pellet+power_pellet]

# Fruit 
fruit = [70, 71, 86, 87] # Each new level loads a new fruit tile to the same tile identifier

consumables = [pellet+power_pellet+fruit]


# Wall 
wall = [272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288]

# Empty Spaces 
empty = [256, 327]
# Info-Panel 
lives_icon =  [132, 133, 148, 149]
first_level_icon = [128, 129, 144, 145]
second_level_icon = [130, 131, 146, 147]
third_level_icon = [160, 161, 176, 177]
fourth_level_icon = third_level_icon
fifth_level_icon = [162, 163, 184, 185]
sixth_level_icon = fifth_level_icon
seventh_level_icon = [192, 193, 208, 209]
eighth_level_icon = seventh_level_icon
ninth_level_icon = [194, 195, 210, 211]
tenth_level_icon = ninth_level_icon
eleventh_level_icon = [226, 227, 242, 243]
twelfth_level_icon = eleventh_level_icon
thirteenth_level_icon = [224, 225, 240, 241]
remaining_level_icon = thirteenth_level_icon

zero = [304]
one = [305]
two = [306]
three = [307]
four = [308]
five = [309]
six = [310]
seven = [311]
eight = [312]
nine = [313]
empty_place = [320]

score_identifier_map = {zero[0]:0, one[0]:1, two[0]:2, three[0]:3, four[0]:4, five[0]:5, six[0]:6, seven[0]:7, eight[0]:8, nine[0]:9, empty_place[0]:0}

info_panel_icons = [lives_icon, first_level_icon, second_level_icon, third_level_icon, fourth_level_icon, fifth_level_icon, sixth_level_icon, seventh_level_icon, eighth_level_icon, ninth_level_icon, tenth_level_icon, eleventh_level_icon, twelfth_level_icon, thirteenth_level_icon, remaining_level_icon]

TILES = 384
tiles_minimal = np.zeros(TILES, dtype=np.uint8)
minimal_list = [
    pacman_alive+pacman_dead, # All of Pacmans tile identifiers

    consumables, # All of the consumables tile identifiers

    wall, # All of the wall tile identifiers

    ghosts_danger+ghosts_scared+ghosts_eyes, # All of the ghosts tile identifiers

    empty, # All of the empty tile identifiers
]
for i, tile_list in enumerate(minimal_list):
    for tile in tile_list:
        tiles_minimal[tile] = i + 1

tiles_compressed = np.zeros(TILES, dtype=np.uint8)
compressed_list = [
    pacman_alive, 
    pacman_dead, 
    ghosts_danger, 
    ghosts_scared, 
    ghosts_eyes, 
    pellet, 
    power_pellet,
    fruit, 
    wall, 
    empty, 
]

for i, tile_list in enumerate(compressed_list):
    for tile in tile_list:
        tiles_compressed[tile] = i + 1

np_in_mario_tiles = np.vectorize(lambda x: x in base_scripts)

# Hard code the window tilemap locations for some things
HIGH_SCORE_TENS=(1,4)
HIGH_SCORE_HUNDREDS=(1,3)
HIGH_SCORE_THOUSANDS=(1,2)
HIGH_SCORE_TEN_THOUSANDS=(1,1)
HIGH_SCORE_HUNDRED_THOUSANDS=(1,0)

HIGH_SCORE_PLACES = [HIGH_SCORE_TENS, HIGH_SCORE_HUNDREDS, HIGH_SCORE_THOUSANDS, HIGH_SCORE_TEN_THOUSANDS, HIGH_SCORE_HUNDRED_THOUSANDS]

CURRENT_SCORE_TENS=(4,4)
CURRENT_SCORE_HUNDREDS=(4,3)
CURRENT_SCORE_THOUSANDS=(4,2)
CURRENT_SCORE_TEN_THOUSANDS=(4,1)
CURRENT_SCORE_HUNDRED_THOUSANDS=(4,0)

CURRENT_SCORE_PLACES = [CURRENT_SCORE_TENS, CURRENT_SCORE_HUNDREDS, CURRENT_SCORE_THOUSANDS, CURRENT_SCORE_TEN_THOUSANDS, CURRENT_SCORE_HUNDRED_THOUSANDS]

TWO_LIVES_LEFT=(14, 2)
ONE_LIFE_LEFT=(14, 0)

LEVEL_ONE = (9,0)
LEVEL_TWO = (9,1)
LEVEL_THREE = (9,2)
LEVEL_FOUR = (9,3)


LEVELS = [LEVEL_ONE, LEVEL_TWO, LEVEL_THREE, LEVEL_FOUR]

def _bcm_to_dec(value):
    return (value >> 4) * 10 + (value & 0x0F)


class GameWrapperPacMan(PyBoyGameWrapper):
    """
    This class wraps Pac-Man, and provides easy access to score, lives left, level, and more.

    If you call `print` on an instance of this object, it will show an overview of everything this object provides.
    """
    cartridge_title = "PAC-MAN"
    tiles_compressed = tiles_compressed
    tiles_minimal = tiles_minimal

    def __init__(self, *args, **kwargs):
        self.shape = (20, 18) # 160x144
        """The shape of the game area"""
        self.level = 0
        """The current level"""
        self.lives_left = 2
        """The number of lives Pac Man has left"""
        self.score = 0
        """The score provided by the game"""
        self.high_score = 0
        """The high score provided by the game"""
        self.fitness = 0
        """
        A built-in fitness scoring. Taking points, level progression, time left, and lives left into account.

        .. math::
            fitness = (lives\\_left \\cdot 10000) + (score + time\\_left \\cdot 10) + (\\_level\\_progress\\_max \\cdot 10)
        """

        super().__init__(*args, game_area_section=(0, 2) + self.shape, game_area_wrap_around=True, **kwargs)

    def post_tick(self):
        self._tile_cache_invalid = True
        self._sprite_cache_invalid = True

        level_identifiers = [self.pyboy.botsupport_manager().tilemap_window().tile_identifier(*level_loc[::-1]) for level_loc in LEVELS if self.pyboy.botsupport_manager().tilemap_window().tile_identifier(*level_loc[::-1])!=320]
        self.level = len(level_identifiers)

        score_place_identifiers = [self.pyboy.botsupport_manager().tilemap_window().tile_identifier(*score_loc[::-1]) for score_loc in CURRENT_SCORE_PLACES[::-1]]

        self.score = np.sum(np.array([score_identifier_map[ti] for ti in score_place_identifiers])*[10000, 1000, 100, 10, 1])*10

        self.coins = self._sum_number_on_screen(9, 1, 2, blank, -256)
        self.lives_left = _bcm_to_dec(self.pyboy.get_memory_value(ADDR_LIVES_LEFT))
        self.score = self._sum_number_on_screen(0, 1, 6, blank, -256)
        self.time_left = self._sum_number_on_screen(17, 1, 3, blank, -256)

        level_block = self.pyboy.get_memory_value(0xC0AB)
        mario_x = self.pyboy.get_memory_value(0xC202)
        scx = self.pyboy.botsupport_manager().screen().tilemap_position_list()[16][0]
        self.level_progress = level_block*16 + (scx-7) % 16 + mario_x

        if self.game_has_started:
            self._level_progress_max = max(self.level_progress, self._level_progress_max)
            end_score = self.score + self.time_left * 10
            self.fitness = self.lives_left * 10000 + end_score + self._level_progress_max * 10

    def set_lives_left(self, amount):
        """
        Set the amount lives to any number between 0 and 99.

        This should only be called when the game has started.

        Args:
            amount (int): The wanted number of lives
        """
        if not self.game_has_started:
            logger.warning("Please call set_lives_left after starting the game")

        if 0 <= amount <= 99:
            tens = amount // 10
            ones = amount % 10
            self.pyboy.set_memory_value(ADDR_LIVES_LEFT, (tens << 4) | ones)
            self.pyboy.set_memory_value(ADDR_LIVES_LEFT_DISPLAY, tens)
            self.pyboy.set_memory_value(ADDR_LIVES_LEFT_DISPLAY + 1, ones)
        else:
            logger.error(f"{amount} is out of bounds. Only values between 0 and 99 allowed.")

    def set_world_level(self, world, level):
        """
        Patches the handler for pressing start in the menu. It hardcodes a world and level to always "continue" from.

        Args:
            world (int): The world to select a level from, 0-3
            level (int): The level to start from, 0-2
        """

        for i in range(0x450, 0x461):
            self.pyboy.override_memory_value(0, i, 0x00)

        patch1 = [
            0x3E, # LD A, d8
            (world << 4) | (level & 0x0F), # d8
        ]

        for i, byte in enumerate(patch1):
            self.pyboy.override_memory_value(0, 0x451 + i, byte)

    def start_game(self, timer_div=None, world_level=None, unlock_level_select=False):
        """
        Call this function right after initializing PyBoy. This will start a game in world 1-1 and give back control on
        the first frame it's possible.

        The state of the emulator is saved, and using `reset_game`, you can get back to this point of the game
        instantly.

        The game has 4 major worlds with each 3 level. to start at a specific world and level, provide it as a tuple for
        the optional keyword-argument `world_level`.

        If you're not using the game wrapper for unattended use, you can unlock the level selector for the main menu.
        Enabling the selector, will make this function return before entering the game.

        Kwargs:
            timer_div (int): Replace timer's DIV register with this value. Use `None` to randomize.
            world_level (tuple): (world, level) to start the game from
            unlock_level_select (bool): Unlock level selector menu
        """
        PyBoyGameWrapper.start_game(self, timer_div=timer_div)

        if world_level is not None:
            self.set_world_level(*world_level)

        # Boot screen
        while True:
            self.pyboy.tick()
            if self.tilemap_background[6:11, 13] == [284, 285, 266, 283, 285]: # "START" on the main menu
                break
        self.pyboy.tick()
        self.pyboy.tick()
        self.pyboy.tick()

        self.pyboy.send_input(WindowEvent.PRESS_BUTTON_START)
        self.pyboy.tick()
        self.pyboy.send_input(WindowEvent.RELEASE_BUTTON_START)

        while True:
            if unlock_level_select and self.pyboy.frame_count == 71: # An arbitrary frame count, where the write will work
                self.pyboy.set_memory_value(ADDR_WIN_COUNT, 2 if unlock_level_select else 0)
                break
            self.pyboy.tick()
            self.tilemap_background.refresh_lcdc()

            # "MARIO" in the title bar and 0 is placed at score
            if self.tilemap_background[0:5, 0] == [278, 266, 283, 274, 280] and \
               self.tilemap_background[5, 1] == 256:
                self.game_has_started = True
                break

        self.saved_state.seek(0)
        self.pyboy.save_state(self.saved_state)

        self._set_timer_div(timer_div)

    def reset_game(self, timer_div=None):
        """
        After calling `start_game`, use this method to reset Mario to the beginning of world 1-1.

        If you want to reset to later parts of the game -- for example world 1-2 or 3-1 -- use the methods
        `pyboy.PyBoy.save_state` and `pyboy.PyBoy.load_state`.

        Kwargs:
            timer_div (int): Replace timer's DIV register with this value. Use `None` to randomize.
        """
        PyBoyGameWrapper.reset_game(self, timer_div=timer_div)

        self._set_timer_div(timer_div)

    def game_area(self):
        """
        Use this method to get a matrix of the "game area" of the screen. This view is simplified to be perfect for
        machine learning applications.

        In Super Mario Land, this is almost the entire screen, expect for the top part showing the score, lives left
        and so on. These values can be found in the variables of this class.

        In this example, Mario is `0`, `1`, `16` and `17`. He is standing on the ground which is `352` and `353`:
        ```text
             0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19
        ____________________________________________________________________________________
        0  | 339 339 339 339 339 339 339 339 339 339 339 339 339 339 339 339 339 339 339 339
        1  | 320 320 320 320 320 320 320 320 320 320 320 320 320 320 320 320 320 320 320 320
        2  | 300 300 300 300 300 300 300 300 300 300 300 300 321 322 321 322 323 300 300 300
        3  | 300 300 300 300 300 300 300 300 300 300 300 324 325 326 325 326 327 300 300 300
        4  | 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300
        5  | 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300
        6  | 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300 300
        7  | 300 300 300 300 300 300 300 300 310 350 300 300 300 300 300 300 300 300 300 300
        8  | 300 300 300 300 300 300 300 310 300 300 350 300 300 300 300 300 300 300 300 300
        9  | 300 300 300 300 300 129 310 300 300 300 300 350 300 300 300 300 300 300 300 300
        10 | 300 300 300 300 300 310 300 300 300 300 300 300 350 300 300 300 300 300 300 300
        11 | 300 300 310 350 310 300 300 300 300 306 307 300 300 350 300 300 300 300 300 300
        12 | 300 368 369 300 0   1   300 306 307 305 300 300 300 300 350 300 300 300 300 300
        13 | 310 370 371 300 16  17  300 305 300 305 300 300 300 300 300 350 300 300 300 300
        14 | 352 352 352 352 352 352 352 352 352 352 352 352 352 352 352 352 352 352 352 352
        15 | 353 353 353 353 353 353 353 353 353 353 353 353 353 353 353 353 353 353 353 353
        ```

        Returns
        -------
        memoryview:
            Simplified 2-dimensional memoryview of the screen
        """
        return PyBoyGameWrapper.game_area(self)

    def game_over(self):
        # Apparantly that address is for game over
        # https://datacrystal.romhacking.net/wiki/Super_Mario_Land:RAM_map
        return self.pyboy.get_memory_value(0xC0A4) == 0x39

    def __repr__(self):
        adjust = 4
        # yapf: disable
        return (
            f"Super Mario Land: World {'-'.join([str(i) for i in self.world])}\n" +
            f"Coins: {self.coins}\n" +
            f"lives_left: {self.lives_left}\n" +
            f"Score: {self.score}\n" +
            f"Time left: {self.time_left}\n" +
            f"Level progress: {self.level_progress}\n" +
            f"Fitness: {self.fitness}\n" +
            "Sprites on screen:\n" +
            "\n".join([str(s) for s in self._sprites_on_screen()]) +
            "\n" +
            "Tiles on screen:\n" +
            " "*5 + "".join([f"{i: <4}" for i in range(20)]) + "\n" +
            "_"*(adjust*20+4) +
            "\n" +
            "\n".join(
                [
                    f"{i: <3}| " + "".join([str(tile).ljust(adjust) for tile in line])
                    for i, line in enumerate(self.game_area())
                ]
            )
        )
        # yapf: enable
