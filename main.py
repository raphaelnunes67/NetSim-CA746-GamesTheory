from opendssdirect import dss
from constants import TARGET_LOADS_CA746, ColumnsMapVoltages
from plotter import Plotter


if __name__ == '__main__':
  dss.NewContext()

  dss.Text.Command(f'Redirect ./dss/CA746.dss')
  
  dss.Text.Commands(TARGET_LOADS_CA746)
  dss.Text.Command('New Monitor.residence_1_voltages element=Load.residence1 terminal=1 mode=0')
  
  dss.Text.Command('')
  dss.Text.Command('Calcvoltagebases')
  dss.Text.Command('Set mode=daily')
  dss.Text.Command('Set stepsize=1m')
  dss.Text.Command('Set number=1440')
  dss.Text.Command('Set maxcontroliter=1000')
  dss.Text.Command('Set maxiterations=1000')
  dss.Text.Command('Set controlmode=time')
  dss.Solution.Solve()
  
  print(dss.Monitors.AllNames())
  dss.Monitors.Show()
  
  print(dss.Monitors.Channel(ColumnsMapVoltages.V1.value))
  
  plotter = Plotter()
  
  x_values = list(range(len(dss.Monitors.Channel(ColumnsMapVoltages.V1.value))))
  
  plotter.set_data(
    x_values, 
    [list(dss.Monitors.Channel(ColumnsMapVoltages.V1.value))],
    {0: "V1", 1: "V2", 2: "V3"}             
  )
  
  plotter.perform_plot()
  plotter.configure_output(show_grid=True)
  # plotter.show_max_min()
  # plotter.show_figure()
  plotter.save_figure(figure_name="Voltages")
  
  
  