import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.pipeline import process_ndvi_time_series

# Coordinates for target field in Wallonia, Belgium
LAT = 50.66153879825414
LON = 4.618252268024664

# Define a small Bounding Box around the point [min_lon, min_lat, max_lon, max_lat]
DELTA = 0.001
point_bbox = [LON - DELTA, LAT - DELTA, LON + DELTA, LAT + DELTA]

def main():
    print(f"📍 Querying target location: Lat {LAT}, Lon {LON}")
    
    # Process time series across a 6-month crop window
    df_monthly = process_ndvi_time_series(
        source=point_bbox,
        start_date="2026-03-01",
        end_date="2026-08-31"
    )
    
    print("\n📊 Monthly Aggregated Results:")
    print(df_monthly.to_string(index=False))

    # Generate Phenology Plot
    if not df_monthly.empty:
        plt.figure(figsize=(9, 4.5))
        plt.plot(
            df_monthly["year_month"], 
            df_monthly["mean_ndvi"], 
            marker="o", 
            color="#2e7d32", 
            linewidth=2.5, 
            label="Clean Target Pixel (SCL Masked)"
        )
        
        plt.title(f"NDVI Phenology Curve | Location: ({LAT:.4f}, {LON:.4f})", fontsize=11, fontweight="bold")
        plt.xlabel("Year-Month", fontsize=10)
        plt.ylabel("Mean NDVI", fontsize=10)
        plt.ylim(0, 1.0)
        plt.grid(True, linestyle=":", alpha=0.6)
        plt.legend(loc="upper left")
        plt.tight_layout()
        
        output_plot = "belgium_field_ndvi.png"
        plt.savefig(output_plot, dpi=300)
        print(f"\n✅ Plot saved as '{output_plot}'")

if __name__ == "__main__":
    main()