#!pip install dash

# Run this app with 'python 4-Dashboard.py' and
# visit http://127.0.0.1:8050/ in your web browser.

# Import required libraries
import numpy as np
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the Job data into a Pandas dataframe
df = pd.read_csv("Dataset_Clean.csv").rename(columns = {'Average Salary': 'Salary'})

max_salary = df['Salary'].max()
min_salary = df['Salary'].min()

# Plotting functions

# Job Demand: Pie Chart
def plot_pie_chart(df):

  job_df = pd.DataFrame(df['Job'].value_counts().reset_index().rename(columns = {'index': 'Job', 'Job': 'Count'}))
  pie_colors = ['#06477D','#84BDEC','#B4D4EF', '#C8E4FC','aliceblue']
  demand_job_plot = px.pie(job_df, values='Count', names='Job', color = 'Job', hole = 0.7,  
                           color_discrete_sequence=px.colors.sequential.Blues_r,
                           title='Demand of Data Jobs Per Category')
  demand_job_plot.update_traces(hoverinfo='label+percent+name', textinfo='percent', textfont_size=16,
                    marker=dict(colors=pie_colors, line=dict(color='white', width=4)))
  
  return demand_job_plot

# Company Demand: Treemap
def plot_treemap(df):

  top = 30

  company_df = pd.pivot_table(data = df, index = ['Company'], columns = 'Job', values = 'Location', aggfunc = 'count').fillna(0).reset_index()
  company_df['Total'] = company_df.sum(axis=1, numeric_only= True)
  company_df = company_df.sort_values('Total', ascending = False)[:top]
  company_df['Company'] = company_df['Company'].map(lambda x: x[:15])

  demand_company_plot = px.treemap(company_df, path = [px.Constant("."), 'Company'], values='Total', color = 'Total', 
                                  color_continuous_scale=px.colors.sequential.Blues,
                                  title= f'Top {top} Companies Demanding Data Jobs',
                                  labels={'Total':'Vacancies'})

  return demand_company_plot

# Location Demand: Cloropleth
def plot_cloropleth(df):

  # States dictionary with corresponding ID
  location_dict = {'Aguascalientes': 'AS', 
              'Baja California': 'BC', 
              'Baja California Sur': 'BS', 
              'Campeche': 'CC',
              'Ciudad de México':'DF',
              'Chiapas': 'CS',
              'Chihuahua':'CH',
              'Coahuila':'CL',
              'Colima':'CM',
              'Durango':'DG',
              'Estado de México':'MC',
              'Guanajuato':'GT',
              'Guerrero':'GR',
              'Hidalgo':'HG',
              'Jalisco':'JC',
              'Michoacán':'MN',
              'Morelos':'MS',
              'Nayarit':'NT',
              'Nuevo León':'NL',
              'Oaxaca':'OC',
              'Puebla':'PL',
              'Querétaro':'QT',
              'Quintana Roo':'QR',
              'San Luis Potosí':'SP',
              'Sinaloa':'SL',
              'Sonora':'SR',
              'Tabasco':'TC',
              'Tamaulipas':'TS',
              'Tlaxcala':'TL',
              'Veracruz':'VZ',
              'Yucatán':'YN',
              'Zacatecas':'ZS'}

  location_df = pd.DataFrame.from_dict(location_dict, orient='index').reset_index().rename(columns={"index": "State", 0: "ID"}).set_index('State')

  demand = pd.DataFrame(df['Location'].value_counts())
  total = sum(demand['Location'])
  demand['Percentage'] = (demand['Location']) / total *100
  demand = demand.reset_index().rename(columns={"index": "State", "Location": "Count"})

  location_df = location_df.merge(demand, left_on='State', right_on='State', how = 'outer').fillna(0)

  demand_location_plot = px.choropleth(location_df, 
                            geojson = 'https://raw.githubusercontent.com/isaacarroyov/data_visualization_practice/master/Python/visualizing_mexican_wildfires_tds/data/states_mx.json', 
                            locations='ID', 
                            color='Percentage',
                            color_continuous_scale="Blues",
                            scope="north america",
                            title='Demand of Data Jobs per Mexican State',
                            labels={'Percentage':'Demand %'}
                            )
  demand_location_plot.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
  demand_location_plot.update_geos(fitbounds="locations", visible=False)

  return demand_location_plot

# Salary Per Job: Boxplot
def plot_boxplot(df):

  salary_job_df = df.dropna(axis = 0, how='any', subset = ['Salary'])

  salary_job_plot = px.box(salary_job_df, x = "Job", y = "Salary", 
                          color = "Job", points="all", 
                          color_discrete_sequence=px.colors.sequential.Blues_r,
                          category_orders={"Job": ['Data Architect', 'Data Scientist', 'Data Engineer', 'Business Analyst', 'Data Analyst']},
                          labels={
                                  "Salary": "Monthly Salary (MXN)",
                                  "Job": "Data Job Category"},
                          title='Salary Per Data Job Category',
                          width=600, height=600
                          )
  salary_job_plot.update_traces(showlegend=False)

  return salary_job_plot

# Salary Per Company: Heatmap

def plot_heatmap(df):

  top = 30

  salary_job_df = df.dropna(axis = 0, how='any', subset = ['Salary'])
  salary_company_df = pd.pivot_table(salary_job_df, index = 'Company', columns = 'Job', values = 'Salary', aggfunc= 'mean')
  salary_company_df['Total Average'] = salary_company_df.mean(axis=1, numeric_only= True)
  salary_company_df = salary_company_df.fillna(0).sort_values('Total Average', ascending = False)[:top].\
                      sort_values('Company', ascending = False).drop(columns = 'Total Average').reset_index().\
                      rename(index = {'Job': 'Index'})
  salary_company_df = pd.melt(salary_company_df, id_vars = 'Company', var_name = 'Job', value_name = 'Salary')

  salary_company_plot = px.density_heatmap(salary_company_df, y='Company', x = 'Job', z = 'Salary',
                          histfunc="avg", color_continuous_scale="Blues",
                          width=720, height=720,
                          title='Salary Per Company And Data Job Category',
                          labels={"Job": "Data Job Category"}
                          )

  return salary_company_plot

# Salary Per Location: Contour plot
def plot_contour(df):

    # States dictionary with corresponding ID
  location_dict = {'Aguascalientes': 'AS', 
              'Baja California': 'BC', 
              'Baja California Sur': 'BS', 
              'Campeche': 'CC',
              'Ciudad de México':'DF',
              'Chiapas': 'CS',
              'Chihuahua':'CH',
              'Coahuila':'CL',
              'Colima':'CM',
              'Durango':'DG',
              'Estado de México':'MC',
              'Guanajuato':'GT',
              'Guerrero':'GR',
              'Hidalgo':'HG',
              'Jalisco':'JC',
              'Michoacán':'MN',
              'Morelos':'MS',
              'Nayarit':'NT',
              'Nuevo León':'NL',
              'Oaxaca':'OC',
              'Puebla':'PL',
              'Querétaro':'QT',
              'Quintana Roo':'QR',
              'San Luis Potosí':'SP',
              'Sinaloa':'SL',
              'Sonora':'SR',
              'Tabasco':'TC',
              'Tamaulipas':'TS',
              'Tlaxcala':'TL',
              'Veracruz':'VZ',
              'Yucatán':'YN',
              'Zacatecas':'ZS'}

  location_df = pd.DataFrame.from_dict(location_dict, orient='index').reset_index().rename(columns={"index": "State", 0: "ID"}).set_index('State')

  demand = pd.DataFrame(df['Location'].value_counts())
  total = sum(demand['Location'])
  demand['Percentage'] = (demand['Location']) / total *100
  demand = demand.reset_index().rename(columns={"index": "State", "Location": "Count"})

  location_df = location_df.merge(demand, left_on='State', right_on='State', how = 'outer').fillna(0)

  salary_job_df = df.dropna(axis = 0, how='any', subset = ['Salary'])

  salary_location_df = pd.pivot_table(data = salary_job_df, index = 'Location', columns = 'Job', values = 'Salary', aggfunc= 'mean').reset_index().\
      merge(location_df, left_on='Location', right_on='State', how = 'outer').set_index('State').drop(columns =['ID', 'Count', 'Percentage', 'Location']).fillna(0).\
      sort_values('State', ascending = False).reset_index()
  salary_location_df = pd.melt(salary_location_df, id_vars= 'State', var_name = 'Job', value_name = 'Salary')

  salary_location_plot = px.density_contour(salary_location_df, y='State', x = 'Job', z = 'Salary',
                          histfunc="avg", 
                          color_discrete_sequence=px.colors.sequential.Blues_r,
                          width=700, height=720,
                          title='Salary Per Location And Data Job Category',
                          labels={
                                  "State": "Location",
                                  'Job': 'Data Job Category'
                                  }
                          )
  salary_location_plot.update_traces(contours_coloring="fill", contours_showlabels = True, colorscale = 'Blues')

  return salary_location_plot


# Helper function for dropdowns
def create_dropdown_options(series):
    options = [{'label': i, 'value': i} for i in series.sort_values().unique()]
    options.append({'label': 'All', 'value': 'All'})
    return options

# Dash application
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div(children=[
                                # First section
                                # Adding Title
                                html.H1('Data Jobs in Mexico Dashboard',
                                        style={'textAlign': 'center', 'color': 'navy',
                                               'font-size': 40, 'font-family': 'Tahoma'}),
                                
                                # Adding Author
                                html.P("By Daniel Eduardo López",
                                        style={'textAlign': 'center', 'color': 'navy',
                                               'font-size': 18, 'font-family': 'Tahoma'}),
                                html.Br(),
                                
                                # Adding a very brief Introduction to the Dashboard
                                html.P("This Dashboard shows the Data Jobs demand and salaries in Mexico in August 2022.",
                                        style={'textAlign': 'center', 'color': 'black',
                                               'font-size': 13, 'font-family': 'Tahoma'}),
                                
                                html.P("Data was collected on August 3, 2022 from the OCC website.",
                                        style={'textAlign': 'center', 'color': 'black',
                                               'font-size': 13, 'font-family': 'Tahoma'}),
                                html.Br(),
                                
                                # Second section: Dropdowns & Slider
                                html.Div(children=[
                                
                                      # Dropdown list to enable Data Job selection
                                      html.Br(),
                                      html.Label("Data Job Selection:", className='dropdown-labels'),
                                      dcc.Dropdown(id='job_dropdown',
                                                  options=create_dropdown_options(df['Job']),
                                                  value='All',
                                                  placeholder="Select Data Job",
                                                  multi=True,
                                                  searchable=True
                                                  ),
                                                                      
                                      # Dropdown list to enable Location selection
                                      html.Br(),
                                      html.Label("Location Selection:", className='dropdown-labels'),
                                      dcc.Dropdown(id='location_dropdown',
                                                  options=create_dropdown_options(df['Location']),
                                                  value='All',
                                                  placeholder="Select Location",
                                                  multi=True,
                                                  searchable=True
                                                  ),
                                
                                      # Dropdown list to enable Company selection
                                      html.Br(),
                                      html.Label("Company Selection:", className='dropdown-labels'),
                                      dcc.Dropdown(id='company_dropdown',
                                                  options=create_dropdown_options(df['Company']),
                                                  value='All',
                                                  placeholder="Select Company",
                                                  multi=True,
                                                  searchable=True
                                                  ),
                                      
                                      # Range Slider for Salary selection
                                      html.Br(),
                                      html.Label("Salary Range Selection (MXN):"),
                                      dcc.RangeSlider(id='salary_slider',
                                                      min=0, max=100000, step=1000,
                                                      marks={0: '$0', 20000: '$20,000', 40000: '$40,000', 60000: '$60,000', 80000: '$80,000', 100000: '$100,000'},
                                                      value=[min_salary, max_salary]),

                                ], id='left-container', 
                                style={'margin-top': '50px',
                                       'width': '100%', 
                                       'height': '300px', 
                                       'background-color': '#B3D5FA', 
                                       'float': 'center', 
                                       'margin': '0'}
                                ),

                                # Third section: Plots
                                html.Div(children=[

                                      # Demand Plots
                                      html.Div(children=[

                                            # Job Demand Plot: Donnut chart
                                            dcc.Graph(id='demand_job_plot'),
                                      
                                            # Company Demand Plot: Treemap
                                            dcc.Graph(id='demand_company_plot'),
                                      
                                            # Location Demand Plot: Treemap
                                            dcc.Graph(id='demand_location_plot'),
                                      
                                      ], id='visualization_demand',
                                         style={'margin-top': '10px', 
                                                'width': '100%',                                        
                                                #'overflow': 'hidden',
                                                'height': '350px'
                                                }
                                      ),

                                      # Salary Plots
                                      html.Div(children=[
                                            
                                            # Job-Salary Plot: Boxplot
                                            dcc.Graph(id='salary_job_plot'),
                                      
                                            # Company-Salary Plot: Heatmap
                                            dcc.Graph(id='salary_company_plot'),
                                      
                                            # Location-Salary Plot: Contourmap
                                            dcc.Graph(id='salary_location_plot'),
                                      
                                      ], id='visualization_salary',
                                         style={'margin-top': '360px', 
                                                  'width': '100%',                                        
                                                  #'overflow': 'hidden',
                                                  'height': '720px'
                                                  }
                                      ),

                                
                                ], id='right-container',
                                style={#'margin-top': '50px',
                                       'margin-left': '335px', 
                                       'height': '1080px', 
                                       #'background-color': '#CEE3F6'                                                                              
                                       }
                                ),

                        ], id='container',
                           style={'width': '100%', 
                                  #'overflow': 'hidden',                                        
                                 }
                      )        

                             

# Callback Functions

# Callback function for 'job_dropdown' as input and 'demand_job_plot' as output
@app.callback([Output(component_id='demand_job_plot', component_property='figure'),
               Output(component_id='demand_company_plot', component_property='figure'),
               Output(component_id='demand_location_plot', component_property='figure'),
               Output(component_id='salary_job_plot', component_property='figure'),
               Output(component_id='salary_company_plot', component_property='figure'),
               Output(component_id='salary_location_plot', component_property='figure')],
              [Input(component_id='job_dropdown', component_property='value'),
               Input(component_id='location_dropdown', component_property='value'),
               Input(component_id='company_dropdown', component_property='value'),
               Input(component_id='salary_slider', component_property='value')]
              )

def update_output(job, location, company, salary):
  """
  This function updates the output plots.
  """
  dff = df.copy()
  low, high = salary
  mask = (dff['Salary'] > low) & (dff['Salary'] < high)
  dff = dff[mask]
  
  if (job and location and company) == 'All':

        demand_job_plot = plot_pie_chart(dff)
        demand_company_plot = plot_treemap(dff)
        demand_location_plot = plot_cloropleth(dff)
        salary_job_plot = plot_boxplot(dff)
        salary_company_plot = plot_heatmap(dff)
        salary_location_plot = plot_contour(dff)

        return demand_job_plot, demand_company_plot, demand_location_plot, salary_job_plot, salary_company_plot, salary_location_plot

  else:
        if (job and location) == 'All':
          dff = dff.loc[dff['Company'] == company] 
        
        if (job and company) == 'All':
          dff = dff.loc[dff['Location'] == location] 
        
        if (company and location) == 'All':
          dff = dff.loc[dff['Job'] == job]
        
        if job == 'All':
          dff = dff.loc[dff['Location'] == location]
          dff = dff.loc[dff['Company'] == company]

        if location == 'All':
          dff = dff.loc[dff['Job'] == job]
          dff = dff.loc[dff['Company'] == company]

        if company == 'All':
          dff = dff.loc[dff['Location'] == location]
          dff = dff.loc[dff['Job'] == job]
        else:
          dff = dff.loc[dff['Job'] == job]
          dff = dff.loc[dff['Location'] == location]
          dff = dff.loc[dff['Company'] == company]

        demand_job_plot = plot_pie_chart(dff)
        demand_company_plot = plot_treemap(dff)
        demand_location_plot = plot_cloropleth(dff)
        salary_job_plot = plot_boxplot(dff)
        salary_company_plot = plot_heatmap(dff)
        salary_location_plot = plot_contour(dff)

        return demand_job_plot, demand_company_plot, demand_location_plot, salary_job_plot, salary_company_plot, salary_location_plot

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
