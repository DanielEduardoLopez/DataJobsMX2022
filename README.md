# Data Jobs Salaries in August 2022 in Mexico
#### by Daniel Eduardo López

Email: **daniel-eduardo-lopez@outlook.com**

LinkedIn: **www.linkedin.com/in/daniel-eduardo-lopez**
____
### **1. Objective:**
To identify which data job category has the highest salary in the Mexican labor market in August 2022 according to the OCC website:
- Business Analyst
- Data Analyst
- Data Architect
- Data Engineer
- Data Scientist
____
### **2. Question:**
Which data job category has the highest salary in the Mexican labor market in August 2022 according to the OCC website?
____
### **3. Hypothesis:**
The **Data Scientist** position has the highest salary in the Mexican labor market in August 2022 according to the OCC website.
____
### **4. Abridged Methodology:**
1) Analytical approach: Descriptive and inferential statistics.
2) Data requirements: Data about job positions such as job name, salary, employer and location.
3) Data was collected from the OCC Website (Mexico) on 03 August 2022, through web scraping with Selenium and BeautifulSoup.
4) Data then was explored and cleaned with Pandas and Numpy. 
5) Data was analyzed through descriptive and inferential statistics with Pandas, Scipy and Statsmodels and visualized with Matplotlib, Seaborn, Folium and Plotly. 
6) A dashboard was built with Plotly and Dash.
7) A final report was written with the complete results obtained from the data.
8) Some slides were prepared with the most important insights from the report.
___
### **5. Dashboard**
To view and play with the interactive Dashboard, please download the **[app](https://github.com/DanielEduardoLopez/DataJobsMX2022/blob/main/4-Dashboard.py)** into a directory of your choice. Then, run the app using the following command:
```bash
python 4-Dashboard.py
```
And visit http://127.0.0.1:8050/ in your web browser.

Please note that Python 3 and its libraries Numpy, Pandas, Dash and Plotly are required for properly running the dashboard.
___
### **6. Main Insights**


___
### **7. Conclusions **
PENDING

___
### **8. Description of Files in Repository:**
File | Description 
--- | --- 
1-DataCollection.ipynb | Notebook with the Python code for collecting the required data from the OCC website.
2-DataWrangling.ipynb | Notebook with the Python code for cleaning and preparing the data retrieved through web scraping.
3-DataAnalysisViz.ipynb | Notebook with the Python code for analyzing and visualizing the data.
4-Dashboard.py | Dash app for rendering the interactive dashboard.
Dataset_Clean.csv | CSV file with the cleaned job data  (Job, Company, Location, Average Salary).
Dataset_Raw.csv | CSV file with the raw data collected through web scraping (Job, Salary, Company, Location).
Report.pdf | Complete report with the results obtained from the data.
Slides.pdf | Slides with the most important insights gained from the data analysis.
