from player_helpers import get_player_by_name


#  -- load dice values when new round starts --
def load_stat(player, data):
    for i in range(len(data)):
        player.stat[data[i]] += 1


#  -- load other players bets to memory if their stat is trustworthy--
def load_memory(current_player, bet, players):
    c_player = get_player_by_name(current_player, players)
    for player in players:
        if current_player != player.name and c_player.temper_for_other_players > 0.55:
            player.memory[int(bet[1])] += 1
        elif current_player == player.name and player.dice != 0:
            player.profile_for_opponents['called_dice'][0] += 1
            player.profile_for_opponents['called_dice'][1][int(bet[1])] += 1


#  -- load self dices to memory --
def load_initial_memory(player, data):
    for i in range(len(data)):
        player.memory[data[i]] += 1

