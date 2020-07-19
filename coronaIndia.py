import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.figure_factory as ff 
import plotly.express as px
import folium
import plotly.graph_objects as go

# Data Analysis of Worldwide Data

def scrapeWorld ():
    url="https://www.worldometers.info//coronavirus//"
    headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response=requests.get(url, headers=headers)
    soup= BeautifulSoup(response.content,'html.parser')
    coronatable= soup.find_all("table")
    co=coronatable[0]
    country=[] 
    total_cases=[]
    new_cases=[]
    total_death=[]
    new_death=[]
    total_recovered=[]
    active_cases=[]
    serious_critical=[]
    totCases_1Mpop=[]
    deaths_1Mpop=[]
    total_tests=[]
    tests_1Mpop=[]
    population=[]
    rows=co.find_all("tr")[9:-8]
    for row in rows:
        col=row.find_all("td") 
        country.append(col[1].text.strip())
        total_cases.append(col[2].text.strip())
        new_cases.append(col[3].text.strip())
        total_death.append(col[4].text.strip())
        new_death.append(col[5].text.strip())
        total_recovered.append(col[6].text.strip())
        active_cases.append(col[7].text.strip())
        serious_critical.append(col[8].text.strip())
        totCases_1Mpop.append(col[9].text.strip())
        deaths_1Mpop.append(col[10].text.strip())
        total_tests.append(col[11].text.strip())
        tests_1Mpop.append(col[12].text.strip())
        population.append(col[13].text.strip())
    
    df = pd.DataFrame(list(zip(country,
    total_cases,
    new_cases, 
    total_death,
    new_death,
    total_recovered,
    active_cases,
    serious_critical,
    totCases_1Mpop,
    deaths_1Mpop,
    total_tests,
    tests_1Mpop,
    population)), columns=["Country","Total Cases","New Cases","Total Deaths","New Deaths","Total Recovered","Active Cases",
                        "Serious,Critical","Total Cases/1Mpop","Deaths/1Mpop","Total Tests","Tests/1Mpop","Population"])

    # Dropping columns those are NOT required
    df.drop(["Serious,Critical","Total Cases/1Mpop","Deaths/1Mpop","New Cases", "New Deaths"],axis=1, inplace = True) 

    #Cleaning Data from columns
    df.loc[df['Total Recovered'] == 'N/A', 'Total Recovered'] = 0
    df.loc[df['Active Cases'] == 'N/A', 'Active Cases'] = 0
    df.loc[df['Tests/1Mpop'] == 'N/A', 'Tests/1Mpop'] = 0
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df.replace(np.nan,0, inplace=True)

    total_cases1=[]
    for i in df["Total Cases"]:
        s=str(i)
        s1=s.replace(",","")
        s2=int(s1)
        total_cases1.append(s2)

    total_death1=[]
    for i in df["Total Deaths"]:
        s=str(i)
        s1=s.replace(",","")
        s2=int(s1)
        total_death1.append(s2)

    total_recovered1=[]
    for i in df["Total Recovered"]:
        s=str(i)
        s1=s.replace("+","")
        s2=s1.replace(",","")
        s3=int(s2)
        total_recovered1.append(s3)

    active_cases1=[]
    for i in df["Active Cases"]:
        s=str(i)
        s1=s.replace("+","")
        s2=s1.replace(",","")
        s3=int(s2)
        active_cases1.append(s3)

    total_tests1=[]
    for i in df["Total Tests"]:
        s=str(i)
        s1=s.replace("+","")
        s2=s1.replace(",","")
        s3=float(s2)
        s4=int(s3)
        total_tests1.append(s4)

    Testsper1Mpop =[]
    for i in df["Tests/1Mpop"]:
        s=str(i)
        s1=s.replace("+","")
        s2=s1.replace(",","")
        s3=int(s2)
        s3=int(s2)
        Testsper1Mpop.append(s3)

    population1=[]
    for i in df["Population"]:
        s=str(i)
        s1=s.replace("+","")
        s2=s1.replace(",","")
        s3=int(s2)
        population1.append(s3)

    df=pd.DataFrame(list(zip(country, total_cases1,
    total_death1,
    total_recovered1,
    active_cases1,
    total_tests1,
    Testsper1Mpop,
    population1)), 
                    columns=["Country","Total Cases","Total Deaths","Total Recovered","Active Cases",
                        "Total Tests","Tests/1Mpop","Population"])
    return df

    
def totalWorld():
    df=scrapeWorld()
    Total_Cases1=df["Total Cases"].sum()
    Total_Recovered1=df["Total Recovered"].sum()
    Total_Deaths1=df["Total Deaths"].sum()
    Active_Cases1=df["Active Cases"].sum()
    return [Total_Cases1,Total_Recovered1,Total_Deaths1,Active_Cases1]


def top20World():
    df=scrapeWorld()
    
    data=df.iloc[0:20,:]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=data["Country"],
                    y=data["Total Cases"],
                    name='Total Cases',
                    ))
    fig.add_trace(go.Bar(x=data["Country"],
                    y=data["Total Deaths"],
                    name='Total Deaths',
                    ))
    fig.add_trace(go.Bar(x=data["Country"],
                    y=data["Total Recovered"],
                    name='Total Recovered',
                    ))
    fig.update_layout(barmode='stack')
        
    return plotly.offline.plot(fig,output_type='div')


# Data Analysis of India Data

def scrape ():
    url="https://www.mohfw.gov.in/"
    headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response=requests.get(url, headers=headers)
    soup= BeautifulSoup(response.content,'html.parser')
    coronatable_in= soup.find_all("table")
    corona1=coronatable_in[0]
    states=[]
    total_cases=[] #confirmed_cases
    cmd=[] #cured_migrated_discharged
    deaths=[]
    active_cases=[]
    rows=corona1.find_all("tr")[1:-6]
    for row in rows:
        col=row.find_all("td")
        states.append(col[1].text.strip())
        active_cases.append(col[2].text.strip())
        total_cases.append(col[3].text.strip())
        cmd.append(col[4].text.strip())
        deaths.append(col[5].text.strip())
    df = pd.DataFrame(list(zip(states, total_cases, cmd, deaths,active_cases,)), 
               columns =["States", "Total Cases","Total Recovered", "Total Deaths","Active Cases"]) 
    df.replace({"Uttarakhand": "Uttaranchal", 
                                  "Odisha":"Orrisa"}, inplace=True) 
    df["Active Cases"] = df["Active Cases"].astype(str).astype(int)
    df["Total Recovered"] = df["Total Recovered"].astype(str).astype(int)
    df["Total Deaths"] = df["Total Deaths"].astype(str).astype(int)
    df["Total Cases"] = df["Total Cases"].astype(str).astype(int)
    return df

def table():
    df=scrape()
    
    df3 = ff.create_table(df)
    # return df3
    return plotly.offline.plot(df3,output_type='div')  

def total():
    df=scrape()
    Total_Cases=df["Total Cases"].sum()
    Total_Cured=df["Total Recovered"].sum()
    Total_Deaths=df["Total Deaths"].sum()
    Active_Cases=df["Active Cases"].sum()
    return [Total_Cases,Total_Cured,Total_Deaths,Active_Cases]

def top20():
    df=scrape()
    df_latest=df.sort_values(by=["Total Cases"], ascending=False)
    df_latest.reset_index(drop=True,inplace=True)

    dfCovidImpactInd=df_latest.iloc[0:20,:]

    fig = go.Figure()
    fig = go.Figure(go.Bar(x=dfCovidImpactInd["States"], y=dfCovidImpactInd["Total Cases"], name='Total Cases'))
    fig.add_trace(go.Bar(x=dfCovidImpactInd["States"], y=dfCovidImpactInd["Total Deaths"], name='Total Deaths'))
    fig.add_trace(go.Bar(x=dfCovidImpactInd["States"], y=dfCovidImpactInd["Total Recovered"], name='Total Recovered'))
    fig.update_layout(barmode='stack')
    
    return plotly.offline.plot(fig,output_type='div')



def datewise():
    df=pd.read_csv(r"C:\Users\ADMIN\Desktop\COVID19 project\covid_19_india.csv")
    df.drop(["Sno","Time","ConfirmedIndianNational","ConfirmedForeignNational"],axis=1, inplace = True)
    df.groupby(['State/UnionTerritory']) 
    covid19_Mah = df[df['State/UnionTerritory'] == "Maharashtra"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=covid19_Mah["Date"], y=covid19_Mah["Confirmed"], 
                    mode='lines+markers',
                    name='Total Cases'))
    fig.add_trace(go.Scatter(x=covid19_Mah["Date"], y=covid19_Mah["Cured"], 
                    mode='lines+markers',
                    name='Total Recovered'))
    fig.add_trace(go.Scatter(x=covid19_Mah["Date"], y=covid19_Mah["Deaths"], 
                    mode='lines+markers',
                    name='Total Deaths'))
    
    return plotly.offline.plot(fig,output_type='div')

    
def ageWise():
    df=pd.read_csv(r"AgeGroupDetails.csv")
    df1= df.rename(index = {"Oct-19": "10-19"})
    fig = px.bar(df1, x='AgeGroup', y='TotalCases', color='Percentage', height=600)
    return plotly.offline.plot(fig,output_type='div')




