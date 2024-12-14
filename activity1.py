import streamlit as st
import mesa
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import matplotlib.pyplot as plt
import numpy as np
import time

# --- Agent Definitions ---
class Crop(mesa.Agent):
    def __init__(self, unique_id, pos, model, is_ripe=False):
        super().__init__(str(unique_id), model)  # Convert unique_id to string
        self.pos = pos
        self.is_ripe = is_ripe

    def step(self):
        if not self.is_ripe and self.random.random() < 0.1:
            self.is_ripe = True


class PickerRobot(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(str(unique_id), model)  # Convert unique_id to string
        self.pos = pos
        self.target_location = None
        self.storage = 0
        self.storage_capacity = 10

    def step(self):
        if self.storage >= self.storage_capacity:
            self.move_towards((0, 0))  # Go back to base to unload
            if self.pos == (0, 0):
                self.storage = 0
        elif self.target_location:
            self.move_towards(self.target_location)
            if self.pos == self.target_location:
                self.collect_crop()
        else:
            self.move_randomly()

    def collect_crop(self):
        crops = [a for a in self.model.grid.get_cell_list_contents(self.pos) if isinstance(a, Crop) and a.is_ripe]
        if crops:
            crops[0].is_ripe = False
            self.storage += 1

    def move_towards(self, target):
        new_pos = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        best_move = min(new_pos, key=lambda p: self.distance(p, target))
        self.model.grid.move_agent(self, best_move)

    def move_randomly(self):
        moves = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        self.model.grid.move_agent(self, self.random.choice(moves))

    def distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Drone(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(str(unique_id), model)  # Convert unique_id to string
        self.pos = pos

    def step(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        self.model.grid.move_agent(self, self.random.choice(neighbors))


# --- Model Definition ---
class FarmModel(mesa.Model):
    def __init__(self, num_pickers, num_drones, width, height):
        self.num_pickers = num_pickers
        self.num_drones = num_drones
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.width = width
        self.height = height

        # Add crops
        for i in range((width * height) // 4):
            x, y = self.grid.find_empty()
            crop = Crop(i, (x, y), self)
            self.grid.place_agent(crop, (x, y))
            self.schedule.add(crop)

        # Add trees in rows of 3
        for y in range(2, height, 5):  # Spaced every 5 rows
            for x in range(0, width, 3):  # Groups of 3
                tree = Crop(f"tree_{x}_{y}", (x, y), self, is_ripe=False)
                self.grid.place_agent(tree, (x, y))
                self.schedule.add(tree)

        # Add a straight river
        river_col = width // 2
        for y in range(height):
            self.grid.place_agent(Crop(f"river_{y}", (river_col, y), self), (river_col, y))

        # Add robots and drones
        for i in range(num_pickers):
            x, y = self.grid.find_empty()
            picker = PickerRobot(f"picker_{i}", (x, y), self)
            self.grid.place_agent(picker, (x, y))
            self.schedule.add(picker)

        for i in range(num_drones):
            x, y = self.grid.find_empty()
            drone = Drone(f"drone_{i}", (x, y), self)
            self.grid.place_agent(drone, (x, y))
            self.schedule.add(drone)

    def step(self):
        self.schedule.step()

    def get_grid(self):
        grid_data = np.zeros((self.grid.height, self.grid.width, 3), dtype=int)
        for cell in self.grid.coord_iter():
            contents, x, y = cell
            for agent in contents:
                if isinstance(agent, Crop):
                    if agent.unique_id.startswith("river"):
                        grid_data[y][x] = [0, 0, 255]  # Blue for river
                    elif agent.unique_id.startswith("tree"):
                        grid_data[y][x] = [34, 139, 34]  # Forest green for trees
                    else:
                        grid_data[y][x] = [255, 0, 0] if agent.is_ripe else [128, 64, 0]  # Red for ripe crops
                elif isinstance(agent, PickerRobot):
                    grid_data[y][x] = [0, 255, 0]  # Green for picker robots
                elif isinstance(agent, Drone):
                    grid_data[y][x] = [255, 255, 0]  # Yellow for drones
        return grid_data


# --- Streamlit UI ---
st.title("Farm Simulation")

# Sidebar controls
st.sidebar.header("Simulation Controls")
num_pickers = st.sidebar.slider("Number of Picker Robots", 1, 10, 5)
num_drones = st.sidebar.slider("Number of Drones", 1, 5, 2)
grid_width = st.sidebar.slider("Grid Width", 10, 50, 20)
grid_height = st.sidebar.slider("Grid Height", 10, 50, 20)

# Initialize the model
farm_model = FarmModel(num_pickers, num_drones, grid_width, grid_height)

# Sidebar for color legends
st.sidebar.header("Color Legends")
st.sidebar.write("Drone: Yellow")
st.sidebar.write("Picker Robot: Green")
st.sidebar.write("Ripe Crop: Red, Unripe Crop: Brown")
st.sidebar.write("Tree: Forest Green")
st.sidebar.write("River: Blue")

# Simulation controls
placeholder = st.empty()  # Placeholder for dynamic grid updates
stop_button = st.button("Stop Simulation")
run_simulation = st.button("Run Simulation")

if run_simulation:
    while not stop_button:
        farm_model.step()
        grid_data = farm_model.get_grid()

        # Update the grid display
        fig, ax = plt.subplots()
        ax.imshow(grid_data, interpolation="nearest")
        ax.axis("off")
        placeholder.pyplot(fig)

        time.sleep(0.5)  # Control simulation speed
else:
    st.write("Press 'Run Simulation' to start!")
