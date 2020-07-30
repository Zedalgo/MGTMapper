class Planet:
    def __init__(self, grid_x, grid_y, size=0, atmosphere=0, temperature=0, hydrographics=0, population=0, government=0, law_level=0, tech_level=0, gas_giant=False):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size = size
        self.atmosphere = atmosphere
        self.temperature = temperature
        self.hydrographics = hydrographics
        self.population = population
        self.government = government
        self.law_level = law_level
        self.tech_level = tech_level
        self.gas_giant = gas_giant
