from consts import ADJ_C, TO_SEARCH, NUMBERS
from funcs.utils import *
from funcs.actions import click_tile, flag_tile


# fmt: off
"""Gets and returns of set of all grass tiles around a given tile

:param x_mp: the position of the mouse along the x axis
:type x_mp: int
:param y_mp: the position of the mouse along the y axis
:type y_mp: int

:returns: set containing tuples of x and y coordinates of grass tiles
:rtype: set((int, int),...)
"""
# fmt: on
def get_grass_tile_set(x_mp, y_mp):
    grass_set = set()
    for c in TO_SEARCH:
        if is_valid_mouse_pos(x_mp + c[0], y_mp + c[1]):
            tile = get_tile(x_mp + c[0], y_mp + c[1])
            if tile == "grass":
                grass_set.add((x_mp + c[0], y_mp + c[1]))
    return grass_set


# fmt: off
"""Runs advanced searching on a tile at given mouse positions

:param x_mp: the position of the mouse along the x axis
:type x_mp: int
:param y_mp: the position of the mouse along the y axis
:type y_mp: int
:param tile: number of bombs adjacent to current tile
:type tile: int

:returns: true if change was made via advanced searching on tile
:rtype: boolean
"""
# fmt: on
def advanced_search_tile(x_mp, y_mp, tile, x_c, y_c, ignore, searched_pairs):
    change_made = False

    # Determine number of remaining bombs adjacent to tile
    surrounding_tile_info = count_adj_tiles(x_mp, y_mp)
    remaining_bombs = tile - surrounding_tile_info[1]
    cur_grass_set = get_grass_tile_set(x_mp, y_mp)

    # Search around tile
    for c, m in zip(ADJ_C, TO_SEARCH):
        if (
            (x_c + c[0], y_c + c[1]) not in ignore
            and is_valid_mouse_pos(x_mp + m[0], y_mp + m[1])
            and ((x_c, y_c), (x_c + c[0], y_c + c[1])) not in searched_pairs
            and ((x_c + c[0], y_c + c[1]), (x_c, y_c)) not in searched_pairs
        ):
            searched_pairs.add(((x_c, y_c), (x_c + c[0], y_c + c[1])))

            # First, get the tile, if it's a number, continue
            adj_tile = get_tile(x_mp + m[0], y_mp + m[1])
            if adj_tile in NUMBERS:

                # Get the adjacent tile info for the adjacent tile
                adj_tile_info = count_adj_tiles(x_mp + m[0], y_mp + m[1])
                adj_remaining_bombs = adj_tile - adj_tile_info[1]
                adj_tile_grass_set = get_grass_tile_set(x_mp + m[0], y_mp + m[1])

                # Determine, between current tile and current adjcacent tile
                # which tile has more grass tile surrounding it, save those
                # we'll need this information to determine which tile set to
                # perform actions on
                if len(cur_grass_set) >= len(adj_tile_grass_set):
                    larger_bomb_no = remaining_bombs
                    smaller_bomb_no = adj_remaining_bombs
                    larger = cur_grass_set
                    smaller = adj_tile_grass_set
                else:
                    larger_bomb_no = adj_remaining_bombs
                    smaller_bomb_no = remaining_bombs
                    larger = adj_tile_grass_set
                    smaller = cur_grass_set

                # in order for advanced searching techniques to hold true, the set difference of
                # the smaller set - the larger set must be the empty set, this is to ensure that only
                # 1 tile set contains extra tiles
                none_check = smaller - larger

                if len(none_check) == 0:
                    dif = larger - smaller
                    # if the number of bombs between the two tiles is equal
                    # that means that the tiles contained in the larger adj grass set
                    # and not the smaller adj grass set are unnecesarry, so click them
                    if remaining_bombs == adj_remaining_bombs:
                        if len(dif) > 0:
                            change_made = True
                            for mp in dif:
                                click_tile(mp[0], mp[1])

                    # if the difference of the number of bombs in the larger tile set
                    # and the number of bombs in the smaller tile set is equal to the length
                    # of the difference of the grass tile set, that means all extra bombs from
                    # the larger bomb number are in all of the tiles in the difference
                    elif larger_bomb_no - smaller_bomb_no == len(dif):
                        if len(dif) > 0:
                            change_made = True
                            for mp in dif:
                                flag_tile(mp[0], mp[1])

    return change_made
