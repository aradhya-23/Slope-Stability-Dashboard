
import ee, os, json, pandas as pd

DATA_PATH = "data/features.csv"

def collect_data():
    ee.Initialize()
    with open("mines.json") as f:
        mines = json.load(f)
    years = range(2000, 2026)
    records = []

    for mine in mines:
        name = mine["name"]
        point = ee.Geometry.Point([mine["lon"], mine["lat"]])
        buffer = point.buffer(2000)

        for year in years:
            start = f"{year}-01-01"
            end = f"{year}-12-31"

            s2 = ee.ImageCollection("COPERNICUS/S2_SR")\
                .filterDate(start, end).filterBounds(buffer)\
                .map(lambda img: img.normalizedDifference(['B8','B4']).rename('NDVI'))

            dem = ee.Image('USGS/SRTMGL1_003')
            slope = ee.Terrain.slope(dem).rename('slope')

            rain = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')\
                .filterDate(start, end).filterBounds(buffer).sum().rename('rainfall')

            combined = s2.median().addBands(slope).addBands(rain)
            stats = combined.reduceRegion(reducer=ee.Reducer.mean(), geometry=buffer, scale=100, maxPixels=1e8)

            props = stats.getInfo()
            if props:
                props.update({"mine": name, "year": year})
                records.append(props)

    df = pd.DataFrame(records)
    os.makedirs("data", exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print(f"✅ Saved dataset to {DATA_PATH}")

if __name__ == "__main__":
    ee.Authenticate()
    collect_data()
