

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from collections import deque
import heapq
from sys import version_info


class Config(object):

    def __init__(self):
        self.TERRAIN_CHARACTERS = {
                                   'flagstone': '0',
                                   'stone brick': '1',
                                   'solid stone': '#'
        }

        self.TERRAIN_COLORS = {
                               'closed door': 'aqua',
                               'flagstone': 'silver',
                               'open secret door': 'aqua',
                               'open door': 'aqua',
                               'solid stone': 'black',
                               'stone brick': 'white',
                               'closed secret door': 'aqua'
        }
        # NOTE: This could easily be a dict where the keys are the obstructions
        # and the values are the tile characters, pygame surfaces, etc.
        self.OBSTRUCTION_CHARACTERS = {
                                       'stone brick' : '1',
                                       'solid stone': '#'
        }



config = Config()


class Area(object):

    def __init__(self):
        self.terrain = None
        self.width = None
        self.height = None


class Pathfinder(object):
    '''Find a path form x1, y1 to a point or tile(s).

    area -- An instance of the Area() class. See Area() at the top, and the
    c_dist -- Integer or Float, the distance of a step in a cardinal
    direction.
    d_dist -- Integer or Float, the distance of a step in a diagonal
    direction.
    obstruction_characters -- An iterable of characters that obstruct movement.
    '''

    def __init__(self, area):
        self.area = area  # An instance of the Area() class.
        self.c_dist = 70  # Could be 70, 1.0,                10, 100, 1000.
        self.d_dist = 99  # Could be 99, 1.4142135623730951, 14, 141, 1414.
        self.obstruction_characters = config.OBSTRUCTION_CHARACTERS
        self._unobstruct_goals = None  # Find a goal that is an obstruction.
        self._cardinals = [(0, -1, self.c_dist), (1, 0, self.c_dist),
                           (0, 1, self.c_dist), (-1, 0, self.c_dist)]
        self._diagonals = [(-1, -1, self.d_dist), (1, -1, self.d_dist),
                           (1, 1, self.d_dist), (-1, 1, self.d_dist)]
        self._directions = None  # Cardinals, or cardinals + diagonals.
        self._heuristic = None  # The A-Star heuristic
        self._x2, self._y2 = None, None  # Used if the goal is a point.
        self._tile, self._tiles = None, None  # goal is a tile, tiles.
        self._closed_set_coords = set()  # Just the coords to speed up checks.
        # List of lists of parent coordinates to help retrace the path.
        # NOTE: This is a literal Dijkstra map. See ._purge_private() for info.
        self.__parent_map_row = [None] * self.area.width
        self._closed_set_parent_map = []
        self._open_set = []  # Tiles to be evaluated.
        self._open_set_coords = set()  # Just the coords to speed up checks.
        self._is_goal = None  # Is this tile the goal?
        self._print_path_info = False  # Print info from retrace path.

    def _is_goal_point(self, current_tile):
        '''Is this the goal point?

        current_tile -- List in [current + estimated distance, estimated
        distance, distance so far, (current x, current y), (parent x,
        parent y)] format.

        Return: Boolean. (True if the goal is found.)
        '''

        return current_tile[3] == (self._x2, self._y2)

    def _is_goal_tile(self, current_tile):

        cur_x1, cur_y1 = current_tile[3]

        return self.area.terrain[cur_y1][cur_x1] == self._tile

    def _is_goal_iterable(self, current_tile):


        cur_x1, cur_y1 = current_tile[3]

        return self.area.terrain[cur_y1][cur_x1] in self._tiles

    def _cardinal_heuristic(self, x1, y1, x2, y2):
        '''Return the Manhattan distance.

        x1, y1, x2, y2 -- Integers. Start and end coordinates.

        Return: Integer or Float. (The distance estimate.)
        '''

        d_x, d_y = abs(x1 - x2), abs(y1 - y2)

        return (d_x + d_y) * self.c_dist

    def _diagonal_heuristic(self, x1, y1, x2, y2):
        '''Return a distance estimate for grids that allow diagonal movement.


        x1, y1, x2, y2 -- Integers. Start and end coordinates.


        While simple, fast, and producing an admissible heuristic, the more
        diagonal the path the more an estimate would be low.


        C, D = self.c_dist, self.d_dist
        E = 2 * C - D
        (E * abs(d_x - d_y) + D * (d_x + d_y)) / 2

        or

        B = self.d_dist - self.c_dist
        C * d_x + B * d_y if d_x > d_y else
        C * d_y + B * d_x

        for a more accurate estimate. I settled on the latter.

        Return: Integer or Float. (The distance estimate.)
        '''

        d_x, d_y = abs(x1 - x2), abs(y1 - y2)

        # NOTE: Doing this with a max() and min() was slower on Python 3
        if d_x > d_y:
            return self.c_dist * d_x + (self.d_dist - self.c_dist) * d_y
        else:
            return self.c_dist * d_y + (self.d_dist - self.c_dist) * d_x

    def _purge_private(self):
        '''Purge Pathfinder()'s private values, usually before finding a new
        path.'''

        self._x2, self._y2 = None, None
        self._tile, self._tiles = None, None
        self._heuristic = None
        self._directions = None
        self._open_set_coords = set()
        self._open_set = []
        self._closed_set_coords = set()
        self._closed_set_parent_map = [self.__parent_map_row[:] for row in
                                       range(self.area.height)]
        self._is_goal = None
        self._unobstruct_goals = None

    def _look_for_open(self, current_tile, best_path):
        ''' Add the eligible neighbours to open_set adjusting other tiles as
        needed.
        '''

        x, y = current_tile[3]
        current_dist = current_tile[2]

        for direction in self._directions:
            # NOTE: Implementing a '1' based movement cost system should be
            # trivial in the following code.
            x_mod, y_mod, step_dist = direction
            new_x, new_y = x + x_mod, y + y_mod

            # If it's not in bounds...
            if 0 > new_x == self.area.width or 0 > new_y == self.area.height:

                continue
            else:
                the_tile = self.area.terrain[new_y][new_x]

            # Or if it is in the closed_set...
            if (new_x, new_y) in self._closed_set_coords:

                continue

            # If not unobstructing goals and it hits an obstruction...
            elif not self._unobstruct_goals and the_tile in \
                    self.obstruction_characters:

                continue

            # When looking for a goal find it even if it's an obstruction when
            # unobstructing goals...
            elif self._unobstruct_goals and the_tile in \
                    self.obstruction_characters:

                if self._x2 and self._y2 and (
                        new_x, new_y) != (self._x2, self._y2):

                    continue
                elif self._tile and self.area.terrain[
                    new_y][new_x] != self._tile:

                    continue
                elif self._tiles and self.area.terrain[
                    new_y][new_x] not in self._tiles:

                    continue

            # Update the distance travelled
            dist = current_dist + step_dist
            # Generate a heuristic distance for a goal that's a point.
            # NOTE: if self._heuristic == None then do a Dijkstra search
            # where the heuristic distance is just the distance traveled so
            # far, and the distance estimate is None.
            heuristic_estimate = None
            heuristic_distance = dist
            if self._heuristic:
                heuristic_estimate = self._heuristic(new_x, new_y,
                                                     self._x2, self._y2)
                heuristic_distance += heuristic_estimate

            # Not in the open_set so add it.
            if (new_x, new_y) not in self._open_set_coords:
                self._open_set_coords.add((new_x, new_y))
                heapq.heappush(self._open_set,
                               [heuristic_distance,  # Heuristic distance
                                heuristic_estimate,  # Estimated distance
                                dist,  # Distance traveled
                                (new_x, new_y),  # (x, y)
                                (x, y)])  # (parent_x, parent_y)

                continue
            # In the open_set and we want the best path.
            elif best_path and (new_x, new_y) in self._open_set_coords:
                for tile in self._open_set:
                    if (new_x, new_y) == tile[3]:
                        # In the open_set and better.
                        if tile[2] > dist:
                            tile[0] = heuristic_distance
                            tile[1] = heuristic_estimate
                            tile[2] = dist
                            tile[4] = (x, y)
                            # Turns out naively re-heapifying is faster.
                            heapq.heapify(self._open_set)

                        break

    def _retrace_path(self, current_tile):
        '''Retrace a path to the start.

        current_tile -- List in [current + estimated distance, estimated
        distance, distance so far, (current x, current y), (parent x,
        parent y)] format.

        Retrace a path to (x1, y1). A path includes the (x, y) of the goal /
        target, but not that of the starting tile.

        Return: deque(). (A deque of (x, y) Tuples representing the path.)
        '''

        parent = current_tile[4]
        the_path = deque()
        if parent:
            # Add the endpoint.
            the_path.appendleft(current_tile[3])

            while parent:
                # Add the parent until we get to to the starting x, y
                x, y = parent
                if self._closed_set_parent_map[y][x]:
                    the_path.appendleft(parent)
                parent = self._closed_set_parent_map[y][x]

        if self._print_path_info:
            print("\n\n==========")
            print("\nCurrent:")
            print(current_tile)
            # print("\nOpen Set Coordinates:")
            # print(self._open_set_coords)
            print("\nOpen Set Length:")
            print(len(self._open_set_coords))
            # print("\nClosed Set Coordinates:")
            # print(self._closed_set_coords)
            print("\nClosed Set Length:")
            print(len(self._closed_set_coords))
            print("\nPath:")
            print(the_path)
            print("\nTile Steps:")
            print(len(the_path))

        return the_path



    def _find_path(self, best_path, abort, goal_only):
        '''Find a path.

        best_path -- Boolean. 'True' to look for the best path. This is slower
        as it involves modifying already processed tiles and possibly breaking
        the heap invariant.
        abort -- False, or Integer. If the len(self._closed_set_coords) > abort
        stop searching.

        Return: deque, list, or None. (A deque of (x, y) Tuples, or a Tuple of
        (x, y, tile name) if goal only == true, or None if no path is found.)
        '''

        while self._open_set:
            current_tile = heapq.heappop(self._open_set)
            self._open_set_coords.remove(current_tile[3])
            x, y = current_tile[3]

            # Yay, we found the goal!
            if self._is_goal(current_tile) and not goal_only:
                return self._retrace_path(current_tile)
            elif self._is_goal(current_tile) and goal_only:
                return (x, y, self.area.terrain[y][x])

            # No goal, let's update the self._closed_set* and look for more
            # tiles...
            self._closed_set_coords.add(current_tile[3])
            # Abort search. Remember False == 0.
            if len(self._closed_set_coords) > abort > 0:
                return None
            self._closed_set_parent_map[y][x] = current_tile[4]
            self._look_for_open(current_tile, best_path)

        # Ooops, couldn't find a path!
        return None

    def find_point(self, x1, y1, x2, y2, use_diagonals=True, best_path=True,
                   abort=False):
        '''Look for a specified point.

        x1, y1, x2, y2 -- Integers. The start and end point.
        use_diagonals -- Boolean. Path including diagonal directions. This is
        slower as it has to check twice the tiles.
        best_path -- Boolean. 'True' to look for the best path. This is slower
        as it involves modifying already processed tiles and possibly breaking
        the heap invariant. If set to 'False' paths are often somewhat more
        organic, and can somewhat approximate a 'greedy best first' search.
        abort -- False, or Integer. If the 'len(self._closed_set_coords) >
        abort' stop searching. This should stop any 'too slow' searches.

        Return: deque or None. (A deque of (x, y) Tuples, or None if no path
        is found.)
        '''

        self._purge_private()
        self._x2 = x2
        self._y2 = y2
        self._unobstruct_goals = False

        if use_diagonals:
            self._heuristic = self._diagonal_heuristic
            self._directions = set(self._cardinals + self._diagonals)
        else:
            self._heuristic = self._cardinal_heuristic
            self._directions = set(self._cardinals)

        self._is_goal = self._is_goal_point
        self._open_set_coords.add((x1, y1))
        heuristic_estimate = self._heuristic(x1, y1, x2, y2)

        heapq.heappush(self._open_set,
                       [0 + heuristic_estimate,  # A-Star
                        heuristic_estimate,  # Distance estimate
                        0,  # Distance traveled
                        (x1, y1),  # (x, y)
                        None])  # (parent_x, parent_y)

        return self._find_path(best_path, abort, False)

    def is_point_findable(self, x1, y1, x2, y2, use_diagonals=True,
                          abort=False):
        '''


        x1, y1, x2, y2 -- Integers. The start and end point.
        use_diagonals -- Boolean. Path including diagonal directions. This is
        slower as it has to check twice the tiles.
        abort -- False, or Integer. If the 'len(self._closed_set_coords) >
        abort' stop searching. This should stop any 'too slow' searches.


        Return: Boolean. (True if the point is findable)
        '''

        self._purge_private()
        self._x2 = x2
        self._y2 = y2
        self._unobstruct_goals = False

        if use_diagonals:
            self._heuristic = self._diagonal_heuristic
            self._directions = set(self._cardinals + self._diagonals)
        else:
            self._heuristic = self._cardinal_heuristic
            self._directions = set(self._cardinals)

        self._is_goal = self._is_goal_point
        self._open_set_coords.add((x1, y1))
        heuristic_estimate = self._heuristic(x1, y1, x2, y2)

        heapq.heappush(self._open_set,
                       [0 + heuristic_estimate,  # A-Star
                        heuristic_estimate,  # Distance estimate
                        0,  # Distance traveled
                        (x1, y1),  # (x, y)
                        None])  # (parent_x, parent_y)

        found = self._find_path(False, abort, True)
        if found:
            return True
        else:
            return False

    def find_tile(self, x1, y1, tile, use_diagonals=True, best_path=True,
                  abort=False):
        '''

        x1, y1 -- Integers. The start point.
        tile -- String or Iterable. The tile, or an iterable of tiles, being
        sought.
        use_diagonals -- Boolean. Path including diagonal directions. This is
        slower as it has to check twice the tiles.
        best_path -- Boolean. 'True' to look for the best path. This is slower
        as it involves modifying already processed tiles and possibly breaking
        the heap invariant. If set to 'False' paths are often somewhat more
        organic, and can somewhat approximate a 'greedy best first' search.
        abort -- False, or Integer. If the 'len(self._closed_set_coords) >
        abort' stop searching. This should stop any 'too slow' searches.

        Return: deque or None. (A deque of (x, y) Tuples, or None if no path
        is found.)
        '''

        self._purge_private()

        if type(tile) == str:
            self._tile = tile
            self._is_goal = self._is_goal_tile
        else:
            self._tiles = tile
            self._is_goal = self._is_goal_iterable

        self._unobstruct_goals = True

        if use_diagonals:
            self._directions = set(self._cardinals + self._diagonals)
        else:
            self._directions = set(self._cardinals)

        self._open_set_coords.add((x1, y1))

        heapq.heappush(self._open_set,
                       [0,  # Dijkstra
                        None,  # Distance estimate
                        0,  # Distance traveled
                        (x1, y1),  # (x, y)
                        None])  # (parent_x, parent_y)

        return self._find_path(best_path, abort, False)

    def nearest(self, x1, y1, tile, use_diagonals=True, abort=False):
        '''Look for a specified tile, or tile in an iterable of tiles, and
        return the location and name of that tile.

        x1, y1 -- Integers. The start point.
        tile -- String or Iterable. The tile, or an iterable of tiles, being
        sought.
        use_diagonals -- Boolean. Path including diagonal directions. This is
        slower as it has to check twice the tiles.
        abort -- False, or Integer. If the len(self._closed_set_coords) >
        abort stop searching. This should stop any 'too slow' away searches.


        Return: Tuple or None. (A Tuple of (x, y, tile name), or None.)
        '''

        self._purge_private()

        if type(tile) == str:
            self._tile = tile
            self._is_goal = self._is_goal_tile
        else:
            self._tiles = tile
            self._is_goal = self._is_goal_iterable

        self._unobstruct_goals = True

        if use_diagonals:
            self._directions = set(self._cardinals + self._diagonals)
        else:
            self._directions = set(self._cardinals)

        self._open_set_coords.add((x1, y1))

        heapq.heappush(self._open_set,
                       [0,  # Dijkstra
                        None,  # Distance estimate
                        0,  # Distance traveled
                        (x1, y1),  # (x, y)
                        None])  # (parent_x, parent_y)

        return self._find_path(False, abort, True)



