import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder

def get_frequent_itemset_lib_algos(transactions, min_support, min_confidence, algorithm="apriori"):
    te = TransactionEncoder()
    te_data = te.fit_transform(transactions)
    ohe_transactions = pd.DataFrame(te_data, columns=te.columns_)
    lib_apriori_association_rules = None

    if algorithm == "apriori":
        lib_apriori_association_rules = association_rules(apriori(ohe_transactions, min_support=min_support, use_colnames=True), metric="confidence", min_threshold=min_confidence)
    
    if algorithm == "fpgrowth":
        lib_apriori_association_rules = association_rules(fpgrowth(ohe_transactions, min_support=min_support, use_colnames=True), metric="confidence", min_threshold=min_confidence)
    
    print(f"\n\nAssociation Rules from library {algorithm} algorithm:\n")
    for i, rule in enumerate(lib_apriori_association_rules.to_dict("records")):
        print(f"Rule {i+1}: {set(rule['antecedents'])} -> {set(rule['consequents'])}\nConfidence: {rule['confidence'] * 100:.2f}%\nSupport: {rule['support'] * 100:.2f}%\n")

    return lib_apriori_association_rules
