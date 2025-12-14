import pandas as pd
import numpy as np

def synthesis(data):

    """
    Import raw data from xls/csv/xlsx into a dataframe.
    NV, Toulouse, 07/2025

    """
    all_date = []
    all_total = []
    df = pd.DataFrame([])

    for col_index, (col_name,col_data) in enumerate(data.items()):

        if col_index > 0:
            date_col = col_data.iloc[:,0]
            all_date.append(date_col)
            all_total.append(col_data['TOTAL']) 

    combined_date  = pd.concat(all_date,axis=0,sort=False).to_frame(name='date')  
    combined_total = pd.concat(all_total,axis=0,sort=False).to_frame(name='Total')
    df = pd.concat([combined_date,combined_total],axis=1)
    
   

    df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%d/%m/%Y')  # Specify your date format!
    df = df.dropna(subset=['date'])  # Drop rows with invalid dates
    df = df.drop_duplicates(subset=['date'])  # Drop duplicate dates
    df = df.replace(0, np.nan) #Replace 0 with NaN
    df = df.dropna() #Drop NaN
    df = df.reset_index(drop=True)  # Reset the index

    df['Day of Week'] = df['date'].dt.day_name()  # Extract day of the week

   
    # Define weekday order
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Convert to categorical with ordered weekdays
    df['Day of Week'] = pd.Categorical(df['Day of Week'], categories=weekday_order, ordered=True)

    # Group and sort by weekday order
    income_per_day = (
        df.groupby('Day of Week')['Total']
          .agg(['mean', 'std', 'sum'])
          .reindex(weekday_order)   # ensures Monday first
    )

    return income_per_day, df


