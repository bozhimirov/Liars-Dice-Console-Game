from collections import deque

from player import Player


#  -- get player by name if name is a string, not object --
def get_player_by_name(player_name: Player, players: deque) -> Player:
    for pl in players:
        if pl.name == player_name:
            return pl


#  -- load dice values when new round starts --
def load_stat(player: Player, data: list) -> None:
    for i in range(len(data)):
        player.stat[data[i]] += 1


#  -- load other players bets to memory if their stat is trustworthy--
def load_memory(current_player: Player, bet: list, players: deque) -> None:
    c_player = get_player_by_name(current_player, players)
    for player in players:
        if current_player != player.name and c_player.temper_for_other_players > 0.55:
            player.memory[int(bet[1])] += 1
        elif current_player == player.name and player.dice != 0:
            player.profile_for_opponents['called_dice'][0] += 1
            player.profile_for_opponents['called_dice'][1][int(bet[1])] += 1


#  -- load self dices to memory --
def load_initial_memory(player: Player, data: list) -> None:
    for i in range(len(data)):
        player.memory[data[i]] += 1
