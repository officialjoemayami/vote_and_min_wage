import pandas as pd
import numpy as np


unemp_county = pd.read_csv("dataset/output.csv")
df = pd.read_csv("dataset/mwd.csv", encoding="latin")
pres16 = pd.read_csv("dataset/pres16results.csv")
state_abbv = pd.read_csv("dataset/state_abbv.csv", index_col=0)


act_min_wage = pd.DataFrame()

for name, group in df.groupby("State"):
    if act_min_wage.empty:
        act_min_wage = group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018":name})
    else:
        act_min_wage = act_min_wage.join(group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018":name}))

act_min_wage = act_min_wage.replace(0, np.NaN).dropna(axis=1)

def get_min_wage(year, state):
    try:
        return act_min_wage.loc[year][state]
    except:
        return np.NaN
unemp_county['min_wage'] = list(map(get_min_wage, unemp_county['Year'], unemp_county['State']))
unemp_county[['Rate','min_wage']].corr()
unemp_county[['Rate','min_wage']].cov()

county_2015 = unemp_county[ (unemp_county['Year']==2015) & (unemp_county["Month"]=="February")]
state_abbv_dict = state_abbv.to_dict()['Postal Code']
county_2015['State'] = county_2015['State'].map(state_abbv_dict)
print(len(county_2015))
print(len(pres16))