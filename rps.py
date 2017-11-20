#/usr/bin/python
import doctest
import getpass
import json
import os
import random
import sys

moves = ["rock", "paper", "scissors"]

def instructions():
    print "Welcome to Rock Paper Scissors! Please follow the instructions\n"

def first_beats_second(move1, move2):
    """
    >>> first_beats_second("rock", "scissors")
    True
    >>> first_beats_second("paper", "paper")
    False
    >>> first_beats_second("paper", "scissors")
    False
    """
    return moves[(moves.index(move2)+1)%len(moves)] == move1

def compute_winner(players):
    """
    >>> compute_winner([{"player": "1", "move":"rock"}, {"player": "2", "move":"paper"}])
    1
    >>> compute_winner([{"player": "1", "move":"rock"}, {"player": "2", "move":"scissors"}])
    0
    >>> compute_winner([{"player": "1", "move":"rock"}, {"player": "2", "move":"rock"}])
    >>> compute_winner([{"player": "1", "move":"rock"}, {"player": "2", "move":"rock"}, {"player": "3"}])
    """
    if len(players) != 2:
        return None
    for index in range(len(players)):
        if(first_beats_second(players[index]["move"], players[(index + 1)%2]["move"])):
            return index
    return None

def clean_str(string):
    """
    >>> clean_str("Hello")
    'hello'
    >>> clean_str("nothing changed")
    'nothing changed'
    >>> clean_str(None)
    """
    if string is None:
        return string
    return string.lower()

def prefix_to_move(prefix):
    """
    >>> prefix_to_move("r")
    'rock'
    >>> prefix_to_move("SCI")
    'scissors'
    >>> prefix_to_move("pap")
    'paper'
    >>> prefix_to_move("papers")
    """
    prefix = clean_str(prefix)
    for move in moves:
        if move.startswith(prefix):
            return move
    return None

def input_player(player_name):
    move = None
    while move is None:
        move = prefix_to_move(getpass.getpass("Hello " + player_name + ", please pick r (rock), p (paper), or s (scissors): "))
    return move

def usage():
    print "python rps.py /path/to/game/history.json player_1_name player_2_name"

def verify_game_history(game_history):
    """
    >>> verify_game_history({})
    True
    >>> verify_game_history({"player": "1", "move":"rock"})
    False
    >>> verify_game_history({"mafaldo":{"wins":1, "ties": 1, "games":2, "rock":1, "paper":0, "scissors":1}})
    True
    """
    
    if not isinstance(game_history, dict):
        return False
    for key, value in game_history.items():
        if not isinstance(value, dict):
            return False
        for mandatory_key in ["ties", "wins", "rock", "paper", "scissors", "games"]:
            if mandatory_key not in value:
                return False
    return True

def load_game_history(path_to_game_history):
    mode = 'rU'
    if not os.path.exists(path_to_game_history):
        mode = "w+"
    with open(path_to_game_history, mode) as f:
        try:
            history = json.load(f)
        except ValueError as v:
            if os.stat(path_to_game_history).st_size == 0:
                #Empty File, no problem
                return {}
            #nonempty file, big problem
            raise v
    
    if not verify_game_history(history):
        raise ValueError("improper history format")

    return history

def persist_game_history(path_to_game_history, game_history):
    with open(path_to_game_history, 'w') as f:
        json.dump(game_history, f)
    
def update_history(history_name, history, players, winner):
    for player in players:
        player_name = clean_str(player["player"])
        player_history = history.get(player_name, {"ties": 0, "wins": 0, "rock": 0, "paper": 0, "scissors": 0, "games": 0})
        player_history[player["move"]] += 1
        player_history["games"] += 1
        if winner == None:
            player_history["ties"] += 1
        elif player == players[winner]:
            player_history["wins"] += 1
        history[player_name] = player_history
    persist_game_history(history_name, history)

def compute_move_for_mafaldo(game_history, opponent):
    opponent_name = clean_str(opponent["player"])
    opponent_history = game_history.get(opponent_name, {"ties": 0, "wins": 0, "rock": 0, "paper": 0, "scissors": 0, "games": 0})
    games = opponent_history["games"]
    probability_scissors = 1.0/3
    probability_rock = 1.0/3
    probability_paper = 1.0/3
    if games > 0:
        probability_scissors = 1.0*opponent_history["paper"]/games
        probability_rock = 1.0*opponent_history["scissors"]/games
        probability_paper = 1.0*opponent_history["rock"]/games
    decision = random.uniform(0,1)
    if decision < probability_scissors:
        return "scissors"
    elif decision < probability_rock + probability_scissors:
        return "rock"
    else:
        return "paper"
    
def dump_score(history, players):
    for player in players:
        player_name = clean_str(player["player"])
        print player["player"] + " has won " + str(history[player_name]["wins"]) + " games out of " + str(history[player_name]["games"]) + " total"
        

def main():
    if len(sys.argv) != 4:
        usage()
        exit(1)
    instructions()

    players = []
    game_history_name = sys.argv[1]
    game_history = load_game_history(game_history_name)

    args = sys.argv[2:4]
    random.shuffle(args)
    if clean_str(args[0]) == clean_str(args[1]):
        print "Players cannot play themselves, please enter two distinct player names."
        exit(1)
    mafaldo_is_playing = False
    for arg in args:
        if clean_str(arg) == "mafaldo":
            mafaldo_is_playing = True
            continue
        p_name = arg
        move = input_player(p_name)
        players.append({"player": p_name, "move": move})

    if mafaldo_is_playing:
        move = compute_move_for_mafaldo(game_history, players[0])
        p_name = "mafaldo"
        players.append({"player": p_name, "move": move})
        print "Mafaldo has chosen."

    winner = compute_winner(players)
    if winner is None:
        print "Tie! (" + players[0]["move"] + " == " + players[0]["move"]+ ")"
    else:
        print players[winner]["player"] + " won! (" + players[winner]["move"] + " > " + players[(winner + 1)%2]["move"] + ")"
    update_history(game_history_name, game_history, players, winner)
    dump_score(game_history, players)
    exit(0)

if __name__ == "__main__":
    doctest.testmod()
    main()
