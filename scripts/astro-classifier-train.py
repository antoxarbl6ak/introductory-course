import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import classification_report
from scipy.stats import uniform, randint

df = pd.read_csv("..\data\public_data.csv")
#df = df.drop(columns=["Row_id", "obj_ID", "run_ID", "rerun_ID", "cam_col", "field_ID", "spec_obj_ID", "plate", "fiber_ID"])
df = df.drop(columns=["Row_id"])
df["class"] = df["class"].map({"STAR": 0, "QSO": 1, "GALAXY": 2})

X = df.iloc[:, df.columns != "class"]
Y = df["class"]
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

model = xgb.XGBClassifier(
    n_estimators=1000,
    objective="multi:softmax",
    num_class=3,
    random_state=42
)

cv_scores = cross_val_score(
    model,
    x_train,
    y_train,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)
print("cv scores:", cv_scores)

param_grid = {
    "learning_rate": [0.12],
    "max_depth": [9],
    "min_child_weight": [2],
    "n_estimators": [1000]
}
grid_search = GridSearchCV(
    estimator=model, 
    param_grid=param_grid,
    scoring="accuracy",
    cv=5,
    n_jobs=-1)
grid_search.fit(x_train, y_train)
print("best params:", grid_search.best_params_)
print("best score:", grid_search.best_score_)

"""param_random = {
    "learning_rate": uniform(0.01, 0.3),
    "max_depth": randint(3, 10),
    "min_child_weight": randint(1, 10),
    "gamma": uniform(0, 0.5)
}
random_search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_random,
    n_iter=100,
    scoring="accuracy",
    cv=5,
    n_jobs=-1,
    random_state=42
)
random_search.fit(x_train, y_train)
print("best params:", random_search.best_params_)
print("best score:", random_search.best_score_)"""

best_model = grid_search.best_estimator_
best_model.fit(x_train, y_train)

#y_pred = best_model.predict(x_test)
#print(classification_report(y_test, y_pred, digits=4))

best_model.save_model("..\\data\\bestmodel-gboost.json")
