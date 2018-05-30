from ..boards.memory_board import MemoryBoard
from ..servers.server import Server
from ..states.follower import Follower

board = MemoryBoard()
state = Follower()
self.server = Server( 1, state, [], board, [] )