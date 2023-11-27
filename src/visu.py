import matplotlib.pyplot as plt
import numpy as np


class Field_loc:
    # Field class represents a single field on the map
    def __init__(self, x, y, elevation):
        # Initialize the field's position and elevation
        self.x = x
        self.y = y
        self.elevation = elevation

    def __repr__(self):
        # Return a string representation of the field
        return f'Field(x={self.x}, y={self.y}, elevation={self.elevation})'

    def __eq__(self, other):
        # Return True if the fields are equal, False otherwise
        return self.x == other.x and self.y == other.y and self.elevation == other.elevation

def plot_path(path_data, y_size, x_size):
    # Creating a white matrix
    grid = np.ones((y_size, x_size, 3))  # Initialize with white color (RGB: 1, 1, 1)

    count = 0

    # Plotting the path on the grid
    for field in path_data:
        # Convert path coordinates to matrix indices
        grid_y = field.y  # Reverse y-axis to match Matplotlib's coordinate system
        grid_x = field.x

        # Assign color based on elevation
        color = plt.cm.RdYlGn(field.elevation / 25)  # Convert elevation to a color in the RdYlGn colormap
        

        # Fill the corresponding field in the grid with the color
        grid[grid_y, grid_x] = color[:3]  # Keep only RGB channels
        
        # Annotate the cell with the count number
        plt.text(x=grid_x, y=grid_y, s=str(count))
        count += 1  # Increment the count

    # Display the grid as an image
    plt.imshow(grid, interpolation='nearest', aspect='auto')

    # Adding labels and title
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Colored Path on Grid')

    # Show the plot
    plt.show()

if __name__ == '__main__':
    # Grid dimensions
    x_size = 6
    y_size = 5

    # Example path data: list of Field objects
    path_data = [
        Field_loc(0, 0, 0),
        Field_loc(1, 1, 5),
        Field_loc(2, 2, 10),
        Field_loc(3, 2, 15),
        Field_loc(4, 3, 20),
        Field_loc(5, 3, 22),
        Field_loc(5, 4, 25)
    ]
    plot_path(path_data, y_size, x_size)