# Import classes from api.py and processor.py
from flight_api import FlightFinder
from processor import FlightDataProcessor

def main ():
    # Create an instance of FlightFinder with the desired flight search parameters
    finder = FlightFinder(
    originLocationCode='AYT', 
    destinationLocationCode='WAW', 
    departureDate='2024-11-09', 
    adults=1
)
# Check if the flight query was successful; exit the program if no flights are found 
    if not finder.query_flight():
        print("No flights found. Exiting program!")
        exit(1)
# Pass the fetched flight data to the FlightDataProcessor
    processor = FlightDataProcessor(finder.data)

# Normalize the data
    df = processor.normalize_data()

# Clean and load the itineraries from the normalized data
    flight_infos = processor.clean_load_itineraries(df)

# Extract flight segments and additional flight information
    df_flights = processor.extract_flights(flight_infos, df)

# Process additional services information from the flights data
    final_df = processor.process_additional_services(df_flights)

# Fill missing values with placeholder '-'
    final_df = final_df.fillna('-')

# Save the final DataFrame as a CSV file in the 'itineraries' directory
    FlightDataProcessor.create_itineraries_directory_and_save_csv(final_df)

# Plot 'Grand Total vs Flight Number' and save it in the 'itineraries' directory
    FlightDataProcessor.plot_grand_total_vs_flight_number(final_df)

if __name__ == '__main__':
    main()



