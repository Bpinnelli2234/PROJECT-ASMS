import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load processed data
flight_df = pd.read_csv('data/processed/processed_flight_data.csv')
weather_df = pd.read_csv('data/processed/processed_weather_data.csv')

# Clean the flight data
flight_df['velocity'] = flight_df['velocity'].fillna(0)
flight_df['latitude'] = flight_df['latitude'].fillna(0)
flight_df['longitude'] = flight_df['longitude'].fillna(0)
flight_df = flight_df[(flight_df['latitude'] != 0) & (flight_df['longitude'] != 0)]

# Extract weather condition from the 'weather' column
weather_df['weather_main'] = weather_df['weather'].apply(lambda x: eval(x)[0]['main'] if pd.notnull(x) else 'Unknown')

# Initialize the Dash app
app = Dash(__name__)
app.title = "Aviation Safety Monitoring Dashboard"

# Flight Data Map Visualization
fig_flight = px.scatter_geo(
    flight_df,
    lat='latitude',
    lon='longitude',
    hover_name='callsign',
    color='origin_country',
    size='velocity',
    projection="natural earth",
    title='Flight Positions Across the Globe'
)

# Weather Data Bar Chart
fig_weather = px.bar(
    weather_df,
    x='name',                # City name
    y='main.temp',           # Temperature
    color='weather_main',    # Extracted weather condition
    title='Current Weather Conditions'
)

# Dash Layout
app.layout = html.Div([
    html.H1("AI-Driven Aviation Safety Monitoring System", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Graph(figure=fig_flight)
    ], style={'padding': '20px'}),

    html.Div([
        dcc.Graph(figure=fig_weather)
    ], style={'padding': '20px'})
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

