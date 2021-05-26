# This is a catan Python script.
import catan
import player
import copy

# The game is played for maximum 30 rounds (30*4 = 120 turns) to prevent
# infinite loops
MAXIMUM_ROUNDS = 30

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # build catan board
    board = catan.CatanBoard()

    # insert players
    players = list()
    NUM_PLAYERS = 4
    """
    -- This needs a try-except, and check for max-players == 4
    NUM_PLAYERS=int(input("Number of players: \n"))
     """
    for player_nr in range(NUM_PLAYERS):
        players.append(player.CatanPlayer(player_nr))

    # game set up of the two settlement
    # first settlement with road
    for player_nr in range(NUM_PLAYERS):
        current_player = players[player_nr]
        board_safety_copy = copy.deepcopy(board.board)
        settle_position, road_position \
            = current_player.start_settlement_placement(board_safety_copy)
        board.start_settelment_first(player_nr, settle_position, road_position)

    # second settlement with road
    for player_nr in range(NUM_PLAYERS-1, 0, -1):
        current_player = players[player_nr]
        board_safety_copy = copy.deepcopy(board.board)
        settle_position, road_position \
            = current_player.start_settlement_placement(board_safety_copy)
        board.start_settelment_second(
            players[player_nr],
            player_nr,
            settle_position,
            road_position)

    # game will be played for maximum MAXIMUM_ROUNDS
    for game_round in range(MAXIMUM_ROUNDS):
        # print statements for debugging
        print(game_round)
        # in each round each player has his turn
        for player_nr in range(NUM_PLAYERS):
            current_player = players[player_nr]
            # print statements for debugging
            print('It is turn of player number:{0}'.format(
                current_player.player_nr))
            # Each turn starts with rolling the dice
            # roll dice at the start of each turn
            dice_number = board.roll_dice()
            if dice_number == 7:
                for p_nr in range(4):
                    p = players[p_nr]
                    resources = p.discard_half()
                    # The above checks if the player has more than seven
                    # cards. It returns the cards to discard, or None.
                    if resources is not None:
                        board.discard_half(p, resources)
                # steal resource after everybody discarded cards
                position, target_player_nr = current_player.steal_card(board_safety_copy)
                board.steal_card(players[player_nr], position, players[target_player_nr])

            """ The player is given option as what to do during the turn.
            The turn ends when player hits zero. """
            turns = 0  # To keep track if dev_card can be played
            choice = 42  # Sentinel
            while choice > 0:
                # making safety working copy of board (can be changed in later
                # implementation to only visible data)
                board_safety_copy = copy.deepcopy(board.board)
                # player makes the choice what to do.  The choices are
                # integers. 0 or negative integer ends the turn.
                choice = current_player.turn_choice(board_safety_copy)
                # print statements for debugging

                """ buy roads, settlements, cities """
                if choice == 1:
                    position = current_player.set_settlement(board_safety_copy)
                    # Check if player chose a position. It will return None if
                    # the player doesn't have the resources to buy the item.
                    if position is not None:
                        board.buy_settlement(players[player_nr], player_nr, position)
                elif choice == 2:
                    position = current_player.set_city(board_safety_copy)
                    # Check if player chose a position. It will return None if
                    # the player doesn't have the resources to buy the item.
                    if position is not None:
                        board.buy_city(players[player_nr], player_nr, position)
                elif choice == 3:
                    position = current_player.set_road(board_safety_copy)
                    # Check if player chose a position. It will return None if
                    # the player doesn't have the resources to buy the item.
                    if position is not None:
                        board.buy_road(players[player_nr], player_nr, position)
                    
                    """ buy development card """
                elif choice == 4:
                    board.buy_dev_card(turns, players[player_nr], player_nr,)

                    """ play development cards """
                elif choice == 5:
                    position, target_player_nr = current_player.steal_card(board_safety_copy)
                    board.play_knight(turns, players[player_nr], player_nr, 
                                      position, players[target_player_nr])
                elif choice == 6:
                    position1, position2 = current_player.play_roads(board_safety_copy)
                    board.play_roads(turns, players[player_nr], player_nr, position1, position2)
                elif choice == 7:
                    resource1, resource2 = current_player.play_plenty(board_safety_copy)
                    board.play_plenty(turns, players[player_nr], resource1, resource2)
                elif choice == 8:
                    resource = current_player.play_mono(board_safety_copy)
                    board.play_mono(turns, players, player_nr, resource)

                    """ trading """
                elif choice == 9:
                    response = current_player.trade_bank(board_safety_copy)
                    if response is not None:
                        resource_own, resource_bank, give = response
                        board.trade_bank(players[player_nr], resource_own, resource_bank, give)
                elif choice == 10:
                    resources_own, target_player_nr, resources_target = \
                        current_player.trade_offer(board_safety_copy)
                    answer_target = players[target_player_nr].trade_answer(
                        board_safety_copy, resources_own, resources_target)
                    board.trade_offer(player_nr, resources_own,
                        target_player_nr, resources_target, answer_target)

                # Increment turns, so that dev_cards' status can be tracked
                turns += 1
                # Check for winner / end game after each round.  Break out
                # of the loop when game ends.
                game_end, winner = board.check_points()
                if game_end:
                    print("player {0} won".format(winner))
                    break

    print('game ended')
    board.board.gui.window.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
