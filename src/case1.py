from opendssdirect import dss
from constants import ColumnsMapVoltages, ColumnsMapPowers
from plotter import Plotter
from itertools import permutations, combinations
import csv
import os


def get_all_contributions():
  print('Obtendo dados de energia...')
  dss.NewContext()
  dss.Text.Command(f'Redirect ../dss/CA746.dss')
  
  # Insere a curva de carga do VE
  column_index = 1
  column_data = []
  with open('../data/electrical_vehicles/ev_shapes_charge.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    column_data = [row[column_index] for row in csv_reader]
    
  column_values_str = ' '.join(map(str, column_data))
  dss.Text.Command(f'New Loadshape.shape_ev_1 npts=1440 minterval=1 mult=({column_values_str})')
  
  # Insere a curva VW para os VEs
  dss.Text.Command('New XyCurve.vw_curve_ev npts=4 Yarray=(0.0, 0.0, 1.0, 1.0) Xarray=(0.0, 0.866141, 0.921259, 1.0)')
  total_loads = len(dss.Loads.AllNames())
  dss.Loads.First()
  for _ in range(total_loads):
    
    if dss.Loads.Name().find("residence") != -1:
      residence = dss.Loads.Name()
      n_res = int(residence[residence.find("residence") + 9:])
      # Modifica todas as cargas das residências para 2.5kW
      dss.Loads.kW(2.5)
      # Aplica o mesmo loadshape para todas as residencias
      dss.Loads.Daily('RES-Type1-WE')
      phase_a, phase_b = (1, 2)
      # dss.Text.Command(
      #   f'New Storage.ev_{n_res} bus1=EVRES{n_res}.{phase_a}.{phase_b} phases=2 kV=0.220 kWhrated=40 kWhstored=0 ' 
      #   f'pf=0.95 kW=24 kWrated=12 conn=delta daily=shape_ev_1 dispmode=FOLLOW %stored=0 '
      #   'model=1 State=CHARGING %reserve=100 %EffCharge=100 '
      #   '%Discharge=0 TimeChargeTrig=0 %Charge=100'
      # ) 
      
      # Adiciona o controle voltwatt
      # dss.Text.Command(
      #   f'New InvControl.control_voltwatt_{n_res} mode=voltwatt '
      #   'voltage_curvex_ref=rated '
      #   'voltageChangeTolerance=0.01 '
      #   'activePChangeTolerance=0.01 deltaP_factor=0.1 '
      #   'enabled=true voltwattCH_curve=vw_curve_ev monVoltageCalc=MAX '
      #   'RiseFallLimit=-1 voltwattYaxis=PMPPPU '
      #   f'DERlist=(Storage.ev_{n_res})'
      # )
      
      # Adiciona o medidor
      meter_name = f'{dss.Loads.Name()}_meter'
      # dss.Text.Command(
      #   f'New EnergyMeter.{meter_name} '
      #   f'element=line.LINE_EV{n_res} terminal=1'
      # )
      
      dss.Text.Command(
        f'New EnergyMeter.{meter_name} '
        f'element=Bus.CA746RES{n_res} terminal=1'
      )
    dss.Loads.Next()
      
  dss.Text.Command('Calcvoltagebases')
  dss.Text.Command('Set maxcontroliter=1000')
  dss.Text.Command('Set maxiterations=1000')
  dss.Text.Command('Set controlmode=time')
  
  # Resolve o circuito 
  dss.Text.Command('Set mode=daily')
  dss.Text.Command('Set stepsize=1m')
  dss.Text.Command('Set number=1')
  
  if os.path.exists('./energies'):
    for file in os.listdir('./energies'):
      os.remove('./energies/' + file)
  
  n_steps = 1440  # 24 horas, 1 minuto cada
  for i in range(n_steps):
    dss.Solution.Solve()
    # Obter os dados de energia por minuto
    dss.Meters.First()
    for _ in range(dss.Meters.Count()):
      # print(f'{dss.Meters.Name()}: {dss.Meters.RegisterValues()[0]} kWh')
      if not os.path.exists('./energies'):
        os.mkdir('./energies')
      with open(f'./energies/{dss.Meters.Name()}.txt', 'a') as file:
        file.write(f'{dss.Meters.RegisterValues()[0]}\n')
      dss.Meters.Next()
      
  print('Obtendo dados de energia obtidos!')


def calculate_shapley_values(coalition_values, players, player):
  contributions = []
  for perm in permutations(players):
      player_index = perm.index(player)
      coalition_before = tuple(sorted(perm[:player_index]))
      coalition_after = tuple(sorted(perm[:player_index + 1]))
      contrib = coalition_values[coalition_after] - coalition_values[coalition_before]
      contributions.append(contrib)
  return sum(contributions) / len(contributions)

if __name__ == '__main__':
  get_all_contributions()
  exit()
  dss.NewContext()
  dss.Text.Command('Redirect ../dss/CA746.dss')
  
  # Preparação do ckt
  # Insere a curva de carga do VE
  column_index = 1
  column_data = []
  with open('../data/electrical_vehicles/ev_shapes_charge.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    column_data = [row[column_index] for row in csv_reader]

      
  column_values_str = ' '.join(map(str, column_data))
  dss.Text.Command(f'New Loadshape.shape_ev_1 npts=1440 minterval=1 mult=({column_values_str})')
  
  dss.Loads.First()
  for _ in range(dss.Loads.Count()):
    if dss.Loads.Name().find("residence") != -1:
      residence = dss.Loads.Name()
      n_res = int(residence[residence.find("residence") + 9:])
      # Modifica todas as cargas das residências para 2.5kW
      dss.Loads.kW(2.5)
      # Aplica o mesmo loadshape para todos as residencias
      dss.Loads.Daily('RES-Type1-WE')
      # Insere a curva VW para cada residência
      dss.Text.Command(f'New XyCurve.vw_curve_ev_{n_res} npts=4 Yarray=(0.0, 0.0, 1.0, 1.0) Xarray=(0.0, 0.866141, 0.921259, 1.0)')
      # Insere o VE
      dss.Text.Command(
        f'New Storage.ev_{n_res} bus1=EVRES{n_res}.1.2 phases=2 kV=0.220 kWhrated=40 kWhstored=0 ' 
        f'pf=0.95 kW=24 kWrated=12 conn=delta daily=shape_ev_1 dispmode=FOLLOW %stored=0 '
        'model=1 State=CHARGING %reserve=100 %EffCharge=100 '
        '%Discharge=0 TimeChargeTrig=0 %Charge=100'
      )
      # Insere o controle
      dss.Text.Command(
        f'New InvControl.control_voltwatt_{n_res} mode=voltwatt '
        'voltage_curvex_ref=rated '
        'voltageChangeTolerance=0.01 '
        'activePChangeTolerance=0.01 deltaP_factor=0.1 '
        f'enabled=true voltwattCH_curve=vw_curve_ev_{n_res} monVoltageCalc=MAX '
        'RiseFallLimit=-1 voltwattYaxis=PMPPPU '
        f'DERlist=(Storage.ev_{n_res})'
      )
      # Insere o monitor 
      power_monitor_name = f'{dss.Loads.Name()}_powers'
      dss.Text.Command(
          f'New Monitor.{power_monitor_name} element=Line.LINE_EV{n_res} terminal=1 mode=1 ppolar=no'
      )
      # Insere o medidor de energia
      meter_name = f'{dss.Loads.Name()}_meter'
      dss.Text.Command(
        f'New EnergyMeter.{meter_name} '
        f'element=line.LINE_EV{n_res} terminal=1'
      )
    dss.Loads.Next()
    
  dss.Text.Command('Calcvoltagebases')
  dss.Text.Command('Set maxcontroliter=1000')
  dss.Text.Command('Set maxiterations=1000')
  dss.Text.Command('Set controlmode=time')
  
  # Resolve o circuito 
  dss.Text.Command('Set mode=daily')
  dss.Text.Command('Set stepsize=1m')
  dss.Text.Command('Set number=1')
  
  n_steps = 1440  # 24 horas, 1 minuto cada
  for i in range(n_steps):
    dss.Solution.Solve()
    dss.Meters.First()
    player_values = dict()
    for j in range(dss.Meters.Count()):
      player_values[j + 1] = dss.Meters.RegisterValues()[0]
      if not os.path.exists('./energies'):
        os.mkdir('./energies')
      with open(f'./energies/{dss.Meters.Name()}.shapley.txt', 'a') as file:
        file.write(f'{dss.Meters.RegisterValues()[0]}\n')
      dss.Meters.Next()

    
    # Binning adaptativo para garantir <= 5 grupos
    interval = 0.1
    min_value = min(player_values.values())
    max_value = max(player_values.values())

    while True:
        bins_values = {}
        bins_indexes = {}
        for player, value in player_values.items():
            bin_index = int((value - min_value) // interval)
            bins_values.setdefault(bin_index, []).append(value)
            bins_indexes.setdefault(bin_index, []).append(player)
        
        if len(bins_values) > 5:
            break
        
        last_bin_values = bins_values.copy()
        last_bin_indexes = bins_indexes.copy()
        interval = interval / 10

    # Print dos grupos de valores
    # print("last_bin_values (valores dos jogadores em cada grupo):")
    # print(last_bin_values)
    # print("last_bin_indexes (índices dos jogadores em cada grupo):")
    # print(last_bin_indexes)

    # Média dos valores em cada grupo
    bins_average = {group: sum(vals) / len(vals) for group, vals in last_bin_values.items()}
    # print("bins_average (média dos valores em cada grupo):")
    # print(bins_average)

    # Preparação para cálculo do Shapley
    players = list(bins_average)
    coalition_values = {}
    for r in range(len(players) + 1):
        for combo in combinations(players, r):
            coalition_values[tuple(sorted(combo))] = sum(bins_average[p] for p in combo)

    # Cálculo dos valores de Shapley para cada grupo
    shapley_dict = {player: calculate_shapley_values(coalition_values, players, player) for player in players}
    # print("shapley_dict (valor de Shapley de cada grupo):")
    # print(shapley_dict)

    # Normalização: menor valor vira 1.0, os outros caem proporcionalmente
    min_shapley = min(shapley_dict.values())
    normalized_shapley = {player: min_shapley / value for player, value in shapley_dict.items()}
    print("normalized_shapley (valores de Shapley normalizados):")
    print(normalized_shapley)
    
    # Novo dicionário: grupos de jogadores como chave, valor normalizado de Shapley como valor
    new_dict = {tuple(last_bin_indexes[k]): normalized_shapley[k] for k in last_bin_indexes}
    print("new_dict (grupos de jogadores -> valor de Shapley normalizado):")
    print(new_dict)
    
    # Atualização das curvas VW
    for group in new_dict.keys():
      dss.XYCurves.First()
      vw_curve_id = 1
      for _ in range(dss.XYCurves.Count()):
        if dss.XYCurves.Name().find('vw_curve_ev_') != -1:
          if vw_curve_id in group:
            dss.XYCurves.YArray([0.0, 0.0, new_dict[group], new_dict[group]])
          vw_curve_id += 1
          
        dss.XYCurves.Next()
 
    