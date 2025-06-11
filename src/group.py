# binning ou discretização por intervalos

player_values = {
    1: 0.0014001179550361456, 2: 0.0014003179768234232, 3: 0.0013986122066381658, 4: 0.0013984899992594208,
    5: 0.0013979515184058518, 6: 0.001397988579170951, 7: 0.0013960037346733038, 8: 0.0013961466684913018,
    9: 0.0013927426947526517, 10: 0.001392891961574732, 11: 0.0013907335741909705, 12: 0.0013905776281417344,
    13: 0.0013887596226061542, 14: 0.001385800940536946, 15: 0.0013924690057226343, 16: 0.0013910153810318606,
    17: 0.0013904639464730705, 18: 0.0013844602151047135, 19: 0.001377886868633406, 20: 0.001377727000464618,
    21: 0.001377792547269662, 22: 0.0013737960471287072, 23: 0.0013734036936648882, 24: 0.0013700402541847775,
    25: 0.00137004446900153, 26: 0.0013693460794636843
}

interval = 0.1

min_value = min(player_values.values())
max_value = max(player_values.values())

bins_values = {}
bins_indexes = {}
last_bin_values = {}
while True:
  for player, value in player_values.items():
      # binning
      bin_index = int((value - min_value) // interval)
      bins_values.setdefault(bin_index, []).append(value)
      bins_indexes.setdefault(bin_index, []).append(player)
      
  # Print groups
  # for bin_index, players_in_bin in bins.items():
  #     bin_start = min_value + bin_index * interval
  #     bin_end = bin_start + interval
  #     print(f"Grupo {bin_index} (de {bin_start:.7f} até {bin_end:.7f}): jogadores {players_in_bin}")
      
  if len(bins_values) > 5:
      break
  
  last_bin_values = bins_values.copy()
  last_bin_indexes = bins_indexes.copy()
  interval = interval / 10
  bins_values.clear()
  bins_indexes.clear()
      
print(last_bin_values)
print(last_bin_indexes)
bins_average= {}
for group in last_bin_values.keys():
  bins_average[group] = sum(last_bin_values[group]) / len(last_bin_values[group])

print(bins_average)