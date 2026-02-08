import pandas as pd
import os

from src.distance_matrix import create_distance_matrix
from src.vrp_solver import solve_vrp
from src.map_visualization import plot_routes

# -------------------- Paths --------------------
DATA_PATH = os.path.join("data", "delivery_location.csv")
OUTPUT_DIR = "outputs"
OUTPUT_TXT = os.path.join(OUTPUT_DIR, "optimized_routes.txt")

# Create outputs folder if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------- Load Data --------------------
df = pd.read_csv(DATA_PATH)

locations = list(zip(df["latitude"], df["longitude"]))

# -------------------- Distance Matrix --------------------
distance_matrix = create_distance_matrix(locations)

# -------------------- Solve VRP --------------------
routes = solve_vrp(distance_matrix, num_vehicles=2)

print("DEBUG routes:", routes)

# -------------------- Save Optimized Routes --------------------
with open(OUTPUT_TXT, "w") as f:
    f.write("Optimized Delivery Routes\n")
    f.write("=========================\n\n")

    if not routes:
        f.write("No routes were generated.\n")
    else:
        for vehicle_id, route in enumerate(routes):
            f.write(f"Vehicle {vehicle_id + 1} Route:\n")
            for stop in route:
                lat, lon = locations[stop]
                f.write(f"  - Location {stop}: ({lat}, {lon})\n")
            f.write("\n")

# -------------------- Plot Map --------------------
plot_routes(locations, routes)

print("✅ Route Optimization Completed Successfully!")
print("📄 Optimized routes saved to outputs/optimized_routes.txt")
print("🗺 Map generated successfully")