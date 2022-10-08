### DATA JOBS DASHBOARD

"""
By Daniel Eduardo López
Date: 2022-08-24
GitHub: https://github.com/DanielEduardoLopez
LinkedIn: https://www.linkedin.com/in/daniel-eduardo-lopez
"""

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
from dash.exceptions import PreventUpdate
import plotly.express as px

# Read the Job data into a Pandas dataframe
df = pd.read_csv("https://raw.githubusercontent.com/DanielEduardoLopez/DataJobsMX2022/main/Dataset_Clean.csv").rename(columns = {'Average Salary': 'Salary'})

max_salary = df['Salary'].max()
min_salary = df['Salary'].min()

# Plotting functions

# Job Demand: Pie Chart
def plot_pie_chart(df):

  job_df = pd.DataFrame(df['Job'].value_counts().reset_index().rename(columns = {'index': 'Job', 'Job': 'Count'}))
  pie_colors = ['#06477D','#84BDEC','#B4D4EF', '#C8E4FC','white']
  demand_job_plot = px.pie(job_df, values='Count', names='Job', color = 'Job', hole = 0.7,  
                           color_discrete_sequence=px.colors.sequential.Blues_r,
                           height=450,
                           title='Demand of Data Jobs Per Category')
  demand_job_plot.update_traces(hoverinfo='label+percent+name', textinfo='percent', textfont_size=16,
                    marker=dict(colors=pie_colors, line=dict(color="rgba(0,0,0,0)", width=4)))
  demand_job_plot.update_layout(transition_duration=400, title_x=0.5, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  
  return demand_job_plot

# Company Demand: Treemap
def plot_treemap(df):

  top = 20

  #company_df = pd.pivot_table(data = df, index = ['Company'], columns = 'Job', values = 'Location', aggfunc = 'count').fillna(0).reset_index()
  company_df =  df.groupby(by='Company', as_index=False)['Job'].count().sort_values(by = 'Job', ascending = False).\
                rename(columns = {'Job': 'Vacancies'})[:top]
  company_df['Company'] = company_df['Company'].map(lambda x: x[:15])
  company_df = company_df[company_df['Vacancies'] > 0]

  demand_company_plot = px.treemap(company_df, path = [px.Constant("."), 'Company'], values='Vacancies', color = 'Vacancies', 
                                  color_continuous_scale=px.colors.sequential.Blues,
                                  title= f'Top {top} Companies Demanding Data Jobs'
                                  )
  demand_company_plot.update_layout(transition_duration=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

  return demand_company_plot

# Alternative: Company Demand: Bar Chart
def plot_barchart(df):

  top = 15
  bar_colors = ['#84BDEC',] * 14
  bar_colors.insert(14,'#06477D')
  company_df = df.groupby(by = 'Company', as_index= False)['Job'].count().sort_values(by = 'Job', ascending = False).rename(columns = {'Job': 'Vacancies'})[:top]
  company_df['Company'] = company_df['Company'].map(lambda x: x[:25])
  company_df = company_df[company_df['Vacancies'] > 0]

  demand_company_plot = px.bar(company_df.sort_values(by = 'Vacancies'), x='Vacancies', y='Company',
            color = 'Vacancies', color_continuous_scale=bar_colors,
            #text="Vacancies", 
            height=450,
            title= f'Top {top} Companies Demanding Data Jobs',
            opacity = 0.8)
  demand_company_plot.update_traces(marker_color= bar_colors, marker_line_color='#06477D', textfont_size=11, textangle=0, textposition="outside", cliponaxis=False)
  demand_company_plot.update_layout(transition_duration=400, title_x=0.5, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

  return demand_company_plot

# Location Demand: Choropleth Map
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
                            #title='Demand of Data Jobs per Mexican State',
                            labels={'Percentage':'National <br>Demand %'}
                            )
  demand_location_plot.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, transition_duration=300,
                                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", geo_bgcolor = "rgba(0,0,0,0)")
  demand_location_plot.update_geos(fitbounds="locations", visible=False)
  demand_location_plot.update_layout(transition_duration=400, title_x=0.5)
  
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
                          height=450
                          )
  salary_job_plot.update_traces(showlegend=False)
  salary_job_plot.update_layout(transition_duration=400, title_x=0.5, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  salary_job_plot.update_yaxes(tickformat = '$,~s')

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
                          height=720,
                          title='Salary Per Company And Data Job Category',
                          labels={"Job": "Data Job Category"}
                          )
  salary_company_plot.update_layout(transition_duration=400, title_x=0.5, coloraxis_colorbar=dict(title="Avg. Mth. <br>Salary (MXN)"),
                                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  salary_company_plot.update_coloraxes(colorbar_tickformat = '$,~s')
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
                          height=720,
                          title='Salary Per Location And Data Job Category',
                          labels={
                                  "State": "Location",
                                  'Job': 'Data Job Category'
                                  }
                          )
  salary_location_plot.update_traces(contours_coloring="fill", contours_showlabels = True, 
                                    colorscale = 'Blues', colorbar_tickformat='$,~s',
                                    colorbar_title_text='Avg. Mth. <br>Salary (MXN)')
  salary_location_plot.update_layout(transition_duration=400, title_x=0.5, coloraxis_colorbar=dict(title="Vacancies"),
                                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

  return salary_location_plot


# Helper function for dropdowns
def create_dropdown_options(series):
    options = [{'label': i, 'value': i} for i in series.sort_values().unique()]
    options.insert(0, {'label': 'All', 'value': 'All'})
    return options

# Dash application
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div(children=[
                                # First section
                                # Adding Title
                                html.Div(children=[ html.H1('Data Jobs in Mexico Dashboard',
                                        style={'textAlign': 'center', 'color': 'white',
                                               'font-size': 40, 'font-family': 'Tahoma'})], 
                                               style={'margin-top': '0',
                                                      'width': '100%', 
                                                      'height': '60px', 
                                                      'background-color': 'navy', 
                                                      'float': 'center', 
                                                      'margin': '0'}  
                                        ),
                                
                                # Adding Author
                                html.P("By Daniel Eduardo López",
                                        style={'textAlign': 'center', 'color': 'navy',
                                               'font-size': 15, 'font-family': 'Tahoma'}),
                                dcc.Link(html.A('GitHub'), href="https://github.com/DanielEduardoLopez",
                                        style={'textAlign': 'center', 'color': 'navy',
                                               'font-size': 12, 'font-family': 'Tahoma',
                                               'margin': 'auto',
                                               'display': 'block'}),
                                
                                dcc.Link(html.A('LinkedIn'), href="https://www.linkedin.com/in/daniel-eduardo-lopez",
                                        style={'textAlign': 'center', 'color': 'navy',
                                               'font-size': 12, 'font-family': 'Tahoma',
                                               'margin': 'auto',
                                               'display': 'block'}),
                                # html.Br(),
                                
                                # Adding a very brief Introduction to the Dashboard
                                html.P("This Dashboard shows the Data Jobs demand and salaries in Mexico in August 2022.",
                                        style={'textAlign': 'center', 'color': 'black',
                                               'font-size': 14, 'font-family': 'Tahoma'}),
                                
                                html.P("Data was collected on August 3, 2022 from the OCC website.",
                                        style={'textAlign': 'center', 'color': 'black',
                                               'font-size': 14, 'font-family': 'Tahoma'}),
                                html.Br(),
                                
                                # Second section: Dropdowns & Slider
                                html.Div(children=[
                                
                                      # Dropdown list to enable Data Job selection
                                      html.Br(),
                                      #html.Br(),
                                      html.Label("Data Job Selection:", className='dropdown-labels',
                                                style={'textAlign': 'left', 'color': 'navy',
                                                  'font-size': 15, 'font-family': 'Tahoma'}
                                                ),
                                      dcc.Dropdown(id='job_dropdown',
                                                  options=create_dropdown_options(df['Job']),
                                                  value='All',
                                                  placeholder="Select Data Job",
                                                  multi=True,
                                                  searchable=True,
                                                  style={'textAlign': 'left', 'color': '#2e2d2d',
                                                  'font-size': 14, 'font-family': 'Tahoma'}
                                                  ),
                                                                      
                                      # Dropdown list to enable Location selection
                                      html.Br(),
                                      #html.Br(),
                                      html.Label("Location Selection:", className='dropdown-labels',
                                                style={'textAlign': 'left', 'color': 'navy',
                                                  'font-size': 15, 'font-family': 'Tahoma'}
                                                ),
                                      dcc.Dropdown(id='location_dropdown',
                                                  options=create_dropdown_options(df['Location']),
                                                  value='All',
                                                  placeholder="Select Location",
                                                  multi=True,
                                                  searchable=True,
                                                  style={'textAlign': 'left', 'color': '#2e2d2d',
                                                  'font-size': 14, 'font-family': 'Tahoma'}
                                                  ),
                                
                                      # Dropdown list to enable Company selection
                                      html.Br(),
                                      #html.Br(),
                                      html.Label("Company Selection:", className='dropdown-labels',
                                                  style={'textAlign': 'left', 'color': 'navy',
                                                  'font-size': 15, 'font-family': 'Tahoma'}
                                                  ),
                                      dcc.Dropdown(id='company_dropdown',
                                                  options=create_dropdown_options(df['Company']),
                                                  value='All',
                                                  placeholder="Select Company",
                                                  multi=True,
                                                  searchable=True,
                                                  style={'textAlign': 'left', 'color': '#2e2d2d',
                                                  'font-size': 14, 'font-family': 'Tahoma'}
                                                  ),
                                      
                                      # Checkbox for selecting only positions with disclosed salary 
                                      html.Br(),
                                      #html.Br(),
                                      dcc.Checklist(id='salary_filter',
                                                      options=['Enable Salary Range Selection'],
                                                      inline=True,
                                                      style={'textAlign': 'left', 'color': 'navy',
                                                      'font-size': 15, 'font-family': 'Tahoma'}
                                                      ),
                                      html.Label("(Displays Only Positions With Disclosed Salary)",
                                                style={'textAlign': 'center', 'color': 'navy',
                                                  'font-size': 12, 'font-family': 'Tahoma'}
                                                ),
                                      
                                      
                                      # Range Slider for Salary selection
                                      html.Br(),
                                      html.Br(),
                                      html.Label("Salary Range Selection (MXN):",
                                                style={'textAlign': 'left', 'color': 'navy',
                                                  'font-size': 15, 'font-family': 'Tahoma'}
                                                ),
                                      dcc.RangeSlider(id='salary_slider',
                                                      min=0, max=100000, step=1000,
                                                      marks={0: '$0', 20000: '$20,000', 40000: '$40,000', 60000: '$60,000', 80000: '$80,000', 100000: '$100,000'},
                                                      value=[min_salary, max_salary],
                                                      ),
                                      
                                                                                           

                                ], id='left-container', 
                                style={'margin-top': '10px',
                                        'margin-left': '10px',
                                        'width': '25%', 
                                       'height': '400px', 
                                       'background-color': '#B3D5FA', 
                                       'float': 'center', 
                                       }
                                ),

                                # Third section: Plots
                                html.Div(children=[

                                      # First Plot
                                      html.Div(children=[

                                            # Job Demand Plot: Donnut chart
                                            dcc.Graph(id='demand_job_plot'),                                   
                                    
                                            ], id='Donnut_chart',
                                              style={'margin-top': '-400px',
                                                      'margin-left': '350px',
                                                      'width': '36%', 
                                                      'height': '400px',                                                                                                            
                                                      }                                                
                                            ),

                                      # Second plot
                                      html.Div(children=[
                                      
                                            # Job-Salary Plot: Boxplot
                                                  dcc.Graph(id='salary_job_plot'),
                                          
                                          ], id='Boxplot',
                                            style={'margin-top': '-400px',
                                                    'margin-left': '60%',
                                                    'width': '36.5%', 
                                                    'height': '400px',                                                                                                            
                                                    }                                                
                                          ),
                                      
                              # Second Plot Section
                              html.Div(children=[

                                            #Third Plot
                                            html.Div(children=[

                                            # Company Demand Plot: Treemap
                                            dcc.Graph(id='demand_company_plot'),

                                            ], id='Treemap',
                                            style={'margin-top': '-330px',
                                                    'margin-left': '20px', 
                                                    'width': '50%',
                                                    'height': '400px',                                                                                                            
                                                    }                                                
                                            ),                                 
                                                                        
                                            #Fourth Plot
                                            html.Div(children=[       

                                            # Location Demand Plot: Map
                                            dcc.Graph(id='demand_location_plot'), 
                                            ], id='Map',
                                            style={'margin-top': '-380px',
                                                    'margin-left': '47%', 
                                                    'width': '48%',
                                                    'height': '380px',                                                                                                            
                                                    }                                                
                                            ),                        
                                      
                                      ], id='Second_plot_section',
                                         style={'margin-top': '360px', 
                                                  'width': '100%',                                        
                                                  #'overflow': 'hidden',
                                                  'height': '720px'
                                                  }
                                      ),

                            # Third Plot Section
                             html.Div(children=[

                                      #Fifth Plot
                                      html.Div(children=[

                                            # Company-Salary Plot: Heatmap
                                            dcc.Graph(id='salary_company_plot'),

                                            ], id='Heatmap',
                                            style={'margin-top': '-280px',
                                                    'margin-left': '10px', 
                                                    'width': '50%',
                                                    'height': '720px',                                                                                                            
                                                    }                                                
                                            ),  

                                      #Sixth Plot
                                      html.Div(children=[

                                            # Location-Salary Plot: Contourmap
                                            dcc.Graph(id='salary_location_plot'),

                                            ], id='Contourmap',
                                            style={'margin-top': '-720px',
                                                    'margin-left': '51%', 
                                                    'width': '48%',
                                                    'height': '720px',                                                                                                            
                                                    }                                                
                                            ), 


                                ], id='Third_plot_section',                                
                                ),
                        ])

                        ], id='container',
                           style={'width': '100%', 
                                  'overflow': 'hidden',
                                  'background-color': 'aliceblue', 
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
               Input(component_id='salary_slider', component_property='value'),
               Input(component_id='salary_filter', component_property='value')]
              )
def update_output(job, location, company, salary, salary_filter):
  """
  This function updates the output plots based on the parameters of:
  - job
  - location
  - company
  - salary
  """
  dff = df.copy()
  low, high = salary

  if salary_filter == ['Enable Salary Range Selection']:
    mask = (dff['Salary'] >= low) & (dff['Salary'] <= high)
    dff = dff[mask]

  if (job or company or location or salary) == None:
        raise PreventUpdate 
  
  if 'All' in job and 'All' in location and 'All' in company:
    
    demand_job_plot = plot_pie_chart(dff)
    demand_company_plot = plot_barchart(dff)
    demand_location_plot = plot_cloropleth(dff)
    salary_job_plot = plot_boxplot(dff)
    salary_company_plot = plot_heatmap(dff)
    salary_location_plot = plot_contour(dff)

  else:

        if ('All' in (company and location)) and ('All' not in job):
          dff = dff[dff.Job.isin(job)]

          demand_job_plot = plot_pie_chart(dff)
          demand_company_plot = plot_barchart(dff)
          demand_location_plot = plot_cloropleth(dff)
          salary_job_plot = plot_boxplot(dff)
          salary_company_plot = plot_heatmap(dff)
          salary_location_plot = plot_contour(dff)
        
        elif ('All' in (job and location)) and ('All' not in company):
          dff = dff[dff.Company.isin(company)]

          demand_job_plot = plot_pie_chart(dff)
          demand_company_plot = plot_barchart(dff)
          demand_location_plot = plot_cloropleth(dff)
          salary_job_plot = plot_boxplot(dff)
          salary_company_plot = plot_heatmap(dff)
          salary_location_plot = plot_contour(dff)
        
        elif ('All' in (company and job)) and ('All' not in location):
          dff = dff[dff.Location.isin(location)]

          demand_job_plot = plot_pie_chart(dff)
          demand_company_plot = plot_barchart(dff)
          demand_location_plot = plot_cloropleth(dff)
          salary_job_plot = plot_boxplot(dff)
          salary_company_plot = plot_heatmap(dff)
          salary_location_plot = plot_contour(dff)              
        
        elif ('All' in job) and ('All' not in (company and location)):
          dff = dff[(dff.Company.isin(company)) & (dff.Location.isin(location))]

          demand_job_plot = plot_pie_chart(dff)
          demand_company_plot = plot_barchart(dff)
          demand_location_plot = plot_cloropleth(dff)
          salary_job_plot = plot_boxplot(dff)
          salary_company_plot = plot_heatmap(dff)
          salary_location_plot = plot_contour(dff)

        elif ('All' in location) and ('All' not in (company and job)):
          dff = dff[(dff.Company.isin(company)) & (dff.Job.isin(job))]

          demand_job_plot = plot_pie_chart(dff)
          demand_company_plot = plot_barchart(dff)
          demand_location_plot = plot_cloropleth(dff)
          salary_job_plot = plot_boxplot(dff)
          salary_company_plot = plot_heatmap(dff)
          salary_location_plot = plot_contour(dff)

        elif ('All' in company) and ('All' not in (location and job)):
          dff = dff[(dff.Location.isin(location)) & (dff.Job.isin(job))]

          demand_job_plot = plot_pie_chart(dff)
          demand_company_plot = plot_barchart(dff)
          demand_location_plot = plot_cloropleth(dff)
          salary_job_plot = plot_boxplot(dff)
          salary_company_plot = plot_heatmap(dff)
          salary_location_plot = plot_contour(dff)

        elif 'All' not in (company and location and job):
          dff = dff[(dff.Job.isin(job)) & (dff.Location.isin(location)) & (dff.Company.isin(company))]

          demand_job_plot = plot_pie_chart(dff)
          demand_company_plot = plot_barchart(dff)
          demand_location_plot = plot_cloropleth(dff)
          salary_job_plot = plot_boxplot(dff)
          salary_company_plot = plot_heatmap(dff)
          salary_location_plot = plot_contour(dff)
        
        else:
          raise PreventUpdate 

  return demand_job_plot, demand_company_plot, demand_location_plot, salary_job_plot, salary_company_plot, salary_location_plot

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
