def get_total_revenue(df):
    revenue = df["total_amount"].sum()
    return round(revenue, 2)

def get_average_profit(df):
    return round(df["profit_margin"].mean(), 2)

def get_top_category(df):
    return df.groupby("category")["total_amount"].sum().idxmax()

def get_top_region(df):
    return df.groupby("region")["total_amount"].sum().idxmax()

def get_total_orders(df):
    return len(df)

def get_total_customers(df):
    return df["customer_id"].nunique()

def get_best_payment_method(df):
    return df["payment_method"].value_counts().idxmax()

def get_top_5_categories(df):
    return df.groupby("category")["total_amount"].sum().sort_values(ascending=False).head(5)

def generate_ai_insights(df):

    top_category = get_top_category(df)
    top_region = get_top_region(df)

    insights = []

    insights.append(
        f"{top_category} is the highest revenue generating category."
    )

    insights.append(
        f"{top_region} is the best performing region."
    )

    return insights