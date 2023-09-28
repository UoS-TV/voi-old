import pandas as pd

df = pd.read_csv('User Selection List.csv').query('Active == "Yes"')

df2 = df[(df["Year 1"]!="No")|(df["Year 2"]!="No")|(df["Year 4"]!="No")].replace(to_replace=['Yes', 'No'], value=['\checkmark', ''])

stock = df2.query('`Asset Type` == 0')[['Category','Asset Name','Asset Description','Year 1','Year 2','Year 4']].sort_values(by=['Year 1','Year 2','Year 4','Asset Name'],ascending=[False,False,False,True])
rooms = df2.query('`Asset Type` == 1')[['Category','Asset Name','Year 1','Year 2','Year 4']].sort_values(by=['Category','Year 1','Year 2','Year 4','Asset Name'],ascending=[True,False,False,False,True])

print(stock)

for col in stock.columns:
    stock[col] = stock[col].str.replace('&','{\&}')
    stock[col] = stock[col].str.replace('#','{\#}')

# Search through the categories for microphones, if there is a match, ignore case, ignore NaNs and replace with just 'Microphones'
stock.loc[stock['Category'].str.contains('microphone', case=False, na=False), 'Category'] = 'Microphones'

# Group the data by category
groups = stock.groupby('Category')

# print(groups)

# Create a dictionary of DataFrames
dfs = {name: group for name, group in groups}

# Remove category column
for df in dfs.values():
    df.drop(['Category'],inplace=True,axis=1)

# print(dfs)

with open('stock.tex', 'w', encoding='utf-8') as file:
    file.write('')

with open('stock.tex', 'a', encoding='utf-8') as file:
    for i in dfs:
        print(i)
        latex = dfs[i].to_latex(index=False,longtable=True,column_format="p{0.25\\textwidth}p{0.4\\textwidth}ccc",caption=i,na_rep="")
        print(latex)
        file.write(latex)
     


# stock_latex = stock.to_latex(index=False,longtable=True,column_format="p{0.3\\textwidth}p{0.3\\textwidth}ccc")
rooms_latex = rooms.to_latex(index=False,longtable=True,column_format="p{0.2\\textwidth}p{0.4\\textwidth}ccc",caption="Rooms")


# print(df)
# print("STOCK:")
# print(stock)
# print("ROOMS:")
# print(rooms)

# print(stock_latex)
# with open('stock.tex', 'w') as tf:
#      tf.write(stock_latex)

# print(rooms_latex)
with open('rooms.tex', 'w') as tf:
     tf.write(rooms_latex)