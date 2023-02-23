import pandas as pd
# df = pd.read_csv("parkinsons.csv")

# rows = df.shape[0]
# #shuffle rows of df
# print(df.head(5))
# df = df.sample(frac=1)
# print(df.head(5))

# train, test = df[:int(rows*0.8)], df[int(rows*0.8):]

# train.to_csv("train_parkinsons.csv", index=False)
# test.to_csv("test_parkinsons.csv",index=False)

# define the file path and chunk size
file_path = 'SUSY.csv'
chunk_size = 10000

# create an empty dataframe to hold the data
df = pd.DataFrame()

# iterate over the file in chunks and append to the empty dataframe
i=0
for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    df = df.append(chunk)
    if i==3:
        break
print(df.shape)
print(df.head(5))
rows = df.shape[0]

# #shuffle rows of df
df = df.sample(frac=1)

train, test = df[:int(rows*0.8)], df[int(rows*0.8):]

train.to_csv("train_susy.csv", index=False)
test.to_csv("test_susy.csv",index=False)

