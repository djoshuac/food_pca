import json
from collections import Counter
from sklearn import linear_model, decomposition
from sklearn.preprocessing import normalize


def basis_vector(data):
    field_counts = Counter()
    for d in data:
        for key in d["ingredients"]:
            field_counts[key] += 1
    return [c[0] for c in field_counts.most_common(100)]

def vectorize(data, basis):
    for d in data:
        yield [
            1 if b in d["ingredients"] else 0
            for b in basis
        ]

def pca(data):
    X = normalize(data)

    pca = decomposition.PCA(n_components=2)
    pca.fit(X)
    X = pca.transform(X)
    # import pdb; pdb.set_trace()

    for c in pca.components_:
        print(" ".join(map(str, c)))

    return X

if __name__ == "__main__":
    train = json.load(open("./data/train.json"))
    basis = basis_vector(train)
    data = list(vectorize(train, basis))

    X = pca(data)
    print(",".join(basis))


    import matplotlib.pyplot as plt
    print(X)
    plt.scatter(X[:,0], X[:,1])
    plt.show()
