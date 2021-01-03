# dailycovid - Easily get covid updates

# Pypi installation
`pip3 install dailycovid`

# Usage


## Simplest

`dailycovid -s statecode`

## Specific Counties in a State

Three ways to do the same thing.

`dailycovid -sc "California-Los Angeles"`

`dailycovid -s CA -c "Los Angeles"`

`dailycovid --state CA --county "Los Angeles"`

## Updating Data

On the first run it will download a csv file containing the most recent data.


Use `dailycovid -g` to update the cache.


# Examples of plots

![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_los-angeles_california.png)

![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_suffolk_massachusetts.png)   

![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_new-york-city_new_york.png)
