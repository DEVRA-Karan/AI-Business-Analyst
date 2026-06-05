import matplotlib.pyplot as plt

def generate_insights(df):
    ...

from analysis import *

def generate_insights(df):
    print("\n===== BUSINESS INSIGHTS =====")

    print(f"Total Revenue: {get_total_revenue(df):,.2f}")

    print(f"Average Profit Margin: {get_average_profit(df):.2f}%")

    print(f"Top Category: {get_top_category(df)}")

    print(f"Top Region: {get_top_region(df)}")