import random

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


class EvPlotter:
    def __init__(self, filepath, column=None):
        self.filepath = Path(filepath)
        self.plt = plt
        self.title = ''
        self.axis_name_x = 'Line Number'
        self.axis_name_y = 'Average Value'
        self.x_values = []
        self.y_values = []
        if column is None:
            self.read_all_data()
        else:
            self.column = column
            self.read_line_data()
            

    def read_line_data(self):
        data = pd.read_csv(self.filepath)
        self.y_values = data.iloc[:, self.column].tolist()
        self.x_values = list(range(1, len(self.y_values) + 1))

    def read_all_data(self):
        data = pd.read_csv(self.filepath)
        self.y_values = data.mean(axis=1).tolist()
        self.x_values = list(range(1, len(self.y_values) + 1))

    def set_title(self, title):
        self.title = title

    def set_axis_name(self, y_name='Average Value', x_name='Column Number'):
        self.axis_name_y = y_name
        self.axis_name_x = x_name

    def plot_data(self):
        x_values = list(range(1, len(self.y_values) + 1))
        self.plt.plot(x_values, self.y_values, marker='o', label='Average per Line')

    def configure_plot(self, show_legend=True, show_grid=False):
        self.plt.title(self.title)
        self.plt.xlabel(self.axis_name_x)
        self.plt.ylabel(self.axis_name_y)
        if show_legend:
            self.plt.legend(loc="upper left")
        if show_grid:
            self.plt.grid(True)

    def show_plot(self):
        self.plt.show()

    def save_plot(self, filename, dpi=300):
        self.plt.savefig(Path(self.filepath.parent / filename), dpi=dpi)


if __name__ == '__main__':
    column = 1
    plotter = EvPlotter('../data/electrical_vehicles/ev_shapes_charge.csv', column)
    plotter.set_title(f'Amostra {column}')
    plotter.set_axis_name(y_name='Valor', x_name='Tempo (s)')
    plotter.plot_data()
    plotter.configure_plot(show_legend=False, show_grid=True)
    plotter.save_plot(filename=f'ev_shape_{column}.png')
    plotter.show_plot()

    # plotter = EvPlotter('../data/electrical_vehicles/ev_shapes.csv')
    # plotter.set_title(f'Dados VE')
    # plotter.set_axis_name(y_name='Valor', x_name='Tempo (s)')
    # plotter.plot_data()
    # plotter.configure_plot(show_legend=False, show_grid=True)
    # plotter.save_plot(filename='ev_shapes.png')
    # plotter.show_plot()