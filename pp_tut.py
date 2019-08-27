import matplotlib.pyplot as plt
import pandas as pd

data_file = "chocolate_data.csv"
data_file2 = "test.csv"

df = pd.read_csv(data_file, sep='\t')
print("The DataFrame shape: {}".format(df.shape))

df.describe()

df['Cocoa Percent'] = df['Cocoa Percent'].str.replace('%','')
df['Cocoa Percent'] = pd.to_numeric(df['Cocoa Percent']) #Casts to float. Maybe think of making them all integers

df.describe() #Now includes stats for coca percent

df.tail()
#See that there are 1937 instances

#Check for missing values for each column
pd.isna(df['Bean Type']).head(7)

keys = df.keys()
kp_dict = {}

for key in keys:		#Alternatively, for col in df.columns:
	missing_vals = pd.isna(df[key]).sum()
	missing_vals_pcent = missing_vals*100/1937	#Bad idea to hardcode total list length
	print("{}=> {}/1937 missing: {}%".format(key,missing_vals, missing_vals_pcent))
	kp_dict[key]= missing_vals_pcent

#The entire for loop above is more concisely expressed as df.count()

for key in keys:
	if (pd.isna(df[key]).sum()/1937) > 0.50:
		df = df.drop(key,axis=1)	#Axis =1 means drop column. Axis=0(default) is drop row

#Check number of missing values per row
total=0
todrop = []
for row in df.index:
	if ((pd.isna(df.iloc[row]).sum())/8) > 0.49:
		#culprit = df.iloc[row]
		total += 1
		todrop.append(row)

df = df.drop(todrop)
print("There are {} rows with too little data".format(total))

#Note the missing values for cocoa percent and ratings
df.shape[0]-df.count(axis=0)	#Find the missing values for all columns


#Plot box and whisker plots for both of these (also describe)
#bp=df['Cocoa Percent'].plot.box()	#Requires matplotlib
#bp=df['Cocoa Percent'].plot.box()	#Requires matplotlib
#Problems Gallore
#https://stackoverflow.com/questions/15884075/tkinter-in-a-virtualenv > For Ubuntu (probably unix-like OSes)
#https://stackoverflow.com/questions/45279754/python-install-tkinter-on-virtualenv-on-linux?noredirect=1&lq=1
#https://stackoverflow.com/questions/40457025/box-plot-of-a-pandas-data-frame
bp=df.boxplot(column='Cocoa Percent')	#Requires matplotlib
plt.show() #Actually display the boxplot. This step may cause tremendous headaches!!!
bp2=df.boxplot(column='Rating')
plt.show()
#Decide for each whether to fill in with mean or mode
#For Rating, there are few outliers, therefore use mean
m= df['Rating'].mean()
df['Rating'] = df['Rating'].fillna(m)

#For Cocoa Percent, there are many outliers, therefore replace with median
m= df['Cocoa Percent'].median()
df['Cocoa Percent'] = df['Cocoa Percent'].fillna(m)

#Plot rating histogram to explain why we use the average

#Comment about how missing values can be data in themselves






