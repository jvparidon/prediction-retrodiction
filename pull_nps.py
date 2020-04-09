import pandas as pd

df_bigrams = pd.read_csv('bigrams_all.tsv', sep='\t', comment='#')  # read bigrams
df_np = df_bigrams[(df_bigrams['unigram1_pos'] == 'ADJ') & (df_bigrams['unigram2_pos'] == 'N')]  # only noun phrases
df_np = df_np.sort_values('bigram_freq', ascending=False)  # sort by bigram count

print(len(df_np))
df_np.to_csv('noun_phrases.tsv', sep='\t', index=False)  # write to file

df_np = df_np[df_np['bigram_freq'] > 1]
print(len(df_np))
df_np.to_csv('noun_phrases_short.tsv', sep='\t', index=False)

df_np = df_np[df_np['bigram_freq'] > 9]
print(len(df_np))
df_np.to_csv('noun_phrases_shorter.tsv', sep='\t', index=False)
