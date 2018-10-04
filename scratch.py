from cards import *
from blackjack import *
random.seed(1)

p = Player(500)
print(p._deal())
print(p.current_hand)
p._hit()
print(p.current_hand)
print(p.current_hand.points_total())
p._hit()
print(p.current_hand)
print(p.current_hand.points_total())
p._hit()
print(p.current_hand)
print(p.current_hand.points_total())
