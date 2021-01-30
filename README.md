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


# Initial run

![gif](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/ex.gif)


# Examples of plots

![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_LOS-ANGELES_CA.png)

![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_SUFFOLK_MA.png)   

![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_NEW-YORK-CITY_NY.png)
