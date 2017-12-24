import json
from collections import Counter, namedtuple
from sklearn import linear_model, decomposition
from sklearn.preprocessing import normalize
from utils.csv_wrapper import save_csv, load_csv

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
    X = normalize(data)
    pca = decomposition.PCA(n_components=10)
    pca.fit(X)
    X = pca.transform(X)
    print(pca.explained_variance_ratio_)
    print(sum(pca.explained_variance_ratio_))

    return X, pca.components_

def boat(value):
    if value == "":
        return 0
    else:
        return float(value)

if __name__ == "__main__":
    parse_map = {
        "NDB_No": str,
        "Shrt_Desc": str,
        "Water_g": boat,
        "Energ_Kcal": boat,
        "Protein_g": boat,
        "Lipid_Tot_g": boat,
        "Ash_g": boat,
        "Carbohydrt_g": boat,
        "Fiber_TD_g": boat,
        "Sugar_Tot_g": boat,
        "Calcium_mg": boat,
        "Iron_mg": boat,
        "Magnesium_mg": boat,
        "Phosphorus_mg": boat,
        "Potassium_mg": boat,
        "Sodium_mg": boat,
        "Zinc_mg": boat,
        "Copper_mg": boat,
        "Manganese_mg": boat,
        "Selenium_mewg": boat,
        "Vit_C_mg": boat,
        "Thiamin_mg": boat,
        "Riboflavin_mg": boat,
        "Niacin_mg": boat,
        "Panto_Acid_mg": boat,
        "Vit_B6_mg": boat,
        "Folate_Tot_mewg": boat,
        "Folic_Acid_mewg": boat,
        "Food_Folate_mewg": boat,
        "Folate_DFE_mewg": boat,
        "Choline_Tot_mg": boat,
        "Vit_B12_mewg": boat,
        "Vit_A_IU": boat,
        "Vit_A_RAE": boat,
        "Retinol_mewg": boat,
        "Alpha_Carot_mewg": boat,
        "Beta_Carot_mewg": boat,
        "Beta_Crypt_mewg": boat,
        "Lycopene_mewg": boat,
        "Lut_and_Zea_mewg": boat,
        "Vit_E_mg": boat,
        "Vit_D_mewg": boat,
        "Vit_D_IU": boat,
        "Vit_K_mewg": boat,
        "FA_Sat_g": boat,
        "FA_Mono_g": boat,
        "FA_Poly_g": boat,
        "Cholestrl_mg": boat,
        "GmWt_1": boat,
        "GmWt_Desc1": str,
        "GmWt_2": boat,
        "GmWt_Desc2": str,
        "Refuse_Pct": boat
    }
    train = list(load_csv("./nuts.csv", ",", parse_map))

    fields = [key for key in parse_map if parse_map[key] == boat and key != "GmWt_2" and key != "GmWt_1"]
    Row = namedtuple("Row", fields)
    clean = []
    for row in train:
        cleaned = [getattr(row, d) for d in fields]
        clean.append(Row(*cleaned))

    X, components = pca(clean)
    save_csv("components.csv", fields, components)

    import matplotlib.pyplot as plt
    plt.scatter(X[:,0], X[:,1])
    plt.show()
    #
    # plt.scatter(X[:,0], X[:,2])
    # plt.show()
    #
    # plt.scatter(X[:,1], X[:,2])
    # plt.show()

    count = 0
    for nutr, food in zip(X, train):
        if nutr[0] > 0.7:
            print(nutr, food[1])
            count += 1
    print(count)


    save_csv("pca_food.csv", ["saltiness", "dessertiness"], X)
