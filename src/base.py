from opendssdirect import dss
from constants import ColumnsMapVoltages, ColumnsMapPowers
from plotter import Plotter
import random
import csv


if __name__ == '__main__':
  control_modes = ('vw', '')
  target_residences = (1, 4, 14, 20, 24)
  target_residence_ve = 24
  
  for control_mode in control_modes:
    dss.NewContext()
    # Carrega o arquivo base
    dss.Text.Command('Redirect ../dss/CA746.dss')
    
    # Insere a curva de carga do VE
    column_index = 1
    column_data = []
    with open('../data/electrical_vehicles/ev_shapes_charge.csv') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      column_data = [row[column_index] for row in csv_reader]
  
        
    column_values_str = ' '.join(map(str, column_data))
    dss.Text.Command(f'New Loadshape.shape_ev_1 npts=1440 minterval=1 mult=({column_values_str})')

    # Insere a curva para o VW para os PVs
    dss.Text.Command('New XyCurve.vw_curve_pv npts=4 Yarray=(1.0, 1.0, 0.0, 0.0) Xarray=(0.0, 1.047244, 1.062992, 2.0)')

    # Insere a curva VW para os VEs
    dss.Text.Command('New XyCurve.vw_curve_ev npts=4 Yarray=(0.0, 0.0, 1.0, 1.0) Xarray=(0.0, 0.866141, 0.921259, 1.0)')
    # dss.Text.Command('New XyCurve.vw_curve_ev npts=4 Yarray=(0.0, 0.0, 1.0, 1.0) Xarray=(0.0, 1.0, 1.0, 1.0)')
    # Modifica todos os valores das residencias, adiciona medidores e 
    # veiculos elétricos
    
    dss.Loads.First()
    n_res = 1
    for _ in range(dss.Loads.Count()):
      if dss.Loads.Name().find("residence") != -1:
        # Modifica todas as cargas das residências para 2.5kW
        dss.Loads.kW(2.5)
        # Aplica o mesmo loadshape para todos as residencias
        dss.Loads.Daily('RES-Type1-WE')
        # if n_res == target_residence_ve:
        phase_a, phase_b = random.choice([(1, 2)])
        
        # Insere o VE
        dss.Text.Command(
          f'New Storage.ev_{n_res} bus1=EVRES{n_res}.{phase_a}.{phase_b} phases=2 kV=0.220 kWhrated=40 kWhstored=0 ' 
          f'pf=0.95 kW=24 kWrated=12 conn=delta daily=shape_ev_1 dispmode=FOLLOW %stored=0 '
          'model=1 State=CHARGING %reserve=100 %EffCharge=100 '
          '%Discharge=0 TimeChargeTrig=0 %Charge=100'
        )
        if control_mode:
          dss.Text.Command(
            f'New InvControl.control_voltwatt_{n_res} mode=voltwatt '
            'voltage_curvex_ref=rated '
            'voltageChangeTolerance=0.01 '
            'activePChangeTolerance=0.01 deltaP_factor=0.1 '
            'enabled=true voltwattCH_curve=vw_curve_ev monVoltageCalc=MAX '
            'RiseFallLimit=-1 voltwattYaxis=PMPPPU '
            f'DERlist=(Storage.ev_{n_res})'
          )
        if n_res in target_residences:
          
          voltage_monitor_name = f'{dss.Loads.Name()}_voltages' if not control_mode else  f'{dss.Loads.Name()}_voltages_{control_mode}'
          
          dss.Text.Command(
            f'New Monitor.{voltage_monitor_name} element=Load.{dss.Loads.Name()} terminal=1 mode=0'
          )
          
          power_monitor_name = f'{dss.Loads.Name()}_powers' if not control_mode else  f'{dss.Loads.Name()}_powers_{control_mode}'
          
          dss.Text.Command(
            f'New Monitor.{power_monitor_name} element=Line.LINE_EV{n_res} terminal=1 mode=1 ppolar=no'
          )
          
          meter_name = f'{dss.Loads.Name()}_meter' if not control_mode else  f'{dss.Loads.Name()}_meter_{control_mode}'
          dss.Text.Command(
            f'New EnergyMeter.{meter_name} '
            f'element=line.LINE_EV{n_res} terminal=1'
          )
        n_res += 1
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
      # if i == 900:
      #   dss.XYCurves.First()
      #   dss.XYCurves.Next()
      #   dss.XYCurves.Next()
      #   dss.XYCurves.Next()
      #   dss.XYCurves.YArray([0.0, 0.92, 0.96, 1.0])
      #   print(dss.XYCurves.YArray())
      dss.Solution.Solve()
      # # Obter os dados de energia por minuto
      # total = len(dss.Meters.AllNames())
      # dss.Meters.First()
      # for _ in range(total):
      #   if dss.Meters.Name().find('24') != -1:
      #     print(f'{dss.Meters.Name()}: {dss.Meters.RegisterValues()[0]} kWh')

      #   dss.Meters.Next()

    total_monitors = len(dss.Monitors.AllNames())
    dss.Monitors.First()
    plotter = Plotter()
    plotter.set_images_folder_path('./imgs')
    
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
            figure_name = dss.Monitors.Name() if not control_mode else dss.Monitors.Name() + '_' + control_mode
            plotter.save_figure(figure_name=figure_name)
      
      elif (dss.Monitors.Name().find('powers') != -1):
        
        for id in target_residences:
            if (dss.Monitors.Name().find('residence'+str(id)+'_') != -1):
              # dss.Monitors.Show()
              x_values = list(range(len(dss.Monitors.Channel(ColumnsMapPowers.P1.value))))
              plotter.set_data(
                  x_values, 
                  [list(dss.Monitors.Channel(ColumnsMapPowers.P1.value)), 
                    list(dss.Monitors.Channel(ColumnsMapPowers.P2.value)),
                    list(dss.Monitors.Channel(ColumnsMapPowers.P3.value))],
                  {0: "P1", 1: "P2", 2: "P3"}           
              )
              plotter.perform_plot()
              plotter.configure_output(show_grid=True)
              plotter.save_figure(figure_name=dss.Monitors.Name())
          
      dss.Monitors.Next()
    
    total = len(dss.Meters.AllNames())
    dss.Meters.First()
    for _ in range(total):
      print(f'{dss.Meters.Name()}: {dss.Meters.RegisterValues()[0]} kWh')
      
      dss.Meters.Next()
      
  
  