# Polish cars stats

Polish cars stats is a project of web dashboard showing statistics about car offers from otomoto.pl.
Live demo: [polishcarsstats.herokuapp.com](https://polishcarsstats.herokuapp.com)

### Technologies
- Python 3.8
- [Dash](https://dash.plotly.com/) 1.19.0
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) 4.9.3
- [Plotly](https://plotly.com/python/) 4.14.3
- [Pandas](https://pandas.pydata.org/) 1.1.5

### Project Description

- ##### Data scraping
In the data_scraping directory are 2 files to download the data. Firstly urls_scraper.py is used to download offers' urls from the otomoto.pl site. 
After that we can use data_scraper.py to download data for each offer. It collects make, model, generation, engine capacity, mileage etc.
For this part are used beautifulsoup4 and requests libraries.

- ##### Data preprocessing
If data is downloaded we can preprocess it by preprocessing.py. Script deletes unnecessary endings of features, 
replaces some characters and words, changes currencies to PLN etc. This script uses pandas library.

- ##### Dashboard
Dashboard is created using dash framework. There are three subpages: dashboard.py, more_stats.py and model_stats.py.
Dashboard.py shows main statistics and charts, more_stats.py shows more charts like country of origin pie chart or most popular makes and
by model_stats.py you can check pricing and quantity for particular car model and generation.

### License 
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.