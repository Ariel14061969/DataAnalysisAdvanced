# Import libraries
from src.algo.libs_and_modules import *

def inter_continent(country_data,selected_domain,char_exp,world):
    #Lior Sinay 10/09/26 - Put in comment,importing * from libs and modules
    #import seaborn as sns
    #import matplotlib.pyplot as plt
    #libs_and_modules
    figs = []
    df = country_data
    exclude_col = ["gdp","rel","population","surface_area"]

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
        if col not in exclude_col and  isinstance(df.loc[df.index[0],col],float) and check:

                #Lior Sinay 10/09/2026 - replaced plt with plt.
                #fig, axes = plt.subplots(2,2,figsize=(12, 6))
            fig, ax = plt.subplots()


            lb = col
            if col in DivideByPop:
                df['rel']= df[col]/df['population']
                sns.barplot(data=df, x='rel',  hue='Continent',ax=ax)
                lb = lb + ' per capita'
                ax.set_xlabel(lb)
            else:
                sns.barplot(data=df, x=col,  hue='Continent',ax=ax)
            ax.legend(loc='lower left',fontsize=7,framealpha=0.3)

            #figs.append(fig)
            world['avg_col'] = world.groupby('CONTINENT')[col].transform('mean')
            fig1, ax1 = plt.subplots()
            world.plot(
                    ax=ax1,
                    column='avg_col',
                    cmap='inferno',
                    legend=True,
                    edgecolor='black',
                    linewidth=0.2,
                )
            ax1.set_xlabel(col,fontsize=20)
            ax1.set_ylabel('')
            figs.append(fig1)
    return figs
