# import pandas


# df = pandas.read_csv('dataset.csv')

# for index, row in df.iterrows():
#     print(row.to_dict())

from faker import Faker

f = Faker()
print(f.email() )
