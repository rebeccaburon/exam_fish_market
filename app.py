import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from PIL import Image

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_fish_shellfish_dataset.csv")
PRICE_MODEL_PATH = os.path.join(BASE_DIR, "models", "price_model.pkl")
PROFIT_MODEL_PATH = os.path.join(BASE_DIR, "models", "profit_model.pkl")
CLASSIFIER_MODEL_PATH = os.path.join(BASE_DIR, "models", "profit_classifier.pkl")

# Load data
df = pd.read_csv(DATA_PATH)
logo = Image.open('media/logo.png')

# Page config
st.set_page_config(
    page_title="Fiskerikajens dashboard",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)


with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Forside", "Estimere pris og profit", "Profitabilitet af Produkter", "Vurderet indtjeningspotentiale", "Transportomkostninger", "Vægtpris over tid"],
        icons=["info-circle", "currency-dollar", "bar-chart", "activity", "truck", "bell"],
        menu_icon="cast",
        default_index=0,
    )


st.image(logo, width=200)

# Helper for user input
def get_user_input(include_year=True):
    weight = st.number_input("Vægt (g)", min_value=0.0, value=500.0)
    freight = st.number_input("Transportomkostning (kr)", min_value=0.0, value=10.0)
    if include_year:
        year = st.selectbox("År", sorted(df["year"].unique()))
    else:
        year = None    
    season = st.selectbox("Sæson", ["Sommer", "Forår", "Efterår", "Vinter"])

    season_data = {
        "season_availability_Summer": 1 if season == "Sommer" else 0,
        "season_availability_Spring": 1 if season == "Forår" else 0,
        "season_availability_Autumn": 1 if season == "Efterår" else 0,
        "season_availability_Winter": 1 if season == "Vinter" else 0,
    }

    input_df = pd.DataFrame([{ 
        "weight_g": weight,
        "freight_charge_kr": freight,
        "season_availability_Summer": season_data["season_availability_Summer"],
        "season_availability_Spring": season_data["season_availability_Spring"],
        "season_availability_Autumn": season_data["season_availability_Autumn"],
        "season_availability_Winter": season_data["season_availability_Winter"],
        "year": year
    }])
    
    if include_year:
        input_df["year"] = year

    return input_df

if selected == "Forside":
    st.markdown("""
    <body style="background-color:yellow;">
        <div style="background-color:#095c37 ;padding:10px">
            <h2 style="color:white;text-align:center;">Velkommen til Fiskerikajens dashboard</h2>
        </div>
    </body>
    """, unsafe_allow_html=True)

    st.markdown("""
    Dette dashboard er udviklet med formålet om at give Fiskerikajen datadrevet indsigt i, hvordan pris og profit på fiske- og skaldyrsprodukter påvirkes af nøglefaktorer som vægt, sæson og transportomkostninger. 
    Med udgangspunkt i en machine learning-model (linear regression) kan dashboardet: 
    * Estimere pris og profit baseret på produktets egenskaber (vægt, år, sæson og fragtomkostning). 
    * Identificere de mest profitable produkter pr. sæson og år. 
    * Analysere sammenhængen mellem fragtomkostninger og pris over tid. 
    * Vise hvordan vægten påvirker prissætningen på tværs af forskellige år og produkttyper.

    Brug dashboardet som et værktøj til at træffe  datadrevne beslutninger omkring indkøb og prissætning.
    """)

elif selected == "Estimere pris og profit":
    st.info("""
**Hvad er formålet?**  
    Denne model bruger regressionsalgoritmer til at forudsige både pris og profit baseret på oplysninger som vægt, årstal, sæson og transportomkostninger.  
Ved at indtaste disse værdier, kan du få et estimat på hvad produktet bør koste – og hvor meget profit det kan give.  
Modellen er trænet på historiske data fra Fiskerikajen og giver dermed et datadrevet grundlag for bedre beslutninger i indkøb og prissætning.
""")
    st.title(" Estimér pris og profit")
    st.markdown("Indtast oplysninger om et fiske- eller skaldyrsprodukt for at forudsige pris og profit:")

    input_df = get_user_input()
    price_model = joblib.load(PRICE_MODEL_PATH)
    profit_model = joblib.load(PROFIT_MODEL_PATH)

    if st.button(" Forudsig pris og profit"):
        pred_price = float(price_model.predict(input_df)[0])
        pred_profit = float(profit_model.predict(input_df)[0])
        st.success(f"🔹 Forventet pris: **{pred_price:.2f} kr**")
        st.success(f"🔹 Forventet profit: **{pred_profit:.2f} kr**")

elif selected == "Vurderet indtjeningspotentiale":
    st.title("🔍 Vurder indtjeningsniveau for et produkt")
    st.info("""
**Hvad er formålet?**  
Denne model vurderer, om et fiske- eller skaldyrsprodukt forventes at give **lav**, **mellem** eller **høj** profit.  
Det baseres på vægt, transportomkostning, sæson og type – og giver et hurtigt overblik over, hvor profitabelt produktet sandsynligvis vil være.
""")
    type_choice = st.selectbox("Type", ["Fisk", "Skaldyr"])
    type_data = {
        "type_fish": 1 if type_choice == "Fisk" else 0,
        "type_shellfish": 1 if type_choice == "Skaldyr" else 0
    }
    input_df = get_user_input(include_year=False)
    input_df["type_fish"] = type_data["type_fish"]
    input_df["type_shellfish"] = type_data["type_shellfish"]
    input_df = input_df.drop(columns=["year"])
# Reorder columns to match training input for classifier
    season_columns = [
    "season_availability_Summer",
    "season_availability_Spring",
    "season_availability_Autumn",
    "season_availability_Winter",
]
    classifier_input = input_df[[
    "weight_g",
        "freight_charge_kr",
        "type_fish",
        "type_shellfish"
] +  season_columns]

    

    clf_model = joblib.load(CLASSIFIER_MODEL_PATH)
    prediction = clf_model.predict(classifier_input)[0]

    if st.button("🔍 Forudsig profitkategori"):
        prediction = clf_model.predict(classifier_input)[0]
        st.success(f"🔹 Forventet indtjeningsniveau: **{prediction}**")
    

    
if selected == "Profitabilitet af Produkter":
    
    name_cols = [col for col in df.columns if col.startswith("name_")]
    df['name'] = df[name_cols].idxmax(axis=1).str.replace("name_", "")

    view_option = st.radio("Vælg visning", ["Diagram profit pr. år","Diagram profit pr. sæson","Sæson", "År"], horizontal=True)

    if view_option =="Diagram profit pr. år":
        st.image("media/profit_by_year_boxplot.png", caption="Oversigt over profit fordelt på år", width=800)
        st.markdown("""
                    Dette boksplot viser fordelingen af profit (kr) for fiske- og skaldyrsprodukter i årene 2020 til 2024. 
                    Medianen for profit ligger nogenlunde ens hvert år, hvilket tyder på, at indtjeningen generelt har været stabil over tid.
                    Variationen i profit er også nogenlunde ens hvert år, hvilket viser, at indtjening ikke har ændret sig markant.
                    Der er dog enkelte afvigelser:
                    * I 2024 og 2022 ses nogle meget lave værdier.
                    * I 2023 ses flere produkter med høj profit.
                    * I 2020 er der lidt flere produkter med lav indtjening end de andre år.
                    Alt i alt viser grafen, at profitniveauet har været stabilt, selvom der indimellem forekommer ekstreme værdier.
                    """)
    if view_option =="Diagram profit pr. sæson":
        
        st.image("media/profit_by_season_boxplot.png", caption="Oversigt over profit fordelt på år",  width=800)
        st.markdown(""" 
                    Dette boksplot viser fordelingen af profit (kr) for fiske- og skaldyrsprodukter fordelt på: vinter, sommer, forår og efterår.
                    Medianen ligger nogenlunde ens på tværs af sæsonerne, hvilket tyder på, at indtjeningen er stabil gennem hele året.
                    Variationen i profit er også ensartet, hvilket viser, at der ikke er store udsving mellem sæsonerne.
                    Der ses dog nogle få afvigelser:
                    * Sommer og forår har lidt flere produkter med høj profit.
                    * Vinter har nogle lave outliers.
                    * Efterår og vinter har en lidt højere median end de andre.
                    Overordnet viser grafen, at profitten er jævnt fordelt hen over året, og at sæsonen ikke har en stor indflydelse på indtjeningen. Ekstreme værdier forekommer, men ændrer ikke det generelle billede af stabil profit.
                    """)
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
        top10 = season_df[['name', 'price_kr', 'profit_kr', 'year']].copy()
        top10['year'] = top10['year'].astype(str)
        top10 = top10.sort_values(by='profit_kr', ascending=False).head(3)
        st.markdown("### De mest profitable produkter pr. pågældende sæson")
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


        # Table
        top10 = year_df[['name', 'price_kr', 'profit_kr', 'year']].copy()
        top10['year'] = top10['year'].astype(str)
        top10 = top10.sort_values(by='profit_kr', ascending=False).head(3)
        st.markdown("### Top 3 mest profitable produkter pr. år")
        st.dataframe(top10.reset_index(drop=True), use_container_width=True)

                            
if selected == "Transportomkostninger":
    st.title("📦 Transportomkostninger gennem tiden")
    st.markdown("""
    I denne sektion kan man se hvordan transportomkostninger påvirker fiske- og skaldyrspriser. 
    Dette giver indblik i, om dyr transport hænger sammen med højere priser, og om dette har ændret sig over tid.
    """)
    st.image("media/freight_charge_vs_price.png", caption="Transportomkostning vs Pris", width=800)
    st.markdown("""
                Diagrammet viser sammenhængen mellem transportomkostninger og prisen på fiske- og skaldyrsprodukter. 
                Der er ikke nogen tydelig tendens, da punkterne er spredt ud over hele grafen.
                Det tyder på, at transportomkostningen ikke har stor eller direkte betydning for prisen, og at andre faktorer sandsynligvis spiller en større rolle.
                """)
    st.subheader("📊 Gennemsnitlig transportomkostning pr. år")

    avg_freight_per_year = df.groupby("year")["freight_charge_kr"].mean().reset_index()
    avg_freight_per_year["year"] = avg_freight_per_year["year"].astype(str)
    avg_freight_per_year.columns = ["År", "Gennemsnitlig transportomkostning (kr)"]
    st.table(avg_freight_per_year)

if selected == "Vægtpris over tid":
    st.title("⚖️ Vægtprisen på skalddyr og fisk over tid")
    st.markdown(""" 
        
    """)
    st.image("media/weight_vs_price.png", width=800)
    st.markdown(""" Diagrammet viser sammenhængen mellem vægten på fiske- og skaldyrsprodukter og deres pris. 
                Generelt gælder det, at jo mere produktet vejer, jo højere er prisen. 
                De fleste produkter følger denne tendens, selvom der er nogle få, der skiller sig ud
                """)
       # Select year
    years = sorted(df['year'].unique())
    selected_year = st.selectbox("Vælg år", years)

    # Filter by year
    year_df = df[df["year"] == selected_year].copy()

    # Reconstruct 'type' from one-hot encoding (if needed)
    if "type_shellfish" in year_df.columns and "type_fish" in year_df.columns:
        year_df["type"] = year_df[["type_shellfish", "type_fish"]].idxmax(axis=1).str.replace("type_", "")
    else:
        st.error("Kolonnerne 'type_shellfish' og 'type_fish' mangler i datasættet.")
        st.stop()

    # Calculate weight price
    year_df["vægtpris_kr_pr_g"] = year_df["price_kr"] / year_df["weight_g"]

    # Group and calculate average
    avg_weight_price = year_df.groupby("type")["vægtpris_kr_pr_g"].mean().reset_index()
    avg_weight_price.columns = ["Type", "Gennemsnitlig vægtpris (kr/g)"]

    # Show table
    st.markdown(f"### Gennemsnitlig vægtpris for {selected_year}")
    st.dataframe(avg_weight_price, use_container_width=True)