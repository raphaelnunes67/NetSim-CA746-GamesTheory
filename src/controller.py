from itertools import permutations, combinations
from math import factorial
from time import time
import json

class Controller:
  def __init__():
    pass
  
  @staticmethod
  def powerset(set_):
    for k in range(len(set_) + 1):
        for subset in combinations(set_, k):
            yield set(subset)
            
  @staticmethod
  def calculate_shapley_values(coalition_values: int, player: str) -> int:
    N = max(coalition_values, key=lambda x: len(x))
    n = len(N)
    contribution = 0

    for S in Controller.powerset(N - {player}):
        multiplicity = factorial(len(S)) * factorial(n - len(S) - 1)
        coalition_before = frozenset(S)
        coalition_after = frozenset(S | {player})
        contribution += multiplicity * (coalition_values[coalition_after] - coalition_values[coalition_before])

    return contribution / factorial(n)
  
  
  @staticmethod
  def get_combinations(itens: list):
    
    possible_combinations = dict()
    
    for i in range(1, len(itens) + 1):
      possible_combinations[i] = list(combinations(itens, i))
    return possible_combinations
    
  
if __name__ == '__main__':
  
  coalition_values = {
    frozenset(): 0,
    frozenset("R1"): 10,
    frozenset("R2"): 20,
    frozenset("R3"): 30,
    frozenset("R4"): 40,
    frozenset("R5"): 50,
    frozenset("R6"): 60,
    frozenset(("R1", "R2")): 15,
    frozenset(("R1", "R3")): 25,
    frozenset(("R1", "R4")): 35,
    frozenset(("R1", "R5")): 45,
    frozenset(("R1", "R6")): 55,
    frozenset(("R2", "R3")): 22,
    frozenset(("R2", "R4")): 32,
    frozenset(("R2", "R5")): 42,
    frozenset(("R2", "R6")): 52,
    frozenset(("R3", "R4")): 33,
    frozenset(("R3", "R5")): 43,
    frozenset(("R3", "R6")): 53,
    frozenset(("R4", "R5")): 54,
    frozenset(("R4", "R6")): 64,
    frozenset(("R5", "R6")): 74,
    frozenset(("R1", "R2", "R3")): 28,
    frozenset(("R1", "R2", "R4")): 38,
    frozenset(("R1", "R2", "R5")): 48,
    frozenset(("R1", "R2", "R6")): 58,
    frozenset(("R1", "R3", "R4")): 68,
    frozenset(("R1", "R3", "R5")): 78,
    frozenset(("R1", "R3", "R6")): 88,
    frozenset(("R1", "R4", "R5")): 98,
    frozenset(("R1", "R4", "R6")): 108,
    frozenset(("R1", "R5", "R6")): 118,
    frozenset(("R2", "R3", "R4")): 128,
    frozenset(("R2", "R3", "R5")): 138,
    frozenset(("R2", "R3", "R6")): 148,
    frozenset(("R2", "R4", "R5")): 158,
    frozenset(("R2", "R4", "R6")): 168,
    frozenset(("R2", "R5", "R6")): 178,
    frozenset(("R3", "R4", "R5")): 188,
    frozenset(("R3", "R4", "R6")): 198,
    frozenset(("R3", "R5", "R6")): 208,
    frozenset(("R4", "R5", "R6")): 218,
    frozenset(("R1", "R2", "R3", "R4")): 228,
    frozenset(("R1", "R2", "R3", "R5")): 238,
    frozenset(("R1", "R2", "R3", "R6")): 248,
    frozenset(("R1", "R2", "R4", "R5")): 258,
    frozenset(("R1", "R2", "R4", "R6")): 268,
    frozenset(("R1", "R2", "R5", "R6")): 278,
    frozenset(("R1", "R3", "R4", "R5")): 288,
    frozenset(("R1", "R3", "R4", "R6")): 298,
    frozenset(("R1", "R3", "R5", "R6")): 308,
    frozenset(("R1", "R4", "R5", "R6")): 318,
    frozenset(("R2", "R3", "R4", "R5")): 328,
    frozenset(("R2", "R3", "R4", "R6")): 338,
    frozenset(("R2", "R3", "R5", "R6")): 348,
    frozenset(("R2", "R4", "R5", "R6")): 358,
    frozenset(("R3", "R4", "R5", "R6")): 368,
    frozenset(("R1", "R2", "R3", "R4", "R5")): 378,
    frozenset(("R1", "R2", "R3", "R4", "R6")): 388,
    frozenset(("R1", "R2", "R3", "R5", "R6")): 398,
    frozenset(("R1", "R2", "R4", "R5", "R6")): 408,
    frozenset(("R1", "R3", "R4", "R5", "R6")): 418,
    frozenset(("R2", "R3", "R4", "R5", "R6")): 428,
    frozenset(("R1", "R2", "R3", "R4", "R5", "R6")): 438
  }
  
  initial_time = time()
  players_shapley_values = {}
  for player in ("R1", "R2", "R3", "R4", "R5", "R6"):
    players_shapley_values[player] = Controller.calculate_shapley_values(coalition_values, player)
  
  elapsed_time = time() - initial_time
  
  print(players_shapley_values)
  print(f'Elapsed time: {elapsed_time}')
  
  
  # possible_combinations = R3ontroller.get_combinations(['R1', 'R2', 'R3', 'R4', 'R5', 'R6'])
  
  # possible_combinations_formatted = json.dumps(possible_combinations, indent=2)

  # print(possible_combinations_formatted)