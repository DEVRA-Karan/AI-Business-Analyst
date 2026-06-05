import plotly.express as px

def create_category_chart(df):

    data = df.groupby("category")["total_amount"].sum().reset_index()

    fig = px.bar(
        data,
        x="category",
        y="total_amount",
        title="Revenue by Category"
    )

    fig.update_layout(
        height=500
    )

    return fig.to_html(full_html=False)