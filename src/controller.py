from itertools import permutations, combinations
import json


class Controller:
  def __init__():
    pass
  
  @staticmethod
  def calculate_shapley_values(coalition_values: int, player: str) -> int:
    players = max(coalition_values, key=lambda x: len(x))
    contributions = []

    for permutation in permutations(players):
        player_index = permutation.index(player)
        coalition_before = frozenset(permutation[:player_index])  # excluding player
        coalition_after = frozenset(permutation[: player_index + 1])  # player joined coalition
        contributions.append(coalition_values[coalition_after] - coalition_values[coalition_before])

    return sum(contributions) / len(contributions)
  
  
  @staticmethod
  def get_combinations(itens: list):
    
    possible_combinations = dict()
    
    for i in range(1, len(itens) + 1):
      possible_combinations[i] = list(combinations(itens, i))
    return possible_combinations
    
  
if __name__ == '__main__':
  
  coalition_values = {
    frozenset(): 0,
    frozenset("A"): 80,
    frozenset("B"): 56,
    frozenset("C"): 70,
    frozenset(("A", "B")): 80,
    frozenset(("A", "C")): 85,
    frozenset(("B", "C")): 72,
    frozenset(("A", "B", "C")): 90
  }
  
  for player in ("A", "B", "C"):
    print(player, Controller.calculate_shapley_values(coalition_values, player))
  
  
  # possible_combinations = Controller.get_combinations(['R1', 'R2', 'R3', 'R4', 'R5', 'R6'])
  
  # possible_combinations_formatted = json.dumps(possible_combinations, indent=2)

  # print(possible_combinations_formatted)