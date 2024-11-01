from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro, ttest_ind, mannwhitneyu

# Load the .mat file
data = loadmat(r"C:\Users\ANTPC\OneDrive\Desktop\Assignment2_2A_NDM_2024.mat\Assignment2_2A_NDM_2024.mat")

# Assuming 'NDM_Assignment2' is the key of interest
x = data["NDM_Assignment2"]

# Initialize lists to store the reaction times for each condition
reaction_times_condition1 = []
reaction_times_condition2 = []

# Iterate through each cell in the 30x2 matrix
for row in x:
    for i, cell in enumerate(row):
        reaction_times = []
        # Iterate through the 100 trials
        for trial in cell:
            # Find the first time point where the value crosses 600
            crossing_time = np.argmax(trial >= 600)
            reaction_times.append(crossing_time)
        # Append the reaction times to the respective condition list
        if i == 0:
            reaction_times_condition1.append(reaction_times)
        else:
            reaction_times_condition2.append(reaction_times)

# Convert lists to numpy arrays for easier manipulation
reaction_times_condition1 = np.array(reaction_times_condition1)
reaction_times_condition2 = np.array(reaction_times_condition2)

# Calculate the mean RT for all 30 participants for both conditions
mean_rt_condition1 = np.mean(reaction_times_condition1, axis=0)
mean_rt_condition2 = np.mean(reaction_times_condition2, axis=0)

# Plot histograms
bins = np.arange(0, 1000, 50)  # 20 bins of 50 ms each

plt.figure(figsize=(12, 6))

# Histogram for condition 1
plt.subplot(1, 2, 1)
plt.hist(mean_rt_condition1, bins=bins, edgecolor='black')
plt.axvline(np.mean(mean_rt_condition1), color='red', linestyle='dashed', linewidth=1)
plt.title(f'Condition 1: Mean RT = {np.mean(mean_rt_condition1):.2f} ms')
plt.xlabel('Reaction Time (ms)')
plt.ylabel('Frequency')

# Histogram for condition 2
plt.subplot(1, 2, 2)
plt.hist(mean_rt_condition2, bins=bins, edgecolor='black')
plt.axvline(np.mean(mean_rt_condition2), color='red', linestyle='dashed', linewidth=1)
plt.title(f'Condition 2: Mean RT = {np.mean(mean_rt_condition2):.2f} ms')
plt.xlabel('Reaction Time (ms)')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Print the values used in plotting
print("Mean RT Condition 1:", mean_rt_condition1)
print("Mean RT Condition 2:", mean_rt_condition2)

# Check for normality using the Shapiro-Wilk test
shapiro_condition1 = shapiro(mean_rt_condition1)
shapiro_condition2 = shapiro(mean_rt_condition2)

print(f'Shapiro-Wilk test for Condition 1: W={shapiro_condition1.statistic}, p={shapiro_condition1.pvalue}')
print(f'Shapiro-Wilk test for Condition 2: W={shapiro_condition2.statistic}, p={shapiro_condition2.pvalue}')

# Determine which test to use based on normality
if shapiro_condition1.pvalue > 0.05 and shapiro_condition2.pvalue > 0.05:
    # Both groups are normally distributed, use independent t-test
    test_stat, p_value = ttest_ind(mean_rt_condition1, mean_rt_condition2)
    test_name = 'Independent t-test'
else:
    # At least one group is not normally distributed, use Mann-Whitney U test
    test_stat, p_value = mannwhitneyu(mean_rt_condition1, mean_rt_condition2)
    test_name = 'Mann-Whitney U test'

print(f'{test_name}: Test Statistic={test_stat}, p-value={p_value}')

# Interpretation
if p_value < 0.05:
    print("There is a significant difference in mean reaction times between the two conditions.")
else:
    print("There is no significant difference in mean reaction times between the two conditions.")
