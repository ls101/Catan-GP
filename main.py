# This is a catan Python script.
import catan
import player
import copy
"""
################################ You ar free to modify and add any comments ##################################

you can and should change and add print statements
it would be also usefull to write log of the game in a file
"""
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# the game is played for maximum 30 rounds (30*4 = 120 turns) to prevent infinite loops
MAXIMUM_ROUNDS = 30

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    def menu():
        print('MENU')
        print('2. Roll the Dice')
        print('3. Buy a settlement')
        print('4. buy a city ')
        print('5. buy a road ')
        print('6. Buy a development card')
        print('8. play a knight ')
        print('9. play a road ')
        print('10.play a plenty')
        print('11. play mono')
        print('12. trade')
        print('13. target ')
        choice=input('Enter Choice: \n')
        try :
            choice=int(choice)
        except:
            ('your choice must be numeric ')
            menu()
        while choice <0 or choice >13:
           choice=input("You must enter a choice between 1 and 13 : \n ")
           try :
               choice=int(choice)
           except:
             ('your choice must be numeric ')
             menu()
    
        return choice

    # build catan board
    board = catan.CatanBoard()

    # insert players
    players = list()
    num_players=int(input("Number of players: \n"))
    
    
    for player_nr in range(1,num_players) :
        players.append(player.CatanPlayer(player_nr))
    
    

    # game set up of the two settelment
    # first settelment with road
    for player_nr in range(1,num_players):
        current_player = players[player_nr]
        board_safety_copy = copy.deepcopy(board.board)
        settle_position, road_position = current_player.start_settelment_first(board_safety_copy)
        board.start_settelment_first(player_nr,settle_position,road_position)


    # second settelment with road
    for player_nr in range(num_players, 0, -1):
        current_player = players[player_nr]
        board_safety_copy = copy.deepcopy(board.board)
        settle_position, road_position = current_player.start_settelment_second(board_safety_copy)
        board.start_settelment_second(players[player_nr], player_nr,settle_position,road_position)

    # game will be played for maximum MAXIMUM_ROUNDS
    for game_round in range(MAXIMUM_ROUNDS):
        # print statements for debugging
        print(game_round)
        # in each round each player has his turn
        for player_nr in range(1,num_players):
            current_player = players[player_nr]
            # print statements for debugging
            print('It is turn of player number:{0}'.format(current_player.player_nr))
            choice = menu()
            
            winner=False
            
            turns =0
            while winner==False or turns <31:
                # making safety working copy of board (can be changed in later
                # implementation to only visible data)
                board_safety_copy = copy.deepcopy(board.board)
                # player makes the choice what to do the choices are integers 0 or negative integer is turn finished
                choice = current_player.turn_choice(board_safety_copy)
                # print statements for debugging
                print(choice)
                if choice == 2:
                    # roll dice
                    ok, dice_number = board.roll_dice(player_nr)
                    if dice_number == 7:
                        for p_nr in range(4):
                            p = players[p_nr]
                            resources = p.discard_half()
                            # The above checks if the player has more than seven cards.
                            # It returns the cards to discard, or None.
                            if resource is not None:
                                board.discard_half(p, resources)
                        # steal resource after everybody discarded cards
                        position, target_player_nr = current_player.steal_card(board_safety_copy)
                        board.steal_card(player_nr, position, target_player_nr)
                if choice == 3:
                    position = current_player.set_settlement(board_safety_copy)
                    # Check if player chose a position. It will return None if
                    # the player doesn't have the resources to buy the item.
                    if position is not None:
                        board.buy_settlement(players[player_nr], player_nr, position)
                if choice == 4:
                    position = current_player.set_city(board_safety_copy)
                    # Check if player chose a position. It will return None if
                    # the player doesn't have the resources to buy the item.
                    if position is not None:
                        board.buy_city(players[player_nr], player_nr, position)
                if choice == 5:
                    position = current_player.set_road(board_safety_copy)
                    # Check if player chose a position. It will return None if
                    # the player doesn't have the resources to buy the item.
                    if position is not None:
                        board.buy_road(players[player_nr], player_nr, position)
                if choice == 6:
                    board.buy_dev_card(players[player_nr],turns)
                if choice == 8:
                    position, target_player_nr = current_player.steal_card(board_safety_copy)
                    board.play_knight(player_nr, position, target_player_nr)
                if choice == 9:
                    position1, position2 = current_player.play_roads(board_safety_copy)
                    board.play_roads(player_nr, position1, position2)
                if choice == 10:
                    resource1, resource2 = current_player.play_plenty(board_safety_copy)
                    board.play_plenty(player_nr, resource1, resource2)
                if choice == 11:
                    resource = current_player.play_mono(board_safety_copy)
                    board.play_mono(player_nr, resource)
                if choice == 12:
                    resource_own, resource_bank, give = current_player.trade_bank(board_safety_copy)
                    board.trade_bank(players[player_nr], resource_own, resource_bank, give)
                if choice == 13:
                    resources_own, target_player_nr, resources_target = current_player.trade_offer(board_safety_copy)
                    answer_target = players[target_player_nr].trade_answer(board_safety_copy, resources_own,
                                                                           resources_target)
                    board.trade_offer(player_nr, resources_own, target_player_nr, resources_target,
                                      answer_target)

                game_end, winner = board.check_points()
                if game_end:
                 print("player {0} won".format(winner))
                 break 
                turns+=1

    print('game ended')
    board.board.gui.window.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
