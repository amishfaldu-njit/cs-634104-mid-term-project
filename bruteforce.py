from library import get_frequent_itemset_lib_algos
from datetime import datetime
import pandas as pd
from itertools import combinations


def calculate_support(itemset: tuple, transactions: list[list]):
    counts = 0
    for transaction in transactions:
        if set(itemset).issubset(set(transaction)):
            counts += 1

    return counts / len(transactions)


def get_frequent_itemset(items: set, transactions, min_support, n=1):
    print(f"Generating frequent itemset for n = {n} \n")
    # print("Items: ", items, "\n")
    # print("Total items: ", len(items), "\n")
    if len(transactions) == 1:
        return []

    itemset = list(combinations(items, n))
    # print("Itemset: ", itemset, "\n")
    # If itemset contains only one item or no items, return empty list
    # because there are no more combinations possible
    if (len(itemset)) <= 1:
        print("Itemsets: No more itemset combinations possible", "\n")
        print("-------------------------------------------", "\n")
        return []

    frequent_itemset = []

    print("Itemsets:")
    for item in itemset:
        support = calculate_support(item, transactions)
        print(item, ": ", support)
        if support >= min_support:
            frequent_itemset.append({"item": set(item), "support": support})

    print("\n")
    print(
        "Frequent Itemset:\n",
        pd.DataFrame(frequent_itemset).to_string(index=False),
        "\n",
    )
    print("-------------------------------------------", "\n")

    frequent_itemset.extend(
        get_frequent_itemset(
            set([item for itemset in frequent_itemset for item in itemset["item"]]),
            transactions,
            min_support,
            n + 1,
        )
    )

    return frequent_itemset


def calculate_confidence(left, itemset, transactions):
    left_count = 0
    itemset_count = 0
    for transaction in transactions:
        if set(itemset).issubset(set(transaction)):
            itemset_count += 1
        if set(left).issubset(set(transaction)):
            left_count += 1

    return itemset_count / left_count


def get_association_rules(frequent_itemset, transactions, min_confidence):
    rules = []
    print("Generating association rules")
    itemsets = filter(lambda x: len(x) > 1, frequent_itemset)
    for itemset in itemsets:
        for i in range(1, len(itemset)):
            itemset_permutations = list(combinations(itemset, i))

            for itemset_p in itemset_permutations:
                left = set(itemset_p)
                right = itemset.difference(itemset_p)
                confidence = calculate_confidence(left, itemset, transactions)
                print("Rule: ", left, "=>", right, "Confidence: ", confidence)
                if confidence >= min_confidence:
                    rules.append(
                        {"left": left, "right": right, "confidence": confidence}
                    )

    print("\n", "-------------------------------------------", "\n")
    return rules


def bruteforce_algorithm(items, transactions, min_support, min_confidence):
    frequent_itemset = get_frequent_itemset(items, transactions, min_support)
    print(
        "Final Frequent Itemset:\n",
        pd.DataFrame(frequent_itemset).to_string(index=False),
        "\n",
    )
    print("-------------------------------------------", "\n")
    rules = get_association_rules(
        [itemset["item"] for itemset in frequent_itemset], transactions, min_confidence
    )
    print("Final Association Rules:\n", pd.DataFrame(rules).to_string(index=False), "\n")
    return rules


# Inputs from user

## Dataset selection input
dataset_mapping = {
    "1": "amazon",
    "2": "bestbuy",
    "3": "kmart",
    "4": "nike",
}
min_dataset_index = list(dataset_mapping.keys())[0]
max_dataset_index = list(dataset_mapping.keys())[-1]
print("Available datasets: ")
for key, value in dataset_mapping.items():
    print(f"{key}. {value}")
dataset_index = input(
    f"Choose a dataset to run the algorithm on ({min_dataset_index}-{max_dataset_index}): "
)
if dataset_index not in dataset_mapping.keys():
    print("Invalid dataset")
    exit()

## Min support input
try:
    min_support = float(input("Enter minimum support: "))
    if min_support < 0 or min_support > 1:
        print("Invalid minimum support")
        exit()
except ValueError:
    print("Invalid minimum support")
    exit()

## Min confidence input
try:
    min_confidence = float(input("Enter minimum confidence: "))
    if min_confidence < 0 or min_confidence > 1:
        print("Invalid minimum confidence")
        exit()
except ValueError:
    print("Invalid minimum confidence")
    exit()

# Load the dataset
transactions_file = f"./data/{dataset_mapping[dataset_index]}-transactions.csv"
transactions_df = pd.read_csv(transactions_file)
items_file = f"./data/{dataset_mapping[dataset_index]}-items.csv"
items_df = pd.read_csv(items_file)

# Run the algorithm
brute_start_time = datetime.now()
bruteforce_algorithm(
    set(items_df["Items"].tolist()),
    transactions_df["Transaction"].apply(lambda t: t.split(", ")).tolist(),
    min_support,
    min_confidence,
)
brute_end_time = datetime.now()

# Run the apriori algorithm
apriori_start_time = datetime.now()
get_frequent_itemset_lib_algos(
    transactions_df["Transaction"].apply(lambda t: t.split(", ")).tolist(),
    min_support,
    algorithm="apriori",
)
apriori_end_time = datetime.now()

# Run the fpgrowth algorithm
fpgrowth_start_time = datetime.now()
get_frequent_itemset_lib_algos(
    transactions_df["Transaction"].apply(lambda t: t.split(", ")).tolist(),
    min_support,
    algorithm="fpgrowth",
)
fpgrowth_end_time = datetime.now()

# Time comparison analysis
print("Time comparison analysis")
print("Bruteforce algorithm: ", brute_end_time - brute_start_time)
print("Apriori algorithm: ", apriori_end_time - apriori_start_time)
print("Fpgrowth algorithm: ", fpgrowth_end_time - fpgrowth_start_time)
