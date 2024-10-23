# FLIGHT TICKET FINDER



## Overview

The **FLIGHT TICKET FINDER** is a Python-based application that retrieves flight data from the [Amadeus Flight-Offers Search API  - check out the documentation for more info-](https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search) processes it, and provides detailed itineraries for the cheapest flights. The program outputs a CSV file with flight details such as departure and arrival destinations, flight duration, and price, along with any additional services like checked baggage. It also generates a PNG file that visualizes the relationship between flight ticket prices and flight numbers.



Through this project, you can learn about handling complex JSON data, working with external APIs, performing data normalization and cleaning, and visualizing datasets with Matplotlib and Seaborn.



## Features

- **Flight Data Retrieval:** Fetches flights between a specified origin and destination using the Amadeus API.

- **Data Normalization & Cleaning:** Preprocesses complex JSON-structured data, including handling additional services like baggage options.

- **CSV Export:** Saves the cleaned flight data as a CSV file, detailing flight routes and prices.

- **Data Visualization:** Generates a plot that shows the relationship between flight ticket prices `grandTotal` and flight numbers.

- **Customizable Parameters:** Modify search parameters such as origin, destination, and departure date.

  

## Project Structure

The project consists of the following key files:



1. **main.py**  

   The entry point for the program. It initializes the flight search, processes the data, and generates both a CSV file and a PNG plot.



2. **flight_api.py**  

   Handles interaction with the Amadeus API. This file includes the `FlightFinder` class responsible for querying the API to retrieve flight data.



3. **processor.py**  

   Processes the flight data returned from the API. This file contains the `FlightDataProcessor` class, which is responsible for data normalization, cleaning, and processing additional services. It also handles the creation of CSV files and plots.



## Dependencies

All the required dependencies are listed in the  requirements.txt file. You can install them by running:
```bash
 pip install -r requirements.txt
```
## Setup

1. Clone this repository 

```bash
 git clone https://github.com/whistlesurprise/Flight-Ticket-Finder.git 
```

2. Set up your environment variables by creating a  `.env` file in the root directory with the following content:
```bash
API_KEY = your_amadeus_api_key
API_SECRET = your_amadeus_api_secret
```
[Check out here](https://developers.amadeus.com/get-started/get-started-with-self-service-apis-335) to find out how to obtain your Amadeus API Key

Replace your_amadeus_api_key and your_amadeus_api_secret with your actual Amadeus API credentials.

3. Run the program 
```bash
python main.py
```
## Output
- **CSV File:** The flight data is saved in the `itineraries/flights_data.csv` file, with columns including departure and arrival destinations, flight segments, total price, and any additional services.

- **PNG Plot:** A plot showing the relationship between `grandTotal (price)` and flight numbers is saved in the `itineraries/grand_total_vs_flight_number.png file`.

## Customization
You can modify the flight search parameters directly in the `main.py` file when creating an instance of `FlightFinder`. The following parameters can be adjusted

- **originLocationCode:**  IATA code for the departure airport.

- **destinationLocationCode:** IATA code for the destination airport.

- **departureDate:** The desired date of departure (format: YYYY-MM-DD).

- **adults:** Number of adult passengers.

Example:
```bash
finder = FlightFinder(
    originLocationCode='AYT', 
    destinationLocationCode='WAW', 
    departureDate='2024-11-09', 
    adults=1
)
```
## Error Handling
The program includes basic error handling. If no flights are found, the program will exit gracefully with a message. If an error occurs while fetching data from the API, detailed error logs will be printed.
