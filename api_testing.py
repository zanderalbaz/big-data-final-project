import requests
import json
import pandas as pd

# https://fiscaldata.treasury.gov/datasets/debt-to-the-penny/debt-to-the-penny

def historic_US_debt_to_csv():
    debt_by_date = {}
    next_link = ""
    while(True):
        response = requests.get('https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?filter=record_date,tot_pub_debt_out_amt&sort=record_date' + next_link)
        data_dict = response.json()
        next_link = data_dict["links"]["next"]
        api_data = data_dict["data"]
        for entry in api_data:
            date = entry["record_date"]
            debt = entry["tot_pub_debt_out_amt"]
            debt_by_date[date] = float(debt)

        if next_link is None:
            break
        print(next_link)

    df = pd.DataFrame([debt_by_date.keys(), debt_by_date.values()]).T
    df.columns = ["Record Date", "Total Public Debt Outstanding"]
    print(df)

    df.to_csv("US_debt.csv", index=False)

def get_yesterdays_debt():
    response = requests.get('https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?filter=record_date,tot_pub_debt_out_amt&sort=-record_date&format=json&page[number]=1&page[size]=1')
    debt = response.json()["data"][0]["tot_pub_debt_out_amt"]
    date = response.json()["data"][0]["record_date"]
    print(date, debt)

if __name__ == "__main__":
    get_yesterdays_debt()
    # historic_US_debt_to_csv()