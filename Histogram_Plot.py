# -*- coding: utf-8 -*-
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define CSV File
file_path = 'Hasil_Join.csv'

# Read the CSV file using Pandas
table_penjualan = pd.read_csv(file_path)

pd.set_option('display.max_rows', 10) # Show all columns
pd.set_option('display.max_columns', None) # Show all columns
pd.set_option('display.expand_frame_repr', False)  # Don't wrap the DataFrame to multiple lines

#Handling Missing Values
table_penjualan.isna().sum()
table_penjualan_cleaned = table_penjualan.dropna(subset=['product_category_name'])
table_penjualan_v2 = table_penjualan_cleaned.dropna(subset=['product_category_name_english'])
table_penjualan_v2

#Handling Duplicate
table_clean_duplicate = table_penjualan_v2.duplicated(subset=['order_id'], keep='last')
table_clean_dup = table_penjualan_v2[~table_clean_duplicate]
table_clean_dup

#Handling Inconsistent Data
table_clean_dup['product_category_name_english'].unique()

#Mapping Data Inconsistent
map_inkonsistent ={
    'small_appliances_home_oven_and_coffee' : 'small_appliances',
    'home_appliances_2' : 'home_appliances',
    'home_comfort_2' : 'home_comfort',
    'home_confort' : 'home_comfort'
}
#Replace Data Mapping

table_clean_dup['product_category_name_english'].replace(map_inkonsistent)
table_clean_dup

#Showing Histogram
plt.figure(figsize=(16, 8))
sns.histplot(data=table_clean_dup,x='product_category_name_english')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.xlabel('Product Category', fontsize=10)  # Adjust the fontsize as needed
plt.ylabel('Jumlah', fontsize=10)  # Adjust the fontsize as needed
plt.title('Jumlah Penjualan Product', fontsize=12)

# Menampilkan Penjualan Tertinggi

category_counts = table_clean_dup['product_category_name_english'].value_counts()
quartiles = category_counts.quantile([0.25])
df_counts = pd.DataFrame({'Product Category': category_counts.index, 'Frequency': category_counts.values})
df_counts = df_counts.sort_values(by='Frequency')
max_bin_value = df_counts['Frequency'].max()
max_bin_category = df_counts.loc[df_counts['Frequency'].idxmax(), 'Product Category']
plt.axvline(x=max_bin_category, color='red', linestyle='--', label=f'Highest Count: {max_bin_category}')

# Menampilkan Jumlah Product Yang Paling Banyak Dijual
plt.annotate(f'Highest Count: {max_bin_category} ({max_bin_value})',
             xy=(max_bin_category, max_bin_value),
             xytext=(max_bin_category, max_bin_value + 10),
             ha='left', color='red')

# Handling Outliers

print("Quartile 25% (Q1):", quartiles.loc[0.25])

#Showing Outliers as Insight to Products
for quartile in quartiles:
    plt.axhline(y=quartile, color='red', linestyle='--', label=f'Quartile: {quartile:.2f}')

plt.legend()
plt.show()
