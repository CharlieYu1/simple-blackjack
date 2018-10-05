'''
Skeleton for a simple blackjack game with rules
'''

from copy import copy, deepcopy
from cards import *


class SingleBlackJackHand(list):
    # only includes the cards in the hand
    def __init__(self, bet=0, first_card=None, second_card=None):
        '''
        :param bet: bet_amount
        :param first_card:
        '''
        self.bet = bet
        assert isinstance(first_card, Card)
        assert isinstance(second_card, Card)
        list.__init__(self)
        self.append(first_card)
        self.append(second_card)

    @property
    def points_total(self):
        total = sum(card.rank.point for card in self)
        if any(card.rank == Rank.ACE for card in self) & (total <= 11):
            total += 10
        return total

    @property
    def busted(self):
        return self.points_total > 21

    def check_blackjack(self):
        # check for 2 cards and 21 points only; doesn't check a split happened or not
        return self.points_total() == 21 and len(self) == 2

    @property
    def is_blackjack(self):
        return self.points_total == 21 and len(self) == 2


class Player():
    def __init__(self, amount=500):
        global game
        '''
        player object.
        :param amount: Amount of money remained
        '''
        self.hands = []
        self.bet_size = 5
        self.amount = amount

    def _deal(self, bet_size = None):
        if bet_size:
            self.bet_size = bet_size

        self.amount -= self.bet_size
        self.hands = [
            SingleBlackJackHand(self.bet_size, game.draw(), game.draw())
        ]
        self.current_hand_index = 0 # point to an index in self.hands during gameplay.

    def next_hand(self):
        self.current_hand_index += 1
        if self.current_hand_index >= len(self.hands):
            self.current_hand_index = -1

    @property
    def _player_turn_end(self):
        return self.current_hand_index == -1

    def _pass(self):
        self.next_hand()

    def _split(self):
        split_card = self.current_hand.pop()
        self.hands.insert(self.current_hand_index + 1, split_card)
        self.hands[self.current_hand_index + 1].bet = self.hands[self.current_hand_index].bet
        self.amount -= self.hands[self.current_hand_index].bet


    @property
    def current_bet(self):
        return self.hands[self.current_hand_index].bet

    @property
    def current_hand(self):
        return self.hands[self.current_hand_index]

    def _hit(self):
        self.current_hand.append(game.draw())
        if self.current_hand.busted:
            self.next_hand()

    @property
    def allowed_to_split(self):
        return len(self.current_hand) == 2 and self.current_hand[0].rank == self.current_hand[1].rank

    @property
    def allowed_to_double(self):
        return len(self.current_hand) == 2


    def _double(self):
        self.amount -= self.hands[self.current_hand_index].bet
        self.hands[self.current_hand_index].bet *= 2
        self.current_hand.append(game.draw())
        self.next_hand()


class Dealer(list):
    def __init__(self):
        list.__init__(self)

    def deal(self):
        self.append(game.draw())

    def print_dealer(self):
        print(f'Dealer: {" ".join(repr(card) for card in self)}')

    @property
    def points_total(self):
        total = sum(card.rank.point for card in self)
        if any(card.rank == Rank.ACE for card in self) & (total <= 11):
            total += 10
        return total

    def dealer_run(self):
        while self.points_total < 17:
            self.append(game.draw())
            self.print_dealer()
        print()

    def reset(self):
        self.__init__()

    @property
    def busted(self):
        return self.points_total > 22

    @property
    def is_blackjack(self):
        return self.points_total == 21 and len(self) == 2


class Game():
    def __init__(self):
        self.deck = Deck()
        self.players = [Player() for _ in range(4)]
        self.dealer = Dealer()

    def draw(self):
        return self.deck.pop()

    def shuffle(self):
        self.deck.__init__()

    def print_game_state(self):
        for i, player in enumerate(self.players):
            for j, hand in enumerate(player.hands):
                print(f'Player {i} Hand {j}: Bet size ${hand.bet} {" ".join(repr(card) for card in hand)}')
        self.dealer.print_dealer()
        print()

    def print_amount(self):
        for i, player in enumerate(self.players):
            print(f'Player {i}: ${player.amount}')
        print()

    def payout(self):
        # payout and print payout
        for i, player in enumerate(self.players):
            for j, hand in enumerate(player.hands):
                result = '' # string to print for payout
                if self.dealer.is_blackjack:
                    if hand.is_blackjack and len(player.hands) == 1: # blackjack only on first hand
                        result = f'Push +${hand.bet}'
                        player.amount += hand.bet
                    else:
                        result = 'Dealer Blackjack'
                elif hand.is_blackjack and len(player.hands) == 1: # player blackjack
                    result = f'Blackjack +${hand.bet * 2.5}'
                    player.amount += hand.bet * 2.5
                elif hand.busted:
                    result = 'Busted'
                elif self.dealer.busted:
                    result = f'Dealer Busted +${hand.bet * 2}'
                    player.amount += hand.bet * 2
                elif hand.points_total > self.dealer.points_total:
                    result = f'Win +${hand.bet * 2}'
                    player.amount += hand.bet * 2
                elif hand.points_total == self.dealer.points_total:
                    result = f'Push +${hand.bet}'
                    player.amount += hand.bet
                else:
                    result = 'Lose'
                print(f'Player {i} Hand {j}: Bet size ${hand.bet} {" ".join(repr(card) for card in hand)} {result}')
        print()

    def main(self):
        '''
        running the game. prompting player turn by turn
        :return:
        '''

        while 1: # mainloop
            self.print_amount()

            # receive bet amounts
            for i, player in enumerate(self.players):
                b = input(f'Enter bet amount for player {i}: (default={player.bet_size})> ')
                if b:
                    player._deal(int(b))
                else:
                    player._deal()
            print()

            # dealing cards
            print('Starting the round')
            self.dealer.reset()
            self.dealer.deal()

            # player turns
            for i, player in enumerate(self.players):
                while player.current_hand_index != -1: # while still have hands in action
                    self.print_game_state()
                    action = input(f'Action for player {i}, hand {player.current_hand_index}'
                                   '(H = Hit, S = Split, D = Double, P=Pass)> ')
                    if action == 'H':
                        player._hit()
                    elif action == 'S':
                        if player.allowed_to_split:
                            player._split()
                        else:
                            print('Error: You must have 2 cards of same rank to split.')
                    elif action == 'D':
                        if player.allowed_to_double:
                            player._double()
                        else:
                            print('Error: You must have 2 cards to double.')
                    elif action == 'P':
                        player._pass()
                    else:
                        print('Error: Invalid command')

            self.dealer.dealer_run()

            self.payout()

            self.print_amount()

            # shuffle if less than 52 cards
            if len(self.deck) < 52:
                self.shuffle()

            # ask if play another round
            if input('Play Another Round? Input 1 to continue, 0 to stop> ') == '0':
                break

game = Game() # global game object
if __name__ == '__main__':
    game.main()
