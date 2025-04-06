import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("..\\data\\public_data.csv")
X = df.iloc[:, df.columns != "class"]
Y = df["class"]
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)
x_test.to_csv("..\\data\\input_data.csv", index=False)
y_test.to_csv("..\\data\\input_classes.csv", index=False)