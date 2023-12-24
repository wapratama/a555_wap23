# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set seaborn style theme
sns.set(style="dark")

# Load dataset
df = pd.read_csv("https://raw.githubusercontent.com/wapratama/Dataset/main/a555_hour_data.csv")
print(df.head())

#  Cast datetime to date column
df['date'] = pd.to_datetime(df.date)
print(df.info())

# Set streamlit page configuration
st.set_page_config(page_title="Bike-sharing Dashboard",
                   page_icon="🚲",
                   layout="wide",
                   menu_items={'About': "# This is a submission for Dicoding Course"}
                   )

# Membuat Komponen Filter
min_date = df["date"].min()
max_date = df["date"].max()
print("Min Date: ", min_date, " & Max Date: ", max_date)

with st.sidebar:
    # Add Logo
    st.image("https://raw.githubusercontent.com/wapratama/Images/9c7df8afb0988b3eb99bae9e0804a369cb8b2393/BikeShare.png")

    # Get start_date & end_date with date_input
    start_date, end_date = st.date_input(label="Date Filter", min_value=min_date, max_value=max_date,
                                         value=[min_date, max_date])

# Create dataframe from filter
main_df = df[(df["date"] >= str(start_date)) & (df["date"] <= str(end_date))]

# Create title of dashboard
st.title("🚲 Bike-sharing Dashboard 🚲")
st.markdown("##")

# Section 1: Number of user
st.subheader("Bike-Sharing Users by Numbers")

col1, col2, col3 = st.columns(3)
with col1:
    total_rental = main_df["total_users"].sum()
    st.metric("Total Bike Rental", value=total_rental)
with col2:
    casual_rental = main_df["casual"].sum()
    st.metric("Casual Bike Rental", value=casual_rental)
with col3:
    regis_rental = main_df["registered"].sum()
    st.metric("Registered Bike Rental", value=regis_rental)
st.markdown("---")

# Section 2: Demography based on times
st.subheader("Bike-Sharing Users by Times")

## Membuat dataframe visualisasi
df = main_df[["year", "season", "month", "weekday", "casual", "registered"]]
tidy = df.melt(id_vars=["year", "season", "month", "weekday"]).rename(columns=str.title)

## Membuat Bar Chart jumlah pelanggan berdasarkan musim, bulan, dan hari
fig, ax = plt.subplots(figsize=(20, 8))
sns.barplot(x="Month", y="Value", hue="Variable", data=tidy,
            estimator="sum", errorbar=None, ax=ax)
ax.set_title("Monthly User Count")
st.pyplot(fig)

fig,(ax1,ax2) = plt.subplots(ncols=2,figsize=(20,5))
sns.barplot(x="Season", y="Value", hue="Variable", data=tidy,
            estimator="sum", errorbar=None, ax=ax1)
ax1.set_title("Seasonal User Count")
order = ["sunday", "monday", "tuesday", "wednesday",
         "thursday", "friday", "saturday"]
sns.barplot(x="Weekday", y="Value", hue="Variable", data=tidy,
            estimator="sum", errorbar=None, order=order, ax=ax2)
ax2.set_title("Daily User Count")
st.pyplot(fig)

## Membuat Line Chart total penyewaan sepeda per jam berdasarkan musim
fig,ax=plt.subplots(figsize=(20,8))

sns.pointplot(x="hour", y="total_users", data=main_df,
              estimator="sum", hue="season", errorbar=None, ax=ax)
ax.set_title("Total User Count by Season & Hour")
st.pyplot(fig)

st.markdown("---")

# Section 3: Weather Factor
st.subheader("Bike-Sharing Users by Weather")

## Membuat visualisasi pengaruh kondisi cuaca
fig,(ax1,ax2) = plt.subplots(ncols=2,figsize=(20,5))

### Membuat Bar Chart distribusi penyewaan sepeda berdasarkan kondisi cuaca
sns.barplot(x="weather_condition", y="total_users", data=main_df,
            hue="weather_condition", estimator="sum", errorbar=None, ax=ax1)
ax1.set_title("Total Rental by Weather Condition")

### Membuat Heat Map korelasi antar parameter kondisi cuaca
correl_df=main_df[["temp","atemp","humidity","windspeed","total_users"]]
mask = np.triu(np.ones_like(correl_df.corr(), dtype=np.bool_))
sns.heatmap(correl_df.corr(), mask=mask, annot=True, vmin=-1, vmax=1, ax=ax2)
ax2.set_title("Weather Factor Correlation Matrix")

st.pyplot(fig)

### Membuat Bar Chart distribusi penyewaan sepeda per bulan berdasarkan kondisi cuaca
fig,ax=plt.subplots(figsize=(20,5))
sns.pointplot(x="month", y="total_users", data=main_df,
              estimator="sum", hue="weather_condition", errorbar=None, ax=ax)
ax.set_title("Total Rental per Month by Weather Condition")
st.pyplot(fig)

st.markdown("---")

with st.expander("Parameter Description"):
    st.write(
        """
        - Month : 
            1 (January), 2 (February), 3 (March), 4 (April), 5 (May), 6 (June), 
            7 (July), 8 (August), 9 (September), 10 (October), 11 (November), 12 (December)
        - Weather Condition :
            - 1: Clear, Few clouds, Partly cloudy, Partly cloudy
            - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
            - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
            - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
        - temp : Temperature in Celsius
        - atemp: Feeling temperature in Celsius.
        - humidity: Humidity with max in 100
        - windspeed: Wind speed.
        """
    )
st.markdown("---")

st.caption("Copyright (c) Wisnu Anugrah Pratama 2023")