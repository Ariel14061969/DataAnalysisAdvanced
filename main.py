# Import libraries

# Import function files
from src.infra.config_app_env import *
from src.infra.manage_app_interface import *
from src.algo.Intra_country_functions import *
from src.algo.Intra_continent_functions import *
from src.algo.Intra_region_functions import *
from src.algo.Inter_Country import *
from src.algo.Inter_Continent import *
from src.algo.Inter_Region import *
from src.algo.Correlation_Matrix import *
from src.algo.Units_Txt import *

# Default values for configurable parameters
row_dropna_threshold_factor = 0.9 # The relation between the number of non empty cells to the total number of cells in a row
plt.rcParams['figure.max_open_warning'] = 30  # Set the limit for warnings on max number of figures ( Default is 20 )

# Configure the Streamlit environment of MyCountry App and run it
set_st_bg('src/infra/streamlit_countries_background.jpg')
#config_st_page()
country_data, country_column_data, country_columns_nan_percentage, country_geo_data = st_ui_start(row_dropna_threshold_factor)
#analysis_type, target_entity = st_user_select_analysis(country_geo_data['countries'],country_geo_data['continents'], country_geo_data['regions'] )
char_exp = units_txt()
domains = char_exp['domain'].unique()
world = gpd.read_file("data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")
world_updated = world.replace('United Republic of Tanzania', 'Tanzania', regex=True)
world_updated = world_updated.replace('Democratic Republic of the Congo', 'Congo (Congo-Brazzaville)', regex=True)
world_updated = world_updated.replace('Republic of the Congo', 'Congo', regex=True)
world_updated = world_updated.replace('Republic of Serbia', 'Serbia', regex=True)
world_updated = world_updated.replace('United States of America', 'United States', regex=True)
NewWorld =  world_updated.merge(country_data, how="left", left_on="SOVEREIGNT", right_on="Country")



st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 3.5 rem; /* Change this value to your preferred size */
    }
    </style>
    """,
    unsafe_allow_html=True,
)
country_tab, continent_tab, region_tab , corr_tab = (
    st.tabs([":rainbow[Country]",":rainbow[Continent]",":rainbow[Region]",":rainbow[Correlation]"]))

plt.gcf().set_figheight(7)

with (country_tab):
    st.markdown("<h3 style='color:white;'><b>Select Country</b></h3>", unsafe_allow_html=True)
    selected_country = st.selectbox("Select Country:", country_geo_data['countries'],label_visibility="collapsed")
    col1, col2 = st.columns(2)

    svg_data = requests.get(country_data.loc[selected_country, 'flag_url']).content

    # Convert vector SVG data into a rasterized PNG byte stream
    png_data = svg.svg2png(bytestring=svg_data)
    img = Image.open(BytesIO(png_data))
    continent_name = country_data.loc[selected_country, 'Continent']
    fig, ax = plt.subplots(figsize=(12, 6))

    cmap = plt.get_cmap('Set3')
    continent_geo = world[world["CONTINENT"] == continent_name]
    continent_geo.plot(ax=ax, color="lightgray", edgecolor="black", linewidth=0.5)
    if continent_name == "Europe":
        ax.set_xlim(-30, 55)
        ax.set_ylim(30, 80)
    elif continent_name == "Oceania":
        ax.set_xlim(100, 200)

    country_geo = continent_geo[continent_geo["SOVEREIGNT"] == selected_country]
    country_geo.plot(ax=ax, color="red", edgecolor="darkgray")

    with col1:
        st.image(img)

    with col2:
        st.pyplot(fig)

    # Run the analysis based on   user's selection

    st.markdown("<h3 style='color:white;'><b>Select country analysis:</b></h3>", unsafe_allow_html=True)
    country_analysis_type = st.selectbox("Select country analysis:", ["Intra", "Inter"],label_visibility='collapsed')
    if country_analysis_type == 'Intra':

        country_row = country_data[country_data.index == selected_country]
        run_intra_country_analysis(country_row, country_column_data['all'] ,NewWorld)
    else:

        st.markdown("<h3 style='color:white;'><b>Select Domain:</b></h3>", unsafe_allow_html=True)
        selected_domain = st.selectbox("Select Domain", domains,key="country",label_visibility='collapsed')

        st.markdown("<h3 style='color:white;'><b>Compare country to:</b></h3>", unsafe_allow_html=True)

        compareTo = st.selectbox("Compare country to :", ["World","Continent","Region"],label_visibility='collapsed')
        col_1, col_2 = st.columns(2)
        figs = inter_country(country_data, selected_country, char_exp, selected_domain, NewWorld,compareTo)
        for i in range(len(figs)):
            fig = figs[i]


            if i % 2 == 0:
                #with col_1:
                    fig.set_figheight(7)
                    st.pyplot(fig)


            else:
                #with col_2:
                    fig.set_figheight(12.6)
                    st.pyplot(fig)



with continent_tab:
    st.markdown("<h3 style='color:white;'><b>Select continent analysis:</b></h3>", unsafe_allow_html=True)
    continent_analysis_type = st.selectbox("Select continent analysis:", ["Intra", "Inter"],label_visibility='collapsed')
    if continent_analysis_type == 'Intra':

        st.markdown("<h3 style='color:white;'><b>Select continent:</b></h3>", unsafe_allow_html=True)
        selected_continent = st.selectbox("Select Continent", country_geo_data['continents'],label_visibility='collapsed')
        df_sorted_continent = country_data[country_data.Continent == selected_continent]
        run_intra_continent_analysis(df_sorted_continent)
    else:
        st.markdown("<h3 style='color:white;'><b>Select Domain:</b></h3>", unsafe_allow_html=True)
        selected_domain = st.selectbox("Select Domain", domains,key="continent",label_visibility='collapsed')
        col1, col2 = st.columns(2)
        figs = inter_continent(country_data,selected_domain,char_exp,NewWorld)
        for i in range(len(figs)):
            fig = figs[i]

            if i % 2 == 0:

                    st.pyplot(fig)
            else:

                    st.pyplot(fig)
with region_tab:
    st.markdown("<h3 style='color:white;'><b>Select region analysis:</b></h3>", unsafe_allow_html=True)
    region_analysis_type = st.selectbox("Select region analysis:", ["Intra", "Inter"],label_visibility='collapsed')
    if region_analysis_type == 'Intra':

        st.markdown("<h3 style='color:white;'><b>Select Region:</b></h3>", unsafe_allow_html=True)

        selected_region = st.selectbox("Select Region", country_geo_data['regions'],label_visibility='collapsed')
        df_sorted_region = country_data[country_data.region == selected_region]
        run_intra_region_analysis(df_sorted_region)
    else:

        st.markdown("<h3 style='color:white;'><b>Select Domain:</b></h3>", unsafe_allow_html=True)
        selected_domain = st.selectbox("Select Domain", domains,key="region",label_visibility='collapsed')
        col1, col2 = st.columns(2)
        figs = inter_region(country_data,selected_domain,char_exp,NewWorld)
        for i in range(len(figs)):
            fig = figs[i]

            if i % 2 == 0:
                #with col1:
                    st.pyplot(fig)
            else:
                #with col2:
                    st.pyplot(fig)

with corr_tab:
    heat_fig , matrix = correlation_matrix(country_data)
    st.pyplot(heat_fig)
    col1, col2 = st.columns(2)
    figs = plot_interesting_correlations(country_data, matrix, 0.8)
    for i in range(len(figs)):
        fig = figs[i]

        if i % 2 == 0:
            with col1:
                st.pyplot(fig)
        else:
            with col2:
                st.pyplot(fig)

# each of the inter... functions return figures handles to be displayed in streamlit.
# inside the functions, we do not call streamlit graphics!


# Describe each of the parameters in the API  and the descriptive statistics of the selected DataFrame on the screen

st.markdown("<div style='color:white; margin-bottom:-20px;'>Description of the numeric variables in the data </div>",unsafe_allow_html=True)
st.markdown("<div style='color:white; margin-bottom:0px;'>---------------------------------------------------------------</div>",unsafe_allow_html=True)
st.dataframe(char_exp)

# Print the descriptive statistics of the selected DataFrame on the screen
st.markdown("<div style='color:white; margin-bottom:-20px;'>Descriptive statistics table of the data </div>",unsafe_allow_html=True)
st.markdown("<div style='color:white; margin-bottom:0px;'>--------------------------------------------------</div>",unsafe_allow_html=True)
#st.dataframe(country_data.describe())

# End of main code
