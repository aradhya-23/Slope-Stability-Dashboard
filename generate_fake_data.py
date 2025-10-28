
import pandas as pd
import numpy as np
import os

# --- Create folder if not exists ---
os.makedirs("data", exist_ok=True)

# --- Realistic mine names (you can add or edit) ---
mine_names = [
    "Jharia Coal Mine", "Korba Open Cast", "Kolar Gold Fields", "Dalli-Rajhara Iron Mine",
    "Bailadila Iron Ore Mine", "Bokaro Coal Mine", "Singrauli Coalfield", "Raniganj Coalfield",
    "Neyveli Lignite Mine", "Talcher Coal Mine", "Panna Diamond Mine", "Joda East Iron Mine",
    "Bicholim Iron Mine", "Sukinda Chromite Mine", "Hutti Gold Mine", "Malanjkhand Copper Mine",
    "Chiria Iron Ore Mine", "Piparwar Coal Mine", "Lakhanpur Coal Mine", "Dudhichua Coal Mine",
    "Kudremukh Iron Ore Mine", "Rajmahal Coal Mine", "Kailash Nagar Coal Mine",
    "Singareni Collieries", "Lingaraj Coal Mine", "North Eastern Coalfields",
    "Gevra Open Cast", "Dipka Coal Mine", "Jayant Coal Mine", "Rajrappa Coal Mine",
    "Jitpur Colliery", "Kaniha Coal Mine", "Topa Coal Mine", "Amrapali Coal Mine",
    "Magadh Coal Project", "Khairagarh Limestone Mine", "Rani Atari Iron Mine",
    "Gua Iron Ore Mine", "Panchpatmali Bauxite Mine", "Nalco Damanjodi Mine",
    "Turamdih Uranium Mine", "Tummalapalle Uranium Mine", "Zawar Zinc Mine",
    "Rampura Agucha Mine", "Sindesar Khurd Mine", "Kolihan Copper Mine",
    "Khetri Copper Mine", "Banwas Copper Mine", "Taregaon Limestone Mine",
    "Ras Limestone Mine"
]

# If you want exactly 50
mine_names = mine_names[:50]

years = np.arange(2008, 2025)
rows = []

for mine in mine_names:
    for year in years:
        rows.append({
            "mine": mine,
            "year": year,
            "NDVI": np.round(np.random.uniform(0.1, 0.9), 3),
            "slope": np.round(np.random.uniform(5, 45), 2),
            "rainfall": np.round(np.random.uniform(200, 1200), 1)
        })

# --- Save the synthetic dataset ---
df = pd.DataFrame(rows)
df.to_csv("data/features.csv", index=False)
print("✅ Synthetic data with 50 real mine names saved to 'data/features.csv'")
