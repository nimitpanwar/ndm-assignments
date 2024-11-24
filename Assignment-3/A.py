import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
a = pd.read_excel('choice.xlsx', sheet_name=None)
b = pd.read_excel('win.xlsx', sheet_name=None)
c = pd.read_excel('loss.xlsx', sheet_name=None)
d1, d2 = a['group1'].values, a['group2'].values
e1, e2 = b['group1'].values, b['group2'].values
f1, f2 = c['group1'].values, c['group2'].values
e1, e2 = e1[:, :100], e2[:, :100]
f1, f2 = f1[:, :100], f2[:, :100]
def solve(d, e, f):
    g, h = [], []
    for i in range(d.shape[0]):
        j, k, l, m = 0, 0, 0, 0
        for n in range(1, d.shape[1]):
            o = e[i, n-1] + f[i, n-1]
            if o >= 0:
                l += 1
                if d[i, n] != d[i, n-1]:
                    j += 1
            else:
                m += 1
                if d[i, n] != d[i, n-1]:
                    k += 1
        g.append(j / l if l > 0 else 0)
        h.append(k / m if m > 0 else 0)
    return g, h
g1, h1 = solve(d1, e1, f1)
g2, h2 = solve(d2, e2, f2)
res = {
    'Group 1': {
        'gain': np.mean(g1), 'loss': np.mean(h1),
        'sem_gain': np.std(g1) / np.sqrt(len(g1)),
        'sem_loss': np.std(h1) / np.sqrt(len(h1))
    },
    'Group 2': {
        'gain': np.mean(g2), 'loss': np.mean(h2),
        'sem_gain': np.std(g2) / np.sqrt(len(g2)),
        'sem_loss': np.std(h2) / np.sqrt(len(h2))
    }
}

print("Group\tGain\tLoss\tSEM Gain\tSEM Loss")
for grp, data in res.items():
    print(f"{grp}\t{data['gain']:.4f}\t{data['loss']:.4f}\t{data['sem_gain']:.4f}\t{data['sem_loss']:.4f}")
def plot_res(res):
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    for i, grp in enumerate(res.keys()):
        gain, loss = res[grp]['gain'], res[grp]['loss']
        sem_gain, sem_loss = res[grp]['sem_gain'], res[grp]['sem_loss']
        x = np.arange(2)
        w = 0.35
        bars1 = axes[i].bar(x - w / 2, [gain, loss], w, color='skyblue', edgecolor='black', label='Proportion')
        bars2 = axes[i].bar(x + w / 2, [sem_gain, sem_loss], w, color='coral', edgecolor='black', label='SEM')
        axes[i].set_title(f'{grp}', fontsize=16, fontweight='bold')
        axes[i].set_ylabel('Proportion / SEM', fontsize=14)
        axes[i].set_xticks(x)
        axes[i].set_xticklabels(['Gain', 'Loss'], fontsize=12)
        axes[i].set_ylim(0, max(gain + sem_gain, loss + sem_loss) + 0.1)
        axes[i].legend(fontsize=12, loc='upper left')
        axes[i].grid(axis='y', linestyle='--', alpha=0.7)
        for bar in bars1 + bars2:
            height = bar.get_height()
            axes[i].text(bar.get_x() + bar.get_width() / 2, height + 0.02, f'{height:.2f}', ha='center', va='bottom', fontsize=10)
    fig.suptitle('Proportion of Switches after Gain/Loss Trials and Corresponding SEMs', fontsize=18, fontweight='bold', y=0.95)
    fig.text(0.5, 0.02, 'Trial Outcome Type (Gain vs. Loss)', ha='center', fontsize=14)
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.show()

plot_res(res)
t_gain, p_gain = stats.ttest_ind(g1, g2)
print(f"Between groups (Gain): t-stat = {t_gain:.4f}, p-value = {p_gain:.4f}")
t_loss, p_loss = stats.ttest_ind(h1, h2)
print(f"Between groups (Loss): t-stat = {t_loss:.4f}, p-value = {p_loss:.4f}")
t_within_g1, p_within_g1 = stats.ttest_rel(g1, h1)
print(f"Within Group 1 (Gain vs Loss): t-stat = {t_within_g1:.4f}, p-value = {p_within_g1:.4f}")
t_within_g2, p_within_g2 = stats.ttest_rel(g2, h2)
print(f"Within Group 2 (Gain vs Loss): t-stat = {t_within_g2:.4f}, p-value = {p_within_g2:.4f}")