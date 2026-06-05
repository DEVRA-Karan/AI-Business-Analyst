from flask import Flask, render_template, request, redirect
import pandas as pd
import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
from plotly_charts import create_category_chart
from analysis import *
from charts import save_revenue_chart, save_region_chart

app = Flask(__name__)

genai.configure(api_key="AQ.Ab8RN6LXB2XjqxVQI9XDmdU6a81fU8TRHJj_HduBRBsaeVWJAg")

model = genai.GenerativeModel("gemini-2.5-flash")

# Default CSV load
current_df = pd.read_csv("sales.csv")

print(current_df.columns)

save_revenue_chart(current_df)
save_region_chart(current_df)

@app.route("/")
def home():

    revenue = get_total_revenue(current_df)
    profit = get_average_profit(current_df)

    top_categories = get_top_5_categories(current_df)
    category = get_top_category(current_df)
    region = get_top_region(current_df)
    orders = get_total_orders(current_df)
    customers = get_total_customers(current_df)
    payment = get_best_payment_method(current_df)
    insights = generate_ai_insights(current_df)
    plotly_chart = create_category_chart(current_df)

    return render_template(
    "index.html",
    revenue=revenue,
    profit=profit,
    category=category,
    region=region,
    orders=orders,
    customers=customers,
    payment=payment,
    top_categories=top_categories,
    insights=insights,
    plotly_chart=plotly_chart
)

@app.route("/upload", methods=["POST"])
def upload():

    global current_df

    file = request.files["file"]

    filepath = os.path.join("uploads", file.filename)

    file.save(filepath)

    current_df = pd.read_csv(filepath)

    save_revenue_chart(current_df)
    save_region_chart(current_df)

    print(current_df.shape)

    return redirect("/")

@app.route("/ask", methods=["POST"])
def ask():

    question = request.form["question"]

    prompt = f"""
You are a Senior Business Analyst.

Dataset Information:

Revenue: {get_total_revenue(current_df)}
Average Profit Margin: {round(get_average_profit(current_df),2)}%
Top Category: {get_top_category(current_df)}
Top Region: {get_top_region(current_df)}
Orders: {get_total_orders(current_df)}
Customers: {get_total_customers(current_df)}

Top Categories:
{get_top_5_categories(current_df).to_string()}

Your task:
1. Analyze the data.
2. Give business recommendations.
3. Identify risks.
4. Suggest profit improvement strategies.
5. Use bullet points.
6. Keep answer under 250 words.
Question:
{question}
"""

    response = model.generate_content(prompt)

    return response.text

@app.route("/download-pdf")
def download_pdf():

    pdf_file = "Business_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(
        Paragraph(
            "AI Business Analyst Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    # KPI Table
    data = [
        ["Metric", "Value"],
        ["Revenue", str(get_total_revenue(current_df))],
        ["Profit", str(round(get_average_profit(current_df), 2))],
        ["Top Category", get_top_category(current_df)],
        ["Top Region", get_top_region(current_df)],
        ["Orders", str(get_total_orders(current_df))],
        ["Customers", str(get_total_customers(current_df))]
    ]

    table = Table(data)

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ])
    )

    content.append(table)
    content.append(Spacer(1, 20))

    # AI Insights
    content.append(
        Paragraph(
            "AI Insights",
            styles["Heading2"]
        )
    )

    insights = generate_ai_insights(current_df)

    if insights:
        for insight in insights:
            content.append(
                Paragraph(
                    f"• {insight}",
                    styles["Normal"]
                )
            )

    content.append(Spacer(1, 20))

    # Revenue Chart
    content.append(
        Paragraph(
            "Revenue Chart",
            styles["Heading2"]
        )
    )

    content.append(
        Image(
            "static/revenue_chart.png",
            width=400,
            height=250
        )
    )

    content.append(Spacer(1, 20))

    # Region Chart
    content.append(
        Paragraph(
            "Region Chart",
            styles["Heading2"]
        )
    )

    content.append(
        Image(
            "static/region_chart.png",
            width=400,
            height=250
        )
    )

    doc.build(content)

    return send_file(pdf_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)