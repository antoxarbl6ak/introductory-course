import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def classify(inputcsv, outputcsv="..\\data\\output.csv", logs=False):
    df = pd.read_csv(inputcsv)
    if "Row_id" in df.keys():
        df_temp = df.drop(columns=["Row_id"])
    else:
        df_temp = df

    # loading model
    model = joblib.load("..\\data\\best_model-gboost.joblib")
    #model.load_model(r"D:\Users\anton\Desktop\rtu-mirea\practice\introductory-course\data\bestmodel-gboost.json")

    
    # predicting
    predictions = model.predict(df_temp)
    if logs:
        print(predictions[:10])
    df["class"] = predictions
    df["class"] = df["class"].map({0: "STAR", 1: "QSO", 2: "GALAXY"})

    # saving
    df.to_csv(outputcsv, index=False)


if __name__ == "__main__":
    classify(r"D:\Users\anton\Desktop\rtu-mirea\practice\introductory-course\data\input_data.csv", logs=True)
    df_pred = pd.read_csv("..\\data\\output.csv")
    y_pred = df_pred["class"]
    y_test = pd.read_csv(r"D:\Users\anton\Desktop\rtu-mirea\practice\introductory-course\data\input_classes.csv")
    y_test["class"] = y_test["class"].map({0: "STAR", 1: "QSO", 2: "GALAXY"})
    print(classification_report(y_test, y_pred=y_pred, digits=4))


