import csv
import pandas as pd

# Reading files (I am testing on 1 file for now...)
data = pd.read_csv("C:/Users/Karim/Desktop/expe/expe/Grp_A_eyesTracking_emotions_Data_Export4.tsv", sep='\t', header=0)

# Columns to be merged
all_columns = ['AOI[bouche]Hit', 'AOI[nez]Hit', 'AOI[oeil_D]Hit', 'AOI[oeil_G]Hit',
               'AOI[joueH_G]Hit', 'AOI[joueH_D]Hit', 'AOI[joueB_G]Hit', 'AOI[menton]Hit',
               'AOI[joueB_D]Hit', 'AOI[front]Hit']

# Merging and droping columns
for c in all_columns:
    cols = [col for col in data.columns if c in col]
    temp = data[cols].apply(
        lambda x: ''.join(x.dropna().astype(int).astype(str)),
        axis=1
    )
    data = data.drop(cols, axis=1)
    data[c] = temp
    print('done : ', c)

# Saving file
print(data.shape)
data.to_csv("test.csv", index=False)

# ==========================================

# Droping non-necessary rows
data = pd.read_csv("test.csv", sep=';', header=0)
print(data.shape)
data = data.dropna(subset=['MediaName'])
d = data[data['MediaName'].str.contains("pages")]
print(d.shape)

# Saving file
d.to_csv("test_3.csv", index=False)
