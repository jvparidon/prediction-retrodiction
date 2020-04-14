import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
mpl.use('agg')
sns.set(style='whitegrid', palette='Set2')


def standardize(series):
    return (series - series.mean()) / series.std()


df = pd.read_csv('noun_phrases.tsv', sep='\t', comment='#')

# subset
#df = df[df['bigram_freq_per_million'] > .1]

# make some histograms
plt.clf()
g = sns.distplot(df['log_bigram_freq'])
plt.savefig('log_bigram_freq.pdf')
plt.savefig('log_bigram_freq.png', dpi=600)

plt.clf()
g = sns.distplot(df['log_btp'])
plt.savefig('log_btp.png', dpi=600)

plt.clf()
g = sns.distplot(df['log_ftp'])
plt.savefig('log_ftp.png', dpi=600)

plt.clf()
g = sns.jointplot(df['log_ftp'], df['log_btp'], kind="hex")
plt.savefig('log_ftp_by_log_btp.pdf')
plt.savefig('log_ftp_by_log_btp.png', dpi=600)

# percentiles within selection
df['ftp_pct'] = df['ftp'].rank(pct=True)
df['btp_pct'] = df['btp'].rank(pct=True)

lower = .2
upper = .8
mid_lower = .3
mid_upper = .7

print('high ftp')
# select high ftp stims
subset = df[df['ftp_pct'] > upper]
# select high btp stims
selection = subset[subset['btp_pct'] > upper]
print(len(selection))
selection.to_csv('high_ftp_high_btp.tsv', sep='\t')
# select mid btp stims
selection = subset[(subset['btp_pct'] > mid_lower) & (subset['btp_pct'] < mid_upper)]
print(len(selection))
selection.to_csv('high_ftp_mid_btp.tsv', sep='\t')
# select low btp stims
selection = subset[subset['btp_pct'] < lower]
print(len(selection))
selection.to_csv('high_ftp_low_btp.tsv', sep='\t')

print('mid ftp')
# select mid ftp stims
subset = df[(df['ftp_pct'] > mid_lower) & (df['ftp_pct'] < mid_upper)]
# select high btp stims
selection = subset[subset['btp_pct'] > upper]
print(len(selection))
selection.to_csv('mid_ftp_high_btp.tsv', sep='\t')
# select mid btp stims
selection = subset[(subset['btp_pct'] > mid_lower) & (subset['btp_pct'] < mid_upper)]
print(len(selection))
selection.to_csv('mid_ftp_mid_btp.tsv', sep='\t')
# select low btp stims
selection = subset[subset['btp_pct'] < lower]
print(len(selection))
selection.to_csv('mid_ftp_low_btp.tsv', sep='\t')

print('low ftp')
# select low ftp stims
subset = df[df['ftp_pct'] < lower]
# select high btp stims
selection = subset[subset['btp_pct'] > upper]
print(len(selection))
selection.to_csv('low_ftp_high_btp.tsv', sep='\t')
# select mid btp stims
selection = subset[(subset['btp_pct'] > mid_lower) & (subset['btp_pct'] < mid_upper)]
print(len(selection))
selection.to_csv('low_ftp_mid_btp.tsv', sep='\t')
# select low btp stims
selection = subset[subset['btp_pct'] < lower]
print(len(selection))
selection.to_csv('low_ftp_low_btp.tsv', sep='\t')
