# Pre-amble
A lot more data available for your entertainment here: https://archive.ics.uci.edu/ml/datasets.php

This doc contains ideas for the data exploration and pre-processing class. The class largely follows [this video](https://www.youtube.com/watch?v=zVImIQuqjQ0&list=PLzH6n4zXuckpfMu_4Ff8E7Z1behQks5ba&index=5) and the dataset comes from [here](http://flavorsofcacao.com/chocolate_database.html). This has been made pretty and is presented in a more convenient format [here](https://github.com/CompSciALU/BD-pre-proc_tutorial/blob/master/chocolate_data.csv)

Note: the dataset is a tab delimited csv file. **Why do you think tabs were used instead of commas?**.

# Introduction
In this exercise we are going to be exploring a dataset and preparing it for some modelling (machine learning, statistical modelling etc.). We shall call this process pre-processing (the modelling is the actual processing). The reason for cleaning data is because data models expect clean data. Clean data is data that is in it's most dense format i.e. having the most amount of information residing in the least amount of data.
The exercise also uses the Python pandas library to manipulate the data (note that the [source video](https://www.youtube.com/watch?v=zVImIQuqjQ0&list=PLzH6n4zXuckpfMu_4Ff8E7Z1behQks5ba&index=5) uses R instad but does the same thing most of the time.)
Make sure you have python and pandas installed and that you have the dataset csv file loaded in a convenient location on your machine.

## Initial prep
To start off, load the dataset using 
```python
import pandas as pd

data_file = "chocolate_data.csv"
#df is the pandas dataframe. It is the main data structure you use in data pre-processing and exploration
df = pd.read_csv(data_file, sep='\t')
```

See the general structure of the dataset using `df.head(5)`. What do you see at this point?
You can also get a few summary statistics here using `df.describe()`. At this point, you should note that summary statistics are only given on numerical figures. You now note that your dataframe(df) is not treating the cocoa percentage as being numerical.

To convert the Cocoa Percent to a numeric type, you would:
```python
df['Cocoa Percent'] = df['Cocoa Percent'].str.replace('%','')
df['Cocoa Percent'] = pd.to_numeric(df['Cocoa Percent']) #Casts to float. 
```
A Quick note about pandas data types:
> The 2 most important data structures to understand in pandas are the DataFrame and the series. You can think of the DataFrame for the most part as an Excel table with several rows and columns. The rows are numbered(indexed), the columns have headings and you can do all typical operations such as sort, insert, delete etc.<br>
> The Series you can think of as a single column. In fact, you can select and manipulate any column of a DataFrame as a Series. In a series (and also a DataFrame column) all elements have to be of the same data type. The pandas Series also offers support for a time series and is usually ideal for plotting visualisations.




## Summary Statistics
These are grouped into:
* Measures of Central Tendency
	* Mean
	* Mode
	* Median
The measures of central tendency try to give a single number which can replace the entire dataset.
* Measures of Spread
	* Standard Deviation
	* Range
	* Interquartile Range
These try to describe how spread out the dataset is.

We can see these summary statistics using `df.describe()`. This should now inclube summary stats for `Cocoa Percent` as well.

## Missing Values
You might be suprised to learn the number of missing values in various datasets. You would think that the people whose job it is to collect the data have only one job and they couldn't possibly fudge that. There are however several real life events that make cause missing values in a dataset. For instance in patient records patients may sometimes fail to show up for observation, extreme weather conditions may hinder taking time sensitive data at certain times, historical data is usually unavailable during times of war, connectivity issues may cause remotely collected data to be lost in transit etc. Basically, things happen.
Pandas considers the string `NaN` (note the capitalisation) to be a missing value. This word comes from the statement "Not a Number". To check the number of missing values in the dataset, use:
```python
keys = df.keys()	#All the column names
kp_dict = {}

for key in keys:		#Alternatively, for col in df.columns:
	missing_vals = pd.isna(df[key]).sum()	#Count total missing values
	missing_vals_pcent = missing_vals*100/1937	#Bad idea to hardcode total list length
	print("{}=> {}/1937 missing: {}%".format(key,missing_vals, missing_vals_pcent))
	kp_dict[key]= missing_vals_pcent

```
As a rule of thumb, when there is more than 50% of the data for a given column missing, we would usually just drop the entire column. This can be done as:

```python
for key in keys:
	if (pd.isna(df[key]).sum()/1937) > 0.50:
		df = df.drop(key,axis=1)	#Axis =1 means drop column. Axis=0(default) is drop row
```

We do the same thing for the rows at this point. Check how many missing values are in each row. Since this is a very big operation (\~2000 rows), we dont actually print out the number of missing values per row, we instead just find the number of rows with >= 50% missing values. This is done as:
```python
total=0
todrop = []	#Empty list
for row in df.index:
	if ((pd.isna(df.iloc[row]).sum())/8) > 0.49:	#df.iloc, gets a row given an index
		#culprit = df.iloc[row]
		total += 1
		todrop.append(row)

df = df.drop(todrop)
print("There are {} rows with too little data".format(total))

```

After doing all this, we find the number of missing values for each of the columns using `df.shape[0] - df.count(axis=0)`. (Find out what each of the terms in this expression actually is)

At this point, we decide to fill in the missing values with appropriate replacements. Despite the fact that we would normally be expected to do this for all the columns, in this exercise, we shall focus on the numerical columns only i.e. `Cocoa Percent` and `Rating`.

In order to know what to replace the missing values with, it is important to understand the concept of outliers.

### Outliers
Outliers are values that are far away from the mean value of the data. How far is far? Well, you decide. Usually, 2-3 standard deviations or as a factor of the interquartile range. This is usually a decision that requires domain knowledge to make.
To quickly see the distribution of the data, use a box plot. A description of what the pandas box plot means can be found in the [pandas docs](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.boxplot.html) and a more general description of a box plit can be found on [Wikipedia](https://en.wikipedia.org/wiki/Box_plot). Draw box plots for the 2 columns using:
```python
import matplotlib.pyplot as plt

#Problems Gallore
#https://stackoverflow.com/questions/15884075/tkinter-in-a-virtualenv > For Ubuntu (probably unix-like OSes)
#https://stackoverflow.com/questions/45279754/python-install-tkinter-on-virtualenv-on-linux?noredirect=1&lq=1
#https://stackoverflow.com/questions/40457025/box-plot-of-a-pandas-data-frame
bp=df.boxplot(column='Cocoa Percent')	#Requires matplotlib
plt.show() #Actually display the boxplot. This step may cause tremendous headaches!!!
bp2=df.boxplot(column='Rating')
plt.show()

```
Note that this step will likely cause headaches because pandas uses a separate module to actually display the graphics and that rendering engine uses another rendering engine to do the drawing. Both these are configurable and not configured by default. Prepare for headache (Also an opportunity to contribute to open source).

Alternatively, you can plot the 2 on the same axes:
```python
import matplotlib.pyplot as plt

bp=df.boxplot(column=['Cocoa Percent','Rating'])	#Requires matplotlib
plt.show() #Actually display the boxplot. This step may cause tremendous headaches!!!
```
but you will find that this isn't so useful because of the different ranges of the numbers.

Note that from the box plots, it can be seen that for the `rating` column, there are very few outliers. Also, the outliers look like they are logical so we won't replace them. instead, we will fill in the missing values with the average data. This can be done as:
```
#Find this out from the docs
```

For the column `Cocoa Percent`, there are several outliers. The mean is not robust to outliers (see [Wikipedia page on outliers](https://en.wikipedia.org/wiki/Outlier)). As a result, it is wisest to replace the missing values with the median. Do this as:
```
#Find this out from the docs
```

Finally, we discuss:
* Co-relations
* Visualisation
* Scaling and normalisation
* Feature Selection and Dimensionality Reduction

