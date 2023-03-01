import pandas as pd

# define the file path and chunk size
file_path = 'bike.csv'
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

df = df.drop(columns=['instant','dteday'])

train, test = df[:int(rows*0.8)], df[int(rows*0.8):]

train.to_csv("train_bike.csv", index=False)
test.to_csv("test_bike.csv",index=False)

