# Lior Sinay 10/09/26 - placed in comment , importing * from libs and modules
#from statistics import mean

# Import libraries
from src.algo.libs_and_modules import *

def inter_country(country_data,MyCountry,char_exp, selected_domain, world, compareTo='World'):

    # Lior Sinay 10/09/26 - placed in comment , importing * from libs and modules
    #import seaborn as sns
    #import matplotlib.pyplot as plt

    figs=[]
    MyContinent = country_data.loc[MyCountry,'Continent']
    MyRegion = country_data.loc[MyCountry,'region']
    exclude_col = ["gdp","rel","population","surface_area"]



    if compareTo == 'World':
        df=country_data
    elif compareTo == 'Continent':
        df = country_data[country_data['Continent']==MyContinent]
    else: #compareTo == 'Region':
        df = country_data[country_data['region']==MyRegion]

    DivideByPop = ['tourists','area','co2_emissions','imports','exports','refugees']

    vars = char_exp['var']
    for i in range(len(vars)):
        vars[i]=vars[i].replace(' ','_')
    for col in df.keys():

        temp_check = char_exp.loc[vars == col, 'domain']
        if not temp_check.empty:
            check = char_exp.loc[vars == col, 'domain'].item() == selected_domain
        else:
            check = False

        if col not in exclude_col and isinstance(df.loc[MyCountry,col],float) and check:
            lb = col
            df['rel']=df[col]
            if col in DivideByPop:
                df['rel']= df['rel']/df['population']
                lb = lb + ' per capita'



            fig, ax = plt.subplots(figsize=[12,5])

            expl = char_exp[char_exp['var'] == col]['explain']
            sns.histplot(df['rel'].dropna() , bins = 30,ax=ax)
            min_country = df['rel'].idxmin()
            max_country = df['rel'].idxmax()
            median_country = (df['rel'] - df['rel'].median()).abs().idxmin()
            countries_of_interest =[min_country,max_country,median_country]
            ax.set_xlabel(lb,fontsize=20)
            #ax.set_title(expl)
            if df.loc[MyCountry,'rel']:
                max_count = max([bar.get_height() for bar in ax.containers[0]])

                xval = df.loc[MyCountry,'rel']

                ax.vlines(x=xval, ymin=0, ymax=max_count, colors="red", linestyles="dashed", lw=2)
                ax.text(x=xval, y=max_count * 0.75, s=f" {MyCountry}", color="red", rotation=0, va='top',fontsize=20)
                for countryOfInterest in countries_of_interest:
                    xval = df.loc[countryOfInterest, 'rel']
                    ax.vlines(x=xval, ymin=0, ymax=max_count, colors="green", linestyles="dashed", lw=1)
                    ax.text(x=xval, y=max_count , s=f" {countryOfInterest}",  color="green", rotation=45, va='center',fontsize=20)

            figs.append(fig)

            fig1, ax1 = plt.subplots(figsize=[12,8])
            if compareTo == 'World':
                world.plot(
                    ax=ax1,
                    column=col,
                    cmap='inferno',
                    legend=True,
                    edgecolor='black',
                    linewidth=0.2,
                )
                ax1.set_ylabel('')
                ax1.set_xlabel(col, fontsize=20)
            elif compareTo == 'Continent':
                continent = world[world['CONTINENT'] == MyContinent]
                continent.plot(
                    ax=ax1,
                    column=col,
                    cmap='inferno',
                    legend=True,
                    edgecolor='black',
                    linewidth=0.2,
                )
                if MyContinent=='Europe':
                    ax1.set_xlim([-30,50])
                    ax1.set_ylim([30, 80])
                elif MyContinent=='Oceania':
                    ax1.set_xlim([100, 180])
                    ax1.set_ylim([-50, 10])
                ax1.set_ylabel('')
                ax1.set_xlabel(col, fontsize=20)

            else:  # compareTo == 'Region':
                region = world[world['region'] == MyRegion]
                region.plot(
                    ax=ax1,
                    column=col,
                    cmap='inferno',
                    legend=True,
                    edgecolor='black',
                    linewidth=0.2,
                )
                ax1.set_ylabel('')
                ax1.set_xlabel(col, fontsize=20)
            figs.append(fig1)

    return figs