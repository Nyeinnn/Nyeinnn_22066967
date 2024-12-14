
# Farm Simulation Project

This project simulates a farm with crops, picker robots, and drones. The model tracks the activities of robots as they collect ripe crops, and drones move across the grid and send a signal with coordinates of where the crops need to be collected. The simulation allows one to visualize the farm environment, adjust the number of picker robots and drones, and track performance metrics such as crop collection efficiency and robot utilization.

## Features

- **Crops**: Crops grow over time, becoming ripe and ready for collection.
- **Picker Robots**: Robots move across the grid, collecting ripe crops and returning them to the base.
- **Drones**: Drones move across the grid and send a signal with coordinates of where the crops need to be collected.
- **River and Trees**: A river is placed along the center, and trees are scattered across the grid.
- **Metrics**:
  - **Crop Collection Efficiency**: The efficiency of crop collection
  - **Robot Utilization**: Tracks the amount of time picker robots are actively moving.

## Requirements

- Python 3.x
- Streamlit
- Mesa
- Numpy
- Matplotlib



Make sure you have the necessary Python environment set up (e.g., using `virtualenv` or `conda`).

## Usage

### Running the simulation:
1. In the terminal, navigate to the project directory and run the following command:

```bash
streamlit run filename.py
```

2. The simulation interface will open in your web browser. You can control the number of picker robots and drones, as well as the grid size, from the sidebar.

3. Press **Run Simulation** to start the simulation. The farm grid will be updated every step, showing the positions of robots, drones, crops, and other elements.

4. After the simulation completes, two performance metrics will be displayed in the sidebar:
   - **Crop Collection Efficiency**
   - **Robot Utilization**: The percentage of steps the picker robots are active.

### Controls
- **Number of Picker Robots**: Adjust the number of picker robots on the farm.
- **Number of Drones**: Adjust the number of drones on the farm.
- **Grid Width**: Adjust the width of the farm grid.
- **Grid Height**: Adjust the height of the farm grid.

### Visualization
The farm is displayed as a grid where:
- **Crops**: Ripe crops are red, and unripe crops are brown.
- **Picker Robots**: Green squares represent picker robots.
- **Drones**: Yellow squares represent drones.
- **Trees**: Forest green squares represent trees.
- **River**: Blue squares represent the river running down the center.

## Performance Metrics

### Crop Collection Efficiency
This metric represents the efficiency of crop collection. 
### Robot Utilization
This metric tracks the percentage of time that picker robots are actively moving and collecting crops.

