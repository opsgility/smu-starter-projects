"""Sample data analysis script."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    data = pd.DataFrame(
        {
            "date": dates,
            "sales": np.random.randint(100, 500, size=30),
            "visitors": np.random.randint(1000, 5000, size=30),
        }
    )

    # Basic analysis
    print("=== Sales Summary ===")
    print(data["sales"].describe())
    print(f"\nTotal sales: {data['sales'].sum()}")
    print(f"Average daily sales: {data['sales'].mean():.1f}")

    # Correlation
    correlation = data["sales"].corr(data["visitors"])
    print(f"\nSales-Visitors correlation: {correlation:.3f}")

    # Create a simple plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data["date"], data["sales"], marker="o", label="Sales")
    ax.set_title("Daily Sales")
    ax.set_xlabel("Date")
    ax.set_ylabel("Sales")
    ax.legend()
    plt.tight_layout()
    plt.savefig("sales_chart.png", dpi=100)
    print("\nChart saved to sales_chart.png")


if __name__ == "__main__":
    main()
