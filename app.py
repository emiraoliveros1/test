
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# 
# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 
# 
# 
# 

# # Both combined

# In[13]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

data = pd.read_csv('nama_10_gdp_1_Data.csv', error_bad_lines = False, engine = 'python', na_values = [':', 'NaN'])

values = [
    'European Union (current composition)',
    'European Union (without United Kingdom)',
    'European Union (15 countries)',
    'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
    'Euro area (19 countries)',
    'Euro area (12 countries)'
            ]

eu_filter = data['GEO'].isin(values)

data = data.loc[~eu_filter.values].reset_index(drop = True)
data['NA_ITEM_UNIT'] = data['NA_ITEM'] + ' (' + data['UNIT'] + ')'

indicators = data['NA_ITEM_UNIT'].unique()
countries = data['GEO'].unique()

app.layout = html.Div(style={'backgroundColor':'#98FB98'},children=[
    html.Div([
        html.H1(
            children = 'Final Project - Emira Oliveros',
                style = {'font-family': 'Arial, Helvetica, sans-serif', 'text-align': 'center', 'color':'red'}
        ),
        html.Div([
            html.P(
                children = 'Select the first indicator:',
                style = {'font-size': '14px', 'font-family': 'Arial, Helvetica, sans-serif', 'color':'red'}
            ),
            dcc.Dropdown(
                id = 'xaxis-column1',
                options = [{'label': i, 'value': i} for i in indicators],
                value = indicators[0],
                
            ),
            dcc.RadioItems(
                id = 'xaxis-type1',
                options = [{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle = {'display': 'inline-block'},
                style = {'font-size': '12px', 'font-family': 'Arial, Helvetica, sans-serif','color':'#20B2AA'}
            )
        ],
        style = {'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.P(
                children = 'Select the second indicator:',
                style = {'font-size': '14px', 'font-family': 'Arial, Helvetica, sans-serif', 'color':'red'}
            ),
            dcc.Dropdown(
                id = 'yaxis-column1',
                options = [{'label': i, 'value': i} for i in indicators],
                value = indicators[1],
                
            ),
            dcc.RadioItems(
                id = 'yaxis-type1',
                options = [{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle = {'display': 'inline-block'},
                style = {'font-size': '12px', 'font-family': 'Arial, Helvetica, sans-serif', 'color':'#20B2AA'}
            )
        ], style = {'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id = 'indicator-graphic1'),
    html.Div([
        dcc.Slider(
            id = 'year--slider1',
            min = data['TIME'].min(),
            max = data['TIME'].max(),
            value = data['TIME'].max(),
            step = None,
            marks = {str(year): str(year) for year in data['TIME'].unique()}
        )
    ], 
        style = {'margin' : '10px 40px'}
    ),
    html.Div([
    ], 
        style = {'margin': '50px 10px 20px 10px', 'background-color': '#98FB98', 'height': '2px'}
    ),
    html.Div([
        html.H1(
            children = 'Task 2',
            style = {'font-family': 'Arial, Helvetica, sans-serif', 'text-align': 'center', 'color':'red'}
        ),
        html.Div([
            html.P(
                children = 'Select a country:',
                style = {'font-size': '14px', 'font-family': 'Arial, Helvetica, sans-serif','color':'red'}
            ),
            dcc.Dropdown(
                id = 'country2',
                options = [{'label': i, 'value': i} for i in countries],
                value = countries[0]
            )
        ],
        style = {'width': '48%', 'display': 'inline-block', 'height': '130px'}),

        html.Div([
            html.P(
                children = 'Select an indicator:',
                style = {'font-size': '14px', 'font-family': 'Arial, Helvetica, sans-serif', 'color':'red'}
            ),
            dcc.Dropdown(
                id = 'yaxis-column2',
                options = [{'label': i, 'value': i} for i in indicators],
                value = indicators[0] 
            )
        ],
        style = {'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], 
        style = {'margin-top': '20px'}
    ),

    dcc.Graph(id = 'indicator-graphic2')
])

@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('xaxis-type1', 'value'),
     dash.dependencies.Input('yaxis-type1', 'value'),
     dash.dependencies.Input('year--slider1', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = data[data['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x = dff[dff['NA_ITEM_UNIT'] == xaxis_column_name]['Value'],
            y = dff[dff['NA_ITEM_UNIT'] == yaxis_column_name]['Value'],
            text = dff[dff['NA_ITEM_UNIT'] == yaxis_column_name]['GEO'],
            mode = 'markers',
            marker = {
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis = {
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log',
                'color':'red'
            },
            yaxis = {
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log',
                'color': 'red'
            },
            margin = {'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode = 'closest',
            plot_bgcolor ='#98FB98',
            paper_bgcolor ='#98FB98'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('country2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])

def update_graph(country_name, yaxis_column_name):    
    
    return {
        'data': [go.Scatter(
            x = data[(data['GEO'] == country_name) & (data['NA_ITEM_UNIT'] == yaxis_column_name)]['TIME'].values,
            y = data[(data['GEO'] == country_name) & (data['NA_ITEM_UNIT'] == yaxis_column_name)]['Value'].values,
            mode = 'lines',
            line={'width': 3, 'color':'red'}
        )],
        'layout': go.Layout(
            xaxis = {
                'title':'Year',
                'titlefont':{'size':10},
                'color':'red'
            },
            yaxis = {
                'title': yaxis_column_name,
                'titlefont': {'size': 10},
                'type': 'linear',
                'color':'red',
                'linecolor':'red'
            },
            margin = {'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode = 'closest',
            plot_bgcolor ='#98FB98',
            paper_bgcolor ='#98FB98'
            
        )
    }

if __name__ == '__main__':
    app.run_server()

