import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def combine_plot(list_df):
            """ Combine multiple years within a single plot """

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


            # Subplot
            fig,axes = plt.subplots(nrows=2, ncols=1,figsize=(10, 8), dpi=100)

            year_list = []
            for df in list_df:

                        df_yr = extract_year(df)
                        year_list.append(df_yr[0])
                        # Sum
                        data = compute_data_per_month(df,agg="sum")
                        axes[0].plot(data["Month"],data["Total"],marker='o',markerfacecolor = 'black')

                        # Mean
                        data = compute_data_per_month(df,agg="mean")
                        axes[1].plot(data["Month"],data["Total"],marker='o',markerfacecolor = 'black')

                
            axes[0].set_title("Somme mensuelle", loc='center')
            axes[1].set_title("Moyenne mensuelle", loc='center')
            axes[0].set_ylabel('CA [euros]')
            axes[1].set_ylabel('CA [euros]')
            axes[0].grid(True) 
            axes[1].grid(True)
            axes[1].legend(year_list,loc='lower center',ncol=2,fontsize=9) 

            # For Streamlit
            return fig
