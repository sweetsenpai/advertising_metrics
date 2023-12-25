import pandas
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

np.seterr(divide='ignore', invalid='ignore')

data = pandas.read_csv(filepath_or_buffer='test_data.csv').fillna(0)
for col_name in data.columns:
    if col_name not in ['Campaign_id', 'Geo', 'Buyer']:
        try:
            data[col_name] = data[col_name].str.replace(r',', '', regex=True)
            data[col_name] = data[col_name].apply(pandas.to_numeric)
        except AttributeError:
            continue

buyers_list = list(data['Buyer'].unique())
geo_list = data['Geo'].unique()
info_geo = {}
for geo in geo_list:
    info_geo[geo] = {}

for buyer in buyers_list:
    for geo in geo_list:
        impressions = data[(data.Geo == geo) & (data.Buyer == buyer)]['Impressions'].sum()
        clicks = data[(data.Geo == geo) & (data.Buyer == buyer)]['Clicks'].sum()
        spend = data[(data.Geo == geo) & (data.Buyer == buyer)]['Spend'].sum()
        installs = data[(data.Geo == geo) & (data.Buyer == buyer)]['Installs'].sum()
        registration = data[(data.Geo == geo) & (data.Buyer == buyer)]['Registrations'].sum()
        incum = data[(data.Geo == geo) & (data.Buyer == buyer)]['Revenue_ad1d'].sum() + \
                data[(data.Geo == geo) & (data.Buyer == buyer)]['Revenue_in_app1d'].sum() + \
                data[(data.Geo == geo) & (data.Buyer == buyer)]['Revenue_ad7d'].sum() + \
                data[(data.Geo == geo) & (data.Buyer == buyer)]['Revenue_in_app7d'].sum() + \
                data[(data.Geo == geo) & (data.Buyer == buyer)]['Revenue_ad30d'].sum() + \
                data[(data.Geo == geo) & (data.Buyer == buyer)]['Revenue_in_app30d'].sum()

        click_per_imp = round((clicks/impressions) * 100, 2)
        try:
            cost_per_click = round(spend/clicks)
        except ValueError:
            cost_per_click = 0
        instal_procent = round((installs/impressions) * 100, 2)
        reg_per_imp = round((registration/impressions)*100, 2)
        if spend == 0:
            return_on_investment = '-'
        else:
            return_on_investment = incum-spend
        info_geo[geo][buyer] = {'CPI': click_per_imp, 'CPC': cost_per_click, 'IP': instal_procent, 'RPI': reg_per_imp, 'RI': return_on_investment}
