import pandas as pd
import xgboost as xgb
import joblib
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split

df  = pd.read_csv(r"..\data\public_data_co2.csv")
df["date"] = pd.to_datetime(df["date"])
df_long = df.melt(id_vars=["date"],
                      var_name="country",
                      value_name="co2")


n_clusters = 3
country_matrix = df.drop(columns=["date"]).T
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(country_matrix)
countries_to_clusters = dict(zip(df.columns[1:], clusters))
df_long["clusters"] = df_long["country"].map(lambda x: countries_to_clusters[x])
df_long["clusters"] = df_long["clusters"].astype("category")
df_long["country"] = df_long["country"].astype("category")
df_long = df_long.sort_values(by=["date"])

for cluster_id in range(n_clusters):
    cluster_data = df_long[df_long["clusters"] == cluster_id].copy()

    cluster_data["lag1"] = cluster_data.groupby("country", observed=False)["co2"].shift(1)
    cluster_data["lag7"] = cluster_data.groupby("country", observed=False)["co2"].shift(7)
    cluster_data["lag30"] = cluster_data.groupby("country", observed=False)["co2"].shift(30)
    cluster_data["lag365"] = cluster_data.groupby("country", observed=False)["co2"].shift(365)
    cluster_data["month"] = cluster_data["date"].dt.month
    cluster_data["rolling_mean_7"] = cluster_data.groupby("country", observed=False)["co2"].transform(
        lambda x: x.rolling(window=7).mean()
    )
    cluster_data["rolling_std_7"] = cluster_data.groupby("country", observed=False)["co2"].transform(
        lambda x: x.rolling(window=7).std()
    )
    cluster_data["rolling_mean_30"] = cluster_data.groupby("country", observed=False)["co2"].transform(
        lambda x: x.rolling(window=30).mean()
    )
    cluster_data["rolling_max_365"] = cluster_data.groupby("country", observed=False)["co2"].transform(
        lambda x: x.rolling(window=365).max()
    )
    cluster_data["dif1"] = cluster_data.groupby("country", observed=False)["co2"].diff(1)
    cluster_data["dif7"] = cluster_data.groupby("country", observed=False)["co2"].diff(7)
    cluster_data = cluster_data.dropna()

    train = cluster_data[cluster_data["date"] < "2023-04-01"]
    test = cluster_data[cluster_data["date"] >= "2023-04-01"]
    x_train = train[["country", "lag1", "lag7", "lag30", "lag365", "month",
                    "rolling_mean_7", "rolling_std_7", "rolling_mean_30", "rolling_max_365",
                    "dif1", "dif7"]]
    y_train = train["co2"]
    x_test = test[["country", "lag1", "lag7", "lag30", "lag365", "month",
                    "rolling_mean_7", "rolling_std_7", "rolling_mean_30", "rolling_max_365",
                    "dif1", "dif7"]]
    y_test = test["co2"]

    model = xgb.XGBRegressor(enable_categorical=True)
    model.fit(x_train, y_train)
    score = model.score(x_test, y_test)
    print(f"cluster{cluster_id}: {score:.4f}")

    joblib.dump(model, rf"..\data\prophet{cluster_id}.joblib")


