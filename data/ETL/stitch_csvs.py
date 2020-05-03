import pandas as pd
import glob

path = r'../../birthdays' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
sorted_frame = frame.sort_values('birthday')
sorted_frame.to_csv('../../all_birthdays/birthday.csv', index=False)