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
