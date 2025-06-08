import matplotlib.pyplot as plt
import os


class Plotter:
    def __init__(self):
        
        self.plt = plt
        self.title = ''
        self.axis_name_x = ''
        self.axis_name_y = ''
        self.x_values = None
        self.y_values = []
        self.labels = dict()
        self.folder_path='./'

    def reset_data(self):
        self.__init__()
    
    def set_images_folder_path(self, path):
        self.folder_path=path
        os.makedirs(name=self.folder_path, exist_ok=True)
        
    def set_data(self, x_values, y_values_list, labels=None):
        """Set the x values and list of y values for plotting"""
        self.x_values = x_values
        self.y_values = y_values_list
        if labels:
            self.labels = labels
        else:
            # Create default labels if none provided
            self.labels = {i: f"Series {i+1}" for i in range(len(y_values_list))}

    def set_labels(self, **kwargs):
        """Set custom labels for each data series"""
        self.labels = kwargs

    def set_title(self, title='title'):
        """Set the plot title"""
        self.title = title

    def set_axis_name(self, y_name='y', x_name='x'):
        """Set axis names/labels"""
        self.axis_name_x = x_name
        self.axis_name_y = y_name

    def perform_plot(self, bases=1.00):
        """Create the plot with all data series"""
        self.plt.figure()
        for i, y_values in enumerate(self.y_values):
            label = self.labels.get(i, f"Series {i+1}")
            self.plt.plot(self.x_values, [y / bases for y in y_values], label=label)

    def configure_output(self, show_legend=True, show_grid=False, limit_up_y=0, limit_down_y=0):
        """Configure plot appearance"""
        self.plt.title(self.title)
        self.plt.xlabel(self.axis_name_x)
        self.plt.ylabel(self.axis_name_y)
        if show_legend:
            self.plt.legend(loc="upper left")
        if show_grid:
            self.plt.grid(True)

        if limit_down_y and limit_up_y:
            self.plt.axhline(y=limit_up_y, color='r', linestyle='--')
            self.plt.axhline(y=limit_down_y, color='r', linestyle='--')

    def show_figure(self):
        """Display the plot"""
        self.plt.show()

    def close_figure(self):
        """Close the plot"""
        self.plt.close()

    def show_max_min(self):
        """Show max and min points on the plot"""
        for i, y_values in enumerate(self.y_values):
            # Find max point
            max_idx = y_values.index(max(y_values))
            x_max = self.x_values[max_idx]
            y_max = y_values[max_idx]
            
            # Find min point
            min_idx = y_values.index(min(y_values))
            x_min = self.x_values[min_idx]
            y_min = y_values[min_idx]
            
            # Plot points
            plt.scatter(x_max, y_max, color='red', s=20)
            plt.annotate(f'({x_max:.2f}, {y_max:.2f})', (x_max, y_max), 
                         textcoords="offset points", xytext=(0, 10), ha='center')
            
            plt.scatter(x_min, y_min, color='black', s=20)
            plt.annotate(f'({x_min:.2f}, {y_min:.2f})', (x_min, y_min), 
                         textcoords="offset points", xytext=(0, -15), ha='center')
            
            # Only adjust y limits for the first series to avoid conflicts
            if i == 0:
                plt.ylim(y_min - 1, y_max + 1)

    def save_figure(self, figure_name, dpi=300):
        """Save the figure to a file"""
        self.plt.savefig(os.path.join(self.folder_path, figure_name), dpi=dpi)
        self.close_figure()


if __name__ == "__main__":
    # Example data
    x = [1, 2, 3, 4, 5]
    y1 = [2, 4, 1, 5, 3]
    y2 = [1, 3, 5, 2, 4]
    
    # Create and configure plotter
    plotter = Plotter()
    plotter.set_data(x, [y1, y2], {0: "First Series", 1: "Second Series"})
    plotter.set_title("Example Plot")
    plotter.set_axis_name("Y Values", "X Values")
    
    # Create and show plot
    plotter.perform_plot()
    plotter.configure_output(show_grid=True)
    plotter.show_max_min()
    
    # Display the plot (commented out for this example)
    plotter.show_figure()
    
    print("Plotter done")