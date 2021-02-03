# dailycovid - Easily get covid updates

# Pypi installation
`pip3 install dailycovid`

# Usage


## Simplest

`dailycovid -s statecode`

## Specific Counties in a State or Whole States

You can now use an arbitrary number of arguments with `-s` or `-sc`.

`dailycovid -sc ny-albany ca-orange "California-Los Angeles"`

`dailycovid -s DELAWARE MA`


Here are three ways to do the same thing.

`dailycovid -sc "California-Los Angeles"`

`dailycovid -s CA -c "Los Angeles"`

`dailycovid --state CA --county "Los Angeles"`

## Making Plots

Use `--plot` or `-p` to make the plots.

## Updating Data

On the first run it will download a csv file containing the most recent data.

Use `dailycovid -g` to update the cache.


# Initial Execution Video

[Full resolution video.](https://streamable.com/j3occ7)



# Examples of plots

'![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_LOS-ANGELES_CA.png)'

![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_SUFFOLK_MA.png)   

![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_NEW-YORK-CITY_NY.png)
