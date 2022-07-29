from datetime import datetime, timedelta
import streamlit as st
import functions
import pydeck as pdk

st.set_page_config(
    page_title="Google Maps Clone",
    page_icon="🗺"
)

st.markdown(
    """<style> div.stButton > button:first-child { width: 100% ; height: 200% ;} </style>""", unsafe_allow_html=True)

st.title("Simple Google Maps Clone")

with st.form("main-form"):
    col1, col2 = st.columns(2)

    origin = col1.text_input("Enter the Origin Address.")
    destination = col2.text_input("Enter the Destination Address.")

    transport_type = col1.selectbox("Select the Type of Transport", [
        "Cycling", "Driving", "Public Transport (National Only)", "Walking", "Bus"])
    transport_type_dict = {"Cycling": "cycling", "Driving": "driving",
                           "Public Transport (National Only)": "public_transport", "Walking": "walking", "Bus": "bus"}

    submit_bttn = col2.form_submit_button("Calculate !")

with st.empty():
    if submit_bttn and len(origin) != 0 and len(destination) != 0:

        data = functions.get_route_data(
            origin, destination, transport_type_dict[transport_type])

        duration = functions.get_duration(data)

        coords = functions.get_coordinates(data)

        path = functions.get_coords_path(coords)

        current_time = datetime.now()
        end_time = current_time + timedelta(seconds=duration.total_seconds())

        duration_str = (datetime(2010, 3, 9, 0, 0, 0) +
                        duration).strftime("%H:%M")
        current_time_str = current_time.strftime("%H:%M")
        end_time_str = end_time.strftime("%H:%M")

        empty, col1, col2, col3 = st.columns([1, 2, 2, 2])
        col1.metric("Trip Duration", duration_str)
        col2.metric("Departure Time", current_time_str)
        col3.metric("Arrival Time", end_time_str)

        r = functions.get_plot(path)

        st.pydeck_chart(r)

    elif submit_bttn:
        st.error("Please input some addresses!!!")
