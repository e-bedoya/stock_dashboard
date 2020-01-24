import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#011627',
    'text': '#FDFFFC'
}
app.layout = html.Div(style={'backgroundColor': '#011627', 'margin': -10}, children=[

    html.Div([
        html.Div([
            dcc.Input(id='stock-input', value='GS', type='text', style={'background': '#999999', 'marginTop': 10, 'marginLeft': 10}),
            html.Button(id='submit-button', n_clicks=0, children='Submit', style={'color': colors['text'], 'marginTop': 10, 'marginLeft': 5}),
        ], className='six columns'),


        html.Div(
            html.H5('Stock Dashboard'),
            style={
                'textAlign': 'right',
                'color': colors['text'],
                'marginTop': 10, 'marginRight': 10
            }
        )
    ]),

    html.Div([
        html.Div(id='company-name',
                style={
                    'textAlign': 'right',
                    'color': colors['text'],
                    'fontSize': 40
                }
        ),

        html.Img(id='company-logo', height='60',
                 style={
                     'marginLeft': 20
                 }
        )
    ], style={'width':'100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),

    html.Div([
        dcc.Graph(id='stock-chart')
    ], style={'width':'100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),

    html.Div([
        html.Div(id='container', children=[
            dcc.Graph(id='income-statement-table')
        ], className='six columns', style={'height':'100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),

        html.Div(id='container2', children=[
            dcc.Graph(id='income-statement-graph')
        ], className='six columns', style={'height':'100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})

    ], style={'color': colors['text'],
                    'fontSize': 14, 'width':'100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),

    # empty Div for border buffer
    html.Div([], style={'backgroundColor': '#011627', 'color': colors['text'],
                    'fontSize': 40, 'margin': 0, 'width':'100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': 30}),

    html.Div([
        html.Div(id='container3', children=[
            dcc.Graph(id='balance-sheet-graph')
        ], className='six columns', style={'height':'100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),

        html.Div(id='container4', children=[
            dcc.Graph(id='balance-sheet-table')
        ], className='six columns', style={'height':'100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),

    ], style={'color': colors['text'],
                    'fontSize': 14, 'width':'100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
    # empty Div for border buffer
    html.Div([], style={'backgroundColor': '#011627', 'color': colors['text'],
                    'fontSize': 40, 'margin': 0, 'width':'100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': 30})
])



@app.callback(
    Output('company-name', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('stock-input', 'value')]
)
def update_co_name(n_clicks, ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info['longName']
    except:
        return html.H6('Ticker not found. Please try again')


@app.callback(
    Output('company-logo', 'src'),
    [Input('submit-button', 'n_clicks')],
    [State('stock-input', 'value')]
)
def update_co_logo(n_clicks, ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info['logo_url']
    except:
        pass

@app.callback(
    Output('stock-chart', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('stock-input', 'value')]
)
def update_stock_chart(n_clicks, ticker):
    try:
        start = datetime.today() - relativedelta(years=10)
        end = datetime.today()

        stock = yf.Ticker(ticker)
        df = stock.history(start=start, end=end)

        fig = go.Figure(data=[go.Candlestick(x=df.index,
                                             open=df.Open,
                                             high=df.High,
                                             low=df.Low,
                                             close=df.Close,
                                             increasing_line_color='#2EC4B6', decreasing_line_color='#E71D36')],
                        )

        layout = dict(

            # GENERAL LAYOUT
            width=1400,
            height=500,
            autosize=True,
            font=dict(
                family="Overpass",
                size=12,
                color='#FDFFFC'
            ),
            margin=dict(
                t=80,
                l=50,
                b=50,
                r=50,
                pad=5,
            ),
            showlegend=False,

            # COLOR THEME
            plot_bgcolor="#011627",
            paper_bgcolor="#011627",

            # LINEAR PLOTS
            xaxis=dict(
                showgrid=False,
                # RANGE
                range=[end-relativedelta(years=5), end],

                # RANGE SLIDER AND SELECTOR
                rangeslider=dict(
                    bordercolor="#FFFFFF",
                    bgcolor="#011627",
                    thickness=0.1,
                ),

                # Buttons for date range (1D, 5D, 1M, 3M, 6M, 1Y, 2Y, 5Y, Max, YTD)
                rangeselector=dict(
                    activecolor="#666666",
                    bgcolor="#999999",
                    buttons=[
                        dict(count=1, step="day", stepmode="backward", label="1D"),
                        dict(count=5, step="day", stepmode="backward", label="5D"),
                        dict(count=1, step="month", stepmode="backward", label="1M"),
                        dict(count=3, step="month", stepmode="backward", label="3M"),
                        dict(count=6, step="month", stepmode="backward", label="6M"),
                        dict(count=1, step="year", stepmode="backward", label="1Y"),
                        dict(count=2, step="year", stepmode="backward", label="2Y"),
                        dict(count=5, step="year", stepmode="backward", label="5Y"),
                        dict(count=1, step="all", stepmode="backward", label="MAX"),
                        dict(count=1, step="year", stepmode="todate", label="YTD"),
                    ]
                ),

            ),
            yaxis=dict(
                tickprefix="$",
                type="linear",
                domain=[0.25, 1],
                showgrid=False
            ),

        )

        fig.update_layout(layout)

        return fig
    except:
        return html.Div('Graph unavailable')

@app.callback(
    Output('container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('stock-input', 'value')]
)
def update_income_statement(n_clicks, ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.financials.transpose()
        df = df[['Total Revenue', 'Cost Of Revenue', 'Gross Profit',
                 'Research Development', 'Selling General Administrative',
                 'Total Operating Expenses', 'Operating Income', 'Interest Expense',
                 'Total Other Income Expense Net', 'Income Before Tax', 'Income Tax Expense',
                 'Net Income From Continuing Ops', 'Net Income',
                 'Net Income Applicable To Common Shares']]
        df = df.transpose().reset_index()
        df.rename(columns={df.columns[0]: "Income Statement"}, inplace=True)
        columns = df.columns[1:].map(lambda t: t.strftime('%Y/%m/%d'))
        columns = columns.insert(0, df.columns[0])
        df.columns = columns
        df.dropna(inplace=True)

        for column in df.columns[1:]:
            df[column] = df[column].map('{:,.0f}'.format)

        fig = go.Figure(data=[go.Table(
            columnorder=[1, 2, 3, 4, 5],
            columnwidth=[75, 35, 35, 35, 35],

            header=dict(values=list(df.columns),
                        fill_color='#011627',
                        align='center',
                        font_color='#FDFFFC',
                        height=50,
                        font_size=16),
            cells=dict(values=[df[{i}] for i in df.columns],
                       fill_color='#011627',
                       align='left',
                       font_color='#FF9F1C',
                       height=35))
        ])

        fig.update_layout(height=400, width=675,
            margin=dict(l=0, r=0, t=0, b=0))

        return dcc.Graph(figure=fig)
    except:
        return html.Div('Graph unavailable')

@app.callback(
    Output('container2', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('stock-input', 'value')]
)
def update_income_statement_graph(n_clicks, ticker):
    try:
        stock = yf.Ticker(ticker)

        df = stock.financials.transpose()

        df = df[['Total Revenue', 'Cost Of Revenue', 'Gross Profit',
                 'Research Development', 'Selling General Administrative',
                 'Total Operating Expenses', 'Operating Income', 'Interest Expense',
                 'Total Other Income Expense Net', 'Income Before Tax', 'Income Tax Expense',
                 'Net Income From Continuing Ops', 'Net Income',
                 'Net Income Applicable To Common Shares']]

        df = df.transpose().dropna()
        df = df.transpose()

        traces = {}
        for col in df.columns:
            traces['trace_' + col] = go.Bar(x=df.index, name=col, y=df[col])

        # convert data to form required by plotly
        data = list(traces.values())

        # build figure
        fig = go.Figure(data)

        fig.update_layout(font_color='#FDFFFC',
                          plot_bgcolor='#011627',
                          paper_bgcolor='#011627',
                          title='Income Statement Items',
                          xaxis=dict(tickvals=df.index,
                                     tickformat='%Y'),
                          margin=dict(l=0, r=0, t=40, b=10),
                          height=400,
                          width=675,
                          )
        return dcc.Graph(figure=fig)
    except:
        return html.Div('Graph unavailable')

@app.callback(
    Output('container3', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('stock-input', 'value')]
)
def balance_sheet_graph(n_clicks, ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.balance_sheet.transpose()

        # possible balance sheet items returned from API
        # in the correct order
        columns_ordered = ['Cash', 'Short Term Investments',
                           'Net Receivables', 'Inventory', 'Other Current Assets', 'Total Current Assets',
                           'Net Tangible Assets',
                           'Property Plant Equipment', 'Long Term Investments', 'Good Will',
                           'Deferred Long Term Asset Charges', 'Intangible Assets', 'Other Assets', 'Total Assets',
                           'Accounts Payable', 'Short Long Term Debt', 'Other Current Liab',
                           'Total Current Liabilities',
                           'Long Term Debt', 'Deferred Long Term Liab', 'Other Liab', 'Total Liab',
                           'Common Stock', 'Retained Earnings', 'Capital Surplus', 'Minority Interest',
                           'Other Stockholder Equity', 'Treasury Stock', 'Total Stockholder Equity']

        non_returned_items = list(set(columns_ordered) - set(df.columns))

        columns = [i for i in columns_ordered if i not in non_returned_items]

        df = df[columns]

        traces = {}
        for col in df.columns:
            traces['trace_' + col] = go.Bar(x=df.index, name=col, y=df[col])

        # convert data to form required by plotly
        data = list(traces.values())

        # build figure
        fig = go.Figure(data)

        fig.update_layout(font_color='#FDFFFC',
                          plot_bgcolor='#011627',
                          paper_bgcolor='#011627',
                          title='Balance Sheet Items',
                          xaxis=dict(tickvals=df.index,
                                     tickformat='%Y'),
                          margin=dict(l=40, r=0, t=40, b=10),
                          height=400,
                          width=675,
                          )
        return dcc.Graph(figure=fig)
    except:
        return html.Div('Graph unavailable')

@app.callback(
    Output('container4', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('stock-input', 'value')]
)
def update_balance_sheet(n_clicks, ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.balance_sheet
        df = df.transpose()

        # possible balance sheet items returned from API
        # in the correct order
        columns_ordered = ['Cash', 'Short Term Investments',
                           'Net Receivables', 'Inventory', 'Other Current Assets', 'Total Current Assets',
                           'Net Tangible Assets',
                           'Property Plant Equipment', 'Long Term Investments', 'Good Will',
                           'Deferred Long Term Asset Charges', 'Intangible Assets', 'Other Assets', 'Total Assets',
                           'Accounts Payable', 'Short Long Term Debt', 'Other Current Liab',
                           'Total Current Liabilities',
                           'Long Term Debt', 'Deferred Long Term Liab', 'Other Liab', 'Total Liab',
                           'Common Stock', 'Retained Earnings', 'Capital Surplus', 'Minority Interest',
                           'Other Stockholder Equity', 'Treasury Stock', 'Total Stockholder Equity']

        non_returned_items = list(set(columns_ordered) - set(df.columns))
        columns = [i for i in columns_ordered if i not in non_returned_items]
        df = df[columns]
        df = df.transpose().reset_index()
        df.rename(columns={df.columns[0]: "Balance Sheet"}, inplace=True)
        columns = df.columns[1:].map(lambda t: t.strftime('%Y/%m/%d'))
        columns = columns.insert(0, df.columns[0])
        df.columns = columns
        df.dropna(inplace=True)

        for column in df.columns[1:]:
            df[column] = df[column].map('{:,.0f}'.format)

        fig = go.Figure(data=[go.Table(
            columnorder=[1, 2, 3, 4, 5],
            columnwidth=[60, 35, 35, 35, 35],

            header=dict(values=list(df.columns),
                        fill_color='#011627',
                        align='center',
                        font_color='#FDFFFC',
                        height=50,
                        font_size=16),
            cells=dict(values=[df[{i}] for i in df.columns],
                       fill_color='#011627',
                       align='left',
                       font_color='#FF9F1C',
                       height=35))
        ])

        fig.update_layout(height=400, width=675,
                          margin=dict(l=0, r=0, t=0, b=0))

        return dcc.Graph(figure=fig)
    except:
        return html.Div('Graph unavailable')

    
if __name__ == '__main__':
    app.run_server(debug=True)
