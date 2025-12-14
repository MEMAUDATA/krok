import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_unique_year(df):
            """ subplot for a unique year """

            def extract_year(df):
                        return df['date'].dt.year.unique()


            def compute_data_per_month(df,agg):
                        """ Take a df and compute sum per month """

                        # Transform data into a period of month
                        df['year_month'] = df['date'].dt.to_period('M')
            
                        if agg == "sum":
                                    monthly_data = df.groupby('year_month')['Total'].sum().reset_index()
                        elif agg == "mean":
                                    monthly_data = df.groupby('year_month')['Total'].mean().reset_index()
            
                        # Rename column
                        monthly_data.columns = ["Month", "Total"]
                        # Change date into month => ex : 2024-01 -> 1
                        monthly_data['month_num'] = monthly_data['Month'].dt.month
                        # Map number to month and replace number to french months
                        months = ["Jan","Fev","Mars","Avr","Mai","Juin","Juil","Aout","Sept","Oct","Nov","Dec"]
                        month_mapping = {i+1: m for i, m in enumerate(months)}
                        # Check that there's 12 months
                        all_months = pd.DataFrame({"month_num": range(1, 13)})
                        # Merge with your monthly_data
                        monthly_data = all_months.merge(monthly_data, on="month_num", how="left")
                        # Map month numbers to names
                        monthly_data['Month'] = monthly_data['month_num'].map(month_mapping)
                        # FillNa
                        monthly_data['Total'] = monthly_data['Total'].fillna(0)
                        # Drop helper column
                        monthly_data = monthly_data.drop('month_num', axis=1)

                        return monthly_data

         

            # Annotation
            def add_info(data,ax):
                        """ Add numbers to the graph """
                        for index, row in data.iterrows(): 
                                    date = row['Month']
                                    value = row['Total']
                                    ax.annotate(f"{value:.2f}", 
                                                (date, value),  
                                                textcoords="offset points",
                                                xytext=(0, 10), ha='center', c="k",
                                                fontsize=9) 

            def find_maxima(df,nb_maxima,ax):
                        """ Detect local maxima """
                        # Detect local maxima
                        is_local_max = (df['Total'] > df['Total'].shift(1)) & (df['Total'] > df['Total'].shift(-1))
                        local_maxima = df[is_local_max]

                        # Look for X maxima
                        top_n_local_maxima = local_maxima.nlargest(nb_maxima, 'Total')

                        # Plot maxima points
                        if not top_n_local_maxima.empty:
                                    ax.scatter(top_n_local_maxima['date'], top_n_local_maxima['Total'],
                                                s=30, c='green', label='Local maxima')

                        for _, row in top_n_local_maxima.iterrows():
                                    ax.annotate(f"{row['Total']} \n({row['date'].strftime('%d-%m')})",
                                                            (row['date'], row['Total']),
                                                            textcoords="offset points",
                                                            xytext=(0, 10), ha='center',
                                                            color="green", fontsize=9)

                                                               


            # Subplot
            fig,axes = plt.subplots(nrows=3, ncols=1,figsize=(12,10), dpi=100)

            # Sum
            data = compute_data_per_month(df,agg="sum")
            axes[0].plot(data["Month"],data["Total"],c='orange',marker='o',markerfacecolor = 'black')
            axes[0].plot(data["Month"],np.tile(data["Total"].mean(),data["Month"].shape[0]),c='r',label = f'Moyenne ({data["Total"].mean():.2f})')
            axes[0].set_ylim((data["Total"].min())-200,8000) 
            add_info(data,axes[0])
            axes[0].legend(loc='lower center',ncol=2,fontsize=9)

          

            # Mean
            data = compute_data_per_month(df,agg="mean")
            axes[1].plot(data["Month"],data["Total"],c='grey',marker='o',markerfacecolor = 'black')
            axes[1].plot(data["Month"],np.tile(data["Total"].mean(),data["Month"].shape[0]),c='r',label = f'Moyenne ({data["Total"].mean():.2f})')
            axes[1].set_ylim((data["Total"].min())-30,(data["Total"].max())+50) 
            add_info(data,axes[1]) 
            axes[1].legend(loc='lower center',ncol=2,fontsize=9) 
             
            # Daily throughout the year
            axes[2].plot(df['date'],df['Total'])
            axes[2].plot(df['date'],np.tile(df['Total'].mean(),df['date'].shape[0]),c='r',label = f'Moyenne ({df["Total"].mean():.2f})')
            axes[2].set_ylim((data["Total"].min())-30,1300) 
            months = ["Jan","Fev","Mars","Avr","Mai","Juin","Juil","Aout","Sept","Oct","Nov","Dec"]
            #axes[2].set_xticklabels(months)
            find_maxima(df,5,axes[2])
            axes[2].legend(loc='upper right',ncol=1,fontsize=9)

       
             
            # extract year
            years = extract_year(df)

            axes[0].set_title(f"{years} - Somme mensuelle", loc='center')
            axes[1].set_title(f"{years} - Moyenne mensuelle", loc='center')
            axes[2].set_title(f"{years} - Activité journalière", loc='center')
            axes[0].set_ylabel('CA [euros]')
            axes[1].set_ylabel('CA [euros]')
            axes[2].set_ylabel('CA [euros]')
            axes[0].grid(True) 
            axes[1].grid(True)
            axes[2].grid(True)  

            # For Streamlit
            return fig

