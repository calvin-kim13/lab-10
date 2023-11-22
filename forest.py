"""Calvin Kim - CS 5001 - Day 9 - Project 9 / Lab 9: Pyglet Window"""

# Imports
from random import randrange, choice
import datetime
import pyglet
from pyglet.window import key
import pyglet_colors
import jsonpickle

# Constants
WIDTH = 800
HEIGHT = 600
MARGIN = 50


# Global Variables
window = pyglet.window.Window()
forest = None
pause = False


# Window Events
@window.event
def on_draw():
    """Pyglet window event for drawing images."""
    window.clear()
    forest.draw()


@window.event
def on_key_press(symbol, _):
    """Pyglet key press function that looks for SPACE key and changes keep_going to False"""
    global pause
    if symbol == key.SPACE:
        pause = True


def update(_):
    """Pyglet update function that updates or refreshes the window to allow movement."""
    if not pause:
        forest.move()
    else:
        pass


# Classes
class ForestConfig:
    """Forest configuration data class"""

    def __init__(
        self, trees, tree_size, babies, flock_size, adult_size, baby_size, flyer_size
    ):
        self.trees = trees
        self.tree_size = tree_size
        self.babies = babies
        self.flock_size = flock_size
        self.adult_size = adult_size
        self.baby_size = baby_size
        self.flyer_size = flyer_size


config = ForestConfig(0, 0, 0, 0, 0, 0, 0)


class Forest:
    """Forest class that instantiates tree objects with a draw method."""

    def __init__(self):
        self.trees = []
        self.animals = []
        for _ in range(config.trees):
            tree = Tree(
                randrange(MARGIN, WIDTH - MARGIN),
                randrange(MARGIN, HEIGHT - MARGIN),
                config.tree_size,
            )
            self.trees.append(tree)

    def create_families(self):
        """Create the different families in the forest."""
        family1 = Family(
            randrange(MARGIN, WIDTH - MARGIN),
            randrange(MARGIN, HEIGHT - MARGIN),
            pyglet_colors.BLUE2,
            Bear,
        )
        self.animals.append(family1)
        family2 = Family(
            randrange(MARGIN, WIDTH - MARGIN),
            randrange(MARGIN, HEIGHT - MARGIN),
            pyglet_colors.GREEN2,
            Rabbit,
        )
        self.animals.append(family2)
        family3 = Flock(pyglet_colors.PINK, Eagle, self.trees)
        self.animals.append(family3)

    def draw(self):
        """Draw method that draws the tree objects instantiated."""
        for tree in self.trees:
            tree.draw()
        for family in self.animals:
            family.draw()

    def move(self):
        """Forest move method that makes each family move."""
        for family in self.animals:
            family.move()


class Tree:
    """Tree class that holds shapes as attributes to draw a tree with a draw method."""

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.batch = pyglet.graphics.Batch()
        self.trunk = pyglet.shapes.Rectangle(
            x - (size // 30),
            y - size,
            size * 0.08,
            size * 0.8,
            pyglet_colors.BROWN,
            batch=self.batch,
        )
        self.circle = pyglet.shapes.Circle(
            x,
            y,
            size * 0.3,
            color=pyglet_colors.DARKSEAGREEN,
            batch=self.batch,
        )

    def draw(self):
        """Draws the batch of shapes at once."""
        self.batch.draw()

    def perch_x(self):
        """Method that returns a x value for the location of the flyer."""
        return self.x

    def perch_y(self):
        """Method that returns a y value for the location of the flyer."""
        return self.y


class Animal:
    """Animal class with shape attributes to draw an animal."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.batch = pyglet.shapes.Batch()
        self.shape_list = []

    def draw(self):
        """Draw method to draw the batch of shapes to output an animal drawing."""
        self.batch.draw()

    def move(self, x, y):
        """Moves each animal"""
        dx = x - self.x
        dy = y - self.y
        for shape in self.shape_list:
            shape.x += dx
            shape.y += dy
        self.x = x
        self.y = y


class Bear(Animal):
    """Bear class that is a sub-class of Animal"""

    def __init__(self, x, y, size, color):
        super().__init__(x, y)
        self.shape_list.append(
            pyglet.shapes.Circle(
                x,
                y,
                radius=size / 3,
                color=color,
                batch=self.batch,
            )
        )


class Rabbit(Animal):
    """Rabbit class that is a sub-class of Animal"""

    def __init__(self, x, y, size, color):
        super().__init__(x, y)
        self.shape_list.append(
            pyglet.shapes.Rectangle(
                x,
                y,
                width=size // 2,
                height=size // 2.5,
                color=color,
                batch=self.batch,
            )
        )


class Eagle(Animal):
    """Eagle class that creates a flyer animal."""

    def __init__(self, x, y, size, color):
        super().__init__(x, y)
        self.shape_list.append(
            pyglet.shapes.Rectangle(
                x,
                y,
                width=size / 2,
                height=size / 1.1,
                color=color,
                batch=self.batch,
            )
        )
        self.last_moved = datetime.datetime.now().second

    def move(self, x, y):
        """Eagle move method that updates each shapes x and y coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        if (datetime.datetime.now().second - self.last_moved) >= randrange(3, 5):
            super().move(x, y)
            self.last_moved = datetime.datetime.now().second


class Flock:
    """Flock class which generates the x and y value of where the flyer should land."""

    def __init__(self, color, animal_class, trees):
        self.flyers = []
        self.trees = trees

        for _ in range(config.flock_size):
            tree = choice(self.trees)
            flyer = animal_class(
                tree.perch_x(), tree.perch_y(), config.flyer_size, color
            )
            self.flyers.append(flyer)

    def draw(self):
        """Draws flyers"""
        for flyer in self.flyers:
            flyer.draw()

    def move(self):
        """Flock move method"""
        for flyer in self.flyers:
            tree = choice(self.trees)
            flyer.move(tree.perch_x(), tree.perch_y())


class Family:
    """Family class to store mom, dad, and cubs as attributes."""

    def __init__(self, x, y, color, animal_class):
        # x and y
        self.x = x
        self.y = y

        # dx and dy
        self.dx = randrange(-20, 20)
        self.dy = randrange(-20, 20)

        # Animals list
        self.animals = []

        # Mama
        self.mama = animal_class(x, y, config.adult_size, color)
        self.animals.append(self.mama)

        # Babies
        self.babies = []
        for _ in range(config.babies):
            baby = animal_class(
                x + randrange(-40, 40),
                y + randrange(-10, 5),
                config.baby_size,
                color,
            )
            self.animals.append(baby)
            self.babies.append(baby)

        # Papa
        self.papa = animal_class(x + 30, y + 25, config.adult_size, color)
        self.animals.append(self.papa)

    def draw(self):
        """Draws the mom, dad, and cubs."""
        for animal in self.animals:
            animal.draw()

    def move(self):
        """Family move method that moves mom, dad, and cubs by certain amount."""
        self.x += self.dx
        self.y += self.dy
        if self.x < 0:
            self.x = -self.x
            self.dx = randrange(10, 20)
        elif self.x > window.width:
            self.dx = randrange(-20, -10)
        if self.y < 0:
            self.y = -self.y
            self.dy = randrange(10, 20)
        elif self.y > window.height:
            self.dy = randrange(-20, -10)
        self.mama.move(self.x, self.y)
        for baby in self.babies:
            baby.move(
                self.x + randrange(-40, 40),
                self.y + randrange(-10, 5),
            )
        self.papa.move(self.x + 30, self.y + 25)


class App:
    """App class that holds the main app functionality with a run method."""

    def run(self):
        """Run method that runs the pyglet library."""
        global forest
        forest = Forest()
        forest.create_families()
        pyglet.clock.schedule_interval(update, 1 / 3)
        pyglet.app.run()


# Main Program
if __name__ == "__main__":
    # Populate the config
    with open(
        file="/Users/calvinkim/Desktop/cs_5001/Module 9/Project 9/config.json", mode="r"
    ) as config_file:
        data = jsonpickle.decode(config_file.read())
        trees = data["trees"]
        tree_size = data["tree_size"]
        babies = data["babies"]
        flock_size = data["flock_size"]
        adult_size = data["adult_size"]
        baby_size = data["baby_size"]
        flyer_size = data["flyer_size"]
        config = ForestConfig(
            trees, tree_size, babies, flock_size, adult_size, baby_size, flyer_size
        )
    app = App()
    app.run()
