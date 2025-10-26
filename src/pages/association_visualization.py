import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pickle
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import mlxtend as ml
from app import app
import dash_cytoscape as cyto


# TO DISPLAY THE VISUALISATIONS OF COUNT OF THE ITEMS AND THE PERCENTAGES
##########################################################################
## importing the saved dataset model to descriptive visualization
file_name = 'src/models/bakery_initial.sav'
loaded_model = pickle.load(open(file_name,'rb'))
print(loaded_model)

## get count of the item 
count_items = loaded_model.Item.value_counts()[:10]
count_items = pd.DataFrame({'items':count_items.index, 'count':count_items.values})
print(count_items)
# get the percentage of the items
percentage_items = loaded_model.Item.value_counts(normalize=True)[:10]
percentage_items = pd.DataFrame({'items':percentage_items.index, 'percentage':percentage_items.values})
print(loaded_model)


## TO VISUALIZE THE HEAT MAP AND THE NETWORK GRAPH
##############################################################
# importing the finally created model of appriori association
file_name = 'src/models/final_model_appriori.sav'
loaded_model = pickle.load(open(file_name, 'rb'))


## MInING THE ASSOCIATION RULES USING THE SUPPORTS OBTAINED
rules = association_rules(loaded_model, metric='lift', min_threshold=0.1)
rules_copy = rules.copy()
print(rules)

## SORTING THE VALUES IN ORDER TO GET THE HIGHEST ASSOCIATION TO THE TOP
rules.sort_values("consequent support", ascending = False, inplace = True)
rules.head(20)


##  return recommended items
cols_keep = {'antecedents':'antecedents', 'consequents':'consequents', 'support':'support', 'confidence':'confidence', 'lift':'lift'}
cols_drop = ['antecedent support', 'consequent support', 'leverage', 'conviction']

## convert frozen set to strings
rules = pd.DataFrame(rules).rename(columns= cols_keep).sort_values(by=['lift'], ascending = False)
rules['antecedents'] = rules['antecedents'].str.join(',')
rules['consequents'] = rules['consequents'].str.join(',')

### creating a pivot matrix to create heatmap
pivot = rules.pivot(index = 'antecedents', 
                    columns = 'consequents', values= 'lift')





## network graph creation block
####################################################
antecedents_label_list = []
for i in rules_copy['antecedents']:
        antecedents_label_list.append(list(i)[0])

consequents_label_list = []
for i in rules_copy['consequents']:
        consequents_label_list.append(list(i)[0])

def vowel_remover(string):
    vowels = ('a', 'e', 'i', 'o', 'u')
    for x in string:
        if x in vowels:
            string = string.replace(x,"")
    return string

whole_item_list = list(set(antecedents_label_list+consequents_label_list))
data_list=[]
for i in range(len(whole_item_list)):
    data_key={}
    values={}
    data_key['data']=values
    data_key['data']['id']=vowel_remover(whole_item_list[i])
    data_key['data']['label']=whole_item_list[i]
    data_list.append(data_key)

for i in range(len(antecedents_label_list)):
    data_key={}
    values={}
    data_key['data']=values
    data_key['data']['source']=vowel_remover(antecedents_label_list[i])
    data_key['data']['target']=vowel_remover(consequents_label_list[i])
    data_list.append(data_key)

#### styling the network graph
default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#A3C4BC'
        }
    }
]











# LAYOUT OF THE PAGE (VISUALIZING ASSOCIATION)
################################################
layout = html.Div([
    dbc.Container([

        ## main topic
        dbc.Row([
            dbc.Col(html.H1(children='Bakery Market Basket', className="main-topic-color"), className="mb-2")
        ],className = "main-topic"),
        ## main sub topic
        dbc.Row([
            dbc.Col(html.H6(children='Visualising Bakery Transactions and association', className="main-topic-color"), className="mb-2")
        ],className = "main-topic"),

      
    ## heading of the count and the percentage visualization
    dbc.Row([
                dbc.Col(dbc.Card([html.H4(children="Bakery Item Count ",className="text-center  text-nav main-topic-color")
                                  
                                            ], body=True, color="light",className = "card-col-main-row")
                        , className="mt-2 mb-1",
                        )
                ], className="main-row"
                ),

    ## count graph and the percentage graph
    dbc.Row([


        dbc.Col(dcc.Graph(id='count-bar'), width=6),
        dbc.Col(dcc.Graph(id='percentage-bar'), width=6)

        ],className="f-card"),

    ## heading of the visualization of the heat map
    dbc.Row([
                dbc.Col(dbc.Card([html.H4(children="Visualization Of Association Rules ",className="text-center text-dark bg-white text-nav")
                                  
                                            ], body=True, color="light",className = "card-col-main-row")
                        , className="mt-5 mb-1",
                        )
                ], className="main-row"
                ),
    ## visualization of the heat map
    dbc.Row([

                dbc.Col(dcc.Graph(id='graph-heat'))
 
            ],className="f-card"),
    
    ## heading of the visualization of the network graph
    dbc.Row([
                dbc.Col(dbc.Card([html.H4(children="Visualization Of Association Rules Using Network Graph ",className="text-center text-dark bg-white text-nav")
                                  
                                            ], body=True, color="light",className = "card-col-main-row")
                        , className="mt-5 mb-1",
                        )
                ], className="main-row"
                ),
    ## visualization of the network graph
    dbc.Row([

            dbc.Col(html.Div([
    #html.P(""),
                cyto.Cytoscape(
                    id='cytoscape',
                    elements= data_list,
                    stylesheet=default_stylesheet,
                    layout={'name': 'circle'},
                    style={'width': '80%', 'height': '500px'} # configure the size as you want
                )
            ],
            style = {
                "background":"white"
            }
            ))
 
       ],className="f-card"),
    

       

],className="container-out")


])

# page callbacks
############################################################################################################################


## callback function for count and the percentage bargraphs
@app.callback([
    Output(component_id='count-bar',component_property='figure'),
    Output(component_id='percentage-bar',component_property='figure')],
    [Input('count-bar', 'hoverData')]
    
)
def update_graph(hover_data):


    barchart_count = px.bar(
        data_frame = count_items,
        title = 'Total Number of Sales by Item',
        x = 'items',
        y =  'count',
        labels={ # replaces default labels by column name
                "items": "Items",  "count": "Count"
            }
    
    )
    barchart_count.layout.template = 'seaborn'

    barchart_percentage = px.bar(
        data_frame = percentage_items,
        title = 'Percentage of Sales by Item',
        x = 'items',
        y =  'percentage',
        labels={ # replaces default labels by column name
                "items": "Items",  "percentage": "Percentage"
            }

    )

    barchart_percentage.layout.template = 'seaborn'
   



    return barchart_count,barchart_percentage



## callback function for heat map
@app.callback(Output("graph-heat", "figure"), [Input("graph-heat", "hover-data")])
def filter_heatmap(cols):
    fig = px.imshow(pivot, color_continuous_scale=px.colors.sequential.Plasma,
                title="Heat Map")
    fig.update_layout(title_font={'size':27}, title_x=0.5,
                        width = 1254, height = 800)
    fig.update_traces(hoverongaps=False,
                  hovertemplate="anticident: %{y}"
                                "<br>concequant: %{x}"
                                "<br>lift: %{z}<extra></extra>"
                  )

    fig.layout.template = 'seaborn'
    

    return fig





