# Import libraries
from src.algo.libs_and_modules import *

def inter_region(country_data,selected_domain,char_exp,world):

    # Lior Sinay 10/09/26 - Put in comment. Reading * from libs and modules instead
    #import seaborn as sns
    #import statistics as stt
    #import matplotlib.pyplot as plt
    figs = []
    df = country_data
    vars = char_exp['var']
    for i in range(len(vars)):
        vars[i]=vars[i].replace(' ','_')
    exclude_col = ["gdp","rel","population","surface_area"]

    DivideByPop = ['tourists','area','co2_emissions','imports','exports','refugees']

    for col in df.keys():
        temp_check = char_exp.loc[vars == col, 'domain']
        if not temp_check.empty:
            check = char_exp.loc[vars == col, 'domain'].item() == selected_domain
        else:
            check = False
        if col not in exclude_col and  isinstance(df.loc[df.index[0],col],float) and check:
            grouped_df = df.groupby('region')[col].mean()


            fig, ax = plt.subplots()


            lb = col
            if col in DivideByPop:
                df['rel']= df[col]/df['population']
                lb = lb + ' per capita'


            sns.barplot(x=grouped_df, y=grouped_df.index, ax=ax)

            max_val = max(bar.get_width() for bar in ax.patches)
            min_val = min(bar.get_width() for bar in ax.patches)
            # 3. Highlight the bar that matches the maximum width
            for bar in ax.patches:
                if bar.get_width() == max_val:
                    bar.set_facecolor('green')  # Highlight color
                if bar.get_width() == min_val:
                    bar.set_facecolor('red')  # Highlight color

            ax.set_xlabel(lb, fontsize=12)
            ax.set_ylabel("")
            ax.tick_params(axis='both', labelsize=12)

            figs.append(fig)
            world['avg_col'] = world.groupby('region')[col].transform('mean')
            fig1, ax1 = plt.subplots()
            world.plot(
                ax=ax1,
                column='avg_col',
                cmap='inferno',
                legend=True,
                edgecolor='black',
                linewidth=0.2,
            )
            ax1.set_xlabel(col, fontsize=20)
            ax1.set_ylabel('')
            figs.append(fig1)

    return figs
