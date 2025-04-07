import pandas as pd
import joblib
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

df = pd.read_csv("..\data\public_data.csv")
df = df.drop(columns=["Row_id", "obj_ID", "run_ID", "rerun_ID", "cam_col", "field_ID", "spec_obj_ID", "plate", "fiber_ID"])
df["class"] = df["class"].map({"STAR": 0, "QSO": 1, "GALAXY": 2})

X = df.iloc[:, df.columns != "class"]
Y = df["class"]
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

pipe = Pipeline([("scaler", StandardScaler()),
                 ("svm", SVC())])
param_grid = {
    'svm__C': [0.1, 1, 10],          
    'svm__gamma': [0.1, 1, 'scale'], 
    'svm__kernel': ['rbf', 'linear']  
}

grid_search = GridSearchCV(
    estimator=pipe,
    param_grid=param_grid,
    cv=5,          
    scoring='accuracy', 
    n_jobs=-1           
)

grid_search.fit(x_train, y_train)

best_model = grid_search.best_estimator_
best_model.fit(x_train, y_train)

y_pred = best_model.predict(x_test)
print(classification_report(y_test, y_pred, digits=4))

joblib.dump(best_model, "..\\data\\best_model-svc.joblib")
