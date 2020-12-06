# daily-covid

Use the New York Time's covid data to get up to date county info.

Plots daily COVID deltas given a county and a state.

Plots fatality rate over time.

`pip3 install requests matplotlib numpy`

`git clone https://github.com/Fitzy1293/daily-covid.git`

`cd daily-covid`

`python3 nytimes_covid.py -state CA -county "Los Angeles" -getdata`

Now that you have an updated list of us-counties.csv, you don't need to run the `-getdata` argument.

For example you could now do this.

`python3 nytimes_covid.py -state ny -county "new york city"`

# Example

![image](example.png)

![image](plots_los_angeles_california.png)

![image](plots_new_york_city_new_york.png)
