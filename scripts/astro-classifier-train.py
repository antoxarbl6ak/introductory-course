import xgboost as xgb
import os
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, log_loss, make_scorer
from sklearn.pipeline import Pipeline
from scipy.stats import uniform, randint

df = pd.read_csv(r"..\data\public_data.csv")
#df = df.drop(columns=["Row_id", "obj_ID", "run_ID", "rerun_ID", "cam_col", "field_ID", "spec_obj_ID", "plate", "fiber_ID"])
df = df.drop(columns=["Row_id"])
df["class"] = df["class"].map({"STAR": 0, "QSO": 1, "GALAXY": 2})

X = df.iloc[:, df.columns != "class"]
Y = df["class"]
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

pipeline = Pipeline([
    ('scaler', StandardScaler()),  # Масштабируем признаки
    ('xgb', xgb.XGBClassifier(
        objective="multi:softmax",
        eval_metric='logloss',
        random_state=42,
        n_jobs=-1
    ))
])

"""model = xgb.XGBClassifier(
    n_estimators=1000,
    objective="multi:softmax",
    num_class=3,
    random_state=42
)"""

"""cv_scores = cross_val_score(
    model,
    x_train,
    y_train,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)
print("cv scores:", cv_scores)"""

param_grid = {
    'xgb__n_estimators': [600],       # Количество деревьев
    'xgb__max_depth': [10],             # Глубина деревьев
    'xgb__learning_rate': [0.1],    # Скорость обучения
}
grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    scoring="accuracy",  
    cv=3,                 
    n_jobs=-1,    
)
grid_search.fit(x_train, y_train)
print("best params:", grid_search.best_params_)
print("best score:", grid_search.best_score_)


best_model = grid_search.best_estimator_
best_model.fit(x_train, y_train)

y_pred = best_model.predict(x_test)
print(classification_report(y_test, y_pred, digits=4))

best_model.save_model("..\\data\\bestmodel-gboost.json")
