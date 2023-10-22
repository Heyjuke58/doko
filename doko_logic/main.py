import argparse

from .Sitting import Sitting

if __name__ == "__main__":
    cmdline_parser = argparse.ArgumentParser("doko")

    cmdline_parser.add_argument("-np", "--number_of_players", default=4, help="Number of players", type=int)

    args, _ = cmdline_parser.parse_known_args()

    number_of_players = args.number_of_players

    game = Sitting(number_of_players=number_of_players, player_names=["Alphons", "Beate", "Gabi", "Detmar"])
    game.play()
