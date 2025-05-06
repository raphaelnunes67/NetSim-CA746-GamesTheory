from opendssdirect import dss


if __name__ == '__main__':
  dss.NewContext()
  dss.Text.Command(f'Redirect ./dss/CA746.dss')

  dss.Loads.First()
  
  print(dss.Loads.Name())
  print(dss.Loads.AllNames())
  