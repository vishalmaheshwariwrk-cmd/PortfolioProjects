import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Task 1: Load dataset ---
df = pd.read_csv(r"D:\Everything APU - Study\Personal\Jobs\Personal Projects\AirBnB dataset\Airbnb_Open_Data.csv")

# Display first 5 rows and data types
print(df.head())
print(df.dtypes)

# --- Task 2: Remove unwanted columns safely ---
df.drop(columns=['host id', 'id', 'country', 'country code'], errors='ignore', inplace=True)

# Display first 5 rows after removal
print("\nAfter removing unwanted columns:")
print(df.head())

# --- Task 3: Handle missing values ---
print("\nMissing values per column:")
print(df.isnull().sum().sort_values(ascending=True))

# Impute missing values
for col in df.columns:
    if df[col].isnull().sum() > 0:
        if df[col].dtype in ['float64', 'int64']:
            df[col].fillna(df[col].median(), inplace=True)
        else:
            df[col].fillna('Unknown', inplace=True)

# Verify no missing values remain
print("\nAfter imputation:")
print(df.isnull().sum())

# Remove duplicates
duplicates_before = df.duplicated().sum()
df.drop_duplicates(inplace=True)
duplicates_after = df.duplicated().sum()
print(f"\nDuplicates before: {duplicates_before}, after removal: {duplicates_after}")
print(f"Total records after cleaning: {len(df)}")

# --- Task 4: Rename and standardize columns ---
df.rename(columns={'availability 365': 'days_booked'}, inplace=True)
df.columns = df.columns.str.lower().str.replace(' ', '_')
print("\nColumns after standardization:")
print(df.columns)

# --- Task 4b: Clean financial columns safely ---
if 'price' in df.columns:
    df['price'] = df['price'].replace('[\$,]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

if 'service_fee' in df.columns:
    df['service_fee'] = df['service_fee'].replace('[\$,]', '', regex=True)
    df['service_fee'] = pd.to_numeric(df['service_fee'], errors='coerce')

# Fill any remaining numeric NaNs after conversion
for col in ['price', 'service_fee']:
    if col in df.columns and df[col].isnull().sum() > 0:
        df[col].fillna(df[col].median(), inplace=True)

print("\nFirst 5 rows after cleaning financial columns:")
print(df.head())

# --- Task 5: Analysis ---
# Room type counts
print("\nRoom type counts:")
print(df['room_type'].value_counts())

# Strict cancellation policy analysis
strict_df = df[df['cancellation_policy'] == 'strict']
room_type_counts = strict_df['room_type'].value_counts()
print("\nRoom types under strict cancellation policy:")
print(room_type_counts)
print("\nRoom type with most strict policies:", room_type_counts.idxmax())

# Visualization for strict cancellation policy
room_type_counts.plot(kind='bar', title='Room Types with Strict Cancellation Policy', color='skyblue')
plt.xlabel('Room Type')
plt.ylabel('Count')
plt.show()

# Average price per neighborhood group
avg_price_by_group = df.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False)
print("\nAverage price per neighborhood group:")
print(avg_price_by_group)
print(f"\nMost expensive neighborhood group: {avg_price_by_group.idxmax()} with an average price of ${avg_price_by_group.max():.2f}")

# Visualization for average price
avg_price_by_group.plot(kind='bar', title='Average Price per Neighborhood Group', color='orange')
plt.xlabel('Neighborhood Group')
plt.ylabel('Average Price')
plt.show()

# --- Export cleaned dataset for Tableau ---
output_path = r"D:\Everything APU - Study\Personal\Jobs\Personal Projects\AirBnB dataset\Airbnb_Cleaned.csv"
df.to_csv(output_path, index=False)
print(f"\nCleaned dataset exported successfully to: {output_path}")

# --- Task 6: Analysis ---
# Load the cleaned dataset
df = pd.read_csv(r"D:\Everything APU - Study\Personal\Jobs\Personal Projects\AirBnB dataset\Airbnb_Cleaned.csv")

# -------------------------------
# Step 1: Top 10 Most and Least Expensive Neighborhoods
# Group by neighborhood and calculate average price
avg_price_by_neighborhood = df.groupby('neighbourhood')['price'].mean().sort_values(ascending=False)

# Top 10 most expensive neighborhoods
top10_expensive = avg_price_by_neighborhood.head(10)

# Top 10 least expensive neighborhoods
bottom10_expensive = avg_price_by_neighborhood.tail(10)

# Plot Top 10 Most Expensive Neighborhoods
plt.figure(figsize=(10, 6))
top10_expensive.plot(kind='barh', color='darkred')
plt.title('Top 10 Most Expensive Neighborhoods')
plt.xlabel('Average Price')
plt.ylabel('Neighborhood')
plt.gca().invert_yaxis()  # Highest price at top
plt.tight_layout()
plt.show()

# Plot Top 10 Least Expensive Neighborhoods
plt.figure(figsize=(10, 6))
bottom10_expensive.plot(kind='barh', color='green')
plt.title('Top 10 Least Expensive Neighborhoods')
plt.xlabel('Average Price')
plt.ylabel('Neighborhood')
plt.gca().invert_yaxis()  # Lowest price at top
plt.tight_layout()
plt.show()

# -------------------------------
# Step 2: Box and Whisker Plot for Price Distribution by Room Type
plt.figure(figsize=(10, 6))
sns.boxplot(x='room_type', y='price', data=df)
plt.title('Price Distribution by Room Type')
plt.xlabel('Room Type')
plt.ylabel('Price')
plt.tight_layout()
plt.show()

# --- Task 7: Analysis ---
# Standardize column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Convert numeric columns
df['price'] = pd.to_numeric(df['price'], errors='coerce')
fee_column = 'cleaning_fee' if 'cleaning_fee' in df.columns else 'service_fee'
df[fee_column] = pd.to_numeric(df[fee_column], errors='coerce')

# Drop missing values
df = df.dropna(subset=['price', fee_column])

# Remove extreme outliers
df = df[(df['price'] <= 1000) & (df[fee_column] <= 500)]

# Aggregate by fee
agg_df = df.groupby(fee_column)['price'].mean().reset_index()

# -------------------------------
# Scatter plot with aggregated data
plt.figure(figsize=(10, 6))
sns.scatterplot(x=fee_column, y='price', data=agg_df, color='blue', s=80)
plt.title(f'Average Price vs {fee_column.replace("_", " ").title()}')
plt.xlabel(fee_column.replace("_", " ").title())
plt.ylabel('Average Price')
plt.tight_layout()
plt.show()

# -------------------------------
# Correlation
corr = df[[fee_column, 'price']].corr().iloc[0, 1]
print(f"Correlation between {fee_column} and price: {corr:.2f}")

# -------------------------------
# Line chart for listings per year
if 'last_review' in df.columns:
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
    df['year'] = df['last_review'].dt.year
elif 'construction_year' in df.columns:
    df['year'] = pd.to_numeric(df['construction_year'], errors='coerce')

listings_per_year = df['year'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
plt.plot(listings_per_year.index, listings_per_year.values, marker='o', color='blue')
plt.title('Total Listings Available Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Listings')
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Task 8: Analysis ---
# Standardize column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Convert numeric columns
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['number_of_reviews'] = pd.to_numeric(df['number_of_reviews'], errors='coerce')
df['review_rate_number'] = pd.to_numeric(df['review_rate_number'], errors='coerce')

# Drop rows with missing values in key columns
df = df.dropna(subset=['price', 'number_of_reviews'])

# -------------------------------
# Step 1: Visualization using review column
plt.figure(figsize=(10, 6))
sns.histplot(df['number_of_reviews'], bins=50, color='purple')
plt.title('Distribution of Number of Reviews')
plt.xlabel('Number of Reviews')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# -------------------------------
# Step 2: Compare Superhosts vs Regular Hosts
# Use 'host_identity_verified' as proxy for Superhost status
df['superhost'] = df['host_identity_verified'].apply(lambda x: 'Superhost' if str(x).lower() == 'verified' else 'Regular')

# Group by Superhost status and calculate average price and average reviews
comparison = df.groupby('superhost').agg({'price': 'mean', 'number_of_reviews': 'mean'}).reset_index()

# Melt for plotting
comparison_melted = comparison.melt(id_vars='superhost', value_vars=['price', 'number_of_reviews'],
                                    var_name='Metric', value_name='Average Value')

# Plot comparison
plt.figure(figsize=(10, 6))
sns.barplot(x='Metric', y='Average Value', hue='superhost', data=comparison_melted)
plt.title('Comparison of Superhosts vs Regular Hosts')
plt.xlabel('Metric')
plt.ylabel('Average Value')
plt.tight_layout()
plt.show()