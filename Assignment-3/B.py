import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

a, b, c = (pd.read_excel(f, sheet_name=None) for f in ['choice.xlsx', 'win.xlsx', 'loss.xlsx'])
def calc_props(d, e, f):
    props = {i: [] for i in range(1, 5)}
    for p in range(d.shape[0]):
        counts, losses = {i: 0 for i in range(1, 5)}, 0
        for t in range(1, d.shape[1]):
            if (net := e[p, t-1] + f[p, t-1]) < 0 and d[p, t] != d[p, t-1]:
                losses += 1
                counts[d[p, t-1]] += 1
        for deck in counts:
            props[deck].append(counts[deck] / losses if losses > 0 else 0)
    return props

p1, p2 = (calc_props(a[g].values, b[g].values, c[g].values) for g in ['group1', 'group2'])
res = {g: {d: {'mean': np.mean(p[d]), 'sem': np.std(p[d]) / np.sqrt(len(p[d]))} for d in p} for g, p in zip(['Group 1', 'Group 2'], [p1, p2])}
for g in res:
    res[g] = dict(sorted(res[g].items(), key=lambda x: x[1]['mean'], reverse=True))
print("Group\tDeck\tMean\tSEM")
for g, data in res.items():
    for d, stats in data.items():
        print(f"{g}\t{d}\t{stats['mean']:.4f}\t{stats['sem']:.4f}")
def plot_res(res):
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    decks = [1, 2, 3, 4]
    for i, g in enumerate(res):
        means = [res[g][d]['mean'] for d in decks]
        sems = [res[g][d]['sem'] for d in decks]
        x, w = np.arange(len(decks)), 0.35
        bars1 = axes[i].bar(x - w / 2, means, w, color='skyblue', edgecolor='black', label='Mean')
        bars2 = axes[i].bar(x + w / 2, sems, w, color='coral', edgecolor='black', label='SEM')
        axes[i].set(title=f'{g} Results', ylabel='Proportion / SEM', xlabel='Deck', xticks=x, xticklabels=[f'Deck {d}' for d in decks], ylim=(0, max(means + sems) + 0.1))
        axes[i].legend(fontsize=12, loc='upper left')
        axes[i].grid(axis='y', linestyle='--', alpha=0.7)
        for bar in bars1 + bars2:
            axes[i].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=10)
    fig.suptitle('Proportion of choices immediately before switching', fontsize=18, fontweight='bold', y=0.95)
    fig.text(0.5, 0.02, 'Decks', ha='center', fontsize=14)
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.show()

plot_res(res)
print("Ranked decks based on mean proportions:")
for g, data in res.items():
    print(f"\n{g}:")
    for rank, (d, stats) in enumerate(data.items(), 1):
        print(f"  Rank {rank}: Deck {d} - Mean = {stats['mean']:.4f}, SEM = {stats['sem']:.4f}")