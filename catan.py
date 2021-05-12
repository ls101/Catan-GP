import numpy as np

# List of resources available to be distributed on the board
RESOURCE_NAMES = ["desert", "brick", "ore", "hay", "wood", "sheep"]
# Create a dictionary of each resource and a corresponding number id
res_dict = dict(zip(RESOURCE_NAMES, np.arange(0, len(RESOURCE_NAMES))))
# List of available ports that can be distributed around the board
PORTS_NAMES = ["3:1", "2brick:1", "2ore:1", "2hay:1", "2wood:1", "2sheep:1"]
# Create a dictionary of each port and a corresponding number id
port_dict = dict(zip(PORTS_NAMES, np.arange(0, len(PORTS_NAMES))))
# Create a dictionary of each dev card and a corresponding number id
DEVELOPMENT_CARD_NAMES = ["knight","victory point", "road building", "year of plenty",  "monopoly"]
dev_dict = dict(zip(DEVELOPMENT_CARD_NAMES,np.arange(0, len(DEVELOPMENT_CARD_NAMES))))

class CatanBoard:
    # Initialize the Catan Board with all the options for resources, numbers to be rolled,
    # settlements/roads, port options
    def __init__(self):
        """initiates CatanBoard()/self according to catan rules:

        ################################ Insert/Modify Comments HERE ##################################

        Do not forget to ensure 6 and 8 are not next to each other: no 6-6 no 6-8 no 8-8
        """
        ################################ Insert/Modify CODE HERE ##################################
        # Array of each resource id number repeated the amount of times that the resource is available on the board
        # This will be used to distribute the resources into slots on the board
        self.board_resources = np.array(
            [res_dict["desert"]] + [res_dict["brick"]] * 3 + [res_dict["ore"]] * 3 + [res_dict["hay"]] * 4 + [
                res_dict["wood"]] * 4 + [res_dict["sheep"]] * 4)
        # Shuffle the resource array for randomized distribution
        np.random.shuffle(self.board_resources)
        # number associated with the desert and 0 can not actually be rolled
        self.roll_numbers = np.array([0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12])
        # shuffle number options
        np.random.shuffle(self.roll_numbers)
        # Array of the port ids, amount of times each port is available -
        self.ports = np.array(
            [port_dict["3:1"]] * 4 + [port_dict["2brick:1"]] + [port_dict["2ore:1"]] + [port_dict["2hay:1"]] +
            [port_dict["2wood:1"]] + [port_dict["2sheep:1"]])
        # shuffle the ports for randomized distribution
        np.random.shuffle(self.ports)
        # Number_of_tiles represents the slots on the board available to receive a resource and number
        # This number is the same length as the available resources
        self.number_of_tiles = len(self.board_resources)
        # Settlements and roads need to be tracked.
        self.settlements = np.array([0] * (30 + 18 + 6))
        self.roads = np.array([0] * (12 * 5 + 6 + 6))

        # Zero_tile_nr will represent where the 0 number exists
        zero_tile_nr = np.where(self.roll_numbers == 0)
        # Desert_tile_nr will represent where the desert resource exists
        desert_tile_nr = np.where(self.board_resources == res_dict["desert"])
        # Robber will keep track of where the robber is and it starts in the desert
        self.robber = desert_tile_nr
        # as the desert tile and replace whatever was already in the desert tile into the empty zero tile
        self.roll_numbers[zero_tile_nr], self.roll_numbers[desert_tile_nr] = (self.roll_numbers[desert_tile_nr],
                                                                              self.roll_numbers[zero_tile_nr])
        # bank resources  "brick", "ore", "hay", "wood", "sheep"
        self.bank = np.array([19,19,19,19])
        # player_points player0, player1, player2, player3
        self.player_points = [0,0,0,0]
        # longest road player_number initialisation with -1
        self.longest_road = -1
        # longest largest_army player_number initialisation with -1
        self.largest_army = -1
        # devcards according to dev_dict dictionary
        self.bank_devcards = np.array([14*[dev_dict["knight"]] + 5*[dev_dict["victory point"]] + 2*[dev_dict["road building"]] + 2*[dev_dict["year of plenty"]] + 2*[dev_dict["monopoly"]]])
        np.random.shuffle(self.bank_devcards)
        # played open knight cards for each player
        self.open_knights = [0,0,0,0]
        # hidden unplayed dev cards for each player
        # as 2d materix  dev_dict x  player_nr
        self.hidden_dev_cards = np.array([[0]*5]*4)
        # how many dev cards were just bought this turn and can not be played
        # as 2d matrix dev_dict x  player_nr
        self.new_hidden_dev_card = np.array([[0]*5]*4)

    # String output for printing the board
    def __str__(self):
        """
        ################################ Insert/Modify Comments HERE ##################################

        output -- str
        """
        ################################ Insert/Modify CODE HERE ##################################
        out = "\n"
        # Port pointer starts at zero and will be incremented as ports are used
        port_nr = 0
        # For each slot in the board - add the resource and roll_number at the corresponding index
        for tile_nr in range(self.number_of_tiles):
            out += RESOURCE_NAMES[self.board_resources[tile_nr]] + "-" + str(self.roll_numbers[tile_nr]) + " "
            # if the current tile is next to a port - add in the port
            if tile_nr in [2, 6, 11, 15, 18]:
                out += " " + PORTS_NAMES[self.ports[port_nr]] + "\n"
                # if the tile is not at the end of the board - add in a second port on the next line
                if tile_nr < 18:
                    out += PORTS_NAMES[self.ports[port_nr + 1]] + " "
                # Increment the port pointer by 2
                port_nr += 2
        """ Return the output string with all the resources, numbers, and ports to be printed when needed.
        The robber should be added to this output to keep track of where it is.
        Also, I think the output could use better formatting to differentiate between ports and resources and to 
        be easier to look at. """
        return out

    def start_settelment_first(self, player_nr, settle_position, road_position):
        """changes CatanBoard()/self if possible according to the rules of
        building the first starting settelment with an road

        ################################ Insert/Modify Comments HERE ##################################
        buy_settlement arguments:
        self -- CatanBoard()
        player_nr -- integer 0-3
        settle_position -- integer 0-54
        road_position -- integer 0-71
        """
        ################################ Insert/Modify CODE HERE ##################################

    def start_settelment_second(self, player_nr, settle_position, road_position):

        """changes CatanBoard()/self if possible according to the rules of
         building the first starting settelment with an road
        ################################ Insert/Modify Comments HERE ##################################
        buy_settlement arguments:
        self -- CatanBoard()
        player_nr -- integer 0-3
        settle_position -- integer 0-54
        road_position -- integer 0-71
        """
        ################################ Insert/Modify CODE HERE ##################################

    def check_points(self):
        """checks if somebody won the game (reached 10 points) and returns the winner or one of the point leaders

        ################################ Insert/Modify Comments HERE ##################################
        output --

        game_end (logical)
        winner (integer 0-3)
        """
        ################################ Insert/Modify CODE HERE #################################
        game_end, winner = False, 0
        return game_end, winner

    def buy_settlement(self, player_nr, position):
        """changes CatanBoard()/self if possible according to the rules of building a settelment:

        ################################ Insert/Modify Comments HERE ##################################

        buy_settlement arguments:
        self -- CatanBoard()
        player_nr -- integer 0-3
        position -- integer 0-53

        """
        ################################ Insert/Modify CODE HERE ##################################

    def buy_city(self, player_nr, position):
        """changes CatanBoard()/self if possible according to the rules of building a city:

        ################################ Insert/Modify Comments HERE ##################################

        buy_city arguments:
        self -- CatanBoard()
        player_nr -- integer 0-3
        position -- integer 0-53
        """
        ################################ Insert/Modify CODE HERE ##################################

    def buy_road(self, player_nr, position):
        """changes CatanBoard()/self if possible according to the rules of building a road:

        ################################ Insert/Modify Comments HERE ##################################

        buy_road arguments:
        self -- CatanBoard()
        player_nr -- integer 0-3
        position -- integer 0-71

        """
        ################################ Insert/Modify CODE HERE ##################################

    def buy_dev_card(self, player_nr):
        """changes CatanBoard()/self if possible according to the rules of buying a development card card:

        ################################ Insert/Modify Comments HERE ##################################

        buy_dev_card input arguments:
        self -- CatanBoard()
        player_nr -- integer 0-3

        """
        ################################ Insert/Modify CODE HERE ##################################

    def roll_dice(self, player_nr):
        """changes CatanBoard()/self if possible according to the rules of rolling dice in catan:

        ################################ Insert/Modify Comments HERE ##################################

        """
        # output roll_numer of dice
        ################################ Insert/Modify CODE HERE ##################################
        roll_number = 7
        return 7

    def discard_half(self, player_nr, resourses):
        """changes CatanBoard()/self if possible according to the rules of discarding cards if 7 rolled

        ################################ Insert/Modify Comments HERE ##################################
        discard_half input arguments:
        self -- CatanBoard()
        player_nr -- integer 0-3
        resourses -- np.array([brick, ore, hay, wood, sheep])
                brick -- integer 0-19
                ore -- integer 0-19
                hay -- integer 0-19
                wood --integer 0-19
                sheep --integer 0-19

        """
        ################################ Insert/Modify CODE HERE ##################################

    def steal_card(self, player_nr, position, target_player_nr):
        """changes CatanBoard()/self if possible according to the rules of discarding cards if 7 rolled

        ################################ Insert/Modify Comments HERE ##################################
        steal_card input arguments:
        self -- CatanBoard()
        player_nr -- integer 0-3
        position -- integer 0 - self.number_of_tiles-1
        target_player_nr -- integer 0-3
        """
        ################################ Insert/Modify CODE HERE ##################################

    def play_knight(self, player_nr, position, target_player_nr):
        """changes CatanBoard()/self if possible according to the rules knight playing in catan:

        ################################ Insert/Modify Comments HERE ##################################
        self -- CatanBoard()
        player_nr -- integer 0-3
        position -- integer 0 - self.number_of_tiles-1
        target_player_nr -- integer 0-3

        """
        ################################ Insert/Modify CODE HERE ##################################

    def play_roads(self, player_nr, position1, position2):
        """changes CatanBoard()/self if possible according to the rules of playing the roadsbuilding dev card :

        ################################ Insert/Modify Comments HERE ##################################
        self -- CatanBoard()
        player_nr -- integer 0-3
        position1 -- integer 0-71
        position2 -- integer 0-71
        """
        ################################ Insert/Modify CODE HERE ##################################

    def play_plenty(self, player_nr, resource1, resource2):
        """changes CatanBoard()/self if possible according to the rules of playing the years of plenty dev card :

        ################################ Insert/Modify Comments HERE ##################################
        self -- CatanBoard()
        player_nr -- integer 0-3
        resource1 -- integer 1-5
        resource1 -- integer 1-5
        """
        ################################ Insert/Modify CODE HERE ##################################

    def play_mono(self, player_nr, resource):
        """changes CatanBoard()/self if possible according to the rules of playing monopoly dev card :

        ################################ Insert/Modify Comments HERE ##################################
        self -- CatanBoard()
        player_nr -- integer 0-3
        resource -- integer 1-5

        """
        ################################ Insert/Modify CODE HERE ##################################

    def trade_bank(self, player_nr, resource_own, resource_bank):
        """changes CatanBoard()/self if possible according to the rules bank trading including ports:

        ################################ Insert/Modify Comments HERE ##################################
        self -- CatanBoard()
        player_nr -- integer 0-3
        resource_own -- integer 1-5
        resource_bank -- integer 1-5
        """
        ################################ Insert/Modify CODE HERE ##################################

    def trade_offer(self, player_nr, resources_own, target_player_nr, resources_target, answer_target=False):
        """changes CatanBoard()/self if possible according to the rules bank trading including ports:

        ################################ Insert/Modify Comments HERE ##################################
        self -- CatanBoard()
        player_nr -- integer 0-3
        resources_own -- np.array([brick, ore, hay, wood, sheep])
        target_player_nr -- integer 0-3
        resources_target -- np.array([brick, ore, hay, wood, sheep])
                brick -- integer 0-19
                ore -- integer 0-19
                hay -- integer 0-19
                wood --integer 0-19
                sheep --integer 0-19
        answer_target -- TRUE for yes or FALSE for no
        """
        ################################ Insert/Modify CODE HERE ##################################


if __name__ == '__main__':
    """
     ################################ Insert/Modify Comments HERE ##################################
     """

    ################################ Insert/Modify CODE HERE ##################################
    b = CatanBoard()
    print(b)
    print('Debug complete')
