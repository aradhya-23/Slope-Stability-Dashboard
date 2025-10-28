import pandas as pd
import random
import os

# Create data directory if not exists
os.makedirs("data", exist_ok=True)

# 50 distinct real mine names
mines = [
    "Korba", "Singrauli", "Talcher", "Dhanbad", "Jharia", "Raniganj",
    "Nagpur", "Wardha", "Godda", "Jharsuguda", "Karanpura", "Bokaro",
    "Chirimiri", "Rajmahal", "Ib Valley", "Gevra", "Kusmunda", "Dipka",
    "Amlohri", "Jayant", "Nigahi", "Bina", "Gorbi", "Krishnashila",
    "Ramagundam", "Singareni", "Manuguru", "Yellandu", "Kothagudem",
    "Sonepur Bazari", "Jamadoba", "Katras", "Tirap", "Tipong", "Ledo",
    "Tikak", "Margherita", "Namchik", "Chandrapur", "Umrer", "Kamptee",
    "Majri", "Ballarpur", "Pench", "New Majri", "Patharkhera", "Satpura",
    "Amgaon", "Ghugus", "Kenda", "Kolar"
]

data = []
for mine in mines:
    for year in range(2010, 2025):
        ndvi = round(random.uniform(0.2, 0.8), 2)
        slope = round(random.uniform(10, 35), 1)
        rainfall = round(random.uniform(300, 900), 1)
        fos = round(random.uniform(0.8, 2.0), 2)
        label = "Stable" if fos >= 1.3 else "Unstable"
        data.append([mine, ndvi, slope, rainfall, label, year, fos])

df = pd.DataFrame(data, columns=["Mine", "Ndvi", "Slope", "Rainfall", "Label", "Year", "FoS"])
df.to_csv("data/labeled_data.csv", index=False)

print("✅ 'data/labeled_data.csv' created successfully with 50 mines and all required columns.")
