import pygame as py
import numpy as np
import sys
import math
import random
from tkinter import *

# Constant variables to assign colours to be used in the GUI
BLACK = '#363636'
WHITE = '#ffffff'

class Game():
  def __init__(self, game_over):

    # Defines the main sizes of the game
    self._r_count = 6
    self._c_count = 7
    self._square = 80
    self._radius = int((self._square // 2) - ((self._square * 0.12) // 1))

    # Defines the colours of used to display the brd
    self._brd_colour = (0,0,255)
    self._brd_outline = (70,70,255)
    self._green = (0,255,0)
    self._black = (0,0,0)

    # Player 1 piece colour
    self._player_1_colour = (255,0,0)
    self._outline_player_1 = (136,0,27)

    # Player 2 piece colour
    self._player_2_colour = (255,255,0)
    self._outline_player_2 = (255,202,24)

    # Initiates the background brd
    self._brd = self.Createbrd()

    # Creates a counter that checks for a draw
    self._full_counter = 0

    # Defines the numbers for the pieces (to be used in arrays)
    self._empty = 0
    self.r_piece = 1
    self.y_piece = 2
    self._piece = 0 # Defined as the default value to be used later

    # Defines the size of the brd
    self._width = self._c_count * self._square
    self._height = (self._r_count+1) * self._square
    self._size = self._width, self._height

    # Sets up the font for later use
    self._font = py.font.Font('freesansbold.ttf', 70)

    # Names the game window 'Connect 4'
    py.display.set_caption('Connect 4')

    # Used in the main game loop
    self._game_over = game_over
    self._turn = random.randint(0,1)

  def StartGameWindow(self, brd):
    # Initiates the graphical interface of the brd
    self._game_window = py.display.set_mode(self._size)
    self.Drawbrd(brd)
    # self.Printbrd(brd)
    py.display.update()

  def Drawbrd(self, brd):
    brd = np.flip(brd, 0)
    for self._col in range(self._c_count):
      for self._row in range(self._r_count):
        # Draws the board for the user to see in pygame
        py.draw.rect(
          self._game_window,
          self._brd_colour,
          (self._col * self._square,
          self._row * self._square + self._square,
          self._square,
          self._square)
        )

        # Draws a circle outline
        py.draw.circle(
          self._game_window,
          self._brd_outline,
          (self._col * self._square + self._square // 2, self._row * self._square + self._square + self._square // 2),
          (self._radius + 3)
        )

        # Checks if the space is blank
        if brd[self._row][self._col] == 0:
          # Draws the empty spaces
          py.draw.circle(self._game_window, self._black, (self._col * self._square + self._square // 2,
            self._row * self._square + self._square + self._square // 2),
            self._radius
          )

        # Checks if the space has a player 1 piece
        elif brd[self._row][self._col] == 1:
          # Draws player 1 piece
          py.draw.circle(self._game_window, self._outline_player_1, (self._col * self._square + self._square // 2, self._row * self._square + self._square + self._square // 2), self._radius - 1)
          py.draw.circle(self._game_window, self._player_1_colour, (self._col * self._square + self._square // 2, self._row * self._square + self._square + self._square // 2), self._radius - 5)

        # Checks if the space has a player 2 piece
        elif brd[self._row][self._col] == 2:
          # Draws player 2 piece
          py.draw.circle(self._game_window, self._outline_player_2, (self._col * self._square + self._square // 2, self._row * self._square + self._square + self._square // 2), self._radius - 1)
          py.draw.circle(self._game_window, self._player_2_colour, (self._col * self._square + self._square // 2, self._row * self._square + self._square + self._square // 2), self._radius - 5)
    py.display.update()

  def Printbrd(self, brd):
    print(np.flip(brd, 0))

  def Createbrd(self):
    brd = np.zeros((self._r_count,self._c_count))
    return brd

  def CreateDrawbrd(self):
    return [[2,2,1,1,2,1,2],[2,2,1,1,2,2,1],[1,1,2,2,1,1,2],[2,2,1,1,1,2,1],[1,1,1,2,1,1,1],[2,2,2,1,2,2,0]]

  def AlternateTurns(self):
    self._turn += 1
    self._turn = self._turn % 2
    return self._turn

  def DropPiece(self, piece, brd, row, column):
    brd[row][column] = piece
    return brd

  def IsValidLocation(self, brd, column):
    return brd[self._r_count-1][column] == self._empty
  
  def IsDraw(self, brd):
    self._full_counter = 0
    for self._col in range(self._c_count):
      if brd[self._r_count-1][self._col] != self._empty:
        self._full_counter += 1
    if self._full_counter == self._c_count:
      return True

  def GetNextOpenRow(self, brd, column):
    for self._row in range(self._r_count):
      if brd[self._row][column] == self._empty:
        return self._row

  def WinningMove(self, piece, brd):
    # Checks for a horizontal win
    for self._col in range(self._c_count-3):
      for self._row in range(self._r_count):
        if brd[self._row][self._col] == piece and brd[self._row][self._col+1] == piece and brd[self._row][self._col+2] == piece and brd[self._row][self._col+3] == piece:
          return True

    # Checks for a vertical win
    for self._col in range(self._c_count):
      for self._row in range(self._r_count-3):
        if brd[self._row][self._col] == piece and brd[self._row+1][self._col] == piece and brd[self._row+2][self._col] == piece and brd[self._row+3][self._col] == piece:
          return True

    # Checks for a positivly sloped diagonal
    for self._col in range(self._c_count-3):
      for self._row in range(self._r_count-3):
        if brd[self._row][self._col] == piece and brd[self._row+1][self._col+1] == piece and brd[self._row+2][self._col+2] == piece and brd[self._row+3][self._col+3] == piece:
          return True

    # Checks for a negativly sloped diagonal
    for self._col in range(self._c_count-3):
      for self._row in range(3, self._r_count):
        if brd[self._row][self._col] == piece and brd[self._row-1][self._col+1] == piece and brd[self._row-2][self._col+2] == piece and brd[self._row-3][self._col+3] == piece:
          return True

class Local(Game):
  def __init__(self, game_over):
    super().__init__(game_over)
    self.__player_1 = 0
    self.__player_2 = 1

  def Local(self):
    self.StartGameWindow(self._brd)

    # Game loop
    while not self._game_over:
      if self.IsDraw(self._brd):
        self._who_wins = 'Draw!'
        self._game_over = True
        break
        
      for event in py.event.get():
        if event.type == py.QUIT:
          sys.exit()

        if event.type == py.MOUSEMOTION:
          # Makes sure that only one circle is shown
          py.draw.rect(self._game_window, self._black, (0,0,self._width, self._square))

          # Draws the circle to show what player and where it will drop
          self._pos_x = event.pos[0]
          if self._turn == self.__player_1:
            py.draw.circle(self._game_window, self._outline_player_1, (self._pos_x, self._square // 2), self._radius - 1)
            py.draw.circle(self._game_window, self._player_1_colour, (self._pos_x, self._square // 2), self._radius - 5)
          elif self._turn == self.__player_2:
            py.draw.circle(self._game_window, self._outline_player_2, (self._pos_x, self._square // 2), self._radius - 1)
            py.draw.circle(self._game_window, self._player_2_colour, (self._pos_x, self._square // 2), self._radius - 5)
          py.display.update()

        if event.type == py.MOUSEBUTTONDOWN:
          # Gets player 1 input
          if self._turn == self.__player_1:

            self._pos_x = event.pos[0]
            self._column = int(math.floor(self._pos_x / self._square))

            if self.IsValidLocation(self._brd, self._column):
              self._row = self.GetNextOpenRow(self._brd, self._column)
              self._brd = self.DropPiece(self.r_piece, self._brd, self._row, self._column)
              
              # Updates the piece at the top of the screen as when the mouse stays static, the colour doesnt change
              py.draw.circle(self._game_window, self._outline_player_2, (self._pos_x, self._square // 2), self._radius - 1)
              py.draw.circle(self._game_window, self._player_2_colour, (self._pos_x, self._square // 2), self._radius - 5)
              py.display.update()
            else:
              self._turn -= 1

            self.Drawbrd(self._brd)

            if self.WinningMove(self.r_piece, self._brd):
              self._who_wins = 'Red Wins!'
              self._game_over = True

          # Gets player 2 input
          elif self._turn == self.__player_2:

            self._pos_x = event.pos[0]
            self._column = int(math.floor(self._pos_x / self._square))
            
            if self.IsValidLocation(self._brd, self._column):
              self._row = self.GetNextOpenRow(self._brd, self._column)
              self._brd = self.DropPiece(self.y_piece, self._brd, self._row, self._column)

              # Updates the piece at the top of the screen as when the mouse stays static, the colour doesnt change
              py.draw.circle(self._game_window, self._outline_player_1, (self._pos_x, self._square // 2), self._radius - 1)
              py.draw.circle(self._game_window, self._player_1_colour, (self._pos_x, self._square // 2), self._radius - 5)
              py.display.update()
            else:
              self._turn -= 1

            self.Drawbrd(self._brd)

            if self.WinningMove(self.y_piece, self._brd):
              self._who_wins = 'Yellow Wins!'
              self._game_over = True


          self._turn = self.AlternateTurns()

    py.display.update()
    py.time.delay(1000)
    py.display.quit()
    win_dow = WinDisplay(self._who_wins)

class AI(Game):
  def __init__(self, game_over, difficulty):
    super().__init__(game_over)
    self.__player = 0
    self.__ai = 1
    self._empty = 0

    # Definition of score to be used in heuristic
    self._score = 0

    # Defines the window to asses for the AI
    self._window_length = 4

    self.__level = difficulty

    self.StartGameWindow(self._brd)

  def AI(self):
    while not self._game_over:
      if self.IsDraw(self._brd):
        self._who_wins = 'Draw!'
        self._game_over = True
        break

      for event in py.event.get():
        if event.type == py.QUIT:
          sys.exit()

        if event.type == py.MOUSEMOTION:
          # Makes sure that only one circle is shown
          py.draw.rect(self._game_window, self._black, (0,0,self._width, self._square))

          # Draws the circle to show what player and where it will drop
          self._pos_x = event.pos[0]
          if self._turn == self.__player:
            py.draw.circle(self._game_window, self._outline_player_1, (self._pos_x, self._square // 2), self._radius - 1)
            py.draw.circle(self._game_window, self._player_1_colour, (self._pos_x, self._square // 2), self._radius - 5)
          py.display.update()

        if event.type == py.MOUSEBUTTONDOWN:
          # Gets player 1 input
          if self._turn == self.__player and not self._game_over:

            self._pos_x = event.pos[0]
            self._column = int(math.floor(self._pos_x / self._square))

            if self.IsValidLocation(self._brd, self._column):
              self._row = self.GetNextOpenRow(self._brd, self._column)
              self._brd = self.DropPiece(self.r_piece, self._brd, self._row, self._column)
              self._turn = self.AlternateTurns()
            else:
              self._turn -= 1

            self.Drawbrd(self._brd)

            # self._piece = self.r_piece
            if self.WinningMove(self.r_piece, self._brd):
              self._who_wins = 'Red Wins!'
              self._game_over = True

        # Gets ai column
        if self._turn == self.__ai and not self._game_over:

          # Random AI loader
          if self.__level == 0:
            self._column = self.__RandomColumn()
          
          # Basic AI loader
          elif self.__level == 1:
            self._column, self._minimax_score = self.MiniMax(self._brd, 2, -math.inf, math.inf, True)

          # Medium AI loader
          elif self.__level == 2:
            self._column, self._minimax_score = self.MiniMax(self._brd, 4, -math.inf, math.inf, True)

          # Hard AI loader
          elif self.__level == 3:
            self._column, self._minimax_score = self.MiniMax(self._brd, 6, -math.inf, math.inf, True)


          if self.IsValidLocation(self._brd, self._column):
            self._row = self.GetNextOpenRow(self._brd, self._column)
            self.DropPiece(self.y_piece, self._brd, self._row, self._column)
            self._turn = self.AlternateTurns()

          self.Drawbrd(self._brd)

          if self.WinningMove(self.y_piece, self._brd):
            self._who_wins = 'Yellow Wins!'
            self._game_over = True

    py.display.update()
    py.time.delay(1000)
    py.display.quit()
    win_dow = WinDisplay(self._who_wins)

  def __RandomColumn(self):
    return random.randint(0, self._c_count-1)

  def GetValidLocations(self, brd):
    valid_locations = []
    for col in range(self._c_count):
      if self.IsValidLocation(brd, col):
        valid_locations.append(col)
    return valid_locations

  def IsTerminalNode(self, brd):
      return self.WinningMove(self.r_piece, brd) or self.WinningMove(self.y_piece, brd) or len(self.GetValidLocations(brd)) == 0

  def EvaluateWindow(self, window, piece):
    # This is the analysis of the 'window' and scores each one accordingly (heiuristic)
    score = 0

    # Sets the opposite piece to yellow
    opp = self.y_piece if piece == self.y_piece else self.y_piece

    # Checks for a possible 4 in a row
    if window.count(piece) == 4:
      score += 100

    # Checks for a possible 3 in a row
    elif window.count(piece) == 3 and window.count(self._empty) == 1:
      score += 5

    # Checks for a possible 2 in a row
    elif window.count(piece) == 2 and window.count(self._empty) == 2:
      score += 2

    # Checks if the opponent can get a 3 in a row and subtracts the score
    if window.count(opp) == 3 and window.count(self._empty) == 1:
      score -= 7

    elif window.count(opp) == 4:
      score -= 30

    return score

  def ScorePosition(self, brd, piece):
    score = 0

    # Score the center column
    center_c = [int(i) for i in list(brd[:, brd.shape[1] // 2])]
    count = center_c.count(piece)
    score += count * 3

    # Score horizontal values
    for r in range(brd.shape[0]):
      for c in range(brd.shape[1] - self._window_length + 1):
        window = [int(i) for i in list(brd[r, c:c + self._window_length])]
        score += self.EvaluateWindow(window, piece)

    # Score vertical values
    for c in range(brd.shape[1]):
      for r in range(brd.shape[0] - self._window_length + 1):
        window = [int(i) for i in list(brd[r:r + self._window_length, c])]
        score += self.EvaluateWindow(window, piece)

    # Score positively sloped diagonal
    for r in range(brd.shape[0] - self._window_length + 1):
      for c in range(brd.shape[1] - self._window_length + 1):
        window = [brd[r+i][c+i] for i in range(self._window_length)]
        score += self.EvaluateWindow(window, piece)

    # Score negatively sloped diagonal
    for r in range(brd.shape[0] - self._window_length + 1):
      for c in range(brd.shape[1] - self._window_length + 1):
        window = [brd[r+self._window_length-1-i][c+i] for i in range(self._window_length)]
        score += self.EvaluateWindow(window, piece)

    return score

  def MiniMax(self, brd, depth, alpha, beta, maximising):
    valid_locations = self.GetValidLocations(brd)
    is_terminal = self.IsTerminalNode(brd)
      
    if depth == 0 or is_terminal:
      if is_terminal:
        if self.WinningMove(self.y_piece, brd):
          return (None, 99999999999)
        elif self.WinningMove(self.r_piece, brd):
          return (None, -99999999999)
        else:
          return (None, 0)
      else:
        return (None, self.ScorePosition(brd, self.y_piece))
      
    if maximising:
      value = -math.inf
      column = random.choice(valid_locations)
      for col in valid_locations:
        row = self.GetNextOpenRow(brd, col)
        brd_copy = brd.copy()
        self.DropPiece(self.y_piece, brd_copy, row, col)
        new_score = self.MiniMax(brd_copy, depth-1, alpha, beta, False)[1]
        if new_score > value:
          value = new_score
          column = col
          alpha = max(alpha, value)
        if alpha >= beta:
          break
      return column, value
      
    else:
      value = math.inf
      column = random.choice(valid_locations)
      for col in valid_locations:
        row = self.GetNextOpenRow(brd, col)
        brd_copy = brd.copy()
        self.DropPiece(self.r_piece, brd_copy, row, col)
        new_score = self.MiniMax(brd_copy, depth-1, alpha, beta, True)[1]
        if new_score < value:
          value = new_score
          column = col
          beta = min(beta, value)
        if alpha >= beta:
          break
      return column, value

class Menu():
  def __init__(self):
    self.__menu = Tk()
    self.__menu.title("Menu")
    self.__menu.config(bg= BLACK)

    self.Greeting()
    self.AiButton()
    self.LocalButton()
    self.ShowRulesButton()
    self.QuitButton()
    self.__menu.mainloop()

  def CloseWindow(self):
    self.__menu.destroy()

  def Greeting(self):
    greeting = Label(
      text= 'ツ Connect 4 ツ',
      foreground= WHITE,
      background= BLACK,
      width= 20,
      heigh= 2,
      font= ('freesansbold.ttf', 20)
    )
    greeting.pack()

  def AiButton(self):
    Button(
      text= 'Play agaist AI',
      foreground= WHITE,
      background= BLACK,
      command= lambda:self.LoadAI(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

  def LoadAI(self):
    self.CloseWindow()
    ai_menu = AiMenu()

  def LocalButton(self):
    Button(
      text= 'Local 1v1',
      foreground= WHITE,
      background= BLACK,
      command= lambda:self.LoadLocal(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

  def LoadLocal(self):
    self.CloseWindow()
    game = Local(False)
    game.Local()

  def ShowRulesButton(self):
    Button(
      text= 'Show Game Rules',
      foreground= WHITE,
      background= BLACK,
      command= lambda:self.ShowRules(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

  def ShowRules(self):
    self.CloseWindow()
    rules = Rules()

  def QuitButton(self):
    Button(
      text= 'Quit',
      foreground= WHITE,
      background= BLACK,
      command= lambda:self.CloseWindow(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

class WinDisplay():
  def __init__(self, winner):
    self.__win_dow = Tk()
    self.__win_dow.title(winner)
    self.__win_dow.config(bg= BLACK)

    self.WinMessage(winner)
    self.ReturnButton()
    self.QuitButton()
    self.__win_dow.mainloop()

  def CloseWindow(self):
    self.__win_dow.destroy()

  def WinMessage(self, winner):
    Label(
      text= winner,
      foreground= '#49fc03',
      background= BLACK,
      width= 15,
      heigh= 1,
      font= ('freesansbold.ttf', 30, 'bold italic')
    ).pack(padx= 7, pady= 5)

  def ReturnButton(self):
    Button(
      text= 'Return',
      foreground= WHITE,
      background= BLACK,
      command= lambda:self.Return(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

  def QuitButton(self):
    Button(
      text= 'Quit',
      foreground= WHITE,
      background= BLACK,
      command= lambda:self.CloseWindow(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

  def Return(self):
    self.CloseWindow()
    menu = Menu()

  def PlayAgainButton(self):
    pass # adds a button to select to play the same game mode again

  def PlayAgain(self):
    pass

class Rules():
  def __init__(self):
    self.__rules = Tk()
    self.__rules.title('Rules')
    self.__rules.config(bg=BLACK)
    self.ReturnButton()
    self.Greeting()
    self.ShowRules()
    self.__rules.mainloop()

  def CloseWindow(self):
    self.__rules.destroy()

  def Greeting(self):
    Label(
      text= 'Connect 4 Rules:',
      foreground= WHITE,
      background= BLACK,
      width= 20,
      heigh= 1,
      font= ('freesansbold.ttf', 21)
    ).pack(padx= 7, pady= 5)

  def ShowRules(self):
    self.__rulebox = Text(
      foreground= WHITE,
      background= BLACK,
      wrap= WORD,
      font= ('freesansbold.ttf', 16),
      width= 29,
      heigh= 16
    )
    self.__rulebox.pack(padx= 7, pady= 5)
    self.InsertRules()

  def InsertRules(self):
    self.__rulebox.insert(END, "1. Click the screen in the column where you want to place you piece.\n\n2. A piece can only be dropped where there is space in the grid, once there are 6 pieces in a column, no more pieces can be dropped in that column.\n\n3. Attempt to place 4 pieces in a row, either vertically, horizontally or diagonally.\n\n4. Once a winning move has been accomplished, the game will end and can be restarted via the menu.")

  def ReturnButton(self):
    Button(
      text= 'Return',
      foreground= WHITE,
      background= BLACK,
      command= lambda:self.Return(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

  def Return(self):
    self.CloseWindow()
    menu = Menu()

class AiMenu():
  def __init__(self):
    self.__ai_menu = Tk()
    self.__ai_menu.title('Menu')
    self.__ai_menu.config(bg= BLACK)

    self.Greeting()
    self.EasyButton()
    self.MediumButton()
    self.Hardbutton()
    self.ReturnButton()
    self.__ai_menu.mainloop()

  def CloseWindow(self):
    self.__ai_menu.destroy()

  def Greeting(self):
    Label(
      text= 'Please select the AI dificulty:',
      foreground= WHITE,
      background= BLACK,
      width= 50,
      heigh= 4
    ).pack(padx= 7, pady=5)

  def EasyButton(self):
    Button(
      text= 'Easy Mode',
      foreground= WHITE,
      background= 'green',
      command= lambda:self.LoadEasy(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

  def LoadEasy(self):
    self.CloseWindow()
    game = AI(False, 1)
    game.AI()

  def MediumButton(self):
    Button(
      text= 'Medium Mode',
      foreground= WHITE,
      background= 'orange',
      command= lambda:self.LoadMedium(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

  def LoadMedium(self):
    self.CloseWindow()
    game = AI(False, 2)
    game.AI()

  def Hardbutton(self):
    Button(
      text= 'Hard Mode',
      foreground= WHITE,
      background= 'red',
      command= lambda:self.LoadHard(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

  def LoadHard(self):
    self.CloseWindow()
    game = AI(False, 3)
    game.AI()

  def ReturnButton(self):
    Button(
      text= 'Return',
      foreground= WHITE,
      background= BLACK,
      command= lambda:self.Return(),
      width= 50,
      height= 4
    ).pack(padx= 7, pady=5)

  def Return(self):
    self.CloseWindow()
    menu = Menu()

if __name__ == "__main__":
  # Initiates pygame
  py.init()

  # Loads the game menu
  menu = Menu()

  # Exits the pygame module and closes the game safely
  py.quit()