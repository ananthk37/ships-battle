import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1100,500))

red = (255,0,0)
green = (0,255,0)
blue = (0,100,255)
white = (250,250,250)





def get_adjacent(x, y):
    """
    Finds the adjacent positions to known hits (left, right, up, down, not necessarily in that order) 
    and updates a global stack of adjacent positions to check next
    
    Returns
    -------
    None.
    """
    global adjacent
    if x == 0:
        if y == 0:
            adjacent.append([x, y + 1])
            adjacent.append([x + 1, y])
        elif y == 9:
            adjacent.append([x, y - 1])
            adjacent.append([x + 1, y])
        else:
            adjacent.append([x, y + 1])
            adjacent.append([x, y - 1])
            adjacent.append([x + 1, y])
    elif x == 9:
        if y == 0:
            adjacent.append([x, y + 1])
            adjacent.append([x - 1, y])
        elif y == 9:
            adjacent.append([x, y - 1])
            adjacent.append([x - 1, y])
        else:
            adjacent.append([x, y + 1])
            adjacent.append([x, y - 1])
            adjacent.append([x - 1, y])
    elif y == 0:
        adjacent.append([x - 1, y])
        adjacent.append([x + 1, y])
        adjacent.append([x, y + 1])
    elif y == 9:
        adjacent.append([x - 1, y])
        adjacent.append([x + 1, y])
        adjacent.append([x, y - 1])
    else:
        adjacent.append([x, y + 1])
        adjacent.append([x, y - 1])
        adjacent.append([x - 1, y])
        adjacent.append([x + 1, y])

def guess():
    """
    If adjacent is empty, guess a random coordinate, else take the next element off of the stack 
    "adjacent" and attempt to guess that position.
    
    Returns
    -------
    None.
    """
    global adjacent
    global hitsOnShip
    
    if len(adjacent) == 0:
        hitsOnShip = 0
        x = random.randint(0,9)
        y = random.randint(0,9)
        if computer_board[x][y][1] and not 1 <= computer_board[x][y][0] <= 2:
            ###Random guess hits
            computer_board[x][y][0] = 1
            get_adjacent(x, y)
            hitsOnShip += 1
            if hitsOnShip > 5:
                adjacent.clear()
        elif computer_board[x][y][1] == False and not 1 <= computer_board[x][y][0] <= 2:
            ###Random guess misses
            computer_board[x][y][0] = 2
        else:
            ###Random guess choses already chosen
            guess()
    else:
        coord = adjacent.pop()
        x = coord[0]
        y = coord[1]
        if computer_board[x][y][1] and not 1 <= computer_board[x][y][0] <= 2:
            ###Popped adjacent guess hits
            computer_board[x][y][0] = 1
            get_adjacent(x, y)
            hitsOnShip += 1
            if hitsOnShip > 5:
                adjacent.clear()
        elif computer_board[x][y][1] == False and not 1 <= computer_board[x][y][0] <= 2:
            ###Popped adjacent guess misses
            computer_board[x][y][0] = 2
        else:
            ###Popped adjacent guess has been guessed before
            guess()



def generate_board():
    """
    Generates a 3D array that represents the gamestate of each board
    board[x][y][0] = 0 : Blank square
    board[x][y][0] = 1 : Hit a ship on this square
    board[x][y][0] = 2 : Missed the shot on this square
    board[x][y][1] = True : There is a ship in this square

    Returns
    -------
    result :  3 dimensional array as explained above

    """
    result = [[[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              ]
    i = 0
    while i < 5:
        length = 5 - i
        if(length == 1):
            length = 3
        x_ship = random.randint(0,9)
        y_ship = random.randint(0,9)
        direction = random.randint(0,1) # 0 is horizontal, 1 is vertical orientation
        
        invalid = False
        if(result[x_ship][y_ship][1]):
            continue
        if(direction == 0):
            if x_ship + length - 1 > 9:
                continue
            for j in range(length):
                if(result[x_ship + j][y_ship][1]):
                    invalid = True
            if(invalid):
                continue
            for j in range(length):
                   result[x_ship + j][y_ship][1] = True
        else:
            if y_ship + length - 1 > 9:
                continue
            for j in range(length):
                if(result[x_ship][y_ship + j][1]):
                    invalid = True
            if(invalid):
                continue
            for j in range(length):
                result[x_ship][y_ship + j][1] = True
        i += 1
    return result



def playersetup():
    """
    Handles user input to setup a board. To setup the board, the user must click
    first on a tile that is the front end of the ship, and then either click a tile directly
    below or above that tile to indicate which direction the ship should lie.
    Returns
    -------
    None.
    
    """
    
    
    print("Welcome to Battleship! To begin, we need to place your ships on the right side.\n")
    i = 0
    while i < 5:
        length = 5 - i
        if(length < 3):
            length += 1
        
        
        #drawing stuff
        populate_board(player_board,0, False)
        populate_board(computer_board,600, True)
        draw_boards()
        pygame.display.update()
        
        print("You are now placing a ship of length", length)
        print("Click on a square as a starting space for your ship.")
       
        
        
        #get initial position
        while(not pygame.event.peek(eventtype= pygame.MOUSEBUTTONDOWN)):
            continue
        mx, my = pygame.mouse.get_pos()
        x_ship,y_ship = (mx - 600) // 50, my // 50
        
        #if taken
        if(computer_board[x_ship][y_ship][1]):
            print("Sorry! That square is occupied.")
            pygame.event.clear()
            continue
        
        while(not pygame.event.peek(eventtype= pygame.MOUSEBUTTONUP)):
            continue
        pygame.event.clear()
        
        
        print("Now indicate the direction of the ship by clicking on an adjacent square either below or to the right of that one.")
        ##get direction of ship
        
        while(not pygame.event.peek(eventtype= pygame.MOUSEBUTTONDOWN)):
            continue
        
        mx, my = pygame.mouse.get_pos()
        x_direct,y_direct = (mx - 600) // 50, my // 50
        
        invalid = False
        
        #if oriented to the right
        if(x_direct > x_ship and y_direct == y_ship):
            #if fits map
            if x_ship + length > 10:
                print("Sorry! That orientation does not fit on the map.")
                pygame.event.clear()
                continue
            
            #if not occupied
            for j in range(length):
                if computer_board[x_ship + j][y_ship][1]:
                    invalid = True
            if(invalid):
                print("Sorry! That lane is occupied.")
                pygame.event.clear()
                continue
            for j in range(length):
                computer_board[x_ship + j][y_ship][1] = True
        
        #if oriented down
        elif(x_direct == x_ship and y_direct > y_ship):
            if y_ship + length > 10:
                print("Sorry! That orientation does not fit on the map.")
                pygame.event.clear()
                continue
            for j in range(length):
                if computer_board[x_ship][y_ship + j][1]:
                    invalid = True
            if(invalid):
                print("Sorry! That lane is occupied.")
                pygame.event.clear()
                continue
            for j in range(length):
                computer_board[x_ship][y_ship + j][1] = True
        
        #if orientation is wrong
        else:
            print("Sorry! That's not a valid orientation")
            pygame.event.clear()
            continue
        #computer_board[x_ship][y_ship][1] = True
        
        while(not pygame.event.peek(eventtype= pygame.MOUSEBUTTONUP)):
            continue
        pygame.event.clear()
        i += 1
        
        
        
def populate_board(board,offset, show):
    """
    Parameters
    ----------
    board : 3D array
        Array representing the state of the board
    offset : How far offset from the left side of the screen the board should be
             ex: player's board should be offset by 0, the computer's board should be offset by 600 pixels
    show : whether or not to show the ships.
    Returns
    -------
    None.

    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(show):
                if board[i][j][1] and board[i][j][0] == 0:
                    pygame.draw.rect(screen, green, (offset + i*50,j*50,50,50))
                elif board[i][j][1] and board[i][j][0] != 0:
                    pygame.draw.rect(screen, red, (offset + i*50,j*50,50,50))
                elif board[i][j][0] == 2:
                    pygame.draw.rect(screen,white, (offset + i*50,j*50,50,50))
                else:
                    pygame.draw.rect(screen, blue, (offset + i*50,j*50,50,50))
            else:
                if board[i][j][0] == 0:
                    ### BLANK
                    pygame.draw.rect(screen, blue, (offset + i*50,j*50,50,50))
                elif board[i][j][0] == 1:
                    ### HIT
                    pygame.draw.rect(screen, red, (offset + i*50,j*50,50,50))
                elif board[i][j][0] == 2:
                    ### MISS
                    pygame.draw.rect(screen,white, (offset + i*50,j*50,50,50))


def draw_boards():
    """
    Draws the dividing lines between each square on the player's board and the computer's board

    Returns
    -------
    None.

    """
    for i in range(0,500,50):
        for j in range(0,500,50):
            pygame.draw.rect(screen , (255,255,255) , (i,j,50,50),1)
            pygame.draw.rect(screen, (255,255,255) , (i + 600,j,50,50),1)

def main():  
    """
    Runs the main game loop. Monitors mouseclick events to play battleship

    Returns
    -------
    The winner of the game

    """
    global turn
    comp_left = 17
    running = True
    winner = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx , my = pygame.mouse.get_pos()
                x , y = mx // 50, my // 50

                if(x > 9 or player_board[x][y][0] == 1 or player_board[x][y][0] == 2):
                    continue
                if player_board[x][y][1] == True:
                    ### HIT
                    player_board[x][y][0] = 1
                    print('HIT!')
                    comp_left -= 1
                    if(comp_left == 0):
                        running = False
                        winner = 1
                else:
                    ### MISS
                    player_board[x][y][0] = 2
                    print('MISS!')
                guess()
                player_hit = 0
                for i in range(10):
                    for j in range(10):
                        if computer_board[i][j][0] == 1:
                            player_hit += 1
                if(player_hit == 17):
                    winner = 2
                    running = False
                
                    
        populate_board(player_board,0, False)
        populate_board(computer_board,600, True)
                    
        ### DRAW GRIDS ON EACH BOARD
        draw_boards()
        pygame.display.update()
    if(winner == 1):
        print("Congratulations! You won!")
    elif(winner == 2):
        print("Wow! The computer beat you!")



#initalizes the board as blank before ships are placed.
computer_board = [[[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              [[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False],[0,False]],
              ]
player_board =  generate_board()
playersetup()

#data structures for AI
adjacent = []
hitsOnShip = 0

main()

pygame.quit()
    