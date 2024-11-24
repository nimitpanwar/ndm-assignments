import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Function to calculate d-prime
def calculate_d_prime(hit_rate, false_alarm_rate):
    # Avoid extreme values
    hit_rate = np.clip(hit_rate, 1e-5, 1 - 1e-5)
    false_alarm_rate = np.clip(false_alarm_rate, 1e-5, 1 - 1e-5)
    
    # Calculate z-scores
    z_hit = stats.norm.ppf(hit_rate)
    z_fa = stats.norm.ppf(false_alarm_rate)
    
    # Calculate d-prime
    d_prime = z_hit - z_fa
    return d_prime

# Load the Excel file
file_path = 'excel.xlsx'
xls = pd.ExcelFile(file_path)

# Initialize a dictionary to store d-prime values for each condition
d_prime_values = {}

# Iterate through each sheet (condition) in the Excel file
for sheet_name in xls.sheet_names:
    # Read the data for the current condition
    df = pd.read_excel(xls, sheet_name=sheet_name)
    
    # Initialize a list to store d-prime values for each participant
    d_prime_list = []
    
    # Iterate through each participant's data
    for participant in range(0, df.shape[1], 2):
        hit_rate = df.iloc[:, participant]
        false_alarm_rate = df.iloc[:, participant + 1]
        
        # Calculate d-prime for the participant
        d_prime = calculate_d_prime(hit_rate, false_alarm_rate)
        
        # Calculate the average d-prime for the participant
        avg_d_prime = np.nanmean(d_prime)
        d_prime_list.append(avg_d_prime)
    
    # Store the d-prime values for the current condition
    d_prime_values[sheet_name] = d_prime_list

# Plot the d-prime values for each condition
plt.figure(figsize=(10, 6))
for condition, d_prime_list in d_prime_values.items():
    plt.plot(d_prime_list, label=condition, marker='o')

plt.xlabel('Participant')
plt.ylabel("d'")
plt.title("d' Values for Each Condition")
plt.legend()
plt.grid(True)
plt.show()