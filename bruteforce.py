from itertools import combinations


def calculate_support(itemset: tuple, transactions: list[list]):
    counts = 0
    for transaction in transactions:
        if set(itemset).issubset(set(transaction)):
            counts += 1

    return counts / len(transactions)


def get_frequent_itemset(items: set, transactions, min_support, n=1):
    # print(f"Generating frequent itemset for n = {n} \n")
    # print("Items: ", items, "\n")
    # print("Total items: ", len(items), "\n")
    if len(transactions) == 1:
        return []

    itemset = list(combinations(items, n))
    # print("Itemset: ", itemset, "\n")
    # If itemset contains only one item or no items, return empty list
    # because there are no more combinations possible
    if (len(itemset)) <= 1:
        # print("Itemsets: No more itemset combinations possible", "\n")
        # print("-------------------------------------------", "\n")
        return []

    frequent_itemset = []

    # print("Itemsets:")
    for item in itemset:
        support = calculate_support(item, transactions)
        # print(item, ": ", support)
        if support >= min_support:
            frequent_itemset.append({"item": set(item), "support": support})

    # print("\n")
    # print(
    #     "Frequent Itemset:\n",
    #     pd.DataFrame(frequent_itemset).to_string(index=False),
    #     "\n",
    # )
    # print("-------------------------------------------", "\n")

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
    # print("Generating association rules")
    itemsets = filter(lambda x: len(x["item"]) > 1, frequent_itemset)
    for itemset in itemsets:
        for i in range(1, len(itemset["item"])):
            itemset_permutations = list(combinations(itemset["item"], i))

            for itemset_p in itemset_permutations:
                left = set(itemset_p)
                right = itemset["item"].difference(itemset_p)
                confidence = calculate_confidence(left, itemset["item"], transactions)
                # print("Rule: ", left, "=>", right, "Confidence: ", confidence)
                if confidence >= min_confidence:
                    rules.append(
                        {
                            "left": left,
                            "right": right,
                            "confidence": confidence,
                            "support": itemset["support"],
                        }
                    )

    # print("\n", "-------------------------------------------", "\n")
    return rules


def bruteforce_algorithm(items, transactions, min_support, min_confidence):
    frequent_itemset = get_frequent_itemset(items, transactions, min_support)
    # print(
    #     "Final Frequent Itemset:\n",
    #     pd.DataFrame(frequent_itemset).to_string(index=False),
    #     "\n",
    # )
    # print("-------------------------------------------", "\n")
    rules = get_association_rules(frequent_itemset, transactions, min_confidence)
    print("\n\nFinal Association Rules:\n")
    for i, rule in enumerate(rules):
        print(
            f"Rule {i+1}: {rule['left']} -> {rule['right']}\nConfidence: {rule['confidence'] * 100:.2f}%\nSupport: {rule['support'] * 100:.2f}%\n"
        )
    return rules
