"""The game of nim"""
from random import randint, choice
from math import log2
from enum import Enum
from argparse import ArgumentParser


class Difficulty(Enum):
    SMART = "smart"
    STUPID = "stupid"


class Player(Enum):
    COMPUTER = "computer"
    HUMAN = "human"


class Game:
    def __init__(self, initial_size=None, starting_player=None, difficulty=None):
        self.pile_size = initial_size or randint(10, 100)
        self.turn = starting_player or choice([Player.COMPUTER, Player.HUMAN])
        self.difficulty = difficulty or choice([Difficulty.STUPID, Difficulty.SMART])

        print("The game of Nim")
        print("Initial size of the pile:", self.pile_size)
        print(Game.get_pronoun(self.turn), Game.conjugate_verb("take", self.turn), "the first turn")
        print("Difficulty:", self.difficulty.value)
        print()

    def run(self):
        while self.pile_size > 0:
            if self.turn == Player.COMPUTER:
                self.computers_turn()
                self.turn = Player.HUMAN
            else:
                self.players_turn()
                self.turn = Player.COMPUTER

    def computers_turn(self):
        print("Computer's turn")

        if self.difficulty == Difficulty.STUPID:
            self.make_move(Player.COMPUTER, randint(1, self.get_upper_limit()))
        else:
            take = self.pile_size - (2**int(log2(self.pile_size)) - 1)
            if self.is_legal_move(take):
                self.make_move(Player.COMPUTER, take)
            else:
                self.make_move(Player.COMPUTER, randint(1, self.get_upper_limit()))

    def players_turn(self):
        print("Your turn")
        while True:
            try:
                take = int(input(f"How many marbles to take [{1}, {self.get_upper_limit()}]: "))
                if self.is_legal_move(take):
                    self.make_move(Player.HUMAN, take)
                    break
                else:
                    print(f"The number must be between [{1}, {self.get_upper_limit()}] inclusive!")
            except ValueError:
                print("Enter an integer!")

    def make_move(self, player, number):
        if self.is_legal_move(number):
            self.pile_size -= number

            print(Game.get_pronoun(player), Game.conjugate_verb("take", player), number, Game.conjugate_noun("marble", number))
            print(self.pile_size, Game.conjugate_noun("marble", self.pile_size), "left")
            print()

            if self.pile_size < 1:
                print(Game.get_pronoun(player), "took the last marble")
                if player == Player.COMPUTER:
                    print("You win!")
                else:
                    print("You lose!")

    def is_legal_move(self, number):
        return 1 <= number <= self.get_upper_limit()

    def get_upper_limit(self):
        return int(self.pile_size / 2) if self.pile_size > 1 else 1

    @staticmethod
    def conjugate_verb(verb, player):
        return verb if player == Player.HUMAN else verb + "s"

    @staticmethod
    def conjugate_noun(noun, number):
        return noun + "s" if number > 1 else noun

    @staticmethod
    def get_pronoun(player):
        return {
            Player.COMPUTER: "Computer",
            Player.HUMAN: "You"
        }[player]


def main():
    parser = ArgumentParser()
    parser.add_argument("-s", "--size", help="initial size of the pile", type=int)
    parser.add_argument("-f", "--first", help="who takes the first turn", type=lambda p: p.lower(), choices=[p.value for p in Player])
    parser.add_argument("-d", "--difficulty", help="difficulty", type=lambda d: d.lower(), choices=[d.value for d in Difficulty])
    args = parser.parse_args()
    print(args)

    game = Game(initial_size=args.size, starting_player=Player[args.first.upper()], difficulty=Difficulty[args.difficulty.upper()])
    game.run()


if __name__ == "__main__":
    main()
