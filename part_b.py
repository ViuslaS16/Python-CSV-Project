'''
Author: Visula Sithum Siriwardana
Date: 20/12/2024
Student ID: w2120213

I assume https://www.udemy.com/course/100-days-of-code/learn/lecture/19911792#overview Dr. Angela Yu's python bootcam for learn oop concepts and tkinter part.
And also use both https://youtu.be/tKyYdnC6sUc?si=BXhwJ6rmfLvX5MvH and https://youtu.be/YXPyB4XeYLA?si=RG339PrxUuxs00Su for some tkinter parts.
'''


import csv
import tkinter as tk
from w2120213 import validate_date_input, process_csv_data, validate_continue_input, save_results_to_file

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.canvas = None
        self.width = 1200
        self.height = 800
        self.margin = {'top': 100, 'bottom': 80, 'left': 50, 'right': 50}
        self.color = {'elm_avenue_bar': '#97FB96', 'hanley_highway_bar': '#FC9595'}
        self.bar_spacing = 20

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.title("Histogram")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='#F3F3F3')
        self.canvas.pack()

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        # Calculate eaach road data
        elm_avenue_data = self.traffic_data['Elm']
        hanley_highway_data = self.traffic_data['Hanley']

        # Calculate bar size
        highest_hour = max(max(elm_avenue_data), max(hanley_highway_data), 1)
        bar_height = (self.height - 2 * self.margin['bottom']) / highest_hour

        # Draw bars
        total_bar_space = self.width - 2 * self.margin['left'] - 23 * self.bar_spacing
        hour_group_width = total_bar_space / 24
        bar_width = hour_group_width / 2

        # Draw axes
        self.canvas.create_line(self.margin['left'], self.height - self.margin['bottom'],
            self.width - self.margin['right'], self.height - self.margin['bottom'],
            fill="#858784", width=2  )
        
        # Draw bars and labels
        for hour in range(24):
            x_axis_on = self.margin['left'] + hour * (2 * bar_width + self.bar_spacing)

            # Elm Avenue bar
            elm_height = elm_avenue_data[hour] * bar_height
            if elm_height > 0:  # Only draw if there's data
                self.canvas.create_rectangle(
                    x_axis_on, self.height - self.margin['bottom'] - elm_height,
                    x_axis_on + bar_width, self.height - self.margin['bottom'],
                    fill=self.color['elm_avenue_bar'] )
                
                # Add value label above bar
                if elm_avenue_data[hour] > 0:
                    self.canvas.create_text(x_axis_on + bar_width/2,self.height - self.margin['bottom'] - elm_height - 5,
                        text=str(elm_avenue_data[hour]),fill="#67C26C",font=("Arial", 10))
                    
            # Hanley Highway bar
            hanley_height = hanley_highway_data[hour] * bar_height
            if hanley_height > 0:  # Check wheather data is visibe
                self.canvas.create_rectangle(
                    x_axis_on + bar_width, self.height - self.margin['bottom'] - hanley_height,
                    x_axis_on + 2 * bar_width, self.height - self.margin['bottom'],
                    fill=self.color['hanley_highway_bar']
                )

                # Add value label above bar
                if hanley_highway_data[hour] > 0:
                    self.canvas.create_text(x_axis_on + 1.5*bar_width,self.height - self.margin['bottom'] - hanley_height - 5,
                        text=str(hanley_highway_data[hour]),fill="#DA8A74",font=("Arial", 10))
                    
            # Hour labels
            self.canvas.create_text(
                x_axis_on + bar_width,self.height - self.margin['bottom'] + 15,text=str(hour).zfill(2),fill="black",font=("Arial", 10))
            
        # Add titles for labbles
        self.canvas.create_text(self.width / 2,self.margin['top'] / 2,text=f"Histogram of Vehicle Frequency per Hour ({self.date})",
            fill="#6E6E6C",font=("Arial", 18, "bold"))
        self.add_legend()

    def add_legend(self):
        """
        Adds a legend to the histogram.
        """
        legend_x_axis = self.margin['left']
        legend_y_axis = self.margin['top']
        
        # Elm Avenue legend
        self.canvas.create_rectangle(legend_x_axis, legend_y_axis,legend_x_axis + 20, legend_y_axis + 20,
        fill=self.color['elm_avenue_bar'],outline="#89B48A")
        self.canvas.create_text(legend_x_axis + 30, legend_y_axis + 10,text="Elm Avenue/Rabbit Road",
        fill="#858784", anchor="w",font=("Arial", 10, "bold"))

        # Hanley Highway legend
        self.canvas.create_rectangle(legend_x_axis, legend_y_axis + 30,legend_x_axis + 20, legend_y_axis + 50,
        fill=self.color['hanley_highway_bar'],outline="#B28E79")
        self.canvas.create_text(legend_x_axis + 30, legend_y_axis + 40,text="Hanley Highway/Westway",
        fill="#858784", anchor="w",font=("Arial", 10, "bold"))

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.root.mainloop()

class MultiCSVProcessor:
    def __init__(self):
        self.current_data = None
        self.histogram = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        try:
            # Get the raw data from process_csv_data
            outcomes = process_csv_data(file_path)
            if outcomes:
                self.clear_previous_data()
                
                #Create list to counting 24 hours
                traffic_data = {
                    "Elm": [0] * 24,
                    "Hanley": [0] * 24
                }
                
                # Process the CSV file again to count vehicles per hour
                csv_file = f"traffic_data{file_path}.csv"
                with open(csv_file, "r") as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)  # Skip header          
                    for row in csv_reader:
                        junction_name = row[0]
                        time = row[2]
                        hour = int(time.split(':')[0])
                        if junction_name == "Elm Avenue/Rabbit Road":
                            traffic_data["Elm"][hour] += 1
                        elif junction_name == "Hanley Highway/Westway":
                            traffic_data["Hanley"][hour] += 1
                
                # Extract date from filename
                date_part = f"{file_path[0:2]}/{file_path[2:4]}/{file_path[4:8]}"
                
                # Create and show histogram
                trafix_app = HistogramApp(traffic_data, date_part)
                trafix_app.run()
                
        except Exception as e:
            print(f"Couldn't load the file: {e}")

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        try:
            with open('results.txt','r') as file:
                data_lines = file.readlines()
                if len(data_lines) > 20:
                    save_results_to_file()
        except FileNotFoundError:
            print("There is no previous data to clear")
        except Exception as v:
            print(f"Some error occured {v}.")

    def process_files(self, file_path):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.load_csv_file(file_path)
        while True:
            user_choice = input("Do you want to load new dataset? [Y] or [N] : ").upper()
            if user_choice == 'N':
                self.clear_previous_data()
                break
            elif user_choice == 'Y':
                file_path = validate_date_input()
                self.load_csv_file(file_path)
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

# Create an instance of the MultiCSVProcessor and start processing files
if __name__ == "__main__":
    processor = MultiCSVProcessor()
    initial_file_path = validate_date_input()
    processor.process_files(initial_file_path)