# financial-tool

Financial tool is a dashboard created with Dash for **2018 RTP financial law revenue**.
- original spreadsheet: \\FILE\dept\Trans\Finance\LRTP Finance\2022 Regional Transportation Plan\Current_Law_Revenue_Tool_Update\Model_Testing_and_Review\Model\July-8-TPB\16_C_RTP_CLR_Tool_Fed_State_No_Gas_July_TPB_County_Breakdown.xlsx
- deep dive slides: X:\Trans\Finance\LRTP Finance\2022 Regional Transportation Plan\Background_Materials\Finance Planning 101\FinanceDeepDive.pptx

### Current features (June 2023):

1. Forecasting scripts for local transit revenue up to 2050
2. Dashboard with 2 tabs 
   - local transit revenue with dropdowns that filter 
(`Revenue Type`, `Transit Agency`,`Dollar Type`,`Format Unit`) and a slider that filters the `Year Range`
   - local transit boardings

### To run dashboard: 

```
python app.py
```


### Planned features

- line chart

### Development Notes

- **preparing data for the app**\
[`create_input_data_2018.py`](https://github.com/psrc/financial-tool/blob/main/scripts/archive_scripts/excel_raw_data_process.ipynb) handles the initial processing from excel data copied from original spreadsheet. 
This notebook is not part of the forecasting script. The processed input data for forecasting is stored in [`scripts/script_data/input_data_2018`](https://github.com/psrc/financial-tool/tree/main/scripts/script_data/input_data_2018). <br> 
The forecasting calculation happens in [`scripts`](https://github.com/psrc/financial-tool/tree/main/scripts). 
The calculated output that is ready for the Dash app is stored in [`app_data`](https://github.com/psrc/financial-tool/tree/main/app_data)

- **code structure**\
   | <br>
   |_ `app_data`: processed output data calculated by `scripts` <br>
   | <br>
   |_ `pages`: each script puts together the components and datatables in a page. A page replaces a tab in the original spreadsheet <br>
   | <br>
   |_ `components`: module components for each page <br>
   &emsp;|<br>
   &emsp;|_`common_components.py`, `common_functions.py`: modules and functions that can be reused across pages are stored here
