from opendssdirect import dss


if __name__ == '__main__':
  dss.NewContext()
  
  for i in range (1000):
    dss.Text.Command(f'Redirect ./dss/CA746.dss')
    dss.Text.Command('Set voltagebases=[13.8 0.220]')
    dss.Text.Command('Calcvoltagebases')
    dss.Text.Command('Set mode=daily')
    dss.Text.Command('Set stepsize=1m')
    dss.Text.Command('Set number=1440')
    dss.Text.Command('Set maxcontroliter=1000')
    dss.Text.Command('Set maxiterations=1000')
    dss.Text.Command('Set controlmode=time')
    dss.Solution.Solve()
    print(f'Finalizada a simulação {i + 1}')
    
  # dss.Loads.First()
  
  # print(dss.Loads.Name())
  # print(dss.Loads.AllNames())
  
  
  