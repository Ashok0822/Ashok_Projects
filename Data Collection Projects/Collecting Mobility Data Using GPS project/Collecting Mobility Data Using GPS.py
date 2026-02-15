from pathlib import Path
import zipfile
import re
import math
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# PATHS CODE
ZIP_PATH  = Path(r"D:/DU-SEM2/Period 1/Data Collection/Lab Report 2 GPS/data-1.zip")
OUT_ROOT  = Path(r"D:/DU-SEM2/Period 1/Data Collection/Lab Report 2 GPS/data-1")

# Task 1 outputs
OUT_DIR_T1   = OUT_ROOT / "output_task1"
EXTRACT_DIR  = OUT_DIR_T1 / "extracted_gsd"
CSV_DIR      = OUT_DIR_T1 / "processed_csv"
COMBINED_CSV = OUT_DIR_T1 / "All_Trips_Combined.csv"
SUMMARY_CSV  = OUT_DIR_T1 / "Trips_Summary.csv"

# Task 2 outputs (combined-only plots)
OUT_DIR_T2   = OUT_ROOT / "output_task2_plots"

for p in [EXTRACT_DIR, CSV_DIR, OUT_DIR_T2]:
    p.mkdir(parents=True, exist_ok=True)
# ==============================================


# DATA CLEANING

def convert_to_decimal(value: int) -> float:
    """Convert 'degrees + decimal minutes × 10,000' to decimal degrees."""
    deg = value // 1_000_000
    minutes = (value - deg * 1_000_000) / 10_000
    return deg + (minutes / 60.0)

def parse_datetime(date_raw: int, time_raw: int):
    """Return a datetime (or NaT) from DDMMYY + HHMMSS integers."""
    try:
        d = str(int(date_raw)).zfill(6)
        t = str(int(time_raw)).zfill(6)
        date_part = datetime.strptime(d, "%d%m%y").date()
        time_part = datetime.strptime(t, "%H%M%S").time()
        return pd.Timestamp(datetime.combine(date_part, time_part))
    except Exception:
        return pd.NaT

def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance (km)."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlmb = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlmb/2)**2
    return 2*R*math.asin(math.sqrt(min(1.0, a)))


# DATA CLEANING

def read_gsd_to_df(gsd_path: Path) -> pd.DataFrame:
    """Read one .gsd file to DataFrame of raw fields."""
    pat = re.compile(r'^\d+=(\d+),(\d+),(\d+),(\d+),(-?\d+),(-?\d+)')
    rows = []
    with gsd_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = pat.match(line.strip())
            if m:
                lat, lon, tim, dat, spd, alt = m.groups()
                rows.append((int(lat), int(lon), int(tim), int(dat), int(spd), int(alt)))
    if not rows:
        raise ValueError(f"No GPS rows parsed from {gsd_path}")
    return pd.DataFrame(rows, columns=[
        "Latitude_raw","Longitude_raw","Time_raw","Date_raw","Speed_raw","Altitude"
    ])

def process_one_trip_to_exact_headers(raw_df: pd.DataFrame, trip_name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns:
      pretty -> EXACT headers + required new columns for assignment (for CSV)
      helper -> includes Datetime & per-segment metrics for summaries
    """
    df = raw_df.copy()

    # Decimal coords -> Y_WGS84 (lat), X_WGS84 (lon)
    df["Y_WGS84"] = df["Latitude_raw"].apply(convert_to_decimal)
    df["X_WGS84"] = df["Longitude_raw"].apply(convert_to_decimal)

    # Datetime → TIME (HH-MM-SS) and DATE (DD-MM-YY)
    dt = df.apply(lambda x: parse_datetime(x["Date_raw"], x["Time_raw"]), axis=1)
    df["_Datetime"] = dt
    df["TIME"] = dt.dt.strftime("%H-%M-%S")
    df["DATE"] = dt.dt.strftime("%d-%m-%y")

    # Speed & Height fields
    df["SPEED"] = df["Speed_raw"].astype(int)
    df["SPEED(KM/H)"] = (df["Speed_raw"] / 100.0)
    df["HEIGHT"] = df["Altitude"].astype(int)

    # IDs at the beginning (per-trip CSV convention: simple 1..N and Trail_ID=1..N)
    n = len(df)
    df.insert(0, "TP_ID", np.arange(1, n+1, dtype=int))
    df.insert(1, "TRAIL_ID", np.arange(1, n+1, dtype=int))
    df.insert(2, "USER_ID", trip_name)

    # Rename raw coords to match screenshot header names
    df = df.rename(columns={
        "Latitude_raw":  "Y_COORDINA",
        "Longitude_raw": "X_COORDINA",
    })

    # --- Per-point metrics required by assignment ---
    # Time diff (seconds)
    df["_Delta_t_s"] = df["_Datetime"].diff().dt.total_seconds().fillna(0.0)

    # Distance between points (km)
    seg_dist = [0.0]
    for i in range(1, n):
        seg_dist.append(haversine_km(df.at[i-1,"Y_WGS84"], df.at[i-1,"X_WGS84"],
                                     df.at[i,  "Y_WGS84"], df.at[i,  "X_WGS84"]))
    df["_Distance_km"] = seg_dist

    # Acceleration (m/s^2) = (Δv/3.6) / Δt
    df["_Delta_v_kmh"] = df["SPEED(KM/H)"].diff().fillna(0.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        accel = (df["_Delta_v_kmh"] / 3.6) / df["_Delta_t_s"]
    accel = pd.Series(accel).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    df["_Acceleration_mps2"] = accel

    # EXACT output order + new columns at the end
    ordered = [
        "TP_ID","TRAIL_ID","USER_ID",
        "Y_COORDINA","X_COORDINA","TIME","DATE","SPEED","HEIGHT","SPEED(KM/H)","Y_WGS84","X_WGS84"
    ]
    pretty = df[ordered].copy()

    # Append required per-point metrics
    pretty["Distance_km"]      = df["_Distance_km"].astype(float)
    pretty["Time_Diff_s"]      = df["_Delta_t_s"].astype(float)
    pretty["Acceleration_mps2"]= df["_Acceleration_mps2"].astype(float)

    return pretty, df


def summarize_trip(helper_df: pd.DataFrame, trip_name: str) -> dict:
    """Trip-level duration, distance, avg speed, avg accel."""
    t0, t1 = helper_df["_Datetime"].min(), helper_df["_Datetime"].max()
    dur_hr = (t1 - t0).total_seconds()/3600.0 if pd.notna(t0) and pd.notna(t1) else 0.0
    dist_km = float(helper_df["_Distance_km"].sum())
    avg_speed = dist_km/dur_hr if dur_hr>0 else np.nan
    avg_accel = float(np.nanmean(np.abs(helper_df["_Acceleration_mps2"]))) if len(helper_df) else np.nan
    return {
        "Trip_ID": trip_name,
        "Points": len(helper_df),
        "Duration_hr": round(dur_hr,3),
        "Distance_km": round(dist_km,3),
        "Avg_Speed_kmh": round(avg_speed,3) if not np.isnan(avg_speed) else np.nan,
        "Avg_Acceleration_mps2": round(avg_accel,4) if not np.isnan(avg_accel) else np.nan,
    }


def run_task1():
    print(f"Extracting ZIP: {ZIP_PATH}")
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        zf.extractall(EXTRACT_DIR)

    # Sort for stable numbering 1..T
    gsd_files = sorted(EXTRACT_DIR.rglob("*.gsd"), key=lambda p: p.stem.lower())
    if not gsd_files:
        raise FileNotFoundError("No .gsd files found after extraction.")
    print(f"Found {len(gsd_files)} .gsd files.")

    combined_rows = []
    summaries = []

    for trip_idx, gsd in enumerate(gsd_files, start=1):
        trip = gsd.stem  # file name as trip id / user id
        print(f"Processing {trip} ...")

        raw_df = read_gsd_to_df(gsd)
        pretty_csv, helper = process_one_trip_to_exact_headers(raw_df, trip)

        # Save per-trip CSV with EXACT headers + new metrics
        out_csv = CSV_DIR / f"{trip}_processed.csv"
        pretty_csv.to_csv(out_csv, index=False, encoding="utf-8")
        print(f"Saved: {out_csv}")

        # Trip summary
        summaries.append(summarize_trip(helper, trip))

        # ---- Combined CSV logic:
        # TP_ID = trip number constant for this trip
        # TRAIL_ID = running counter 1..N within this trip
        comb = pretty_csv.copy()
        comb["TP_ID"] = trip_idx
        comb["TRAIL_ID"] = np.arange(1, len(comb) + 1, dtype=int)
        comb["Trip_File"] = trip  # keep label too
        combined_rows.append(comb)

    # Combined CSV (same headers + Trip_File)
    combined_df = pd.concat(combined_rows, ignore_index=True)
    combined_df.to_csv(COMBINED_CSV, index=False, encoding="utf-8")

    # Summary table
    pd.DataFrame(summaries).to_csv(SUMMARY_CSV, index=False, encoding="utf-8")

    print("\n Task 1 complete.")
    print(f"• Per-trip CSVs   → {CSV_DIR}")
    print(f"• Combined CSV    → {COMBINED_CSV}")
    print(f"• Trips Summary   → {SUMMARY_CSV}")


# -------------------- Task 2: Combined-only Visualizations --------------------

def plot_combined_only_from_combined_csv():
    """
    Build ONLY the 4 combined plots from the exact-header combined CSV.
    """
    if not COMBINED_CSV.exists():
        print(f"Combined CSV not found: {COMBINED_CSV}")
        return

    df = pd.read_csv(COMBINED_CSV)

    needed = {"Trip_File","Y_WGS84","X_WGS84","TP_ID","TRAIL_ID","SPEED(KM/H)","DATE","TIME"}
    miss = needed - set(df.columns)
    if miss:
        raise ValueError(f"Combined CSV missing columns: {miss}")

    df = df.dropna(subset=["Y_WGS84","X_WGS84"])
    df["Y_WGS84"] = df["Y_WGS84"].astype(float)
    df["X_WGS84"] = df["X_WGS84"].astype(float)
    df["SPEED(KM/H)"] = df["SPEED(KM/H)"].astype(float)

    # Datetime for speed-time
    dt = pd.to_datetime(df["DATE"] + " " + df["TIME"], format="%d-%m-%y %H-%M-%S", errors="coerce")
    df["_Datetime"] = dt

    OUT_DIR_T2.mkdir(parents=True, exist_ok=True)

    # 1) Combined Trajectories (per-trip colored lines)
    trips = df["Trip_File"].unique()
    colors = plt.cm.tab20(np.linspace(0, 1, max(1, len(trips))))

    fig = plt.figure(figsize=(10,8))
    for color, trip in zip(colors, trips):
        d = df[df["Trip_File"] == trip].sort_values("TRAIL_ID")
        plt.plot(d["X_WGS84"], d["Y_WGS84"], linewidth=1.2, label=trip, color=color)
    plt.title("Combined GPS Trajectories (All Trips)")
    plt.xlabel("Longitude (°)"); plt.ylabel("Latitude (°)")
    if len(trips) <= 20:
        plt.legend(loc="best", fontsize=8)
    plt.grid(True); plt.tight_layout()
    out = OUT_DIR_T2 / "Combined_Trajectories.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f" Saved: {out}")

    # 2) Combined Trajectory colored by Speed (scatter)
    fig = plt.figure(figsize=(10,8))
    sc = plt.scatter(df["X_WGS84"], df["Y_WGS84"], c=df["SPEED(KM/H)"], s=8)
    cbar = plt.colorbar(sc); cbar.set_label("Speed (km/h)")
    plt.title("Combined Trajectory Colored by Speed")
    plt.xlabel("Longitude (°)"); plt.ylabel("Latitude (°)")
    plt.tight_layout()
    out = OUT_DIR_T2 / "Combined_SpeedColored.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f" Saved: {out}")


    # 3) Combined GPS Density Heatmap (clear and bright version)
    import matplotlib.colors as mcolors

    fig = plt.figure(figsize=(10, 8))

    # Use 2D histogram but with bright colormap and transparent background
    counts, xedges, yedges, img = plt.hist2d(
        df["X_WGS84"], 
        df["Y_WGS84"], 
        bins=150, 
        cmap="YlOrRd",              # Yellow–Orange–Red (high contrast)
        norm=mcolors.PowerNorm(0.5) # Slight gamma correction for visibility
    )

    # Add colorbar and labels
    cbar = plt.colorbar(img)
    cbar.set_label("Point Density", fontsize=10)

    # Improve background visibility
    plt.gca().set_facecolor("white")   # Light background for better contrast
    plt.grid(alpha=0.3, linestyle="--")

    plt.title("Combined GPS Density Heatmap", fontsize=13, weight="bold")
    plt.xlabel("Longitude (°)")
    plt.ylabel("Latitude (°)")

    plt.tight_layout()
    out = OUT_DIR_T2 / "Combined_DensityHeatmap.png"
    fig.savefig(out, dpi=250, facecolor="white")  # Force white background
    plt.close(fig)
    print(f" Saved clearer heatmap: {out}")


    # 4) Combined Speed over Time (per-trip thin lines)
    fig = plt.figure(figsize=(11,5))
    for color, trip in zip(colors, trips):
        d = df[(df["Trip_File"] == trip) & (df["_Datetime"].notna())].sort_values("_Datetime")
        if not d.empty:
            plt.plot(d["_Datetime"], d["SPEED(KM/H)"], linewidth=0.9, label=trip, color=color)
    plt.title("Combined Speed Over Time")
    plt.xlabel("Datetime"); plt.ylabel("Speed (km/h)")
    if len(trips) <= 10:
        plt.legend(loc="best", fontsize=8)
    plt.tight_layout()
    out = OUT_DIR_T2 / "Combined_SpeedOverTime.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f" Saved: {out}")


def run_task2():
    """Only combined plots (no per-trip plotting)."""
    plot_combined_only_from_combined_csv()
    print(f"\n Task 2 finished. Plots → {OUT_DIR_T2}")


# -------------------- Runner --------------------

if __name__ == "__main__":
    # Run Task 1 (extract, clean, write CSVs with exact headers + new metrics, and combined/summary CSVs)
    run_task1()

    # Run Task 2 (ONLY the 4 combined plots)
    run_task2()
