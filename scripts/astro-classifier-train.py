import xgboost as xgb
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, RandomizedSearchCV
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
    ('scaler', StandardScaler()),
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



"""param_grid = {
    'learning_rate': [0.01, 0.1, 0.2],  # Оптимальный шаг обучения
    'max_depth': [3, 5, 7],              # Баланс сложности
    'min_child_weight': [1, 3, 5],       # Контроль переобучения
    'gamma': [0, 0.1, 0.2],             # Минимальное улучшение
    'subsample': [0.6, 0.8, 1.0],            # Доля данных для дерева
    'colsample_bytree': [0.8, 1.0],     # Доля признаков
    'reg_alpha': [0, 0.1, 0.5],         # L1-регуляризация
    'reg_lambda': [0.5, 1, 1.5],        # L2-регуляризация
    'n_estimators': [100, 200, 300, 600]          # Число деревьев
}
grid_search = GridSearchCV(
    estimator=pipeline.,
    param_grid=param_grid,
    scoring="roc_auc",  
    cv=StratifiedKFold(5, shuffle=True, random_state=42),                 
    n_jobs=-1,    
)
grid_search.fit(x_train, y_train)
print("best params:", grid_search.best_params_)
print("best score:", grid_search.best_score_)"""

param_dist = {
    'xgb__learning_rate': uniform(0.01, 0.3),  
    'xgb__max_depth': randint(3, 10),   
    'xgb__min_child_weight': randint(1, 10),   
    'xgb__gamma': uniform(0, 0.5),       
    'xgb__subsample': uniform(0.6, 0.4),      
    'xgb__colsample_bytree': uniform(0.6, 0.4), 
    'xgb__reg_alpha': uniform(0, 1),      
    'xgb__reg_lambda': uniform(0, 1),       
    'xgb__n_estimators': randint(100, 800)      
}

random_search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_dist,
    n_iter=300,
    scoring='roc_auc', 
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    n_jobs=-1,
    random_state=42
)

random_search.fit(x_train, y_train)


best_model = random_search.best_estimator_
best_model.fit(x_train, y_train)

y_pred = best_model.predict(x_test)
print(classification_report(y_test, y_pred, digits=4))

joblib.dump(best_model, "..\\data\\best_model-gboost.joblib")
