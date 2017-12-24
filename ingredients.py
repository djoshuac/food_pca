import json
from collections import Counter
from sklearn import linear_model, decomposition
from sklearn.preprocessing import normalize
from utils.csv_wrapper import save_csv
import numpy as np

def most_common_fields(data, num_fields):
    field_counts = Counter()
    for d in data:
        for key in d["ingredients"]:
            field_counts[key] += 1
    return [c[0] for c in field_counts.most_common(num_fields)]

def vectorize(data, fields):
    for d in data:
        yield [
            1 if f in d["ingredients"] else 0
            for f in fields
        ]

def pca(data):
    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    pca = decomposition.PCA(n_components=2)
    pca.fit(X)

    # X = normalize(data)
    #
    # pca = decomposition.PCA(n_components=3)
    # pca.fit(X)
    # X = pca.transform(X)
    print(pca.explained_variance_ratio_)
    print(pca.n_components_)

    return X, pca.components_

if __name__ == "__main__":
    train = json.load(open("./data/train.json"))
    fields = most_common_fields(train, 100)
    data = list(vectorize(train, fields))

    X, components = pca(data)

    save_csv("components.csv", fields, components)


    import matplotlib.pyplot as plt
    plt.scatter(X[:,0], X[:,1])
    plt.show()

    count = 0
    for food, recipe in zip(X, train):
        if food[0] > 0.7:
            print(recipe, food)
            count += 1
    print(count)


    save_csv("pca_food.csv", ["saltiness", "dessertiness"], X)
