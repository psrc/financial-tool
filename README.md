# financial-tool

Financial tool is a dashboard created with Dash for **2018 RTP financial law revenue**.

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

- ~~aggregate yearly total revenue for each transit agency~~
- line chart

<details>
    <summary>financial-tool structure notes</summary>
    Reference document: <a href="https://community.plotly.com/t/structuring-a-large-dash-application-best-practices-to-follow/62739" target="_blank">Structuring a large Dash application - best practices to follow</a>
   
   Folders
   - assets: css files, javascript files, locally hosted data are stored here
   - components: contain common components used throughout the application
   - utils: for common functions run throughout the application
</details>