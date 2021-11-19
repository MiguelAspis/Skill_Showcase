import numpy as np
import matplotlib.pyplot as plt
import time as time

class Sandpile():
    """Sandpile class

    """
    def __init__(self, grid = None, height = 3, width = 3, grains = 4, max_timesteps = 1000000, live_view=False) -> None:
        """Create a sandpile object
        
        Args:
            grid (2d list, optional): grid values to begin the iterations on. Defaults to None.
            height (int, optional): height of the grid. Defaults to 3.
            width (int, optional): width of the grid. Defaults to 3.
            grains (int, optional): maximum grains allowed on a tile (must be divisible by 4). Defaults to 4.
            max_timesteps (int, optional): defines number of timesteps sandpile will run (convergence not guaranteed). Defaults to 10000.
            live_view (Bool, optional): defines if you want a live view of the sandpile process (significantly slows the process down). Defaults to False.
        """

        # Setting the classes max grain per pile and max timesteps(for automatic case)
        self.max_grains = grains
        self.max_iterations = max_timesteps
        self.live_view = live_view

        # If no grid is given we create one out of zeros, else we use the one given
        if grid == None:
            self.height = height
            self.width = width
            self.grid = np.zeros((height,width), int)
            
        else:
            self.height = len(grid)
            self.width = len(grid[0])
            self.grid = np.array(grid)
            
    
    def topple(self, x, y):
        """does the toppling operation on a given pile 

        Args:
            x (int): x-coordinate
            y (int): y-coordinate
        """

        # Resetting pile after surpassing max limit
        pile = self.grid[x,y]
        incr = pile // self.max_grains
        new = pile % self.max_grains
        self.grid[x,y] = new

        # increasing height of the sand in neighboring piles
        self.grid[x-1,y] += incr
        self.grid[x,y-1] += incr
        self.grid[x+1,y] += incr
        self.grid[x,y+1] += incr

        # border case
        self.grid[0] = self.grid[-1] = 0
        self.grid[:, 0] = self.grid[:, -1] = 0

    
    def set_pile(self, x, y, value):
        """Allows to manually set value in a pile

        Args:
            x (int): x-coordinate
            y (int): y-coordinate
            value (int): number of grains to put in a given pile
        """
        self.grid[x,y] = value

    def run(self):
        """runs the sandpile algorithm

        """

        start = time.time()
        iterations = 0

        # check if grid is empty, if it is go into "automatic" mode
        if not self.grid.any():
            #Loop through pre-set iteration number 
            for i in range(self.max_iterations):
                # generate random position in which to add a grain of sand
                rand_x = round(float(np.random.uniform(0,self.width-1,1)))
                rand_y = round(float(np.random.uniform(0,self.height-1,1)))
                # add a grain of sand into pile
                self.grid[rand_x,rand_y] += 1
                # if a pile is unstable start the toppling process
                if np.max(self.grid) >= self.max_grains:
                    while np.max(self.grid) >= self.max_grains:
                        x, y = np.where(self.grid >= self.max_grains)
                        self.topple(x, y)        
                iterations += 1
                # if live_view is set show grid every 20 iterations
                if self.live_view:
                    if iterations % 1000 == 0:
                        plt.clf()
                        heatmap = plt.pcolor(self.grid)
                        plt.axis('off')
                        plt.imshow(self.grid)
                        plt.colorbar(heatmap, ticks=range(self.max_grains))
                        plt.pause(1e-17)
                    
                print("--- %d iterations %s seconds ---" % (iterations, time.time() - start))
        #if grid already has values in it
        else:
            #while a pile is bigger than allowed topple the piles
            while np.max(self.grid) >= self.max_grains:
                x,y = np.where(self.grid >= self.max_grains)
                self.topple(x,y)
                iterations += 1
                # if live_view is set show grid every 20 iterations
                if self.live_view:
                    if iterations % 1000 == 0:
                        plt.clf()
                        heatmap = plt.pcolor(self.grid)
                        plt.axis('off')
                        plt.imshow(self.grid)
                        plt.colorbar(heatmap, ticks=range(self.max_grains))
                        plt.pause(1e-17)
                    
                print("--- %d iterations %s seconds ---" % (iterations, time.time() - start))
    
    def show(self, file="sandpile.jpg"):
        """show and save the grid final state

        Args:
            file (str, optional): filename on which the image should be saved Defaults to "sandpile.jpg".
        """
        heatmap = plt.pcolor(self.grid)
        plt.axis('off')
        plt.imshow(self.grid)
        plt.colorbar(heatmap, ticks=range(self.max_grains))
        plt.savefig(file, bbox_inches='tight')
        plt.show()
        
    def __add__(self, other):
        """sums 2 sandpiles of same size and start algorithm on sum

        Args:
            other (Sandpile): sandpile object to be added

        Returns:
            result.run(): starts the algorithm on the sum 
        """
        result = Sandpile(height = self.height, width = self.width)
        try:
            result.grid = self.grid + other.grid
            return result.run()
        except ValueError:
            print("ValueError: grid sizes must match")

# Example usage of class
if __name__ == '__main__':
    pile = Sandpile(height=301,width=301, live_view=True)
    #pile.set_pile(250,250,2**18)
    pile.run()
    pile.show()
