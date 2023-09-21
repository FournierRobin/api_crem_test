# Streamlit app
import streamlit as st
from dotenv import load_dotenv
import os
from crem import get_access_token, set_session_token, get_flight_from_date

# Load environment variables
load_dotenv()
url = os.getenv('URL')

def fetch_flights(start_date, end_date, time_filter_type):
    token = get_access_token(url)
    session = set_session_token(token)
    flight_list = get_flight_from_date(url, session, start_date, end_date, time_filter_type)
    return flight_list

# Streamlit UI
def main():
    st.title('Flight Information Fetcher')

    # User Inputs
    start_date = st.text_input('Enter Start Time (e.g., 2023-09-21T06:00:00.000000)')
    end_date = st.text_input('Enter End Time (e.g., 2023-09-21T20:00:00.000000)')
    time_filter_type = st.selectbox('Choose Time Filter Type', ['EOBT', 'ETA', 'AIRBORNE'])

    # Fetch & Display results
    if st.button('Fetch Flights'):
        if start_date and end_date:
            flight_list = fetch_flights(start_date, end_date, time_filter_type)
            if flight_list:
                st.table(flight_list)
            else:
                st.write('No flights found for the given time and filter.')

if __name__ == "__main__":
    main()