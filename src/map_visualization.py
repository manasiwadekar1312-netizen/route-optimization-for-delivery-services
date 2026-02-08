import folium
import os


def plot_routes(locations, routes):
    # ----------------------------
    # Create map centered at depot
    # ----------------------------
    depot_lat = float(locations[0][0])
    depot_lon = float(locations[0][1])

    m = folium.Map(
        location=[depot_lat, depot_lon],
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    # ----------------------------
    # Add markers for locations
    # ----------------------------
    for i, (lat, lon) in enumerate(locations):
        lat = float(lat)
        lon = float(lon)

        if i == 0:
            # Depot
            folium.Marker(
                location=[lat, lon],
                popup="Depot",
                icon=folium.Icon(color="red", icon="home")
            ).add_to(m)
        else:
            # Delivery locations
            folium.Marker(
                location=[lat, lon],
                popup=f"Delivery Point {i}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

    # ----------------------------
    # Plot routes with TRAFFIC
    # ----------------------------
    for vehicle_id, route in enumerate(routes):
        route_coords = [locations[i] for i in route]

        # 🚦 Simulated traffic level
        # Change this manually if you want
        traffic_level = "medium"  # low / medium / high

        if traffic_level == "low":
            color = "green"
        elif traffic_level == "medium":
            color = "orange"
        else:
            color = "red"

        folium.PolyLine(
            locations=route_coords,
            color=color,
            weight=5,
            opacity=0.8,
            popup=f"Vehicle {vehicle_id + 1} | Traffic: {traffic_level.capitalize()}"
        ).add_to(m)

    # ----------------------------
    # Add Traffic Legend
    # ----------------------------
    legend_html = """
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 180px;
        height: 120px;
        background-color: white;
        border: 2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
    ">
    <b>Traffic Levels</b><br>
    <span style="color:green;">●</span> Low Traffic<br>
    <span style="color:orange;">●</span> Medium Traffic<br>
    <span style="color:red;">●</span> High Traffic
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # ----------------------------
    # Save map
    # ----------------------------
    os.makedirs("outputs", exist_ok=True)
    m.save("outputs/route_map.html")