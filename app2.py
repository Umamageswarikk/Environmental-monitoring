import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime
from streamlit_option_menu import option_menu
from PIL import Image


# Initialize Streamlit app configuration
st.set_page_config(page_title="Environmental Monitoring & Forecasting", layout="centered")

# Insert basic CSS for an orange scrollbar
st.markdown(
    """
    <style>
    /* Basic scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px; /* Width of the scrollbar */
        height: 10px; /* Height for horizontal scrollbar */
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1); /* Semi-transparent track */
        border-radius: 10px; /* Rounded edges for the track */
    }

    ::-webkit-scrollbar-thumb {
        background: orange; /* Color of the scrollbar thumb */
        border-radius: 10px; /* Rounded edges for the scrollbar thumb */
    }

    /* For Firefox */
    body {
        scrollbar-width: thin; /* Use thin scrollbars in Firefox */
        scrollbar-color: orange rgba(255, 255, 255, 0.1); /* Color for thumb and track */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Environmental Monitoring and Forecasting")

# Load and preprocess data
data = pd.read_csv("modified_env_monitoring.csv")
data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%d-%m-%Y %H:%M:%S')
data.set_index('Datetime', inplace=True)
data = data.drop(columns=['Date', 'Time', 'Entry ID'])

columns_to_forecast = [
    'Temperature (°C)', 'Humidity (%)', 'Light Resistance (Ω)', 
    'Sound Level (dB)', 'Moisture (%)', 'Turbidity (NTU)', 
    'pH Value', 'DS18B20 Water (°C)', 'DS18B20 Soil (°C)', 
    'MQ135 Ammonia (ppm)', 'MQ135 Benzene (ppm)', 'MQ135 Ethanol (ppm)', 
    'MQ135 Smoke (ppm)', 'MQ7 CO (ppm)', 'MQ2 LPG (ppm)', 
    'MQ2 Methane (ppm)', 'MQ2 Propane (ppm)', 'MQ2 VOCs (ppm)'
]

def load_model(column):
    filename = f"{column.replace(' ', '_')}3.pkl"
    with open(filename, 'rb') as f:
        model_fit = pickle.load(f)
    return model_fit

def forecast_column(column, steps=10):
    series = data[column].dropna()
    model_fit = load_model(column)
    forecast = model_fit.forecast(steps=steps)
    return forecast, series

def plot_selected_graphs(selected_columns, steps=10):
    fig = make_subplots(rows=len(selected_columns), cols=1, shared_xaxes=False, subplot_titles=selected_columns)

    for idx, column in enumerate(selected_columns):
        forecast, series = forecast_column(column, steps=steps)
        fig.add_trace(go.Scatter(x=series.index, y=series, mode='lines', name=f'{column} (Historical)'), row=idx+1, col=1)
        fig.add_trace(go.Scatter(
            x=pd.date_range(start=series.index[-1], periods=steps + 1, freq='T')[1:],
            y=forecast, mode='lines+markers', name=f'{column} (Forecast)', line=dict(color='orange')
        ), row=idx+1, col=1)

    fig.update_layout(height=300 * len(selected_columns), title='Forecast Graphs', showlegend=True)
    st.plotly_chart(fig)

def about_page():
    # Create a container for the "About the Project" section
    with st.container():
        # Title of the section
        st.title("About the Project")
        
        # Project description
        st.write("""
        This project uses environmental sensors to monitor various parameters such as temperature, 
        humidity, volatile organic compounds (VOCs), and more. An ARIMA model is applied to forecast 
        these parameters based on historical data, enabling predictive monitoring of environmental 
        conditions. Below are the monitored parameters with a brief description:
        """)

        col1, col2 = st.columns(2)  # Create two columns

        with col1:
            st.image("img2.png", use_column_width=True)  # Resize image to fit the column width

        with col2:
            st.image("img4.png", use_column_width=True)  # Resize image to fit the column width


        # Displaying the monitored parameters and their brief descriptions
        st.write("""

                 Data Description        

        - **Entry ID**: Unique identifier for each data entry  
        - **Date**: Date of data collection  
        - **Time**: Time of data collection  
        - **Temperature (°C)**: Measured air temperature in degrees Celsius  
        - **Humidity (%)**: Relative humidity as a percentage  
        - **Light Resistance (Ω)**: Light intensity measured as resistance in ohms  
        - **Sound Level (dB)**: Ambient sound level in decibels  
        - **Moisture (%)**: Soil moisture level as a percentage  
        - **Turbidity (NTU)**: Water clarity in nephelometric turbidity units  
        - **pH Value**: Acidity or alkalinity of water  
        - **DS18B20 Water (°C)**: Water temperature measured by a DS18B20 sensor in degrees Celsius  
        - **DS18B20 Soil (°C)**: Soil temperature measured by a DS18B20 sensor in degrees Celsius  
        - **MQ135 Ammonia (ppm)**: Ammonia concentration in parts per million  
        - **MQ135 Benzene (ppm)**: Benzene concentration in parts per million  
        - **MQ135 Ethanol (ppm)**: Ethanol concentration in parts per million  
        - **MQ135 Smoke (ppm)**: Smoke concentration in parts per million  
        - **MQ7 CO (ppm)**: Carbon monoxide concentration in parts per million  
        - **MQ2 LPG (ppm)**: Liquefied petroleum gas concentration in parts per million  
        - **MQ2 Methane (ppm)**: Methane concentration in parts per million  
        - **MQ2 Propane (ppm)**: Propane concentration in parts per million  
        - **MQ2 VOCs (ppm)**: Volatile organic compounds concentration in parts per million  
        """)




def participant_page():
    st.markdown("<h2 style='text-align: center;'>Developer</h2>", unsafe_allow_html=True)

    # Load the image
    image_path = r"C:\MCA\vit projec\Sandy.jpg"  # Update with the correct relative or absolute path
    image = Image.open(image_path)

    # Display the image with CSS for circular and glowing effect
    st.markdown(
        """
        <style>
        .circle-img {
            width: 200px;  /* Increased width and height for larger circle */
            height: 200px;
            border-radius: 50%;
            overflow: hidden;
            display: block;  /* Changed to block for better centering */
            margin: 0 auto;  /* Center the image */
            box-shadow: 0 0 15px rgba(252, 176, 69, 0.8), 0 0 25px rgba(252, 176, 69, 0.8);
            animation: glow 1.5s infinite alternate;
            margin-bottom: 20px;  /* Add space below the image */
        }
        
        .circle-img img {
            width: 100%;
            height: auto;  /* Keep aspect ratio */
            object-fit: cover; /* Ensure the image covers the circle */
        }

        @keyframes glow {
            0% { box-shadow: 0 0 10px rgba(252, 176, 69, 0.8), 0 0 20px rgba(252, 176, 69, 0.8); }
            100% { box-shadow: 0 0 20px rgba(252, 176, 69, 1), 0 0 30px rgba(252, 176, 69, 1); }
        }
        
        .content {
            text-align: center;  /* Center all text in the content div */
            margin-top: 20px;    /* Add space above the content */
            padding: 0 20px;     /* Add some horizontal padding */
        }

        h3, h4 {
            margin: 10px 0;      /* Consistent margin for headings */
        }

        ul {
            padding: 0;
            list-style-type: none; /* Remove default list styles */
            display: inline-block; /* Center the list */
            text-align: left; /* Left-align the text within the block */
        }

        li {
            margin: 5px 0;    /* Add some vertical spacing between list items */
        }

        strong {
            display: inline-block; /* Align labels consistently */
            width: 100px; /* Fixed width for labels for better alignment */
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Wrap the image in a div with the class "circle-img"
    st.markdown(
        f"""
        <div class="circle-img">
            <img src="data:image/jpeg;base64,{image_to_base64(image)}" alt="P Santhosh Kumar" />
        </div>
        """,
        unsafe_allow_html=True
    )

    # Centering the rest of the content
    st.markdown(
        """
        <div class="content">
            <h3>P Santhosh Kumar</h3>
            <p>Christ University, Bangalore</p>
            <h4>Contact Details:</h4>
            <ul>
                <li><strong>Phone:</strong> 6379314514</li>
                <li><strong>Email:</strong> <a href="mailto:santhoshkumar150822@gmail.com">santhoshkumar150822@gmail.com</a></li>
                <li><strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/santhosh-kumar-150822-p" target="_blank">Santhosh Kumar</a></li>
                <li><strong>GitHub:</strong> <a href="https://github.com/SanthoshKumar150822" target="_blank">Santhosh Kumar</a></li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

def image_to_base64(image):
    """Convert image to base64 encoding."""
    import base64
    from io import BytesIO

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

def prediction_page():
    with st.container():
        st.title("Select Date & Time for Prediction")
        
        # Checkbox to select all parameters
        all_parameters = st.checkbox("Select All Parameters")
        
        # If "Select All Parameters" is checked, set selected_columns to all columns
        if all_parameters:
            selected_columns = columns_to_forecast  # Use all columns
        else:
            selected_columns = st.multiselect("Select Sensor Data for Prediction", columns_to_forecast)

        date_time = st.date_input("Select Date")
        time = st.time_input("Select Time")

        if not selected_columns:
            st.warning("Please select at least one parameter to forecast.")
            return

        # Store selected columns in session state
        st.session_state.selected_columns = selected_columns

        if st.button("Predict"):
            predictions = {}
            for column in selected_columns:
                forecast_values, _ = forecast_column(column, steps=10)
                
                # Access forecast values by position using iloc
                if not forecast_values.empty:
                    predictions[column] = forecast_values.iloc[0]  # Use iloc instead of direct indexing
                else:
                    predictions[column] = None  # Handle case where forecast is empty

            # Show predictions
            st.write(f"**Predictions for {datetime.combine(date_time, time).strftime('%Y-%m-%d %H:%M:%S')}:**")
            for column, value in predictions.items():
                if value is not None:
                    st.write(f"- **{column}**: {value:.2f}")
                else:
                    st.write(f"- **{column}**: Prediction unavailable")


def graph_page():
    with st.container():
        st.title("Graph Visualization")

        # Retrieve selected columns from session state, or default to all
        selected_columns = st.session_state.get("selected_columns", columns_to_forecast)

        if st.button("Generate Graphs"):
            if selected_columns:  # Ensure there are selected columns
                plot_selected_graphs(selected_columns, steps=10)
            else:
                st.warning("No parameters selected for graphs. Please select parameters on the Prediction page.")


# Render the option menu navbar
selected = option_menu(
    None, ["About", "Developer", "Prediction", "Graph"],
    icons=["info", "person", "calculator", "graph-up-arrow"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "margin": "0 auto", "max-width": "800px"},
        "icon": {"color": "#fa6607", "font-size": "20px"},
        "nav-link": {
            "font-size": "18px", "text-align": "center", "margin": "0px", 
            "--hover-color": "#eee", "padding": "10px", 
            "color": "orange"  # Set default color for the text
        },
        "nav-link-selected": {"background-color": "#fa6607", "color": "white"},
        "nav-link:hover": {  # Add hover effect for the nav link
            "color": "black"  # Change text color to black on hover
        }
    }
)


# Render the selected page
if selected == "About":
    about_page()
elif selected == "Developer":
    participant_page()
elif selected == "Prediction":
    prediction_page()
elif selected == "Graph":
    graph_page()
