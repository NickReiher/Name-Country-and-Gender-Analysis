"""
I examine name and country data from the 2018 Chicago Marathon.
I already scraped and cleaned up the data - saved as a csv file with the full name and country code (used by Chicago Marathon) of each finisher
"""

import pandas as pd

import plotly as py
import plotly.offline as offline
plotly_username = 'Your_Name'
plotly_api_key = 'Your_Api_Code'
py.tools.set_credentials_file(username=plotly_username, api_key=plotly_api_key)


#Plotly uses ISO-3 country codes to plot data by country.
#Here I import a csv file with all countries and their ISO-3 codes
ISO3_Codes = pd.DataFrame
ISO3_Codes = pd.read_table('ISO3_Country_Codes.txt', encoding='utf8')
ISO3_Codes = ISO3_Codes[['name', 'alpha-3']]

#Some of the country codes don't match the ISO-3 codes, so here is a dictionary matching the
#codes used by the Chicago Marathon to the ISO-3 codes, where they differ. 
#There are more codes that don't match (for countries with fewer finishers) -- need to update
Codes_to_ISO3 = {}
Codes_to_ISO3.update(
        {'GER': 'DEU',
         'CRC': 'CRI',
         'TPE': 'TWN',
         'NED': 'NLD',
         'INA': 'IDN',
         'GUA': 'GTM',
         'POR': 'PRT',
         'CHI': 'CHL',
         'PHI': 'PHL',
         'SUI': 'CHE',
         'DEN': 'DNK',
         'SIN': 'SGP',
         'MAS': 'MYS',
         'PUR': 'PRI',
         'ESA': 'SLV',
         'HON': 'HND',
         'SLO': 'SVK',
         'PAR': 'PRY',
         'RSA': 'ZAF',
         "ALG":"DZA",
         "ARU":"ABW",
         "BAH":"BHS",
         "BAN":"BGD",
         "BAR":"BRB",
         "BER":"BMU",
         "BIZ":"BLZ",
         "BUL":"BGR",
         "CAY":"CYM",
         "CRO":"HRV",
         "GRE":"GRC",
         "IRI":"IRN",
         "KSA":"SAU",
         "KUW":"KWT",
         "LAT":"LVA",
         "LIB":"LBY",
         "MAW":"MWI",
         "MGL":"MNG",
         "MRI":"MRT",
         "NCA":"NIC",
         "NEP":"NPL",
         "NGR":"NGA",
         "PLE":"PSE",
         "TAN":"TZA",
         "TRI":"TTO",
         "UAE":"ARE",
         "URU":"URY",
         "VIE":"VNM",
         "ZAM":"ZMB",
         "ZIM":"ZWE",                      
         })

    
#Import the Chicago Marathon finishers data and clean it up a bit
Names = pd.DataFrame
Names = pd.read_table('Chicago_Marathon_2018_Results_Clean.txt', delimiter=',')
Names['Last Name'], Names['First Name']  = Names['Full Name'].str.split(', ', 1).str
Names['First Name'].fillna('none', inplace=True)
Names['Count'] = 1
del Names['Full Name']

#Change the country code to match the ISO-3 code, where needed
Names['Country'] = Names.apply(lambda row: Codes_to_ISO3[row['Country']] if row['Country'] in Codes_to_ISO3 else row['Country'], axis = 1)
Agg_Country = Names.groupby('Country', as_index=False).count()[['Country', 'Count']]

#This tests to make sure all of the country codes in my data are a valid ISO-3 code
Country_Code_Test = Agg_Country.copy()
Country_Code_Test = pd.merge(Country_Code_Test, ISO3_Codes, left_on = 'Country', right_on = 'alpha-3', how = 'left')
Country_Code_Test = Country_Code_Test[Country_Code_Test['alpha-3'].isnull()]
country_code_errors = len(Country_Code_Test)
print('There are ' + str(country_code_errors) + ' incorrect country codes.')
print(Country_Code_Test)

#Here I create some other dataframe I will pull from later
Agg_Gender = Names.groupby('Gender', as_index=False).count()[['Gender', 'Count']]
Agg_Name = Names.groupby('First Name', as_index=False).count()[['First Name', 'Count']]
Agg_Gender_by_Country = Names.groupby(['Country', 'Gender'], as_index=False).count()[['Country', 'Gender', 'Count']]
Agg_Name_Country = Names.groupby(['First Name', 'Country'], as_index=False).count()
Agg_Name_Gender = Names.groupby(['First Name', 'Gender'], as_index=False).count()[['First Name', 'Gender', 'Count']]
Agg_Name_Gender_by_Country = Names.groupby(['First Name', 'Gender', 'Country'], as_index=False).count()
#for the Agg_Name_MaxCountry dataframe, ties are broken by reverse alphabetical order
idx = Agg_Name_Country.groupby(['First Name'])['Count'].transform(max) == Agg_Name_Country['Count']
Agg_Name_MaxCountry = Agg_Name_Country[idx]
idx = Agg_Name_MaxCountry.groupby(['First Name'])['Country'].transform(max) == Agg_Name_MaxCountry['Country']
Agg_Name_MaxCountry = Agg_Name_MaxCountry[idx]

### GENERAL ANALYSIS ###

#Analyzing finishers by Country
total_finishers = len(Names)
print('')
print('There are ' + str(total_finishers) + ' finishers.')

total_countries = len(Agg_Country)
print()
print('There are ' + str(total_countries) + ' countries represented.')

#Viewing the countries with the most representation
Agg_Country['Percent'] = 100 * round(Agg_Country['Count'] / total_finishers,3)
print()
print('Here are the ones with the most representation')
print(Agg_Country.sort_values('Count', ascending = False).head(5))



#VISUALIZATION of Country
#Create a new dataframe to be used in the visualization of participants by country
By_Country = Agg_Country.copy()

data_country = [ dict(
        type = 'choropleth',
        locations = By_Country['Country'],
        z = By_Country['Count'],
        #Don't like the coloring - can I adjust it somehow to make it clearer?
        colorscale = [[0,"rgb(0, 200, 0)"],[1/10000,"rgb(0, 160, 0)"],[1/1000,"rgb(0, 120, 0)"],\
            [1/100,"rgb(0, 80, 0)"],[1/10,"rgb(0, 40, 0)"],[1,"rgb(0, 0, 0)"]],
        reversescale = False,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            title = 'Number of Finishers'),
      ) ]

layout_country = dict(
    annotations=[
        dict(
            x=0.50,
            y=0.05,
            showarrow=False,
            xref='paper',
            yref='paper'
        )],
    title = '2018 Chicago Marathon <br> Finishers by Country',
    geo = dict(
        showframe = True,
        showcountries = True,
        countrywidth = .5,
        showcoastlines = True,
        coastlinewidth = .5,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data_country, layout=layout_country )

py.plotly.plot(fig, validate=False, filename='chicago_marathon_finishers_by_country_map.html')
offline.plot(fig, validate=False, filename='chicago_marathon_finishers_by_country_map.html')


#Creating a dataframe that shows which countries only had one runner finish
One_Runner = Agg_Country[Agg_Country['Count'] == 1]
del One_Runner['Percent']
one_runner_count = len(One_Runner)
print()
print('There are ' + str(one_runner_count) + ' runners who had no fellow countrymen or countrywomen.')
print('Those countries are:')
print(One_Runner)

#VISUALIZATION of countries with one finisher

data_country = [ dict(
        type = 'choropleth',
        locations = One_Runner['Country'],
        z = One_Runner['Count'],
        #Don't like the coloring - can I adjust it somehow to make it clearer?
        #colorscale = [[0,"rgb(0, 200, 0)"],[1/10000,"rgb(0, 160, 0)"],[1/1000,"rgb(0, 120, 0)"],\
         #   [1/100,"rgb(0, 80, 0)"],[1/10,"rgb(0, 40, 0)"],[1,"rgb(0, 0, 0)"]],
        #reversescale = False,
      ) ]

layout_country = dict(
    title = '2018 Chicago Marathon <br> Countries with Exactly One Finisher',
    showscale = False,
    geo = dict(
        showframe = True,
        showcountries = True,
        countrywidth = .5,
        showcoastlines = True,
        coastlinewidth = .5,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data_country, layout=layout_country )

#need to find a way not to show the scale
py.plotly.plot(fig, validate=False, filename='chicago_marathon_countries_with_one_finisher.html')
offline.plot(fig, validate=False, filename='chicago_marathon_countries_with_one_finisher.html')


#Analyzing finishers by gender
number_of_males = Agg_Gender.loc[Agg_Gender['Gender'] == 'male', 'Count'].iloc[0]
number_of_females = Agg_Gender.loc[Agg_Gender['Gender'] == 'female', 'Count'].iloc[0]
percent_male = number_of_males / total_finishers
print()
print('The finishers are ' + str(100*round(percent_male,2)) + '% male.')

#Looking at the gender division by country - create a dataframe that lists each country, the number and percent of male and female finishers
Gender_by_Country = Agg_Gender_by_Country.pivot(index = 'Country', columns = 'Gender')
Gender_by_Country.columns = ['Female', 'Male']
Gender_by_Country.fillna(0, inplace = True)
Gender_by_Country.reset_index(inplace=True)
Gender_by_Country['Total'] = Gender_by_Country['Male'] + Gender_by_Country['Female']
Gender_by_Country['Percent Male'] = 100*round(Gender_by_Country['Male'] / Gender_by_Country['Total'],3)
Gender_by_Country['Percent Female'] = 100*round(Gender_by_Country['Female'] / Gender_by_Country['Total'],3)
Gender_by_Country['Male'] = Gender_by_Country['Male'].astype('int')
Gender_by_Country['Female'] = Gender_by_Country['Female'].astype('int')
#Look at the countries with at least x finishers
Gender_by_Country = Gender_by_Country[Gender_by_Country['Total'] > 50]
Gender_by_Country['Map Text'] = Gender_by_Country['Male'].astype('str') + ' Males, ' + Gender_by_Country['Female'].astype('str') + ' Females'

#VISUALIZATION of Gender by Country

data_gender = [dict(
        type = 'choropleth',
        locations = Gender_by_Country['Country'],
        z = Gender_by_Country['Percent Female'],
        text = Gender_by_Country['Map Text'],
        name = Gender_by_Country['Total'],
        colorscale = [[0,"rgb(200, 0, 0)"],[20,"rgb(160, 0, 0)"],[40,"rgb(120, 0, 0)"],\
            [60,"rgb(80, 0, 0)"],[80,"rgb(40, 0, 0)"],[100,"rgb(0, 0, 0)"]],
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            ticksuffix = ' %',
            title = 'Percentage of Female Runners'),
      )]

layout_gender = dict(
    annotations=[
        dict(
            x=0.50,
            y=0.05,
            showarrow=False,
            text='Note: Countries with less than 50 runners are ignored',
            xref='paper',
            yref='paper'
        )],
    title = '2018 Chicago Marathon <br> Percentage of Female Runners (by Country)',
    geo = dict(
        showframe = True,
        showcountries = True,
        countrywidth = .5,
        showcoastlines = True,
        coastlinewidth = .5,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict(data=data_gender, layout=layout_gender)

py.plotly.plot( fig, validate=False, filename='chicago_marathon_gender_by_country_map')
offline.plot( fig, validate=False, filename='chicago_marathon_gender_by_country_map')

#For each name, break down how many finishers are from the US and how many not from the US
By_Name = pd.merge(Agg_Name, Agg_Name_Country[Agg_Name_Country['Country'] == 'USA'], on='First Name', how='left')
del By_Name['Gender']
del By_Name['Country']
del By_Name['Last Name']
By_Name.columns = ['First Name', 'Total', 'USA']
By_Name.fillna(0, inplace=True)
By_Name['USA'] = By_Name['USA'].astype('int')
By_Name['Non-USA'] = By_Name['Total'] - By_Name['USA']
By_Name['Percent USA'] = By_Name['USA'] / By_Name['Total']

#Look at the most common names in total
By_Name.sort_values('Total', inplace=True, ascending=False)
print('')
print(By_Name.head())

#Look at the most common names among non-Americans
By_Name.sort_values('Non-USA', inplace=True, ascending=False)
print('')
print(By_Name.head())

#Add data on the gender-breakdown of names to the By_Name dataframe
By_Name = pd.merge(By_Name, Agg_Name_Gender[Agg_Name_Gender['Gender'] == 'male'], on = 'First Name', how = 'left')
By_Name.fillna(0, inplace=True)
del By_Name['Gender']
By_Name = pd.merge(By_Name, Agg_Name_Gender[Agg_Name_Gender['Gender'] == 'female'], on = 'First Name', how = 'left')
By_Name.fillna(0, inplace=True)
del By_Name['Gender']
By_Name.columns = ['First Name', 'Total', 'USA', 'Non-USA', 'Percent USA', 'Males', 'Females']
By_Name['Percent Male'] = By_Name['Males'] / (By_Name['Males'] + By_Name['Females'])

#Create a dataframe that has names with a substantial number from each gender
Gender_Neutral = By_Name[(By_Name['Percent Male'] > .2) & (By_Name['Percent Male'] < .8) & (By_Name['Total'] > 15)]

#Create individual dataframes for some names that are gender neutral to examine country-level effects
Andrea = Agg_Name_Gender_by_Country[Agg_Name_Gender_by_Country['First Name'] == 'Andrea']
Jamie = Agg_Name_Gender_by_Country[Agg_Name_Gender_by_Country['First Name'] == 'Jamie']
Jaime = Agg_Name_Gender_by_Country[Agg_Name_Gender_by_Country['First Name'] == 'Jaime']
Jan = Agg_Name_Gender_by_Country[Agg_Name_Gender_by_Country['First Name'] == 'Jan']
Jordan = Agg_Name_Gender_by_Country[Agg_Name_Gender_by_Country['First Name'] == 'Jordan']
Lee = Agg_Name_Gender_by_Country[Agg_Name_Gender_by_Country['First Name'] == 'Lee']

print('')
print(Andrea)

#All-American names
All_American_Names = By_Name.copy()
All_American_Names = All_American_Names[All_American_Names['Non-USA'] == 0]
All_American_Names = All_American_Names[['First Name', 'Total', 'USA', 'Non-USA']]
All_American_Names.sort_values('Total', inplace=True, ascending=False)
print('')
print(All_American_Names.head())

