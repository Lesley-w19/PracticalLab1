import pandas as pd
import matplotlib.pyplot as plt

def plot_steady_from_db(engine, axes=None, table="fact_measurements_tbl"):
    """
    Plot a steady (static) graph directly from DB fact or staging table.

    Parameters
    ----------
    engine : SQLAlchemy engine
        Database connection
    axes : list[str] or None
        Axis columns to plot (default = axis1..axis7)
    table : str
        Table to query from ('fact_measurements_tbl' or 'staging_measurements')
    """
    if axes is None:
        axes = ["axis1","axis2","axis3","axis4","axis5","axis6","axis7"]

    # Choose query
    if table == "fact_measurements_tbl":
        query = f"""
        SELECT tm.timestamp, {', '.join(['f.'+a for a in axes])}
        FROM fact_measurements_tbl f
        JOIN dim_time_tbl tm ON f.time_id = tm.time_id
        ORDER BY tm.timestamp;
        """
    else:  # staging
        query = f"""
        SELECT time as timestamp, {', '.join(axes)}
        FROM {table}
        ORDER BY time;
        """

    # Load into pandas
    df = pd.read_sql(query, engine)

    # Plot all at once
    plt.figure(figsize=(12,6))
    for a in axes:
        plt.plot(df["timestamp"], df[a], label=a)

    plt.title(f"Steady Data ({table})")
    plt.xlabel("Time")
    plt.ylabel("Current (A)")
    plt.legend(loc="upper left")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
