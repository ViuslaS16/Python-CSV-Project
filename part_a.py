#Author: Visula Sithum Siriwardana
#Date: 01/12/2024
#Student ID: 2120213
import csv
# Task A: Input Validation
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    validate_date = []
    #assign arguments for date type, date format, sarting vale and ending value.
    #Make 3 tupples for day, months and years
    part_of_date = [("day", "dd", 1, 31), ("month", "mm", 1, 12), ("year", "yyyy", 2000, 2024)]
    for section_of_date, section_of_format, first_date, last_date in part_of_date :
        #Use loop structure to countinusly  interate input
        while True:
            try:
                get_user_input = int(input(f"Please enter the {section_of_date} of the survey in the format {section_of_format}: "))
                #Check whether user input in correct date range {star_date}:{end_date}
                if first_date <= get_user_input <= last_date:
                    validate_date.append(get_user_input)
                    break
                else:
                    print(f"Out of range - values must be in the range {first_date} and {last_date}.")
            except ValueError:
                print("Integer required.")
    #Assign validated data into variable and return it
    file_path = (f"{validate_date[0]:02d}{validate_date[1]:02d}{validate_date[2]:04d}") 
    return file_path

def validate_continue_input(get_user_choice):
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    try:
        if get_user_choice == 'y'.upper():
            main()
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
    except ValueError:
        print("Enter Uppercase value please")

# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    #Assigning variables, lists and dictonaries.
    total_bicycles = 0
    total_scooter = 0
    total_vehicales = []
    total_trucks = []
    total_electric_vehicles = []
    total_two_wheel_vehicle = []
    total_buss_leaving_elmavenue = []
    total_vehicales_to_samedirection = []
    total_vehicales_overspeed = []
    total_vehicales_elm = []
    total_vehicales_hanley = []
    rainy_time = []
    hour_count = {}
    try:
        #Open csv file by using csv.reader and use file_path as argument.
        #I watched "https://www.youtube.com/watch?v=4mqyi8Vqk78" this youtube tutorial to use learn to csv  
        
        csv_file = f"traffic_data{file_path}.csv"
        with open(csv_file, "r") as file:
            read_csv_file = csv.reader(file)
            # I watched "https://www.youtube.com/watch?v=bHiiTWn2Kd4" this youtube tutorial to learn how to skip header from the csv file.
            header = next(read_csv_file)
            #Check whether rows are in the range of csv file
            
            for row in read_csv_file:
                #Get total vehicles to a preassigned list
                total_vehicales.append(row[8])
                #GEt total number of trucks to a preassigned list 
                if row[8] == "Truck":
                    total_trucks.append(row[8])
                #Get total number of electric(hybrid) vehicles to a preassigned list
                if row[9] == "True":
                    total_electric_vehicles.append(row[9])
                #get total of two wheeled vehicles (Bicycles, Motorcycles, Scooter) to a preassigned list
                if row[8] in ["Bicycle","Motorcycle","Scooter"]:
                    total_two_wheel_vehicle.append(row[8])
                #get total number of busses leaving from Elm Avenue/Rabbit Road to a preassigned list
                if row[0] == "Elm Avenue/Rabbit Road" and row[8] == "Buss" and row[4] == "N":
                    total_buss_leaving_elmavenue.append(row[8])
                #get total number of vehicles moves to same directions to a preassigned list
                if row[3] == row[4]:
                    total_vehicales_to_samedirection.append(row[8])
                #get total number of vehicles recorded as over speedlimt to a preassigned list
                if int(row[7]) > int(row[6]):
                    total_vehicales_overspeed.append(row[8])
                #get total vehicle cout for passing Elm Avenue/Rabbit Road to a preassigned list
                if row[0] == "Elm Avenue/Rabbit Road":
                    total_vehicales_elm.append(row[8])
                #get total vehicle cout for passing Hanley Highway/Westway to a preassigned list
                if row[0] == "Hanley Highway/Westway":
                    total_vehicales_hanley.append(row[8])
                #Get percentage of trucks from total number of vehicles 
                truck_percentage = round((len(total_trucks) / len(total_vehicales)*100))
                #Get total number of scooters passing Elm Avenue/Rabbit Road
                if row[0] == "Elm Avenue/Rabbit Road" and row[8] == "Scooter":
                    total_scooter += 1
                    total_elm_scooter =round(len(total_vehicales_elm) / total_scooter)
                #get the highest number of vehicles passing Hanley Highway/Westway.
                if row[0] == "Hanley Highway/Westway":
                    #use split to extract ":" from the timeOfDay column.
                    #Consumed "https://www.w3schools.com/python/ref_string_split.aspas" refference.
                    #Watch "https://youtu.be/MZZSMaEAC2g?si=izg0PsKg8S5A37wn" This youtube tutorial to learned dictionaries in python.
                    hours = int(row[2].split(":")[0])
                    #By adding 1 count how many time that hour occurrs 
                    hour_count[hours] = hour_count.get(hours, 0) + 1
                    peak_hour_count = max(hour_count.values())
                    #To get most passed vehicle through Hanley Highway/Westway between time period 
                    peak_vehicle_count = 0 
                    for hour, count in hour_count.items():
                        if count == peak_hour_count:
                           peak_vehicle_count = hour
                #Get the time of raining for the selected date
                if row[5] in ["Light Rain","HeavyRain"]:
                    hours = int(row[2].split(":")[0])
                    if hours not in rainy_time:
                        rainy_time.append(row[8])
                #Calculate average number of bicycles per hour for selected date
                #This is not working 
                if row[8] == "Bicycle":
                    hours = int(row[2].split(":")[0])
                    total_bicycles += 1
                    #Use this condition to avoid ZeroDivisionError
                    if hours > 0 :
                        avg_bicycle_per_hour = round(total_bicycles / hours)
                    else:
                        avg_bicycle_per_hour = 0 
        #Assign arguments into a list and return it.
        outcomes = csv_file, len(total_vehicales), len(total_trucks), len(total_electric_vehicles), len(total_two_wheel_vehicle), len(total_buss_leaving_elmavenue), len(total_vehicales_to_samedirection), truck_percentage, avg_bicycle_per_hour, len(total_vehicales_overspeed), len(total_vehicales_elm), len(total_vehicales_hanley), total_elm_scooter, peak_hour_count, peak_vehicle_count, len(rainy_time)
        return outcomes
    except FileNotFoundError:
        print(f"{csv_file} not found! ")
    
def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    #Display outcomes
    print(f"***************************\ndate file selected is {outcomes[0]}\n***************************")
    print(f"The total number of vehicles recorded for this date is {outcomes[1]}")
    print(f"The total number of trucks recorded for this date is {outcomes[2]}")
    print(f"The total number of electric vehicles for this date is {outcomes[3]}")
    print(f"The total number of two-wheeled vehicles for this date is {outcomes[4]}")
    print(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]}")
    print(f"The total number of Vehicles through both junctions not turning left or right is {outcomes[6]}")
    print(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes[7]}%")
    print(f"The average number of Bicycles per hour for this date {outcomes[8]}")
    print(f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}")
    print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}")
    print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[11]}")
    print(f"{outcomes[12]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
    print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[13]}")
    print(f"The most number of vehicles through Hanley Highway/Westway were recorded between {outcomes[14]}:00 and {outcomes[14]+1}:00")
    print(f"The number of hours of rain for this date is {outcomes[15]}")
    return outcomes
# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    with open(file_name, "w") as file:
        file.write(f"***************************\ndate file selected is traffic_date{outcomes[0]} \n***************************\n")
        file.write(f"The total number of vehicles recorded for this date is {outcomes[1]}\n")
        file.write(f"The total number of trucks recorded for this date is {outcomes[2]}\n")
        file.write(f"The total number of electric vehicles for this date is {outcomes[3]}\n")
        file.write(f"The total number of two-wheeled vehicles for this date is {outcomes[4]}\n")
        file.write(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]}\n")
        file.write(f"The total number of Vehicles through both junctions not turning left or right is {outcomes[6]}\n")
        file.write(f"The percentage of total vehicles recorded that are trucks for this date is {outcomes[7]}\n")
        file.write(f"The average number of Bikes pe hour for this date {outcomes[8]}\n")
        file.write(f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}\n")
        file.write(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}\n")
        file.write(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[11]}\n")
        file.write(f"{outcomes[12]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.\n")
        file.write(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[13]}.\n")
        file.write(f"The number of hours of rain for this date is {outcomes[14]}.\n")
def main():
    #Use this loop to itterate while user choice is "N"
    while True:
        try:
            file = validate_date_input()
            outcomes = process_csv_data(file)
            display_outcomes(outcomes)
            save_results_to_file(outcomes)
            #Ask user want to load other data set or not
            get_user_choice = input("Do you want to load new dataset? [Y] or [N] : ")
            if validate_continue_input(get_user_choice) == 'N':
                print("End of the program")
                break
        #Find any other error
        except Exception as v: 
            print("Please try again!!")
if __name__ == "__main__":
    main()
    
