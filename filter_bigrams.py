import pandas as pd

df_bigrams = pd.read_csv('bigrams_all.tsv', sep='\t', comment='#')  # read bigrams
df_bigrams = df_bigrams[df_bigrams['bigram_freq_per_million'] > .1]  # drop bigrams with a frequency < .1 per million
df_bigrams = df_bigrams[df_bigrams['bigram_freq_per_million'] < 10]  # drop bigrams with a frequency > 10 per million

df_np = df_bigrams[(df_bigrams['unigram1_pos'] == 'ADJ') & (df_bigrams['unigram2_pos'] == 'N')]  # only noun phrases
df_np = df_np.sort_values('bigram_freq', ascending=False)  # sort by bigram count
df_np.to_csv('noun_phrases.tsv', sep='\t', index=False)  # write to file

df_vp = df_bigrams[(df_bigrams['unigram1_pos'] == 'N') & (df_bigrams['unigram2_pos'] == 'WW')]  # only noun phrases
df_vp = df_vp.sort_values('bigram_freq', ascending=False)  # sort by bigram count
df_vp.to_csv('verb_phrases.tsv', sep='\t', index=False)  # write to file
