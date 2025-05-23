import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

df = pd.read_csv('..\data\cleaned_fish_shellfish_dataset.csv')


logo = Image.open('../media/logo.png')

st.set_page_config(

page_title="Fiskerikajens dashboard",

page_icon="🐟",

layout="wide",

initial_sidebar_state="expanded",
)


with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Forside", "Profitabilitet af Produkter", "Transportomkostninger", "Vægtpris over tid"],
        icons=["info-circle", "bar-chart", "truck", "bell"],
        menu_icon="cast",
        default_index=0,
    )

st.image(logo, width=200)

if selected == "Forside":

    banner = """
    <body style="background-color:yellow;">
            <div style="background-color:#095c37 ;padding:10px">
                <h2 style="color:white;text-align:center;">Velkommen til Fiskerikajens dashboard</h2>
            </div>
    </body>
    """
    st.markdown(banner, unsafe_allow_html = True)

    st.markdown(
    """
    ###
    Dette dashboard er udviklet med formålet om at identificere de mest profitabel fiske- og skaldyrsprodukter pr. sæson. Hertil kan man også estimere prisen på fiske- og skaldyr, baseret på nøgleparametre såsom vægt, længde, type og sæson. 
    Med dette dashboard kan du se:
    * Profitabilitet på produktet pr. sæson og år.
    * Transportomkostningers indflydelse på prissætningen.
    * Vægtens pris over tid.

    Brug dashboardet som et værktøj til at træffe bedre og mere datadrevne beslutninger omkring indkøb og prissætning.

    """
)


    
if selected == "Profitabilitet af Produkter":
    name_cols = [col for col in df.columns if col.startswith("name_")]
    df['name'] = df[name_cols].idxmax(axis=1).str.replace("name_", "")

    view_option = st.radio("Vælg visning", ["Sæson", "År"], horizontal=True)

    if view_option == "Sæson":
        season = st.selectbox("Vælg sæson", ["Sommer", "Forår", "Efterår", "Vinter"])
        if season == "Sommer":
            season_df = df[df["season_availability_Summer"] == 1]
        elif season == "Forår":
            season_df = df[df["season_availability_Spring"] == 1]
        elif season == "Efterår":
            season_df = df[df["season_availability_Autumn"] == 1]
        else:
            season_df = df[df["season_availability_Winter"] == 1]
        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x="name", y="profit_kr", data=season_df, ax=ax)
        plt.xticks(rotation=90)
        plt.title(f"Profit pr. Produkt i {season}-sæsonen")
        st.pyplot(fig)
        # Table
        top10 = season_df[['name', 'price_kr', 'profit_kr']].sort_values(by='profit_kr', ascending=False).head(3)
        st.markdown("### Top 3 mest profitable produkter pr sæsonen")
        st.dataframe(top10.reset_index(drop=True), use_container_width=True)

    elif view_option == "År":
        year = st.selectbox("Vælg år", sorted(df["year"].unique()))
        year_df = df[df["year"] == year]
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(x="name", y="profit_kr", data=year_df, ax=ax)
        plt.xticks(rotation=90)
        plt.title(f"Profit pr. Produkt i år {year}")
        st.pyplot(fig)
        #Table
        top10 = year_df[['name', 'price_kr', 'profit_kr', 'year']].sort_values(by='profit_kr', ascending=False).head(3)
        st.markdown("### Top 3 mest profitable produkter pr year")
        st.dataframe(top10.reset_index(drop=True), use_container_width=True)

                            
if selected == "Transportomkostninger":
    "hello 2"

if selected == "Vægtpris over tid":
    "Hejsa"

