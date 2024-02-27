import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth
from mlxtend.preprocessing import TransactionEncoder

def get_frequent_itemset_lib_algos(transactions, min_support, algorithm="apriori"):
    te = TransactionEncoder()
    te_data = te.fit_transform(transactions)
    ohe_transactions = pd.DataFrame(te_data, columns=te.columns_)

    if algorithm == "apriori":
        return apriori(ohe_transactions, min_support=min_support, use_colnames=True)
    
    if algorithm == "fpgrowth":
        return fpgrowth(ohe_transactions, min_support=min_support, use_colnames=True)
