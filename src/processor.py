import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import json
import os 
import re 
from dotenv import load_dotenv
from amadeus import Client, ResponseError

class FlightDataProcessor:

    def __init__(self,data):
        self.data = data
    
    def normalize_data(self):
        if self.data:
            return pd.json_normalize(self.data)
        
        else:
            raise ValueError("No data to normalize")
    
    def to_csv(self,filepath,df):
        return df.to_csv(filepath)
    
    def clean_load_itineraries(self, df):
        flight_info = []
        for i, row in df.loc[:, ['itineraries']].iterrows():
        # Correctly format the JSON string
            row['itineraries'] = json.dumps(row['itineraries'])
            row['itineraries'] = row['itineraries'].replace("'", '"')
            row['itineraries'] = re.sub(r'\bFalse\b', 'false', row['itineraries'])
        
        # Update only the 'itineraries' column for the current row
            df.at[i, 'itineraries'] = row['itineraries']
        
        # Parse the cleaned JSON string
            parsed_data = df['itineraries'].iloc[i]
            final_data = json.loads(parsed_data)
        
        # Append the parsed data to flight_info list
            flight_info.append(final_data)
    
        return flight_info

    def extract_flights(self, data, df):
        l = []
    
    # Loop through each flight data
        for f in data:
            segments = f[0]['segments']
            l.append(segments)
    
    # Create a DataFrame from the list of segments
        df1 = pd.DataFrame(l)

    # Initialize list for normalized columns
        normalized_cols = []
    
    # Iterate through each column in df1
        for i, col in enumerate(df1):
        # Normalize the nested JSON and add suffix for each segment
            normalized_col = pd.json_normalize(df1[i]).apply(pd.Series)
            normalized_col = normalized_col.add_suffix(f'_{i}')
            normalized_cols.append(normalized_col)
    
    # Concatenate all the normalized columns into a single DataFrame
        normalized_df = pd.concat(normalized_cols, axis=1)
    
    # Add the additional columns from the original DataFrame (df)
        
        try:
            normalized_df['additionalServices'] = df['price.additionalServices']
            normalized_df['includedCheckedBagsOnly'] = df['pricingOptions.includedCheckedBagsOnly']
        except KeyError as e: 
            print(f'There is no additional service existing')
        
        normalized_df['grandTotal'] = df['price.grandTotal']
        normalized_df['currency'] = df['price.currency']
        normalized_df['lastTicketingDate'] = df['lastTicketingDate']
        normalized_df['lastTicketingDateTime'] = df['lastTicketingDateTime']
        
        return normalized_df
    
    def process_additional_services(self, df):
        try:
        # Check if 'additionalServices' key exists in the DataFrame
            if 'additionalServices' in df.columns:
            # Replace single quotes with double quotes for JSON parsing
                df['additionalServices'] = df['additionalServices'].apply(
                lambda x: x.replace("'", '"') if isinstance(x, str) else x
            )

            # Convert JSON strings to dictionaries
                df['additionalServices'] = df['additionalServices'].apply(
                lambda x: json.loads(x) if isinstance(x, str) else x
            )

            # Explode the column to expand lists into rows
                df = df.explode('additionalServices')

            # Use json_normalize directly on 'additionalServices' to flatten the dictionary
                additional_services_df = pd.json_normalize(df['additionalServices'])

            # Combine the flattened data with the original DataFrame, dropping the original column
                df = pd.concat([df.reset_index(drop=True), additional_services_df.reset_index(drop=True)], axis=1)

                return df.drop(columns=['additionalServices'], axis=1)
            else:
                print("'additionalServices' key does not exist in the DataFrame.")
                return df  # Return the original DataFrame if the key does not exist

        except KeyError as e:
            print(f"Key error occurred: {e}")

 
    def create_itineraries_directory_and_save_csv(df, directory='itineraries', file_name='flights_data.csv'):
            
            if not os.path.exists(directory):
                os.makedirs(directory)

    # Define file path
            file_path = os.path.join(directory, file_name)

    # Save DataFrame as CSV
            df.to_csv(file_path, index=False)

            print(f'CSV file saved to {file_path}')
    
    def plot_grand_total_vs_flight_number(df, directory='itineraries', file_name='grand_total_vs_flight_number.png'):
    # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Define file path for the plot
        plot_file_path = os.path.join(directory, file_name)

    # Plot
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x=df.index, y=df['grandTotal'], color='red')
        plt.title('Grand Total vs. Flight Number')
        plt.xlabel('Flight Number')
        plt.ylabel('Grand Total in (€)')
        plt.gca().invert_yaxis()
        plt.tight_layout()

    # Save the plot before showing it
        plt.savefig(plot_file_path)

    # Show the plot
        plt.show()

    # Close the plot to free up memory
        plt.close()

        print(f'Plot saved to {plot_file_path}')