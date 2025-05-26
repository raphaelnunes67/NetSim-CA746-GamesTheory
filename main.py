from opendssdirect import dss
from constants import *
import random


def generate_random_target_residences_ev(residences_quantity):
  return random.sample(range(1, TOTAL_RESIDENCES + 1), residences_quantity)
    

def generate_random_target_residences_pv(residences_quantity):
  return random.sample(range(1, TOTAL_RESIDENCES + 1), residences_quantity)


def generate_random_irradiation_week():
    total_possibilities = len(PV_SHAPES_POSSIBILITIES)
    irradiations = []
    for _ in range(7):
      index = random.randint(0, total_possibilities - 1)
      irradiations.append(PV_SHAPES_POSSIBILITIES[index])
    
    return irradiations
 
def generate_random_pv_powers_residences(residences_quantity):
  pv_powers = []
  for _ in range(residences_quantity):
    panel_power = random.randint(
      MaxPowerPVKW.MIN_KW.value, 
      MaxPowerPVKW.MAX_KW.value + 1
    )
    inverter_power = panel_power + 0.5
    pv_powers.append((panel_power, inverter_power))
  
  return pv_powers

def generate_random_ev_chargers_powers(residences_quantity):
  ev_charger_powers = []
  total_possibilities = len(EV_CHARGER_POWER_POSSIBILITIES)
  for _ in range(residences_quantity):
    index = random.randint(0, total_possibilities - 1)
    ev_charger_powers.append(EV_CHARGER_POWER_POSSIBILITIES[index])
  
  return ev_charger_powers

def generate_random_ev_loadshapes(residences_quantity):
  ev_loadshapes_week = []
  for _ in range(7):
    ev_loadshapes = []
    for _ in range(residences_quantity):
      index = random.randint(1, 5001)
      ev_loadshapes.append(index)
    ev_loadshapes_week.append(ev_loadshapes)
      
  return ev_loadshapes_week


def generate_random_ev_phases(residences_quantity):
  ev_phases = []
  for _ in range(residences_quantity):
    phase_a, phase_b = random.choice([(1, 2), (2, 3), (1, 3)])
    ev_phases.append((phase_a, phase_b))

  return ev_phases

def generate_random_pv_phases(residences_quantity):
  pv_phases = []
  for _ in range(residences_quantity):
    phase_a, phase_b = random.choice([(1, 2), (2, 3), (1, 3)])
    pv_phases.append((phase_a, phase_b))

  return pv_phases


if __name__ == '__main__':
  
  print('Week simulation started!')
  
  # EV and PV percentages
  PERCENTAGE_EV = 25
  PERCENTAGE_PV = 25
  
  EV_RESIDENCES_QUANTITY = int(round(TOTAL_RESIDENCES * PERCENTAGE_EV / 100, 1))
  PV_RESIDENCES_QUANTITY = int(round(TOTAL_RESIDENCES * PERCENTAGE_PV / 100, 1))
  
  print(f'EV Penetration Level = {PERCENTAGE_EV}')
  print(f'PV Penetration Level = {PERCENTAGE_PV}')
  
  print(f'Total of residences with EV: {EV_RESIDENCES_QUANTITY}')
  print(f'Total of residences with PV: {PV_RESIDENCES_QUANTITY}')
  
  # Generate random values
  residences_ev = generate_random_target_residences_ev(EV_RESIDENCES_QUANTITY)
  residences_pv = generate_random_target_residences_pv(PV_RESIDENCES_QUANTITY)
  irradiations = generate_random_irradiation_week()
  pv_powers_residences = generate_random_pv_powers_residences(PV_RESIDENCES_QUANTITY)
  ev_chargers_powers = generate_random_ev_chargers_powers(EV_RESIDENCES_QUANTITY)
  ev_loadshapes = generate_random_ev_loadshapes(EV_RESIDENCES_QUANTITY)
  ev_phases = generate_random_ev_phases(EV_RESIDENCES_QUANTITY)
  pv_phases = generate_random_pv_phases(PV_RESIDENCES_QUANTITY)
  
  # BEGIN WEEK SIMULATION IN DAILY MODE
  for day_number in range(0, 7):
    
    print(f'Running simulation - day {day_number + 1}')
    
    dss.NewContext()
    # Load base file
    dss.Text.Command(f'Redirect ./dss/CA746.dss')
    
    # Insert VW curve for PV
    dss.Text.Command(f'New XyCurve.vw_curve_pv npts=4 Yarray=(1.0, 1.0, 0.0, 0.0) Xarray=(0.0, 1.047244, 1.062992, 2.0)')

    # Insert VW curve for EV
    dss.Text.Command('New XyCurve.vw_curve_ev npts=4 Yarray=(0.0, 0.0, 1.0, 1.0) Xarray=(0.0, 0.866141, 0.921259, 1.0)')
    
    for i in range (EV_RESIDENCES_QUANTITY):
      # Insert new EV system loadshape and storage  
      dss.Text.Command(f'New Loadshape.shape_ev_{residences_ev[i]} npts=1440 minterval=1 mult=(file=./data/electrical_vehicles/ev_shapes_charge.csv, col={ev_loadshapes[day_number][i]})')
      dss.Text.Command(
        f'New Storage.ev_{residences_ev[i]} bus1=EVRES{residences_ev[i]}.{ev_phases[i][0]}.{ev_phases[i][1]} phases=2 kV=0.220 kWhrated={EV_BATTERY_CAPACITY_POSSIBILITIES} ' 
        f'pf=0.95 kW=2 conn=delta daily=shape_ev_{residences_ev[i]} dispmode=follow %stored=0 '
        'kvarmax=0.44 kvarmaxabs=0.44 model=1 State=CHARGING'
      )
      # Insert VW control in EV chargers
      dss.Text.Command(
        f'New InvControl.control_voltwatt_ev{residences_ev[i]} mode=voltwatt '
        'voltage_curvex_ref=rated voltwatt_curve=vw_curve_ev '
        'voltwattYaxis=PAVAILABLEPU voltageChangeTolerance=0.001 '
        'activePChangeTolerance=0.001 deltaP_factor=0.1 eventLog=true '
        'enabled=true voltwattCH_curve=vw_curve_ev monVoltageCalc=MAX '
        'RiseFallLimit=-1 '
        f'DERlist=(Storage.ev_{residences_ev[i]})'
      )
      
      # Insert Energy Meters in EV Lines
      dss.Text.Command(
          f'New EnergyMeter.residence_EV{residences_ev[i]} '
          f'element=line.LINE_EV{residences_ev[i]} terminal=1'
      )
      
    for i in range (PV_RESIDENCES_QUANTITY):
      # Insert PV System
      dss.Text.Command(
        f'New PVSystem.pv_{residences_pv[i]} '
        f'bus1=PVRES{residences_pv[i]}.{pv_phases[i][0]}.{pv_phases[i][1]} '
        f'phases=2 conn=delta  kV=0.220  kVA={pv_powers_residences[i][1]} '
        f'pmpp={pv_powers_residences[i][1]} '
        'pf=0.95 ' 
        f'daily={irradiations[day_number]} varFollowInverter=true '
        '%cutin=0.1 %cutout=0.1'
      )
      
      # Insert VW control in PV Systems
      dss.Text.Command(
        f'New InvControl.voltwatt_pv{residences_pv[i]} '
        'mode=voltwatt '
        'voltage_curvex_ref=rated '
        'voltwatt_curve=vw_curve_pv '
        'refReactivePower=VARMAX '
        'monVoltageCalc=MAX '
        'RiseFallLimit=-1 '
        'voltwattYaxis=PAVAILABLEPU '
        'voltageChangeTolerance=0.01 '
        'activePChangeTolerance=0.01 '
        'deltaP_factor=0.1 '
        'eventLog=yes '
        'enabled=true '
        f'DERlist=(PvSystem.pv_{residences_pv[i]})'
      )
      
      # Insert Energy Meters in PV Lines
      dss.Text.Command(
          f'New EnergyMeter.residence_PV{residences_pv[i]} '
          f'element=line.LINE_PV{residences_pv[i]} terminal=1'
      )
      
    # Solve the circuit
    dss.Text.Command('Calcvoltagebases')
    dss.Text.Command('Set mode=daily')
    dss.Text.Command('Set stepsize=1m')
    dss.Text.Command('Set number=1440')
    dss.Text.Command('Set maxcontroliter=1000')
    dss.Text.Command('Set maxiterations=1000')
    dss.Text.Command('Set controlmode=time')
    dss.Solution.Solve()
      
    total = len(dss.Meters.AllNames())
    dss.Meters.First()
    for _ in range(total):
      print(f'{dss.Meters.Name()}: {dss.Meters.RegisterValues()[0]}')
      dss.Meters.Next()

  
  