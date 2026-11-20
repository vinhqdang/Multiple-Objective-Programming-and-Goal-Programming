import requests, pandas as pd
IND = {"SE.XPD.TOTL.GD.ZS":"edu_exp_gdp","SH.XPD.GHED.GD.ZS":"health_exp_gdp","SP.DYN.LE00.IN":"life_exp",
       "SH.DYN.MORT":"u5_mort","SE.SEC.ENRR":"sec_enrol","SE.PRM.CMPT.ZS":"prim_compl",
       "NY.GDP.PCAP.PP.KD":"gdp_pc_ppp","SP.POP.TOTL":"pop","SP.URB.TOTL.IN.ZS":"urban","SP.POP.DPND":"dependency"}
frames=[]
for code,name in IND.items():
    r=requests.get(f"https://api.worldbank.org/v2/country/all/indicator/{code}",params=dict(format="json",per_page=20000,date="2000:2023"),timeout=120).json()
    d=pd.DataFrame([{"iso3":x["countryiso3code"],"country":x["country"]["value"],"year":int(x["date"]),name:x["value"]} for x in r[1] if x["countryiso3code"]])
    frames.append(d.set_index(["iso3","country","year"]))
    print(name,len(d),d[name].notna().sum())
df=pd.concat(frames,axis=1).reset_index()
df.to_csv("data/worldbank_2000_2023.csv",index=False)
