# I) Adding Library And Package

import pandas
import numpy



# II) Loading Dataset

dataset = pandas.read_csv('rafsanjan.csv')



# III) Data Cleaning
# A) Changing Format
# The 'review_count' row encapsulates numeric values within parentheses '()' that need
# to be removed using regular expressions (regex), followed by a conversion to a float data type.

dataset['review_count'] = dataset['review_count'].str.replace(r'\D', '', regex=True)
dataset['review_count'] = dataset['review_count'].astype(float)



# B) Removing The Outliers
# Within the context of adding restaurants to the database, a verification process is conducted. 
# Specifically, it involves examining the geographical information associated with these restaurants 
# to determine if the location contains 'Kerman.' If it does not meet this criterion, the respective 
# entry is subject to deletion.

contains_kerman = dataset['location'].str.contains('Kerman', case=False, na=False)
dataset = dataset[contains_kerman]



# C) Handling Missing Values
# In the context of filling missing data within the attributes related to ratings and review counts, 
# the procedure involves populating these gaps with the numerical value '0.'

dataset.isnull().sum()
dataset.rate.fillna(0, inplace=True)
dataset.review_count.fillna(0, inplace=True)



# D) Removing Duplicates

duplicate_columns = dataset.columns[dataset.nunique() == 1].tolist()
dataset = dataset.drop(columns=duplicate_columns)



# IV) Data Analysis
# A) Calculating the average rating of all restaurants, sum the total number of reviews 
# for all restaurants and average number of reviews per restaurant.

total_metrics = pandas.DataFrame()
totals = ['Average_Rating', 'Total_Reviews', 'Average Review Count']
value = [dataset.rate.mean(), dataset.review_count.sum(), dataset.review_count.mean()]
total_metrics = total_metrics.assign(Totals=totals, Values=value)



# B)  Calculating 1. the number of restaurants for each restaurant type 
#                 2. average rating for each type of restaurant
#                 3. Sum the total number of reviews for each type of restaurant 
#                 4. the average number of reviews per restaurant type.

# 1.

metrics_by_type = pandas.DataFrame()
restaurant_type_counts = dataset['type'].value_counts()
metrics_by_type = pandas.DataFrame({'Restaurant_Type': restaurant_type_counts.index, 'Frequency': restaurant_type_counts.values})

# 2.

average_ratings = dataset.groupby('type')['rate'].mean().reset_index()
average_ratings.columns = ['Restaurant_Type', 'Average_Rating']
metrics_by_type = pandas.merge(average_ratings, metrics_by_type, on='Restaurant_Type')

# 3.

total_review = dataset.groupby('type')['review_count'].sum().reset_index()
total_review.columns = ['Restaurant_Type', 'Total_Review']
metrics_by_type = pandas.merge(total_review, metrics_by_type, on='Restaurant_Type')

# 4.

average_review = dataset.groupby('type')['review_count'].mean().reset_index()
average_review.columns = ['Restaurant_Type', 'Average_Review']
metrics_by_type = pandas.merge(average_review, metrics_by_type, on='Restaurant_Type')

# C) A composite metric that considers both the rating and review count to assess 
# overall customer satisfaction. using this formula
# CSS = ((Rating * Review Count) / Max(Review Count)) * 100

dataset['CSS'] = ((dataset['rate'] * dataset['review_count']) / (total_metrics.loc[total_metrics['Totals'] == 'Total_Reviews', 'Values'].values[0])) * 100




# D) Classification
# Determine the thresholds that will define each category (A to D)
def classify_restaurant(css):
    if css > 70:
        return 'A'
    elif 50 < css <= 70:
        return 'B'
    elif 30 < css <= 50:
        return 'C'
    elif 0 <= css <= 30:
        return 'D'

# Creating a new column in dataset to store the assigned categories (A, B, C, D).

dataset['Classification'] = dataset['CSS'].apply(classify_restaurant)



# V) Adding new datasets to CSV files

dataset.to_csv('Restaurant.csv', index=False)
total_metrics.to_csv('Total.csv', index=False)
metrics_by_type.to_csv('metrics_by_type.csv', index=False)