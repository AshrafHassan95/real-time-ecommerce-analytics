from flask import Flask, render_template
from database.queries import DatabaseQueries
import plotly
import plotly.express as px
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    db = DatabaseQueries()
    
    # Get popular products
    popular_products = db.get_popular_products()
    
    # Create visualization
    fig = px.bar(
        popular_products,
        x='name',
        y='interactions',
        color='category',
        title='Top Products by User Interactions'
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('index.html', graphJSON=graphJSON)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
