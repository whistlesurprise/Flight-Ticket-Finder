import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import json
import os 
import re 
from dotenv import load_dotenv
from amadeus import Client, ResponseError

load_dotenv()

class FlightFinder:
    def __init__(self, originLocationCode, destinationLocationCode, departureDate, adults) -> None:
        self.originLocationCode = originLocationCode
        self.destinationLocationCode = destinationLocationCode
        self.departureDate = departureDate
        self.adults = adults
        self.data = None

    def query_flight(self):
        # Initialize Amadeus client
        amadeus = Client(
            client_id=os.getenv('API_KEY'),
            client_secret=os.getenv('API_SECRET')
        )

        try:
            # Attempt to fetch flight data
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=self.originLocationCode,
                destinationLocationCode=self.destinationLocationCode,
                departureDate=self.departureDate,
                adults=self.adults
            )
            # Save the data if successful
            self.data = response.data
            print("Data fetched successfully!")
        
        except ResponseError as error:
            # Log the error details
            print("Error fetching data:", error)
            if hasattr(error, 'response'):
                print("Response:", error.response)