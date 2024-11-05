import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import friedmanchisquare
import seaborn as sns

# Load the Excel file
file_path = 'Assignment2-2B-NDM-2024.xlsx'  # Update the file path if necessary
excel_data = pd.ExcelFile(file_path)

# Load data for each condition
data_cond1 = excel_data.parse('Cond1')
data_cond2 = excel_data.parse('Cond2')
data_cond3 = excel_data.parse('Cond3')
data_cond4 = excel_data.parse('Cond4')

# Function to clean and organize data for each condition
def clean_data(sheet_data):
    # Drop initial rows to clean data
    sheet_data = sheet_data.drop([0, 1]).reset_index(drop=True)
    participants_data = {}
    
    for i in range(1, 11):  # 10 participants (P1 to P10)
        # Select HT and FA columns for each participant
        ht_col = f"P{i}"
        fa_col = f"Unnamed: {sheet_data.columns.get_loc(ht_col) + 1}"
        participants_data[f"P{i}"] = {
            "HT": sheet_data[ht_col].astype(float),
            "FA": sheet_data[fa_col].astype(float)
        }
    return participants_data

# Organize data for each condition
data_conditions = {
    "Cond1": clean_data(data_cond1),
    "Cond2": clean_data(data_cond2),
    "Cond3": clean_data(data_cond3),
    "Cond4": clean_data(data_cond4)
}

# Function to calculate average HT and FA rates across participants for a condition
def calculate_avg_rates(condition_data):
    avg_ht = []
    avg_fa = []
    for criterion in range(6):  # Assuming 6 criterion levels in each condition
        ht_rates = [participant["HT"].iloc[criterion] for participant in condition_data.values()]
        fa_rates = [participant["FA"].iloc[criterion] for participant in condition_data.values()]
        
        avg_ht.append(np.mean(ht_rates))
        avg_fa.append(np.mean(fa_rates))
    return avg_ht, avg_fa

# Calculate average rates for each condition
avg_rates = {cond: calculate_avg_rates(data) for cond, data in data_conditions.items()}

# Plot ROC curves for each condition
plt.figure(figsize=(10, 8))
for cond, (avg_ht, avg_fa) in avg_rates.items():
    plt.plot(avg_fa, avg_ht, marker='o', label=f'{cond}')
    
# Customize the plot
plt.xlabel("False Alarm Rate (FA)")
plt.ylabel("Hit Rate (HT)")
plt.title("ROC Curves for Different Experimental Conditions")
plt.legend(title="Condition")
plt.grid(True)
plt.show()

# Function to calculate accuracies for each participant in each condition
def calculate_accuracies(condition_data):
    accuracies = []
    for participant in condition_data.values():
        # Calculate accuracy for each criterion level, then take the mean
        accuracies.append(((participant["HT"] + (1 - participant["FA"])) / 2).mean())
    return accuracies

# Calculate accuracies for all participants across the four conditions
accuracies_data = {cond: calculate_accuracies(data) for cond, data in data_conditions.items()}

# Create a DataFrame for easier plotting and analysis
accuracy_df = pd.DataFrame(accuracies_data)

# Box plot for accuracies across conditions with annotations for min, max, and median
plt.figure(figsize=(10, 8))
sns.boxplot(data=accuracy_df)
plt.xlabel("Experimental Condition")
plt.ylabel("Accuracy")
plt.title("Box Plot of Accuracies Across Experimental Conditions")
plt.grid(True)

# Annotate min, max, and median values for each condition
for i, cond in enumerate(accuracy_df.columns):
    cond_data = accuracy_df[cond]
    plt.text(i, cond_data.min(), f"Min: {cond_data.min():.2f}", ha='center', color='blue', fontsize=10)
    plt.text(i, cond_data.median(), f"Median: {cond_data.median():.2f}", ha='center', color='green', fontsize=10)
    plt.text(i, cond_data.max(), f"Max: {cond_data.max():.2f}", ha='center', color='red', fontsize=10)

plt.show()

# Perform Friedman's test
friedman_stat, p_value = friedmanchisquare(
    accuracy_df["Cond1"], accuracy_df["Cond2"], accuracy_df["Cond3"], accuracy_df["Cond4"]
)

# Print the Friedman test results
print(f"Friedman's Chi-square test statistic: {friedman_stat}")
print(f"p-value: {p_value}")

# Interpretation
if p_value < 0.05:
    print("There is a statistically significant difference in accuracies across the four conditions.")
else:
    print("There is no statistically significant difference in accuracies across the four conditions.")
