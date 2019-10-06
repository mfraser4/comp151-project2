"""
Mark Fraser
m_fraser3@u.pacific.edu
Project 2 - Adversarial Search
"""


infinity = float('inf')
search_depth = 7           # number of levels for alpha beta to explore
move = -1                  # recommended next action to take


def load_player(player):
    # insert file reading code here -- whatever is returned by this function will be saved as lookupX and passed into
    # next_move for use when choosing a move.
    return None


def next_move(board, player, lookup_table):
    global move
    
    move = -1 # reset move to be invalid

    # convert provided map to bitmap format
    position, mask = get_position_mask_bitmap(board.board, player)

    value = alphabeta((position, mask), search_depth, -infinity, infinity, True)

    return move


# based on pseudocode at https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
# always assumes board provided is a non-winning state
def alphabeta(board, depth, alpha, beta, is_maximizing_player):
    global move

    # generate set of valid next moves and associated column placement
    mask = board[1]
    children = []
    for col in range(7):
        # check valid move
        if not (mask & (1 << ((col*7) + 5))):
            new_board = (make_move(board[0], board[1], col))
            # check if current player can win with this move
            if connected_four(new_board[0] ^ new_board[1]):
                if is_maximizing_player:
                    if depth == search_depth:
                        move = col
                    return infinity # maximizing opponent wins
                return -infinity # minimizing opponent wins
            children += [(new_board, col)]

    # check terminal case
    # ordered second so as to allow determining board to be a move away from winning
    if depth == 0:
        if is_maximizing_player:
            return get_heuristic_value(board)
        else:
            return get_heuristic_value((board[0] ^ board[1], board[1])) # get value in terms of maximizing player

    if is_maximizing_player:
        value = -infinity
        best_move = -1 # stores move that is best
        for child in children:
            result = alphabeta(child[0], depth-1, alpha, beta, False)
            if result > value:
                value =  result
                best_move = child[1]
            alpha = max(alpha, value)
            if alpha >= beta:
                break # beta cutoff
        # check if need to make recommendation
        if depth == search_depth:
            move = best_move
        return value
    else:
        value = infinity
        for child in children:
            value = min(value, alphabeta(child[0], depth-1, alpha, beta, True))
            beta = min(beta, value)
            if alpha >= beta:
                break # alpha cutoff
        return value


# returns heuristic value of board based on position player
def get_heuristic_value(board):
    # value is score of provided player - score of opponent
    value = _get_player_heuristic_value(board) \
                - _get_player_heuristic_value(((board[0] ^ board[1]), board[1]))
    return value


# get the heuristic value of the provided player
def _get_player_heuristic_value(board):
    position = board[0]
    mask = board[1]
    value = 0

    # calculate number of middle positions controlled
    for i in range(6):
        if position & (1 << (21 + i)):
            value = value + 15

    # calculate number of one-off middle positions controlled
    for i in range(6):
        if position & (1 << (14 + i)):
            value = value + 10
        if position & (1 << (28 + i)):
            value = value + 10

    # calculate number of 3-in-a-rows with an open space

    # vertical 3-in-a-rows
    v = position & (position << 1)
    v = v & (v << 1)
    v = v << 1          # shift to next open space
    o = v & ~mask        # filter all available open slots next to 3-in-a-row
    b = bin(int(o))[2:]
    c = b.count('1')
    for i in range(1,7):
        if o & (1 << (7*i - 1)):
            c = c - 1 # false opening, subtract this from score

    value = value + (10 * c)

    # horizontal 3-in-a-rows
    h = position & (position << 7)
    h = h & (h << 7)
    h = (h << 7) | (h >> 21) # shift to next possible open spaces
    o = h & ~mask           # filter all available open slots next to 3-in-a-row
    b = bin(int(o))[2:]
    c = b.count('1')
    for i in range(1,7):
        if o & (1 << (7*i - 1)):
            c = c - 1 # false opening, subtract this from score

    value = value + (10 * c)

    # diagonal (/) 3-in-a-rows
    d = position & (position << 8)
    d = d & (d << 8)
    d = d << 8          # shift to next open space
    o = d & ~mask        # filter all available open slots next to 3-in-a-row
    b = bin(int(o))[2:]
    c = b.count('1')
    for i in range(1,7):
        if o & (1 << (7*i - 1)):
            c = c - 1 # false opening, subtract this from score

    value = value + (10 * c)

    # diagonal (\) 3-in-a-rows
    d = position & (position >> 8)
    d = d & (d >> 8)
    d = d >> 8          # shift to next open space
    o = d & ~mask        # filter all available open slots next to 3-in-a-row
    b = bin(int(o))[2:]
    c = b.count('1')
    for i in range(1,7):
        if o & (1 << (7*i - 1)):
            c = c - 1 # false opening, subtract this from score

    value = value + (10 * c)

    return value


# ______________________________________________________________________________
"""
Boilerplate Bitmap Functions

the following bitmapping operations have been adopted from multiple online
sources (listed below) to follow the most common strategy taken by complex
Connect4 AI algorithms, and that is saving memory by representing boards as
bitmaps

https://towardsdatascience.com/creating-the-perfect-connect-four-ai-bot-c165115557b0
http://blog.gamesolver.org/
"""

def get_position_mask_bitmap(board, player):
    position, mask = '', ''
    # Start with right-most column
    for j in range(6, -1, -1):
        # Add 0-bits to sentinel 
        mask += '0'
        position += '0'
        # Start with bottom row
        for i in range(0, 6):
            mask += ['0', '1'][board[i][j] != '.']
            position += ['0', '1'][board[i][j] == player]
    return int(position, 2), int(mask, 2)


def connected_four(position):
    # Horizontal check
    m = position & (position >> 7)
    if m & (m >> 14):
        return True

    # Diagonal \
    m = position & (position >> 6)
    if m & (m >> 12):
        return True

    # Diagonal /
    m = position & (position >> 8)
    if m & (m >> 16):
        return True

    # Vertical
    m = position & (position >> 1)
    if m & (m >> 2):
        return True

    # Nothing found
    return False


# makes move in provided column and returns board in context of opponent
def make_move(position, mask, col):
    new_position = position ^ mask
    new_mask = mask | (mask + (1 << (col*7)))
    return new_position, new_mask
