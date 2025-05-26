from opendssdirect import dss
from constants import RESIDENTIAL_LOADS, ColumnsMapVoltages, target_residences
from plotter import Plotter
import random


if __name__ == '__main__':
  dss.NewContext()

  # Carrega o arquivo base
  dss.Text.Command(f'Redirect ./dss/CA746.dss')
  
  # Insere as residências
  dss.Text.Commands(RESIDENTIAL_LOADS)
  
  # Insere a curva de carga do VE
  # dss.Text.Command('New Loadshape.shape_ev_1 npts=1440 minterval=1 mult=(file=./data/electrical_vehicles/ev_shapes_charge.csv, col=11)')

  # Insere a curva para o VW para os PVs
  dss.Text.Command('New XyCurve.vw_curve_pv npts=4 Yarray=(1.0, 1.0, 0.0, 0.0) Xarray=(0.0, 1.047244, 1.062992, 2.0)')

  # Insere a curva VW para os VEs
  dss.Text.Command('New XyCurve.vw_curve_ev npts=4 Yarray=(0.0, 0.0, 1.0, 1.0) Xarray=(0.0, 0.866141, 0.921259, 1.0)')
  
  # Modifica todos os valores das residencias, adiciona medidores e 
  # veiculos elétricos
  total_loads = len(dss.Loads.AllNames())
  dss.Loads.First()
  for i in range(total_loads):
    if dss.Loads.Name().find("residence") != -1:
      # Modifica todas as cargas das residências para 2.5kW
      dss.Loads.kW(2.5)
      # Aplica o mesmo loadshape para todos as residencias
      dss.Loads.Daily('RES-Type1-WE')
    
      phase_a, phase_b = random.choice([(1, 2), (2, 3), (1, 3)])
      dss.Text.Command(
        f'New Storage.ev_{i} bus1=EVRES{i}.{phase_a}.{phase_b} phases=2 kV=0.220 kWhrated=10 ' 
        f'pf=0.95 kW=2 conn=delta daily=shape_ev_{i} dispmode=follow %stored=0 '
        'kvarmax=0.44 kvarmaxabs=0.44 model=1 State=CHARGING'
      )
      # dss.Text.Command(
      #   f'New InvControl.control_voltwatt_{i} mode=voltwatt '
      #   'voltage_curvex_ref=rated voltwatt_curve=vw_curve_ev '
      #   'voltwattYaxis=PAVAILABLEPU voltageChangeTolerance=0.001 '
      #   'activePChangeTolerance=0.001 deltaP_factor=0.1 eventLog=true '
      #   'enabled=true voltwattCH_curve=vw_curve_ev monVoltageCalc=MAX '
      #   'RiseFallLimit=-1 '
      #   f'DERlist=(Storage.ev_{i})'
      # )
      
      dss.Text.Command(
        f'New Monitor.{dss.Loads.Name()}_voltages element=Load.{dss.Loads.Name()} terminal=1 mode=0'
      )  
      
    dss.Loads.Next()
  
  # Adiciona em uma residencia única
  # dss.Text.Command(
  #       'New Storage.ev_1 bus1=EVRES14.1.2 phases=2 kV=0.220 kWhrated=10 ' 
  #       'pf=0.95 kW=8 conn=delta daily=shape_ev_1 dispmode=follow %stored=0 '
  #       'kvarmax=0.44 kvarmaxabs=0.44 model=1 State=CHARGING'
  #     )
  
  # dss.Text.Command(
  #       'New InvControl.control_voltwatt_1 mode=voltwatt '
  #       'voltage_curvex_ref=rated voltwatt_curve=vw_curve_ev '
  #       'voltwattYaxis=PAVAILABLEPU voltageChangeTolerance=0.001 '
  #       'activePChangeTolerance=0.001 deltaP_factor=0.1 eventLog=true '
  #       'enabled=true voltwattCH_curve=vw_curve_ev monVoltageCalc=MAX '
  #       'RiseFallLimit=-1 '
  #       'DERlist=(Storage.ev_1)'
  #     )
      
  # Resolve o circuito
  dss.Text.Command('Calcvoltagebases')
  dss.Text.Command('Set mode=daily')
  dss.Text.Command('Set stepsize=1m')
  dss.Text.Command('Set number=1440')
  dss.Text.Command('Set maxcontroliter=1000')
  dss.Text.Command('Set maxiterations=1000')
  dss.Text.Command('Set controlmode=time')
  dss.Solution.Solve()
    
  total_monitors = len(dss.Monitors.AllNames())
  dss.Monitors.First()
  plotter = Plotter()
  
  for i in range(total_monitors):
    if (dss.Monitors.Name().find('voltages') != -1):
      
      for id in target_residences:
        if (dss.Monitors.Name().find('residence'+str(id)+'_') != -1):
          x_values = list(range(len(dss.Monitors.Channel(ColumnsMapVoltages.V1.value))))
          
          plotter.set_data(
            x_values, 
            [list(dss.Monitors.Channel(ColumnsMapVoltages.V1.value)), 
            list(dss.Monitors.Channel(ColumnsMapVoltages.V2.value)),
            list(dss.Monitors.Channel(ColumnsMapVoltages.V3.value))],
            {0: "V1", 1: "V2", 2: "V3"}           
          )
          plotter.perform_plot()
          plotter.configure_output(show_grid=True)
          plotter.save_figure(figure_name=dss.Monitors.Name())
    dss.Monitors.Next()

      
  
  