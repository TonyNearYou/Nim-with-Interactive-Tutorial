import random

# =====================================================================
# DATA & STATE MODEL
# =====================================================================
class nimPile:
    '''Records Nim pile, modifications, and what the optimal move is'''
    def __init__(self, pilesize):
        '''Constructor, takes one int parameter, constructs object with one instance variable of the parameter'''
        self.pilesize = int(pilesize)

    def getPileSize(self):
        '''no parameters, returns the current pile size'''
        return self.pilesize

    def validmove(self, stone):
        '''takes one int parameter, returns bool based on where or not the move is valid'''
        return (stone > 0 and stone <= self.pilesize / 2) or stone == 1 

    def removeStone(self, stone):
        '''takes one int parameter, removes stone from pile'''
        self.pilesize -= stone

    def optimalMove(self):
        '''takes no parameters, returns the optimal amount of stones to take, -1 if there is no such move'''
        i = 0
        #For cases where you can only take one from a pile of 1
        if self.pilesize == 1:
            return 1
        #Goes through losing position equation, finds optimal based on that
        while True:
            optimal = 3 * 2**i - 1
            if optimal > self.pilesize:
                i-= 1
                break
            #For cases where the current pile is a losing position
            if optimal == self.pilesize:
                return -1
            i+=1
        #Optimal amount of stones to take
        return self.pilesize - (3 * 2**i - 1)

    
# =====================================================================
# GAME CONTROL & INTERFACE DRIVER
# =====================================================================
class nimDriver:
    '''Starts and controls game of Nim'''
    def __init__(self):
        '''constructor, takes no parameters, prompts user for what version of nim they want to play and executes accordingly'''
        #Initialize instance variables
        self.pile = 0
        self.isplayerturn = 0
        #used to end program
        self.endProgram = False

    def mainmenu(self):
        '''Takes no parameters, Prompts user for choice and calls appropriate functions'''
        #Prompt user for what they want to play, throughs error message and prompts again if given invalid input
        option = input("Hello, please choose from the menu:\n 1. Tutorial\n 2. Regular Nim\n 3. Quit\n")
        while option != "1" and option != "2" and option != "3":
            option = input("Please type a valid choice ('1', '2', or '3'): ")

        #Play Tutorial
        if option == "1":
            self.playTutorial()
            
        #Play regular Nim
        elif option == "2":
            check = input("Would you like to enter how many stones to play with (y / n): ")
            while check != "y" and check != "n":
                check = input("Invalid input, enter 'y' or 'n':")

            if check == "y":
                check = input("Enter the amount of stones (greater than 0): ")
                while not check.isdigit() or int(check) <= 0:
                    check = input("Invalid input, please enter a integar greater than 0: ")
                self.pile = nimPile(check)

            else:
                self.pile = nimPile(random.randint(10,75))
                                
            firstTurn = input("Would you like to go first? (y / n ): ")
            while firstTurn != "y" and firstTurn != "n":
                firstTurn = input("Invalid input, enter 'y' or 'n':")
            self.isplayerturn = 0

            if firstTurn == "y":
                self.isplayerturn = True

            else:
                self.isplayerturn = False
            self.playGame()
            print()

        #Quit
        else:
            self.endProgram = True

        
    def programDone(self):
        '''Takes no parameters, returns boolean based on whether the user has quit or not'''
        return self.endProgram
    
    def playGame(self):
        '''This function takes no parameters, Plays a game of nim and returns none'''
        #loop to play game
        while self.pile.getPileSize() > 0:
            self.playTurn()

        #if and else statements to decide winner
        if self.isplayerturn:
            print("Computer won!")
        else:
            print("Player won!")
    
    def playTurn(self):
        '''Takes no parameters, promps and displays a single turn of nim'''
        #call to display
        self.displayGame()
        #initialize takestone
        takestone = 0
        #gets amount to take stone depending on who's turn it is, and modifies pile
        if self.isplayerturn:
            takestone = self.validinput()
            self.pile.removeStone(takestone)
            print("You have taken", takestone, "stone(s).")
        else:
            takestone = self.pile.optimalMove()
            if takestone == -1:
                takestone = random.randint(1,int(self.pile.getPileSize()) // 2)
            self.pile.removeStone(takestone)
            print("Computer has taken", takestone, "stones.")
        print()
        #changes turn
        self.isplayerturn = not self.isplayerturn
        

    def playTutorial(self):
        '''This functions takes no parameters, and loads the tutorial for the user to follow'''
        #Introduction
        print("As surprising as it may seem, Nim has a pattern which the computer has used in order to consistently win.")
        print("Though when looking at bigger pile sizes, it is pretty hard to spot, so let's break it down to see it.")
        input("We'll start with the pile size being one on our turn, and we'll work up from there.\nEnter anything to continue: ")
        print()

        #demonstrates position that pile size of one takes
        self.pile = nimPile(1)
        self.isplayerturn = True
        self.displayGame()
        print("Notice how we can take one stone and win here, so we can call this instance a winning position for us.")
        input("Now lets check out what happens when the pile becomes 2.\nEnter anything to continue: ")
        print()

        #same thing for 2, explains why it is a losing position
        self.pile = nimPile(2)
        self.displayGame()
        print("In this case, when we have to take from the pile of 2, we can only take one stone.")
        print("The problem with that, however, is that doing so would give our opponent a pile size of 1 on their turn.")
        print("Since we are forced to give our opponent a winning position, we can call this instance a losing position")
        input("Let us move on a pile size of 3.\nEnter anything to continue: ")
        print()

        #Explains why 3 and 4 are winning positions
        self.pile = nimPile(3)
        self.displayGame()
        print("Notice how here, we can take 1 stone to put our opponent into a losing position")
        print("Since we can put our opponent into a losing position, we can call this one a winning position")
        print("The same is true for a 4 stone, as we can take 2 stones instead to put our opponent into another losing position")
        print("Both of these winning positions allows us to make our opponent lose in the next turn. Lets see if thats true for a pile of 5")
        input("Enter anything to continue: ")
        print()

        #Explains why 5 is a losing position
        self.pile = nimPile(5)
        self.displayGame()
        print("Now here, no matter what we take, we will give our opponenet a winning position.")
        print("Taking one would lead to our opponent having a pile size of 4, and taking 2 would lead to our opponent having a pile size of 3.")
        print("Given those are the only valid moves, we can call this instance a losing position.")
        print("We can repeat this thought process to find that: 2, 5, 11, 23, and 47 are losing positions.")
        print("No matter what we take, it allows our opponent to put us into another losing position until we end up at one assuming they play optimally")

        #Muiltiple choice to let user try to find equation
        choice = input("With this understanding, we now only need to find the pattern in order to get these numbers.\n Please choose from the following options where n is the nth occurance starting at 0:\n a. 2^n + 1\n b. 3^n -1\n c. 3 * 2^n -1\n")
        while choice != "a" and choice != "b" and choice != "c":
            choice = input("Please type a valid choice ('a', 'b', or 'c'): ")
        
        if choice == "c":
            print("Correct! this equation gives us the ability to find the nth losing position")
        else:
            print("Incorrect! :( the correct equation was c : 3 * 2^n - 1")
        print()

        #explanation on how to take optimal amount of stones
        print("\nNow that we now what these losing numbers are, we can now find our optimal move")
        print("For the optimal move, we want to leave our opponent into a losing positionm")
        print("We can find this by finding the highest valued term from this equation that is less than the current pile size")
        print("Then subtracting that from the pile size in order to find out how many stones we need to take in order to do so")

        #Example, promopt user to find optimally amount of stones to take from a randomly generatored pile that is a winning position
        print("Let's try an example:\n")
        self.pile = nimPile(random.randint(24,100))
                            
        while self.pile.optimalMove() == -1:
            self.pile = nimPile(random.randint(24,100))
        self.displayGame()
        print("How many stones should we take to put our opponent in a losing position?")
        stones = self.validinput()
        while stones != self.pile.optimalMove():
            print("Incorrect! Remember, we need to get the pile into a losing position")
            stones = self.validinput()
        #Ending statemnts
        print("\nYou got it! Remember, this strategy only works if you are able to put your opponent into a losing position first.")
        print("Otherwise, they can play optimally as well and there is no way for you to win!")
        print("Hopefully this has given you insights on how we can break down problems to find solutions")
        print("You will be sent back to the menu, try playing against the computer with this newfound knowledge")
        input("Enter anything to continue: ")
        print()
        
        
                
            
    def validinput(self):
        '''Takes no parameters, prompts the user and returns a valid amount of stones to take based on current pile'''
        #upper bound calculation
        upper = str(int(self.pile.getPileSize()) // 2)
        
        #prompt user
        takestone = input("Enter the amount of stones you would like to take from 1 to " + upper + ": ")

        #Loop handling invalid inputs and prompting user for valid inputs
        while not takestone.isdigit() or not self.pile.validmove(int(takestone)):
                #Hard coded case for pile size = 1
                if int(self.pile.getPileSize()) == 1:
                     outString = "Invalid input, please enter 1 (it's the only valid move): "

                #Other occurances
                else:
                    outString = "Invalid input, please enter an integar between 1 and " + upper + ": "

                takestone = input(outString)
        return int(takestone)
        
            
    def displayGame(self):
        '''takes no parameters, displays the current turn'''
        #displays who's turn it currently is
        if self.isplayerturn:
            print("It is the player's turn")
        else:
            print("It is the computer's turn")
        #displays the pile size
        print("The current pile size is " + str(self.pile.getPileSize()) + ".")

# =====================================================================
# EXECUTION
# =====================================================================
#intiliaze variable
sentinal = False
game = nimDriver()
#loop through until user quits
while not sentinal:
    game.mainmenu()
    sentinal = game.programDone()

#final message to user
print("Thank you for playing!")