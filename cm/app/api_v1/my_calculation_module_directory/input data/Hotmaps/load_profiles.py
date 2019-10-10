# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 16:41:56 2019

This script provides some functions for the Load Profiles Data Set
@author: hasani
"""

#% import modules
import pandas as pd, numpy as np,seaborn as sns,matplotlib.pyplot as plt
from pathlib import Path
import os,sys,glob,pickle,json
sns.set()
#% Paths
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR.joinpath("LOAD PROFILES")
#% Global Variables  
# manually adapt the urls when datasets change
urls = dict(
        residential_sector = dict(
                hot_water = "https://gitlab.com/hotmaps/load_profile/load_profile_residential_shw_yearlong_2010/raw/master/data/hotmaps_task_2.7_load_profile_residential_shw_yearlong_2010.csv",
                space_heating = "https://gitlab.com/hotmaps/load_profile/load_profile_residential_heating_yearlong_2010/raw/master/data/hotmaps_task_2.7_load_profile_residential_heating_yearlong_2010.csv"
                )
        ,
        service_sector = dict(
                space_heating = "https://gitlab.com/hotmaps/load_profile/load_profile_tertiary_heating_yearlong_2010/raw/master/data/hotmaps_task_2.7_load_profile_tertiary_heating_yearlong_2010.csv",
                hot_water = "https://gitlab.com/hotmaps/load_profile/load_profile_tertiary_shw_yearlong_2010/raw/master/data/hotmaps_task_2.7_load_profile_tertiary_shw_yearlong_2010.csv"
                )
        )

#% Functions
def normalize_and_save(data,path):
    data["load"] /= sum(data["load"])
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path,index=False)
    return data

def save(data,typ,foldername,output_path):
    df = pd.read_csv(data[typ])
    for nuts2_code, data in df.groupby(["NUTS2_code"]):
        print(nuts2_code)
        path = output_path.joinpath(foldername,typ,f"{nuts2_code}.csv")
        normalize_and_save(data.copy(),path)

def summary(urls,path=DB_DIR):
    report =  {sector:{typ:[entry.stem for entry in path.joinpath(sector,typ).iterdir() if entry.is_file()]  for typ,_ in data.items()} for sector,data in urls.items() }
    report2 = {sector:{"total":list(sorted(set([item for sublist in [liste for typ,liste in dictionary.items()] for item in sublist])))} for sector,dictionary in report.items()}
    for sector in list(report):
        report[sector] = {**report[sector],**report2[sector]}
    
    with path.joinpath("summary.json").open("w") as fp:
        json.dump(report,fp,indent=4, sort_keys=True)
    
    return report 
            
def create_structure(urls=urls,output_path=DB_DIR):
    for foldername,data in urls.items():
        save(data,"hot_water",foldername,output_path)
        save(data,"space_heating",foldername,output_path)
    
    return summary(urls,output_path)


def get_profile(nuts_code,sector,typ,input_path=DB_DIR):
    return pd.read_csv(input_path.joinpath(sector,typ,f"{nuts_code}.csv")).load.values

def get_peaks(nuts_code,sector,input_path=DB_DIR):
    sh = get_profile(nuts_code,sector,"space_heating",input_path=input_path)
    hw = get_profile(nuts_code,sector,"hot_water",input_path=input_path)
    arg_max_sh = sh.argmax()
    f_sh = sh[arg_max_sh] 
    f_hw = hw[arg_max_sh]
    return f_sh,f_hw

def get_abs_profile(nuts_code,residential_sh,residential_hw,service_sh,service_hw,input_path=DB_DIR,output_path=None):
    sh_residential = get_profile(nuts_code,"residential_sector","space_heating",input_path=input_path) * residential_sh
    hw_residential = get_profile(nuts_code,"residential_sector","hot_water",input_path=input_path) * residential_hw
    sh_service = get_profile(nuts_code,"service_sector","space_heating",input_path=input_path) * service_sh
    hw_service = get_profile(nuts_code,"service_sector","hot_water",input_path=input_path) * service_hw
    
    tot = sh_residential + hw_residential + sh_service + hw_service
    sh = sh_residential + sh_service
    hw = hw_residential + hw_service
    
    df = pd.DataFrame({"total":tot,     
                      "space_heating":sh,
                      "hot_water":hw,
                      "space_heating_rel":sh/tot,
                      "hot_water_rel":hw/tot,
                      "residential_space_heating":sh_residential,
                      "residential_hot_water":hw_residential,
                      "service_space_heating":sh_service,
                      "service_hot_water":hw_service,
                      "residential_space_heating_rel":sh_residential/tot,
                      "residential_hot_water_rel":hw_residential/tot,
                      "service_space_heating_rel":sh_service/tot,
                      "service_hot_water_rel":hw_service/tot,
                      })
    if type(output_path) == type(None):
        return df
    else:
        df.to_csv(output_path,index=False)
        return df

def set_space_heating_savings(sav,df,abs_profile=None):
    if type(abs_profile) != type(None):
        factor = (df.loc[:,"space_heating_rel"]*(1-sav) + df.loc[:,"hot_water_rel"]).values
        y = abs_profile * factor
    else:
        y = (df.loc[:,"space_heating"]*(1-sav) + df.loc[:,"hot_water"]).values
    return y   

def duration_curve_with_savings(df,gesamt=1,abs_profile=None):
    data= {}
    data2_normed= {}
    fig,(ax,ax2) = plt.subplots(2,1)
    for sav in range(0,110,10):
        sav /= 100
        y=set_space_heating_savings(sav,df,abs_profile)
        y2 = y/sum(y) * gesamt 
        y2=np.sort(y2)[::-1]
        y.sort()
        y = y[::-1]
        
        data[f"{str(int(sav*100)).zfill(3)}%"]=y
        data2_normed[f"{str(int(sav*100)).zfill(3)}%"]=y2
        
        ax.plot(range(8760),y,label=f"savings={round(sav,2)*100} & Total Demand={round(sum(y)*1e-3,2)}GWh & Peak: {round(max(y),2)}MW")
        ax2.plot(range(8760),y2,label=f"savings={round(sav,2)*100} & Total Demand={round(sum(y2)) if gesamt==1 else round(sum(y2)*1e-3,2)} {'GWh' if gesamt!=1 else ''} & Peak: {round(max(y2)*1e6,2) if gesamt == 1 else round(max(y2),2)}{'MW' if gesamt!=1 else ''}")
    
    ax.legend()
    ax2.legend()    
    fig.show()
    return fig,pd.DataFrame(data),pd.DataFrame(data2_normed)


def main():
    if not DB_DIR.exists():
        print("Downloading Files from Gitlab, Please be patient....")
        summary = create_structure()
    f_sh,f_hw=get_peaks("DE71","residential_sector")
    df = get_abs_profile(nuts_code="DE71",residential_sh=2808e3,residential_hw=381e3,service_sh=3536e3,service_hw=125e3)
    fig,data,data_normed = duration_curve_with_savings(df)
    return df
#% Main 
if __name__ == "__main__":
    df = main()
