import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc

df_all_crime = pd.read_csv("BostonCrime2022_8000_sample.csv")
df_all_crime.rename(columns={"Lat":"lat", "Long": "lon"}, inplace= True)

df_bos_shootings = df_all_crime[df_all_crime["SHOOTING"].isin([1])]
df_bos_burglaries = df_all_crime[df_all_crime["OFFENSE_CODE"].isin([520,540])]
df_bos_assaults = df_all_crime[df_all_crime["OFFENSE_CODE"].isin([801, 423])]
descending_date = df_all_crime.sort_values(by='OCCURRED_ON_DATE')


def generate_charts(df_1, desc):
        days = df_1['DAY_OF_WEEK'].value_counts()
        names = df_1['DAY_OF_WEEK'].value_counts().index.tolist()
        ax1.pie(days,labels= names, autopct='%.1f%%')
        ax1.set_title(f"Day of the week {desc}")
        n = 5
        offense_desc = df_1['OFFENSE_DESCRIPTION'].value_counts()[:n]
        offense_type = df_1['OFFENSE_DESCRIPTION'].value_counts().index.tolist()[:n]
        ax2.bar(offense_type,offense_desc)
        ax2.set_title(f"Most common types of {desc}")
        ax2.set_xlabel("Types")
        ax2.set_ylabel(f"Number of {desc}")
        street_freq = df_1['STREET'].value_counts()[:n]
        st_names = df_1['STREET'].value_counts().index.tolist()[:n]
        ax3.bar(st_names, street_freq)
        ax3.set_title(f"5 most common streets for {desc}")
        ax3.set_xlabel("Streets")
        ax3.set_ylabel(f"Number of {desc}")
        district_freq = df_1['DISTRICT'].value_counts()
        districts = df_1['DISTRICT'].value_counts().index.tolist()
        ax4.scatter(districts, district_freq, marker = '*', color='r', s = 40)
        ax4.set_xlabel('Districts')
        ax4.set_ylabel(f'Number of {desc}')
        ax4.set_title(f'District {desc} ')
        return plt





selected_map = st.sidebar.radio("Please select the page", ["Home Page", "All crimes", "Shootings", "Burglaries", "Assaults"])
if selected_map == "Home Page":
    st.title("Boston crimes sorted by type")
    st.write("This website will examine the different types of crimes committed in Boston in 2022. On each page for the different types of crimes there is a map of the locations. Additionally on each page there are graphs detailing the days of the week the crimes are committed, the types of crimes more in depth, and the most common sreets for them to occur.")
    jan = descending_date[descending_date['MONTH'].isin([1])]
    feb = descending_date[descending_date['MONTH'].isin([2])]
    mar = descending_date[descending_date['MONTH'].isin([3])]
    apr = descending_date[descending_date['MONTH'].isin([4])]
    may = descending_date[descending_date['MONTH'].isin([5])]



    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    slider = st.select_slider("Select a month", months)
    st.subheader(f"Crimes for the month of {slider}")
    if slider == 'Jan':
        st.write(jan)
    elif slider == 'Feb':
        st.write(feb)
    elif slider == 'Mar':
        st.write(mar)
    elif slider == 'Apr':
        st.write(apr)
    elif slider == 'May':
        st.write(may)


    st.subheader('Fire reports on any day')
    day_choice = df_all_crime['DAY_OF_WEEK'].value_counts().index.tolist()
    select_day = st.multiselect("Please choose a day of the week", day_choice)
    for day in select_day:
        for row in df_all_crime.itertuples():
            if row.DAY_OF_WEEK == day:
                wed_fire = df_all_crime[(df_all_crime.OFFENSE_CODE == 3108) & (df_all_crime.DAY_OF_WEEK == day)]
        st.write(wed_fire)


    st.subheader("All crimes by day of the week")
    pivot = df_all_crime.pivot_table(index=['DAY_OF_WEEK'], values=['OFFENSE_DESCRIPTION'], aggfunc= 'count').sort_values(by=['OFFENSE_DESCRIPTION'], ascending=False)
    st.write(pivot)
    st.subheader("All crimes by dates committed")
    descending_date = df_all_crime.sort_values(by='OCCURRED_ON_DATE')

    st.write(descending_date)

    st.subheader("Crimes committed on each street")
    streets = df_all_crime['STREET'].value_counts().index.tolist()
    select_street = st.multiselect('Please select a street name', streets)
    df_all_crime.set_index('INCIDENT_NUMBER', inplace=True)


    for street in select_street:
        for row in df_all_crime.itertuples():
            if row.STREET == street:
                st.write(row.OFFENSE_DESCRIPTION, ", ",row.STREET,", ", row.OCCURRED_ON_DATE)


    st.subheader("Dates and times of each type of crime")

    descending_date = df_all_crime.sort_values(by='OCCURRED_ON_DATE')

    crimes = df_all_crime['OFFENSE_DESCRIPTION'].value_counts().index.tolist()

    select_crime = st.multiselect('Please select a crime', crimes)

    for crime in select_crime:
        for row2 in descending_date.itertuples():
            if row2.OFFENSE_DESCRIPTION == crime:
                st.write(row2.OCCURRED_ON_DATE,", " ,row2.OFFENSE_DESCRIPTION)

    new_list = df_all_crime.values.tolist()
    st.subheader("List of Verbal Disputes")
    list_2 = [x for x in new_list if "VERBAL DISPUTE" in x]
    st.write(list_2)





elif selected_map == "All crimes":

    st.title('All Boston Crimes')
    # The most basic map, st.map(df)
    st.map(df_all_crime)



    fig1 = plt.figure(figsize=(12,8))

    ax1 = fig1.add_axes([0.1,0.6,0.3,0.3])
    ax2 = fig1.add_axes([0.6,0.6,0.3,0.3])
    ax3 = fig1.add_axes([0.1,0.1,0.3,0.3])
    ax4 = fig1.add_axes([0.6,0.1,0.3,0.3])

    st.pyplot(generate_charts(df_all_crime, "crimes"))


elif selected_map == "Shootings":

    st.title('All Boston Shootings')
    # The most basic map, st.map(df)
    st.map(df_bos_shootings)
    fig2 = plt.figure(figsize=(12,8))

    ax1 = fig2.add_axes([0.1,0.6,0.3,0.3])
    ax2 = fig2.add_axes([0.6,0.6,0.3,0.3])
    ax3 = fig2.add_axes([0.1,0.1,0.3,0.3])
    ax4 = fig2.add_axes([0.6,0.1,0.3,0.3])

    st.pyplot(generate_charts(df_bos_shootings, "shootings"))




elif selected_map == "Burglaries":

    st.title('All Boston Burlaries')
    # The most basic map, st.map(df)
    st.map(df_bos_burglaries)
    fig3 = plt.figure(figsize=(12,8))

    ax1 = fig3.add_axes([0.1,0.6,0.3,0.3])
    ax2 = fig3.add_axes([0.6,0.6,0.3,0.3])
    ax3 = fig3.add_axes([0.1,0.1,0.3,0.3])
    ax4 = fig3.add_axes([0.6,0.1,0.3,0.3])
    st.pyplot(generate_charts(df_bos_burglaries, "burglaries"))



elif selected_map == "Assaults":

    st.title('All Boston Assaults')
    # The most basic map, st.map(df)
    st.map(df_bos_assaults)
    fig4 = plt.figure(figsize=(12,8))

    ax1 = fig4.add_axes([0.1,0.6,0.3,0.3])
    ax2 = fig4.add_axes([0.6,0.6,0.3,0.3])
    ax3 = fig4.add_axes([0.1,0.1,0.3,0.3])
    ax4 = fig4.add_axes([0.6,0.1,0.3,0.3])


    st.pyplot(generate_charts(df_bos_assaults, "assaults"))
