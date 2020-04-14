import pandas as pd
import numpy as np

df_bigrams = pd.read_csv('nl.words.bigrams.tsv', sep='\t', comment='#')
df_unigrams = pd.read_csv('nl.words.unigrams.tsv', sep='\t', comment='#')
df_subtlex = pd.read_csv('subtlex.tsv', sep='\t', comment='#')[['Word', 'dominant.pos']]  # immediately dump useless columns

# join dominant POS to unigram freqs
df_unigrams = df_unigrams.merge(df_subtlex, left_on='unigram', right_on='Word').drop('Word', axis=1)

# split bigrams
df_bigrams['unigram1'] = df_bigrams['bigram'].apply(lambda x: x.split(' ')[0])
df_bigrams['unigram2'] = df_bigrams['bigram'].apply(lambda x: x.split(' ')[1])

# join unigram freqs for word 1 to bigram freqs
df_unigrams1 = df_unigrams.rename(columns={'unigram': 'unigram1', 'unigram_freq': 'unigram1_freq', 'dominant.pos': 'unigram1_pos'})
df_bigrams = df_bigrams.merge(df_unigrams1, left_on='unigram1', right_on='unigram1')

# join unigram freqs for word 2 to bigram freqs
df_unigrams2 = df_unigrams.rename(columns={'unigram': 'unigram2', 'unigram_freq': 'unigram2_freq', 'dominant.pos': 'unigram2_pos'})
df_bigrams = df_bigrams.merge(df_unigrams2, left_on='unigram2', right_on='unigram2')

df_bigrams = df_bigrams.dropna()  # drop rows with missing values
df_bigrams['bigram_freq'] = df_bigrams['bigram_freq'] / 3
df_bigrams['unigram1_freq'] = df_bigrams['unigram1_freq'] / 3
df_bigrams['unigram2_freq'] = df_bigrams['unigram2_freq'] / 3

# compute forward and backward transitional probabilities
df_bigrams['ftp'] = df_bigrams['bigram_freq'] / df_bigrams['unigram1_freq']
df_bigrams['btp'] = df_bigrams['bigram_freq'] / df_bigrams['unigram2_freq']

# compute log counts
df_bigrams['log_bigram_freq'] = np.log(df_bigrams['bigram_freq'])
df_bigrams['log_unigram1_freq'] = np.log(df_bigrams['unigram1_freq'])
df_bigrams['log_unigram2_freq'] = np.log(df_bigrams['unigram2_freq'])
df_bigrams['log_ftp'] = np.log(df_bigrams['ftp'])
df_bigrams['log_btp'] = np.log(df_bigrams['btp'])

# compute frequency per million
df_bigrams['bigram_freq_per_million'] = df_bigrams['bigram_freq'] / (df_bigrams['bigram_freq'].sum() / 1e6)  # 1486.607706

# compute quantiles
df_bigrams['bigram_pct'] = df_bigrams['bigram_freq'].rank(pct=True)
df_bigrams['ftp_pct'] = df_bigrams['ftp'].rank(pct=True)
df_bigrams['btp_pct'] = df_bigrams['btp'].rank(pct=True)

df_bigrams = df_bigrams.sort_values('bigram_freq', ascending=False)
df_bigrams.to_csv('bigrams_all.tsv', sep='\t', index=False)  # write to file
