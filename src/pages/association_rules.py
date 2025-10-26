import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, dash_table as dt
import dash_bootstrap_components as dbc
import pickle
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import mlxtend as ml
from app import app

## IMPORTING THE FINAL MODEL CREATED USING PICKLE
###################################################
## LAODING THE CREATED MODEL USING pickle LIBRARY
file_name = 'src/models/final_model_appriori.sav'
loaded_model = pickle.load(open(file_name, 'rb'))


print(loaded_model)

## MIING THE ASSOCIATION RULES USING THE SUPPORTS OBTAINED
rules = association_rules(loaded_model, metric='lift', min_threshold=0.1)
print(rules)

## SORTING THE VALUES IN ORDER TO GET THE HIGHEST ASSOCIATION TO THE TOP
rules.sort_values("consequent support", ascending = False, inplace = True)
rules.head(20)





## FUNCTION OF OUTPUTTING THE RECOMMENDED BASKET OF BAKERY ITEMS
#################################################################
def recomended_mining():
    # Recommendation of Market Basket
    rec_rules = rules[ (rules['lift'] > 1) & (rules['confidence'] >= 0.2) ]

    # Recommendation of Market Basket Dataset
    cols_keep = {'antecedents':'antecedents', 'consequents':'consequents', 'support':'support', 'confidence':'confidence', 'lift':'lift'}
    cols_drop = ['antecedent support', 'consequent support', 'leverage', 'conviction']

    # Converting the frozenset to normal string 
    recommendation_basket = pd.DataFrame(rec_rules).rename(columns= cols_keep).drop(columns=cols_drop).sort_values(by=['lift'], ascending = False)
    recommendation_basket['antecedents'] = recommendation_basket['antecedents'].str.join(',')
    recommendation_basket['consequents'] = recommendation_basket['consequents'].str.join(',')
    

    return recommendation_basket

## used in table of top 10 associations
recommendation = recomended_mining()






## displaying the items with highest confidence
#################################################
sorted_df = rules.sort_values(["consequent support"], ascending=False).drop_duplicates(["consequent support"],keep = 'last')
print(sorted_df)

cols_keep = {'antecedents':'antecedents', 'consequents':'consequents', 'support':'support', 'confidence':'confidence', 'lift':'lift'}
cols_drop = ['antecedent support', 'consequent support', 'leverage', 'conviction']

recommendation_basket = pd.DataFrame(sorted_df).rename(columns= cols_keep).sort_values(by=['confidence'], ascending = False)
recommendation_basket['antecedents'] = recommendation_basket['antecedents'].str.join(',')
recommendation_basket['consequents'] = recommendation_basket['consequents'].str.join(',')





## layout of the card component of the items
############################################
def generate_ios(item):

    return (dbc.Row([
                dbc.Col(dbc.Card([html.H5(children=item[1],className="text-left text-dark bg-white text-nav"),
                                  html.H6(children=item[3],className="text-left text-dark bg-white text-nav mt-2")
                                            ], body=True, color="light",className = "card-col-k")
                        , className="mt-1 mb-1",
                        )
                ]))









## CRETING THE TABLE OF ASSOCIATION
###################################
def iter_row(item):
    return (html.Tr([html.Td(html.P(item[0])), html.Td(item[1]), html.Td(item[3]), html.Td(item[4])]))

## table header
table_header = [
    html.Thead(html.Tr([html.Th("antecedents", className=" main-topic-color"), html.Th("consequents", className=" main-topic-color"),html.Th("confidence", className=" main-topic-color"),html.Th("lift", className=" main-topic-color")]))
]


## table body
table_body = [html.Tbody([iter_row(r) for i,r in recommendation.head(10).iterrows()])]
## whole table to disply recommended item lists
table = dbc.Table(children = table_header + table_body, bordered=True, striped = True, hover=True)



# card content for the table of associations
#############################################
card_content = [
    dbc.CardHeader(html.H5("Highest selling combos", className=" main-topic-color"), className = "card-header-k"),
    dbc.CardBody(
        children = [
           
            html.P([

                # table created before
                table
                
                
                ],
                className="card-text",
            ),
        ],className = "card-body-k"
    ),
]





## DISPLAY ASSOCIATED ITEMS OF SPECIFIC ITEM
###############################################
## GET THE RECOMMENDED ITEMS BY ITEMS
def recomended_mining_items(confidence):
    # Recommendation of Market Basket
    rec_rules = rules[ (rules['lift'] > 1) & (rules['confidence'] >= confidence) ]

    # Recommendation of Market Basket Dataset
    cols_keep = {'antecedents':'antecedents', 'consequents':'consequents', 'support':'support', 'confidence':'confidence', 'lift':'lift'}
    cols_drop = ['antecedent support', 'consequent support', 'leverage', 'conviction']


    recommendation_basket = pd.DataFrame(rec_rules).rename(columns= cols_keep).drop(columns=cols_drop).sort_values(by=['confidence'], ascending = False)
    recommendation_basket['antecedents'] = recommendation_basket['antecedents'].str.join(',')
    recommendation_basket['consequents'] = recommendation_basket['consequents'].str.join(',')
    

    return recommendation_basket

## change the confidence here
recommendation_items = recomended_mining_items(0.2)
print(recommendation)


## second card content for the second table of 
# the association displaying the associations of specific items
###############################################################
card_content2 = [
    dbc.CardBody(
        children = [
            html.H2("Best Selling Combos", className="card-title main-topic-color"),
            html.P([

                ## table of association
                html.Div(id="final_table")
                
                
                ],
                className="card-text",
            ),
        ],className = "card-body-k"
    ),
]


df_filtered = recommendation_items[(recommendation_items["antecedents"]=='Cake')]
columns=[{"name": i, "id": i} for i in df_filtered.columns]
print(columns)
data=df_filtered.to_dict('records')
print(data)










## MAIN TOPIC AND THE SUB TOPIC
################################
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Bakery Market Basket ', className=" main-topic-color"), className="mb-2 mr-4")
        ],className = "main-topic"),
        dbc.Row([
            dbc.Col(html.H6(children='Visualising Bakery Association rules',className=" main-topic-color"), className="mb-2")
        ],className = "main-topic"),
# choose between cases or deaths
      
## SECON MAIN TOPIC
# for some reason, font colour remains black if using the color option
    dbc.Row([
                dbc.Col(dbc.Card([html.H4(children="Association rules ",className="text-center text-nav main-topic-color")
                                  
                                            ], body=True, color="light",className = "card-col-main-row")
                        , className="mt-2 mb-1",
                        )
                ], className="main-row"
                ),


## container for items with highest support and the top 10 items which has highest lift
    dbc.Row([
        dbc.Col([        
               generate_ios(r) for i,r in recommendation_basket.head(10).iterrows()    
        ], width=3),       
        dbc.Col([            
            dbc.Row([
                    dbc.Col(dbc.Card(children = card_content, color="#6495ED", outline=True, className = 'card-k')),                    
            ])                        
            ], width=9,className="mt-1")
        ],className="f-card"),


## THIRD TOPIC (item association)
    dbc.Row([
                dbc.Col(dbc.Card([html.H4(children="Item association",className="text-center text-nav main-topic-color")
                                  
                                            ], body=True, color="light",className = "card-col-main-row")
                        , className="mt-5 mb-1",
                        )
                ], className="main-row"
                ),

## DISPLAYING THE ASSOCIATED ITEM FOR SPECIFIC ITEMS                            
    dbc.Row([
        dbc.Col([        
               dbc.Row([
                dbc.Col(dbc.Card([html.H5(children="Select an item",className="text-left text-dark bg-white text-nav"),
                                  
                                  
                                   dcc.Dropdown(id='dropdown_d1', options=[{'label': r, 'value': r} for r in recommendation_items['antecedents'].unique()], value=None),

                                    html.H3(id="dyna-word",className="text-left text-dark bg-white text-nav mt-4"),

                                            ], body=True, color="light",className = "card-col-k-2")
                        , className="mt-1 mb-1",
                        )
                ])
        ], width=3),

       ## second table of association of specific items
        dbc.Col([            
            dbc.Row([
                    dbc.Col(dbc.Card(card_content2, color="#F08080", outline=True, className = 'card-k-2')),                    
            ])            
            ], width=9,className="mt-1")

        ],className="f-card"),



],className="container-out")


])

# page callbacks
##################################################
## callback of the second table which dispalys association rules of specific items
@app.callback(Output('final_table', 'children'),
          [
            Input('dropdown_d1', 'value'),
          ])
def update_table(d1):

    if(d1 != None):
        df_filtered = recommendation_items[(recommendation_items["antecedents"]==d1)]

        return [dt.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_filtered.columns],
            data=df_filtered.to_dict('records'),
        )]
    else:
        print("none")
        return []

## callback to change the item text dynamically
@app.callback(Output('dyna-word', 'children'),
          [
            Input('dropdown_d1', 'value'),
          ])
def update_text(d1):
    print(d1)
    if(d1 != None):
        df_filtered = d1
        return df_filtered
    else:
        return ()







