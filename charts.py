import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

def save_revenue_chart(df):

    revenue = df.groupby("category")["total_amount"].sum()

    plt.figure(figsize=(8,5))
    revenue.plot(kind="bar")

    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")

    plt.tight_layout()

    plt.savefig("static/revenue_chart.png")

    plt.close()

def save_region_chart(df):

    revenue = df.groupby("region")["total_amount"].sum()

    plt.figure(figsize=(8,5))
    revenue.plot(kind="bar")

    plt.title("Revenue by Region")

    plt.tight_layout()

    plt.savefig("static/region_chart.png")

    plt.close()