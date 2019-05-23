#manipulate dataframes in python
import pandas as pd
import sys

#make API calls with python
import requests

#sys.path.insert(0, '/path/to/application/app/folder') used to import 
# local python file, in this case local keys
sys.path.insert(0, '../src/')
import localvars

#allows us to store results of API call cleanly
import json

# List of Years
strYears =["2010", "2013", "2014", "2015", "2016", "2017"]

tables = pd.read_csv("../src/data/tables.csv").to_dict(orient="row")
tablesdf = pd.DataFrame(tables)
tablesdf2 = tablesdf.set_index("table", drop = False)
for index, row in tablesdf2.iterrows():
    tablename= row['table']
    #print("value: " + tablesdf2.loc[tablename,'file'])
    # Using for loop 
    metric = pd.DataFrame() #creates a new dataframe that's empty
    for i in strYears: 

        #construct the API call we will use
        baseAPI = "https://api.census.gov/data/%s/acs/acs5?get=%s&for=tract:*&in=state:47%%20county:125&key=%s" 

        calledAPI = (baseAPI % (i, row['table'], localvars.apiKey))

        #call the API and collect the response
        response = requests.get(calledAPI)

        #load the response into a JSON, ignoring the first element which is just field labels
        try:
            formattedResponse = json.loads(response.text)[1:]

            #flip the order of the response from [population, zipcode] -> [zipcode, population]
            formattedResponse = [item[::-1] for item in formattedResponse]

            #store the response in a dataframe
            strColYear = "y_" + i

            metrictemp = pd.DataFrame(columns=['id', '2', '3', strColYear], data=formattedResponse)
            del metrictemp['2']
            del metrictemp['3']
            if i == "2010":
                metric=metrictemp
            else: 
                metric = metric.merge(metrictemp, on='id', how='outer')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    #save that dataframe to a CSV spreadsheet
    strFile = "../src/data/ProcessedData/" + row['file'] + ".csv"
    metric.to_csv(strFile, index=False)
    print("Output: " + strFile)

