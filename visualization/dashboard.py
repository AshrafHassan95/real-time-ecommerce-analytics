from flask import Flask, render_template
import pymysql
from dotenv import load_dotenv
import os
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

@app.route('/')
def dashboard():
    # Get data for visualizations
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # Product activity by category
            cursor.execute("""
                SELECT p.category, COUNT(ua.activity_id) as activity_count
                FROM user_activity ua
                JOIN products p ON ua.product_id = p.product_id
                WHERE ua.created_at >= %s
                GROUP BY p.category
                ORDER BY activity_count DESC
            """, (datetime.now() - timedelta(hours=24),))
            category_data = cursor.fetchall()
            
            # Activity types distribution
            cursor.execute("""
                SELECT activity_type, COUNT(*) as count
                FROM user_activity
                WHERE created_at >= %s
                GROUP BY activity_type
            """, (datetime.now() - timedelta(hours=24),))
            activity_data = cursor.fetchall()
            
            # Recent AI insights
            cursor.execute("""
                SELECT p.name, ai.insight_text, ai.generated_at
                FROM ai_insights ai
                JOIN products p ON ai.product_id = p.product_id
                ORDER BY ai.generated_at DESC
                LIMIT 5
            """)
            ai_insights = cursor.fetchall()
            
            # Time series of activities
            cursor.execute("""
                SELECT 
                    DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:00:00') as hour,
                    COUNT(*) as activity_count
                FROM user_activity
                WHERE created_at >= %s
                GROUP BY hour
                ORDER BY hour
            """, (datetime.now() - timedelta(hours=24),))
            time_series = cursor.fetchall()
            
    finally:
        connection.close()
    
    # Create visualizations
    category_df = pd.DataFrame(category_data, columns=['Category', 'Activity Count'])
    category_fig = px.bar(
        category_df, 
        x='Category', 
        y='Activity Count',
        title='Activity by Product Category (Last 24 Hours)'
    )
    category_chart = category_fig.to_html(full_html=False)
    
    activity_df = pd.DataFrame(activity_data, columns=['Activity Type', 'Count'])
    activity_fig = px.pie(
        activity_df, 
        names='Activity Type', 
        values='Count',
        title='Activity Type Distribution (Last 24 Hours)'
    )
    activity_chart = activity_fig.to_html(full_html=False)
    
    time_df = pd.DataFrame(time_series, columns=['Hour', 'Activity Count'])
    time_fig = px.line(
        time_df, 
        x='Hour', 
        y='Activity Count',
        title='Activity Over Time (Last 24 Hours)'
    )
    time_chart = time_fig.to_html(full_html=False)
    
    return render_template(
        'index.html',
        category_chart=category_chart,
        activity_chart=activity_chart,
        time_chart=time_chart,
        ai_insights=ai_insights
    )

if __name__ == "__main__":
    app.run(debug=True)