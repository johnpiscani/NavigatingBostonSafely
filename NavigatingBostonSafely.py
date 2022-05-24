import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

csvFile = "/Users/johnpiscani/Library/CloudStorage/OneDrive-BentleyUniversity/cs230/classNotes/finalProject/BostonCrimeData.csv"


def main():
    df = pd.read_csv(csvFile)
    # getting rid of rows with 0, 0 for lat, lon
    df = df[df.Lat != 0]
    df = df[df.Long != 0]

    intro()
    sidebar(df)
    bpdDistricts = "/Users/johnpiscani/Library/CloudStorage/OneDrive-BentleyUniversity/cs230/classNotes/finalProject/bpdDistricts.png"
    st.caption('Below is a map of all of the police department districts')
    st.image(bpdDistricts)


# bar chart
def getDataLine(df, day):
    df.index = df['DAY_OF_WEEK']
    dfOutput = df[['HOUR']]
    df = dfOutput.loc[[day]]
    countList = df['HOUR'].value_counts()
    hourList = []
    occurList = []
    for i in range(24):
        hour = i
        occur = countList[i]
        hourList.append(hour)
        occurList.append(occur)
    return hourList, occurList


def linePlot(hours, occurs):
    fig, ax = plt.subplots()
    ax.plot(hours, occurs)
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Number of Crimes')
    ax.set_title('Number of Crimes Per Hour of the Day')
    st.header('Line Plot')
    st.caption('This pie chart uses the hour and day of the week in each police report')
    st.pyplot(fig)


def getDataBar(df):
    out = df.STREET.value_counts()
    df = out.to_frame()
    df.reset_index(inplace=True)
    df = df[0:10]
    streets = []
    amts = []
    for index, row in df.iterrows():
        streets.append(row['index'])
        amts.append(row['STREET'])
    return streets, amts


def barChart(s, a):
    fig, ax = plt.subplots()
    ax.bar(s, a)
    ax.set_xlabel('Street Name')
    ax.set_ylabel('Number of Police Reports')
    ax.set_title('Number of Police Reports per Street')
    ax.tick_params(labelrotation=45)
    st.header('Bar Chart')
    st.caption('This pie chart uses the hour and day of the week in each police report')
    st.pyplot(fig)


def getDataPie(df, month):
    dfPie = df[['MONTH', 'OFFENSE_DESCRIPTION']]
    dfPie.columns = ['Month', 'Description']
    dfPie.index = dfPie['Month']
    dfPie = dfPie.loc[[month]]
    if month == 1:
        monthName = 'Data from January'
    elif month == 2:
        monthName = 'Data from February'
    elif month == 3:
        monthName = 'Data from March'
    elif month == 4:
        monthName = 'Data from April'
    dfPie = dfPie['Description'].value_counts()
    dfPie = dfPie.to_frame()
    dfPie.reset_index(inplace=True)
    dfPie = dfPie[0:10]
    dfPie.columns = ['Description', 'Amount']
    descriptionSeries = pd.Series(dfPie.Description)
    amountSeries = pd.Series(dfPie.Amount)
    return descriptionSeries, amountSeries, monthName


def pieChart(d, a, m):
    fig, ax = plt.subplots()
    ax.pie(a, autopct='%1.1f%%')
    ax.legend(d, loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title(m)
    st.header('Pie Chart')
    st.caption('This pie chart uses the month and description in each police report')
    st.pyplot(fig)


def getDataMap(df, district):
    df = df[df.Lat != 0]
    df = df[df.Long != 0]
    df.index = df['DISTRICT']
    df = df[['Lat', 'Long']]
    df.columns = ['lat', 'lon']
    df = df.loc[[district]]
    return df


def makeMap(df):
    st.header('Map')
    st.caption('This pie chart uses the district, latitude, and longitude in each police report')
    st.map(df)


# first screen
def intro():
    st.markdown("<h1 style='text-align: center;;'>Navigating Boston Safely</h1>", unsafe_allow_html=True)
    image = "/Users/johnpiscani/Library/CloudStorage/OneDrive-BentleyUniversity/cs230/classNotes/finalProject/boston.jpeg"
    st.image(image)
    st.markdown("<h2 style='text-align: center;'>By John Piscani</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Data from data.boston.gov. This data includes data of crime incident reports from 2015 to 2022.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Using the sidebar, you may customize and view more information on the charts and map.</p>", unsafe_allow_html=True)


def sidebar(df):
    st.sidebar.title("Directory")

    st.sidebar.header('Line Plot')
    st.sidebar.subheader('Number of Crimes per Hour of the Day')
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    day = st.sidebar.selectbox("Please choose day of the week:", days)
    for x in range(len(days)):
        if day == days[x]:
            hours, occurs = getDataLine(df, days[x])
            linePlot(hours, occurs)

    st.sidebar.header('Bar Chart')
    st.sidebar.subheader('Location of Crime based on Street')
    st.sidebar.caption('This bar chart shows the top ten streets in Boston with the most police reports')
    s, a = getDataBar(df)
    barChart(s, a)

    st.sidebar.header('Pie Chart')
    st.sidebar.subheader('Top Ten Crimes Per Month')
    month = st.sidebar.radio('Select', options=[1, 2, 3, 4])
    des, amt, m = getDataPie(df, month)
    pieChart(des, amt, m)

    st.sidebar.header('Map')
    st.sidebar.subheader('Map of crimes based on District')
    dist = st.sidebar.selectbox('Pick a district', ['B2', 'D4', 'C11', 'A1', 'B3', 'C6', 'D14', 'E18', 'E13', 'E5', 'A7', 'A15'])
    out = getDataMap(df, dist)
    makeMap(out)


main()
