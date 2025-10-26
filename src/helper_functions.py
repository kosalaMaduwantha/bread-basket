from flask import Flask, jsonify, request, make_response,render_template
from flask_cors import CORS, cross_origin
import numpy as np
import pickle
import json
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import mlxtend as ml
import os
import pandas as pd

os.getcwd()

## initial Bakery data imported
file_name1 = 'models/bakery_initial.sav'
initial_model = pickle.load(open(file_name1, 'rb'))
initial_model.Item.value_counts(normalize=True)[:10]

## creating pivote table
pv = pd.pivot_table(initial_model)


## LAODING THE CREATED MODEL USING pickle LIBRARY
file_name = 'flaskAPI/models/final_model_appriori.sav'
loaded_model = pickle.load(open(file_name, 'rb'))


print(loaded_model)

## MIING THE ASSOCIATION RULES USING THE SUPPORTS OBTAINED
rules = association_rules(loaded_model, metric='lift', min_threshold=0.1)
print(rules)



## SORTING THE VALUES IN ORDER TO GET THE HIGHEST ASSOCIATION TO THE TOP
rules.sort_values("lift", ascending = False, inplace = True)
rules.head(10)




def recomended_mining():
    # Recommendation of Market Basket
    rec_rules = rules[ (rules['lift'] > 1) & (rules['confidence'] >= 0.2) ]

    # Recommendation of Market Basket Dataset
    cols_keep = {'antecedents':'item_1', 'consequents':'item_2', 'support':'support', 'confidence':'confidence', 'lift':'lift'}
    cols_drop = ['antecedent support', 'consequent support', 'leverage', 'conviction']


    recommendation_basket = pd.DataFrame(rec_rules).rename(columns= cols_keep).drop(columns=cols_drop).sort_values(by=['lift'], ascending = False)
    recommendation_basket['item_1'] = recommendation_basket['item_1'].str.join('()')
    recommendation_basket['item_2'] = recommendation_basket['item_2'].str.join('()')
    

    return recommendation_basket

recommendation = recomended_mining()
print(recommendation)


## GET THE RECOMMENDED ITEMS BY ITEMS
def items_brought_together(item_spec):

    items = []
    for index, row in rules.iterrows():
        anti, = row['antecedents']
        conc, = row['consequents']
        
        if anti == item_spec:
            items.append(conc)

    return items


iems = items_brought_together('Tea')
print(iems)


