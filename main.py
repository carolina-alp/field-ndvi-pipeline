import argparse
from datetime import datetime
import matplotlib.pyplot as plt
from src.pipeline import process_ndvi_time_series


def validate_date(date_string: str) -> str:
    """Validates if input string matches YYYY-MM-DD format."""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return date_string
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date format: '{date_string}'. Must be YYYY-MM-DD."
        )


def prompt_date_interactive(prompt_message: str, default_val: str) -> str:
    """Prompts the user interactively in console for date inputs."""
    user_input = input(f"{prompt_message} [Default: {default_val}]: ").strip()
    if not user_input:
        return default_val
    try:
        datetime.strptime(user_input, "%Y-%m-%d")
        return user_input
    except ValueError:
        print("⚠️ Invalid format entered. Using default value.")
        return default_val

def plot_ndvi_time_series(df_monthly, output_path: str = "ndvi_phenological_curve.png"):
    """Generates and saves the phenological NDVI plot with clean X-axis labels."""
    if df_monthly.empty:
        print("⚠️ Cannot plot: Monthly NDVI DataFrame is empty.")
        return

    plt.figure(figsize=(12, 6))
    
    for field_id, group in df_monthly.groupby("field_id"):
        plt.plot(
            group["year_month"],
            group["mean_ndvi"],
            marker="o",
            linewidth=2.0,
            markersize=5,
            label=f"{field_id} ({group['crop'].iloc[0]})"
        )

    plt.title("NDVI Phenological Time-Series Curve", fontsize=13, fontweight="bold")
    plt.xlabel("Year-Month", fontsize=11)
    plt.ylabel("Mean NDVI", fontsize=11)
    plt.ylim(0, 1.0)
    plt.axhline(y=0.2, color="gray", linestyle="--", alpha=0.5, label="Bare Soil Threshold (0.2)")
    plt.axhline(y=0.7, color="green", linestyle="--", alpha=0.5, label="Peak Canopy (0.7)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left")
    
    # --- Mejora del Eje X ---
    # Rotar etiquetas 45 grados y mostrar solo 1 de cada 2 o 3 meses si hay muchos datos
    ax = plt.gca()
    labels = group["year_month"].tolist()
    
    if len(labels) > 15:
        # Mostrar etiquetas intercaladas para evitar amontonamiento
        step = max(1, len(labels) // 12)
        ax.set_xticks(range(0, len(labels), step))
        ax.set_xticklabels(labels[::step], rotation=45, ha="right")
    else:
        plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"📊 Plot saved successfully as '{output_path}'")


def main():
    parser = argparse.ArgumentParser(
        description="🌾 Cloud-Native Agricultural Field NDVI Pipeline & Monthly Analyzer"
    )

    parser.add_argument(
        "--source",
        type=str,
        default="data/sample_fields.geojson",
        help="Path to spatial input file (.geojson, .shp) or bounding box.",
    )
    parser.add_argument(
        "--start-date",
        type=validate_date,
        default=None,
        help="Start date for temporal analysis (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--end-date",
        type=validate_date,
        default=None,
        help="End date for temporal analysis (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--output-plot",
        type=str,
        default="ndvi_phenological_curve.png",
        help="Path or name of the output image plot.",
    )

    args = parser.parse_args()

    print("=" * 65)
    print("🌾 CLOUD-NATIVE AGRICULTURAL FIELD NDVI PIPELINE")
    print("=" * 65)

    start_date = args.start_date
    end_date = args.end_date

    if not start_date or not end_date:
        print("\n📅 Temporal Window Configuration:")
        if not start_date:
            start_date = prompt_date_interactive(
                "👉 Enter START DATE (YYYY-MM-DD)", "2026-03-01"
            )
        if not end_date:
            end_date = prompt_date_interactive(
                "👉 Enter END DATE (YYYY-MM-DD)", "2026-08-31"
            )

    print(f"\n🚀 Processing Period: {start_date} ➔ {end_date}")
    print(f"📂 Spatial Source: {args.source}\n")

    monthly_series = process_ndvi_time_series(
        source=args.source, start_date=start_date, end_date=end_date
    )

    print("\n📈 Monthly Aggregated NDVI Summary (Mean Value per Month):")
    print(monthly_series.to_string(index=False))

    # Generar y guardar el gráfico de la curva fenológica
    print("\n📈 Generating NDVI Plot...")
    plot_ndvi_time_series(monthly_series, output_path=args.output_plot)


if __name__ == "__main__":
    main()