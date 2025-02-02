import pandas as pd
import numpy as np
df = pd.read_excel('apartmets.xlsx')

df.sort_values("Price per m2")
df[df["Price per m2"]]

# Feature Engineering and Scoring
df['Price'] = pd.to_numeric(df['Price'])
df['Location_Score'] = np.where(df['Adress'].str.contains('Center|Old Town'), 3,
                                np.where(df['Adress'].str.contains('Podgórze|Kazimierz'), 2, 1))
df['Floor_Score'] = np.where(df['Floor'].str.contains('parter|suterena'), 1,
                             np.where(df['Floor'].str.contains('1 piętro'), 2, 3)) #Adjust weights as needed

df['Total_Score'] = df['Location_Score'] * 2 + df['Floor_Score'] + (1/df['Price'])*10**8  # Adjust weights as needed


# Ranking and Selection of Top Offers
df['Rank'] = df['Total_Score'].rank(ascending=False, method='first')
top_offers = df[df['Rank'] <= 20].sort_values('Rank')

top_offers.to_excel("best_20_offers.xlsx", index=False)