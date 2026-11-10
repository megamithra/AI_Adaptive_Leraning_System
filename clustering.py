import pandas as pd
from sklearn.cluster import KMeans

def run_clustering():
    data = pd.read_csv("data.csv")

    X = data[['study_hours', 'quiz_score', 'accuracy', 'attendance']]

    model = KMeans(n_clusters=3, random_state=42)

    data['cluster'] = model.fit_predict(X)

    return data, model