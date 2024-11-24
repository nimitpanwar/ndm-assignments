import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro, ttest_ind, mannwhitneyu

# Load the data
mat = scipy.io.loadmat('Assignment2_2A_NDM_2024.mat')
data = mat['NDM_Assignment2']  # shape (30, 2), 30 participants, 2 conditions

# Initialize lists to store mean RTs for each participant in each condition
mean_rt_condition_1 = []
mean_rt_condition_2 = []

# Loop over participants to extract RTs for each condition
for participant_data in data:
    for i, condition_data in enumerate(participant_data):
        # Each condition_data has shape (100, 1000) - 100 trials, 1000 ms
        rts = []
        for trial in condition_data:
            rt_index = np.argmax(trial >= 600)  # Find index where evidence reaches threshold (600)
            rts.append(rt_index)
        mean_rt = np.mean(rts)  # Calculate mean RT across 100 trials for the participant
        
        if i == 0:
            mean_rt_condition_1.append(mean_rt)
        else:
            mean_rt_condition_2.append(mean_rt)

# Convert to numpy arrays
mean_rt_condition_1 = np.array(mean_rt_condition_1)
mean_rt_condition_2 = np.array(mean_rt_condition_2)

# Plot histograms
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Histogram for Condition 1
axes[0].hist(mean_rt_condition_1, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
axes[0].axvline(np.mean(mean_rt_condition_1), color='red', linestyle='--', linewidth=2)
axes[0].set_title(f'Condition 1 Mean RT Distribution\nMean: {np.mean(mean_rt_condition_1):.2f} ms')
axes[0].set_xlabel('Reaction Time (ms)')
axes[0].set_ylabel('Frequency')

# Histogram for Condition 2
axes[1].hist(mean_rt_condition_2, bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
axes[1].axvline(np.mean(mean_rt_condition_2), color='red', linestyle='--', linewidth=2)
axes[1].set_title(f'Condition 2 Mean RT Distribution\nMean: {np.mean(mean_rt_condition_2):.2f} ms')
axes[1].set_xlabel('Reaction Time (ms)')

plt.tight_layout()
plt.show()

# Statistical testing
# Normality check
stat1, p1 = shapiro(mean_rt_condition_1)
stat2, p2 = shapiro(mean_rt_condition_2)

if p1 > 0.05 and p2 > 0.05:
    # Use t-test if both distributions are normal
    stat, p_value = ttest_ind(mean_rt_condition_1, mean_rt_condition_2)
    test_type = 'T-test'
else:
    # Use Mann-Whitney U test otherwise
    stat, p_value = mannwhitneyu(mean_rt_condition_1, mean_rt_condition_2)
    test_type = 'Mann-Whitney U test'

# Display test results
print(f"{test_type} Results: Statistic={stat:.3f}, p-value={p_value:.3f}")






# B

