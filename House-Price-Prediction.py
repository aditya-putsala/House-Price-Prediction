# -*- coding: utf-8 -*-
"""House Price Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19GO2NxeeQdKNcr5g14aw_Z8iG3_hWM3u
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import seaborn as sns

sns.set(rc={'figure.figsize':(15,5)})

from google.colab import drive
drive.mount('/content/drive')

df =  pd.read_csv('/content/drive/MyDrive/Colab Notebooks/House Price Prediction/train-chennai-sale.csv')

df.head()

df.info()

"""# ***Understanding attributes in the data***



1.   PART_Id: unique ID for each house.
2.   AREA: The area where house is located.
3.   INT_SQFT: Total area of the house in square feet.
4.   DATE_SALE: The date in which the house got sold.
5.   DIST_MAINROAD: How many meters the house is far from main road.
6.   N_BEDROOM: Total Number of Bedrooms.
7.   N_BATHROOM: Total Number of bathrooms.
8.   SALE_COND: Sale condition.
9.   PARK_FACIL: Parking facility.
10.  DATE_BUILD: The date in which the house was built. 
11. BUILDTYPE: What type of building.
12. UTILITY_AVAIL: What are the public facilities are available.
13. STREET: Type of street the house is located.
14. MZZONE: What zone the house belongs to. (There are currently 13 zones in Chennai)
15. QS_ROOMS: Masked rooms.
16. QS_BATHROOM: Masked bathrooms.
17. QS_BEDROOM: Masked bedroom.
18. QS_OVERALL: 
19. REG_FEE: Total registration fee.
20. COMMIS: Total commission payed.
21. SALES_PRICE: Sale price of the house


"""

df.describe()

"""

*  The House price in Chennai ranges from 21 lakh to 2 Crore 36 lakh, where, maximum price of house in the dataset is ₹ 23,667,340.00 and minimum price is ₹ 2,156,875.00.
*   The commission price ranges from ₹ 5055 to 5 Lakh.
*   Maximum registration fee is ₹ 983922.00 whereas minimum registration fee ₹ 71177.00.
*   Highest number of room is 6 whereas minimum number of room is 2.
*   Highest number of bedroom is 4 whereas minimum number of bedroom is 1.
*   Highest number of bathroom is 2 whereas minimum number of bathroom is 1.
*   Some houses are completely near to main road whereas some houses are 200 meters away from the main road.
*    The houses in the dataset ranges from 500 to 2500 sq ft.



"""

df = df.drop(columns ='PRT_ID')

"""PART_ID, should be removed , which leads to overfitting."""

df['SALES_PRICE'] = df.SALES_PRICE + df.REG_FEE + df.COMMIS

"""Even though the reg_fee and commision are not useful features, but indirectly affects the sales_price, so we are adding them to sales_price."""

df = df.drop(columns = ['REG_FEE','COMMIS'])
df.head()

df.describe()

"""# ***1. AREA***"""

df["AREA"].isna().sum()

df.AREA.unique()

df["AREA"] = df["AREA"].replace({'Adyr':'Adyar','Ana Nagar':'Anna Nagar','Ann Nagar':'Anna Nagar','Chormpet':'Chrompet','Chrompt':'Chrompet','Chrmpet':'Chrompet','KKNagar':'KK Nagar','Velchery':'Velachery','TNagar':'T Nagar','Karapakam':'Karapakkam'})

df.AREA.unique()

df.AREA.hist(bins = 60 ,figsize = (15,5))
plot.title("Number of Plot Lands in locality",fontsize='large',fontweight='bold')
plot.xticks(rotation=00)

"""Most plot lands are from chrompet and least plots are from T Nagar."""

df.groupby("AREA")["SALES_PRICE"].mean().plot.bar()
plot.title("Mean price in each locality",fontsize='large',fontweight='bold')
plot.xticks(rotation=00)

df.groupby("AREA")["SALES_PRICE"].mean().sort_values().plot.bar()
plot.title("Mean price in each locality",fontsize='large',fontweight='bold')
plot.xticks(rotation=00)

"""The mean house price in the karapakkam is lowest and T Nagar has the highest mean house price. For this categorical column ,in the linear format. so, one hot encoding is best method.

# ***2. BUILDTYPE***
"""

df["BUILDTYPE"].isna().sum()

df["BUILDTYPE"].unique()

df["BUILDTYPE"] = df["BUILDTYPE"].replace({'Comercial':'Commercial','Other':'Others'})

df.BUILDTYPE.value_counts().plot(kind='pie',autopct='%.2f',figsize = (5,5))
plot.title("Type of house")
plot.ylabel("                             ")
plot.show()

df[['BUILDTYPE','SALES_PRICE']].groupby('BUILDTYPE').mean().sort_values('SALES_PRICE')

df[['BUILDTYPE','SALES_PRICE']].groupby('BUILDTYPE').mean().sort_values('SALES_PRICE').plot.bar()
plot.title("Buildtype vs Price")
plot.xticks(rotation=00)

"""*   The commercial type buildings are pricer than house type buildings.
*   one hot encoding should be used.


"""

sns.set_palette('terrain_r')
plot.figure(figsize=(15,5))
sns.kdeplot(data=df, x='SALES_PRICE', hue='BUILDTYPE', shade=True)
plot.title("Variation in sales price as per building type")
plot.show()

"""*   Commercial house types are pricer than others and house type house, but sold less than them.

# ***3. SALE_COND***
"""

df["SALE_COND"].isna().sum()

df.SALE_COND.unique()

df["SALE_COND"] = df["SALE_COND"].replace({'Ab Normal':'AbNormal','Partiall':'Partial','PartiaLl':'Partial','Adj Land':'AdjLand'})

df.SALE_COND.value_counts().plot(kind='pie',autopct='%.2f',figsize = (5,5))
plot.title("Type of sales condition")
plot.ylabel("                             ")
plot.show()

df[['SALE_COND','SALES_PRICE']].groupby('SALE_COND').mean().sort_values('SALES_PRICE')

df[['SALE_COND','SALES_PRICE']].groupby('SALE_COND').mean().sort_values('SALES_PRICE').plot.bar()
plot.title("sales condition vs price")
plot.xticks(rotation=00)

"""

*   Sale condition of house with respect to house price follows a linear trend.
*   Encoding of sale condition column will follow label encoding.

"""

sns.set_palette('terrain_r')
plot.figure(figsize=(15,5))
sns.kdeplot(data=df, x='SALES_PRICE', hue='SALE_COND', shade=True)
plot.title("Variation in sales price as per sales type")
plot.show()

"""*   all the sale_conditions are similar.

# ***4. PARK_FACIL***
"""

df["PARK_FACIL"].isna().sum()

df["PARK_FACIL"].unique()

df["PARK_FACIL"] = df["PARK_FACIL"].replace({'Noo':'No'})

df.PARK_FACIL.value_counts().plot(kind='pie',autopct='%.2f',figsize = (5,5))
plot.title("Parking area availability")
plot.ylabel("                             ")
plot.show()

"""

*   The availability of parking area is approximately half-half.

"""

df[['PARK_FACIL','SALES_PRICE']].groupby('PARK_FACIL').mean().sort_values('SALES_PRICE')

df[['PARK_FACIL','SALES_PRICE']].groupby('PARK_FACIL').mean().sort_values('SALES_PRICE').plot.bar()
plot.title("Parking space availability vs price")
plot.xticks(rotation=00)

"""

*   The mean house price with parking space is higher than house without parking space.

"""

sns.set_palette('terrain_r')
plot.figure(figsize=(15,5))
sns.kdeplot(data=df, x='SALES_PRICE', hue='PARK_FACIL', shade=True)
plot.title("Price difference between house with and without parking space")
plot.show()

"""# ***5. STREET***"""

sns.set_palette('terrain_r')

df["STREET"].isna().sum()

df["STREET"].unique()

df["STREET"] = df["STREET"].replace({'Pavd':'Paved','NoAccess':'No Access'})

df.STREET.value_counts().plot(kind='pie',autopct='%.2f',figsize = (5,5))
plot.title("Street road")
plot.ylabel("                             ")
plot.show()

"""

*   Gravel road and Paved road are having similar houses.
*   No access houses are significant.

"""

df[['STREET','SALES_PRICE']].groupby('STREET').mean().sort_values('SALES_PRICE')

df[['STREET','SALES_PRICE']].groupby('STREET').mean().sort_values('SALES_PRICE').plot.bar()
plot.title("Street road vs price")
plot.xticks(rotation=00)

sns.set_palette('terrain_r')
plot.figure(figsize=(15,5))
sns.kdeplot(data=df, x='SALES_PRICE', hue='STREET', shade=True)
plot.title("Price difference between house with types of street road")
plot.show()

"""# ***6.	UTILITY_AVAIL***"""

df["UTILITY_AVAIL"].isna().sum()

df["UTILITY_AVAIL"].unique()

df["UTILITY_AVAIL"] = df["UTILITY_AVAIL"].replace({'All Pub':'AllPub'})

df.UTILITY_AVAIL.value_counts().plot(kind='pie',autopct='%.2f',figsize = (5,5))
plot.title("Utilities")
plot.ylabel("                             ")
plot.show()

df[['UTILITY_AVAIL','SALES_PRICE']].groupby('UTILITY_AVAIL').mean().sort_values('SALES_PRICE')

df[['UTILITY_AVAIL','SALES_PRICE']].groupby('UTILITY_AVAIL').mean().sort_values('SALES_PRICE').plot.bar()
plot.title("Utilities vs price")
plot.xticks(rotation=00)

"""

*   The utilities are in linear form.

"""

sns.set_palette('terrain_r')
plot.figure(figsize=(15,5))
sns.kdeplot(data=df, x='SALES_PRICE', hue='UTILITY_AVAIL', shade=True)
plot.title("Price difference bY utilities")
plot.show()

"""# ***7. MZZONE***"""

df["MZZONE"].isna().sum()

df["MZZONE"].unique()

df.MZZONE.value_counts().plot(kind='pie',autopct='%.2f',figsize = (5,5))
plot.title("Municipality Zone")
plot.ylabel("                             ")
plot.show()

"""

*  There are houses from 6 municipality zone are present in the dataset.
*  Most number of houses are from RL, RH and RM zone.

"""

df[['MZZONE','SALES_PRICE']].groupby('MZZONE').mean().sort_values('SALES_PRICE')

df[['MZZONE','SALES_PRICE']].groupby('MZZONE').mean().sort_values('SALES_PRICE').plot.bar()
plot.title("Municipality zone vs price")
plot.xticks(rotation=00)

"""

*   Municipality zone is in linear form.
*   House price increases with the municipality zone.
*   RM zone has most expensive houses, whereas A zone has cheapest houses.
"""

sns.set_palette('terrain_r')
plot.figure(figsize=(15,5))
sns.kdeplot(data=df, x='SALES_PRICE', hue='MZZONE', shade=True)
plot.title("Municipality Zone vs Price")
plot.show()

"""*   A,C,I are lowest price in municipality zones.

# ***8. INT_SQFT***
"""

df["INT_SQFT"].values

df["INT_SQFT"].isna().sum()

q3 = df.INT_SQFT.quantile(0.75)
q1 = df.INT_SQFT.quantile(0.25)
iqr = q3 - q1
iqr

q3 + 1.5*iqr

q1 - 1.5*iqr

"""***There are no outliers in this column.***"""

df.INT_SQFT.plot.kde()
plot.title("Distribution in INT_SQFT")
plot.xlabel('INT_SQFT')
plot.show()

"""

*   Non linearly distributed data like the INT_SQFT that doesn't follow a normal distribution need to be transformed.

"""

df.head()

plot.figure(figsize=(15,5))
sns.scatterplot(data=df, x='INT_SQFT', y='SALES_PRICE', hue='AREA', palette='bright')
plot.title("SALES_PRICE Vs INT_SQFT w.r.t AREA")
plot.legend(title='AREA',bbox_to_anchor=(1.05, 1))
plot.show()

"""*  INT_SQFT follows linear relationship with SALES_PRICE in individual level as well as in cumulative level.
*   KK Nagar houses are comparatively bigger in size than houses in other areas.
*   Karapakkam, Adyar has lower size houses.

# ***9. DATE_SALE and DATE_BUILD (AGE and BUILT_YEAR)***

Both the date_sale and date_build are in string format. We have to change in datetimeindex and converted into age of building.
"""

df['AGE'] = pd.DatetimeIndex(df['DATE_SALE']).year - pd.DatetimeIndex(df['DATE_BUILD']).year

df['BUILT_YEAR'] = pd.DatetimeIndex(df['DATE_BUILD']).year

"""No need for date_sale and date_build."""

df['SALE_YEAR'] = pd.DatetimeIndex(df['DATE_SALE']).year

df = df.drop(columns = ['DATE_SALE','DATE_BUILD'])

df.head()

sns.histplot(data=df, x='SALE_YEAR', palette='terrain_r',kde = True)
plot.title("Number of Houses sold per year")
plot.show()

"""All the houses are sold in between 2005 and 2015."""

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='SALE_YEAR', y='SALES_PRICE')
plot.title("Relationship between sale year and sales price")
plot.show()

"""As the sell year versus sales price are in uniform form, it is useless feature."""

df = df.drop(columns ='SALE_YEAR')

df.BUILT_YEAR.describe()

sns.histplot(data=df,x = 'BUILT_YEAR', palette='terrain_r',kde = True)
plot.title("Number of Houses build per year")
plot.show()

"""
*   All the houses are built in between 1949 and 2010.
*   The distribution in number of houses built per year is right skewed.

"""

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='BUILT_YEAR', y='SALES_PRICE')
plot.title("Relationship between built year and sales price")
plot.show()

"""As the built year versus sales price are in linear form"""

sns.histplot(data=df,x = 'AGE', palette='terrain_r',kde = True)
plot.title("Number of Houses as by their age")
plot.show()

"""*   The minimum age of a house is 3 years and maximum age of house is 55 year.

*   What is best way to represent age of house with respect to sales_price?
*   Build_type because it is not effected with age of house.
"""

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='AGE', y='SALES_PRICE')
plot.title("Relationship between built year and sales price")
plot.show()

plot.figure(figsize=(15,5))
ax = sns.lmplot(data=df, x='AGE', y='SALES_PRICE', hue='AREA')

"""

*   As the age increases, the sales_price decreases.

"""

df.head()

"""# ***10. QS_ROOMS, QS_BATHROOM, QS_BEDROOM and QS_OVERALL***"""

df["QS_ROOMS"].isna().sum()

df["QS_BATHROOM"].isna().sum()

df["QS_BEDROOM"].isna().sum()

df["QS_OVERALL"].isna().sum()

"""QS_overall has 48 vacanices."""

df.QS_OVERALL.mean()

df.QS_OVERALL.mode()

df.QS_OVERALL.median()

"""As the mean,mode and median are near to 3.5, I am replacing the missing data with 3.5."""

df['QS_OVERALL'] = df['QS_OVERALL'].replace(np.nan, df.QS_OVERALL.mean().round(3))

df["QS_OVERALL"].isna().sum()  #check

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='QS_ROOMS', y='SALES_PRICE')
plot.title("Relationship between qs_rooms and sales price")
plot.show()

"""QS rooms follows uniform discrete distribution with sales price."""

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='QS_BATHROOM', y='SALES_PRICE')
plot.title("Relationship between qs_bathroom and sales price")
plot.show()

"""QS bathroom follows uniform discrete distribution with sales price."""

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='QS_BEDROOM', y='SALES_PRICE')
plot.title("Relationship between qs_bedroom and sales price")
plot.show()

"""QS bedroom follows uniform discrete distribution with sales price."""

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='QS_OVERALL', y='SALES_PRICE')
plot.title("Relationship between qs_overall and sales price")
plot.show()

"""QS overalll follows uniform discrete distribution with sales price.

*   QS overalll follows uniform discrete distribution with sales price.
*   QS_ROOMS, QS_BATHROOM, QS_BEDROOM and QS_OVERALL are all uniform with respect to sales_price , thus are useless feature. so, we drop them.


"""

df = df.drop(columns = [ 'QS_ROOMS', 'QS_BATHROOM', 'QS_BEDROOM' ,'QS_OVERALL'])

df.head()

"""# ***11. DIST_MAINROAD***"""

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='DIST_MAINROAD', y='SALES_PRICE')
plot.title("Relationship between distance from main road and sales price")
plot.show()

"""In general, the furthur house from main road, the price decreases.

*   But , the distance from main road is uniform with respect to sales price, which makes it useless feature.

"""

df = df.drop(columns = 'DIST_MAINROAD')

df.head()

"""# ***12. N_BEDROOM, N_BATHROOM and N_ROOM***

*   Given the N_BEDROOM and N_BATHROOM are in float64, but 1.5 room doesn't makes sense . It should be in int.
"""

df['N_BEDROOM'].isna().sum()

df.N_BEDROOM.mean()

df.N_BEDROOM.mode()

df.N_BEDROOM.median()

df['N_BEDROOM'] = df['N_BEDROOM'].replace(np.nan, df.N_BEDROOM.mode().values[0])

"""We are filling the missing data in N_BEDROOM with mode."""

df['N_BATHROOM'].isna().sum()

df.N_BATHROOM.mean()

df.N_BATHROOM.mode()

df.N_BATHROOM.median()

"""We are filling the missing data in N_BATHROOM with mode."""

df['N_BATHROOM'] = df['N_BATHROOM'].replace(np.nan, df.N_BATHROOM.mode().values[0])

df['N_BEDROOM'] = df.N_BEDROOM.apply(int)
df['N_BATHROOM'] = df.N_BATHROOM.apply(int)

df.info()

sns.set_palette('terrain_r')
df.N_ROOM.value_counts().plot(kind='pie', autopct="%.2f")
plot.title("houses with respect to number of rooms")
plot.ylabel('')
plot.show()

"""

*   Most are interested in 4 room house.

"""

df[['N_ROOM','SALES_PRICE']].groupby('N_ROOM').mean().sort_values('SALES_PRICE')

df[['N_ROOM','SALES_PRICE']].groupby('N_ROOM').mean().sort_values('SALES_PRICE').plot.bar()
plot.title("Number of rooms vs price")
plot.xticks(rotation=00)

"""

*   As expected, with increase in rooms, the price increases.
"""

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='N_ROOM', y='SALES_PRICE')
plot.title("Relationship between number of rooms and sales price")
plot.show()

"""

*  With increase in room number, house price increase.
*  Follows a linear trend.

"""

sns.set_palette('terrain_r')
df.N_BEDROOM.value_counts().plot(kind='pie', autopct="%.2f")
plot.title("houses with respect to number of BED rooms")
plot.ylabel('')
plot.show()

"""

*   Most people are interested in one bedroom.

"""

df[['N_BEDROOM','SALES_PRICE']].groupby('N_BEDROOM').mean().sort_values('SALES_PRICE')

df[['N_BEDROOM','SALES_PRICE']].groupby('N_BEDROOM').mean().sort_values('SALES_PRICE').plot.bar()
plot.title("Number of bed rooms vs price")
plot.xticks(rotation=00)

"""

*   There is sudden hike in price from one bedrom and two bedroom , three bedroom and four bedrooms.
"""

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='N_BEDROOM', y='SALES_PRICE')
plot.title("Relationship between number of bedrooms and sales price")
plot.show()

sns.set_palette('terrain_r')
df.N_BATHROOM.value_counts().plot(kind='pie', autopct="%.2f")
plot.title("houses with respect to number of bath rooms")
plot.ylabel('')
plot.show()

"""More than 75 percent house has one bedroom , people are prefering the one bathroom."""

df[['N_BATHROOM','SALES_PRICE']].groupby('N_BATHROOM').mean().sort_values('SALES_PRICE')

df[['N_BATHROOM','SALES_PRICE']].groupby('N_BATHROOM').mean().sort_values('SALES_PRICE').plot.bar()
plot.title("Number of bath rooms vs price")
plot.xticks(rotation=00)

"""As usual , the with increase in bathrooms,price increases."""

plot.figure(figsize=(15,5))
sns.regplot(data=df, x='N_BATHROOM', y='SALES_PRICE')
plot.title("Relationship between number of bathrooms and sales price")
plot.show()

"""

*   Follows Linear trend.
"""

df.head()

"""# ***Exploratory Data Analysis***"""

df.corr()

plot.figure(figsize=(15,5))
sns.barplot(x='AREA',y='SALES_PRICE', data=df, hue='PARK_FACIL', palette='terrain_r')
plot.title("Area wise house with parking space or not")
plot.xticks(rotation=00)
plot.show()

"""Almost all the house are split between in having parking space or not."""

plot.figure(figsize=(15,5))
sns.barplot(x='AREA',y='SALES_PRICE', data=df, hue='STREET', palette='bright')
plot.title("Area wise house with which type of road")
plot.xticks(rotation=00)
plot.show()

"""

*   All the houses in KK Nagar has access to road.
*   More houses are connected to gravel roads than paved road.

"""

plot.figure(figsize=(15,5))
sns.barplot(x='AREA',y='SALES_PRICE', data=df, hue='MZZONE', palette='terrain_r')
plot.title("Area wise house with municipality zones")
plot.xticks(rotation=00)
plot.show()

"""

*   Karapakkam, Adyar and Velachery are all areas comes under all municipality zones.
*   some of all areas comes under RM,RL and RH municipality zones.

"""

plot.figure(figsize=(15,5))
sns.barplot(x='AREA',y='SALES_PRICE', data=df, hue='N_ROOM', palette='bright')
plot.title("Area wise house price with respect to number of rooms")
plot.xticks(rotation=00)
plot.show()

"""

*   All the house in Anna Nagar ,Velachery and T Nagar have 5 or 6 rooms.
*   Minimum number of rooms in house are 2 and maximum number of rooms in house are 6.

"""

plot.figure(figsize=(15,5))
sns.barplot(x='AREA',y='SALES_PRICE', data=df, hue='N_BEDROOM', palette='terrain_r')
plot.title("Area wise house price with respect to number of  bedrooms")
plot.xticks(rotation=00)
plot.show()

"""

*   KK Nagar only has range of bedrooms from 1 to 4.
*   Velachery has either two or three bedrooms.
*   Remaining all other areas has one or two bedrooms.

"""

plot.figure(figsize=(15,5))
sns.barplot(x='AREA',y='SALES_PRICE', data=df, hue='N_BATHROOM', palette='bright')
plot.title("Area wise house price with respect to number of  bathrooms")
plot.xticks(rotation=00)
plot.show()

"""*   All the house in Anna Nagar and Chrompet have only one bathroom.
*   Remaining all other areas have both one or two bathrooms.

# ***Encoding***
"""

df.head()

df['AREA'] = df.AREA.map({'Karapakkam': 0, 'Adyar': 1, 'Chrompet': 2, 'Velachery': 3, 'KK Nagar': 4, 'Anna Nagar': 5, 'T Nagar': 6})
df['SALE_COND'] = df.SALE_COND.map({'Partial': 0, 'Family': 1,'AbNormal': 2, 'Normal Sale': 3, 'AdjLand': 4})
df['PARK_FACIL'] = df.PARK_FACIL.map({"No":0,'Yes':1,})
df['UTILITY_AVAIL'] = df.UTILITY_AVAIL.map({'ELO': 0, 'NoSeWa': 1, 'NoSewr ': 2,'AllPub': 3})
df['STREET'] = df.STREET.map({'No Access': 0,'Paved': 1, 'Gravel': 2})
df['MZZONE'] = df.MZZONE.map({'A': 0, 'C': 1, 'I': 2, 'RH': 3, 'RL': 4, 'RM': 5})

df.head()

df = pd.get_dummies(df)

# normalization in INT_SQFT
df['INT_SQFT'] = np.log(df.INT_SQFT)

df.head()

"""# ***Modelling***"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

y = df.SALES_PRICE
X = df.drop(["SALES_PRICE"],axis = 1)
X.shape, y.shape

"""Feature Scaling"""

X_train, X_test, y_train, y_test = train_test_split(X,y, shuffle=True, random_state=47, test_size=0.2)
X_train.shape, y_train.shape, X_test.shape, y_test.shape

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

"""# ***Linear Regression***"""

lr = LinearRegression().fit(X_train, y_train)
y_pred = lr.predict(X_test)

lr_score = metrics.r2_score(y_test, y_pred)
lr_mae = metrics.mean_absolute_error(y_test, y_pred)
print("Linear Regression Training score: {:.2f}".format(lr.score(X_train, y_train)))
print("Linear Regression Test score: {:.2f}".format(lr.score(X_test, y_test)))
print("R2 score: {:.2f}".format(metrics.r2_score(y_test, y_pred)))
print("MSE: {:.2f}".format(metrics.mean_squared_error(y_test, y_pred)))
print("MAE: {:.2f}".format(metrics.mean_absolute_error(y_test, y_pred)))

"""*   Training score and Testing score look good.

**Prediction**
"""

lr_prediction = pd.DataFrame({'actual':y_test, 'predicted':y_pred.flatten() })

lr_prediction.head()

plot.figure(figsize=(15,5))
sns.set_palette('bright')
sns.kdeplot(data=lr_prediction, x='actual', label='actual', shade=True)
sns.kdeplot(data=lr_prediction, x='predicted', label='predicted', shade=True)
plot.title("Actual Price Vs Predicted Price by Linear Regression")
plot.legend()
plot.show()

"""

*   Linear Regression model showing high prices than actual and sometimes low prices than the actual price.
*   This model has 92% r2 score.

"""

lr_coefficient = pd.Series(lr.coef_, index=X.columns.tolist())

plot.figure(figsize=(30, 5))
lr_coefficient.plot(kind='bar',color = 'red')
plot.title("Coefficients of attributes for linear regressor")
plot.xticks(rotation=30)
plot.show()

"""*   By this model, the most important features are number of rooms, buildtype and Area.

# ***KNN Regression***
"""

knn_regressor = KNeighborsRegressor(n_neighbors=3).fit(X_train, y_train)
knn_ypred = knn_regressor.predict(X_test)
knn_score = metrics.r2_score(y_test, knn_ypred)
knn_mae = metrics.mean_absolute_error(y_test, knn_ypred)
knn_mse = metrics.mean_squared_error(y_test,y_pred)
print("KNN regressor train score: {:.2f}".format(knn_regressor.score(X_train, y_train)))
print("KNN regressor test score: {:.2f}".format(knn_regressor.score(X_test, y_test)))
print("KNN r2 score: {:.2f}".format(knn_score))
print("MSE: {:.2f}".format(metrics.mean_squared_error(y_test, y_pred)))
print("MAE: {:.2f}".format(metrics.mean_absolute_error(y_test, y_pred)))

knn_prediction = pd.DataFrame({'actual':y_test, 'predicted': knn_ypred.flatten()})

plot.figure(figsize=(15,5))
sns.set_palette('bright')
sns.kdeplot(data=knn_prediction, x='actual', label='actual', shade=True)
sns.kdeplot(data=knn_prediction, x='predicted', label='predicted',shade=True)
plot.title("Actual Price Vs Predicted Price by KNN Regression")
plot.legend()
plot.show()

"""*   Some predictions are higher than actual price.

# ***Decision Tree Regression***
"""

dt_regressor = DecisionTreeRegressor(max_depth=8).fit(X_train, y_train)
dt_y_predict = dt_regressor.predict(X_test)

dt_score = metrics.r2_score(y_test, dt_y_predict)
dt_mae = metrics.mean_absolute_error(y_test, dt_y_predict)
print("DT Training score: {:.2f}".format(dt_regressor.score(X_train, y_train)))
print("DT Test score: {:.2f}".format(dt_regressor.score(X_test, y_test)))
print("DT R2 score: {:.2f}".format(metrics.r2_score(y_test, dt_y_predict)))
print("DT MSE: {:.2f}".format(metrics.mean_squared_error(y_test, dt_y_predict)))
print("DT MAE: {:.2f}".format(metrics.mean_absolute_error(y_test, dt_y_predict)))

dt_prediction = pd.DataFrame({'actual':y_test, 'predicted': dt_y_predict.flatten()})

plot.figure(figsize=(15,5))
sns.kdeplot(data=dt_prediction, x='actual', label='actual', shade=True)
sns.kdeplot(data=dt_prediction, x='predicted', label='predicted',shade=True)
plot.title("Actual Price Vs Predicted Price by Decision Tree Regressor")
plot.legend()
plot.show()

"""

*   Decision Tree Regression model better than KNN and Linear regression model.
*   This model is more accurate with high r2 score.
"""

dt_coefficient = pd.Series(dt_regressor.feature_importances_, index=X.columns.tolist())

plot.figure(figsize=(30, 5))
dt_coefficient.plot(kind='bar')
dt_coefficient.plot(kind='bar',color = 'red')
plot.title("Coefficients of attributes in Decision Tree Regressor")
plot.legend()
plot.xticks(rotation=30)
plot.show()

"""*   The Area is the most important feature.

# ***Random Forest Regression***
"""

rf_regressor = RandomForestRegressor(random_state=0).fit(X_train, y_train)
rf_y_predict = rf_regressor.predict(X_test)

rf_score = metrics.r2_score(y_test, rf_y_predict)
rf_mae = metrics.mean_absolute_error(y_test, rf_y_predict)

print("RF Training score: {:.2f}".format(rf_regressor.score(X_train, y_train)))
print("RF Test score: {:.2f}".format(rf_regressor.score(X_test, y_test)))
print("RF R2 score: {:.2f}".format(metrics.r2_score(y_test, rf_y_predict)))
print("RF MSE: {:.2f}".format(metrics.mean_squared_error(y_test, rf_y_predict)))
print("RF MAE: {:.2f}".format(metrics.mean_absolute_error(y_test, rf_y_predict)))

"""

*   Random forest regression has the most r2 score than decision tree regression.

"""

rf_prediction = pd.DataFrame({ 'actual':y_test, 'predicted': rf_y_predict.flatten()})

plot.figure(figsize=(15,5))
sns.kdeplot(data=rf_prediction, x='actual', label='actual', shade=True)
sns.kdeplot(data=rf_prediction, x='predicted', label='predicted',shade=True)
plot.title("Actual Price Vs Predicted Price by RF Regressor")
plot.legend()

plot.show()

rf_coefficient = pd.Series(rf_regressor.feature_importances_, index=X.columns.tolist())

plot.figure(figsize=(30, 4))
rf_coefficient.plot(kind='bar',color="green")
plot.title("Coefficients of attributes in RF Regressor")
plot.xticks(rotation=30)
plot.legend()
plot.show()

"""*   The coefficients are same as Decision tree coefficients.

# ***Comparision***
"""

models_df = pd.DataFrame({
    'model': "Linear KNN Decision_Tree Random_Forest".split(),
    'r2_score': [lr_score,knn_score, dt_score, rf_score],
    'mae': [lr_mae, knn_mae, dt_mae, rf_mae]
})

models_df

fig, ax = plot.subplots(nrows=1, ncols=2, figsize=(20,5))
fig.suptitle("Regression Model Comparision")
ax[0].plot(models_df.model, models_df.r2_score, color='green')
ax[0].set_title("R^2")
ax[1].plot(models_df.model, models_df.mae, color='blue')
ax[1].set_title("Mean Absolute Error")
plot.show()

"""*   ***Random Forest has best R2 score along with mean absolute error followed by Decision tree model.***

# ***Summary***

*  *All the houses are from seven areas which ar Karapakkam, Anna Nagar,Adyar,Chrompet, KK Nagar, T Nagar and Velachery.*
*   *Given the house are all built in between 1949 to 2010.*
*  *All the houses are sold in between 2004 to 2014.*
*   *Highest number of houses were sold in 2010-11. Houses are ranges in between rupees 20 Lakh to more than 2 Crore.*
*   *More number of houses were sold in Chrompet and Karapakkam. Most of these houses have single bedroom and of lower price than houses in T Nagar and Anna Nagar.*
* *In Karapakkam the streets have limited or no access, which causes the house price to drop.*
* *Houses near to Gravel type of street come with highest price, followed by paved roads.*
*  *Streets with no access gets less value.*
*  *The building type and available utilities effects the house price.*
*  *The most important feature for the random forest regression is in which area the house is located.*
*  *Random Forest is a better model with a coefficient of determination of 98% and mean absolute error as minimum as. Better than rest of the regression models.*
"""