import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from codeforces_problems_data import Problem
from collections import Counter
from codeforces_rating_history import CodeforcesRating


### Step 1 and 2: dataset collection using codeforces api and clean the dataset using Pandas and Numpy
def fetch_and_prepare_data():
    try:
        data = Problem()
        column_names = ['ID', 'creationTimeSeconds', 'contestId', 'index', 'name',
                        'rating', 'tags', 'participantType', 'programmingLanguage',
                        'verdict', 'timeConsumedMillis', 'memoryConsumedKiloBytes']

        pd.set_option('display.max_columns', None)  ## for all columns display
        df = pd.DataFrame(data.all_problems, columns=column_names)

        ### Remove duplicates all wrong and AC
        # df.drop_duplicates(subset=['contestId', 'index', 'name', 'rating', 'verdict'], keep='first', inplace=True)
        # Resetting the index after removing duplicates
        # df.reset_index(drop=True, inplace=True)
        # print(df.tail(50))

        # Filter and remove duplicates for AC solutions
        df_ok = df[df['verdict'] == "OK"]
        df_ok.drop_duplicates(subset=['contestId', 'index', 'name', 'rating'], keep='first', inplace=True)

        # Include non-AC solutions
        df_non_ok = df[df['verdict'] != "OK"]

        # Combine and reset index
        df = pd.concat([df_ok, df_non_ok]).reset_index(drop=True)

        return df
    except requests.exceptions.ChunkedEncodingError as e:
        print("Error fetching data:", e)
        return None


### step 3: Handle missing values and Preprocess the columns using Pandas and Numpy
def preprocess_data(df):
    # Handle missing values, replace "Not Rated" by mean rating with its nearest a hundred and data types
    df['rating'] = pd.to_numeric(df['rating'].replace("Not Rated", np.nan), errors='coerce')
    df['rating'].fillna(int(round(df['rating'].mean(), -2)), inplace=True)
    df['rating'] = df['rating'].astype(int)
    df['memoryConsumedKiloBytes'] = df['memoryConsumedKiloBytes'].astype(int)

    # Convert creation time to datetime and calculate solving time in minutes
    df['creationTimeSeconds'] = pd.to_datetime(df['creationTimeSeconds'])

    # Extract tags and count frequencies
    tags_list = []
    for tags in df['tags']:
        try:
            if isinstance(tags, str):
                # If tags is a string, evaluate it to get the list
                tag_list = eval(tags)
            elif isinstance(tags, list):
                # If tags is already a list, use it directly
                tag_list = tags
            else:
                continue
            tags_list.extend(tag_list)
        except:
            continue

    tag_frequencies = Counter(tags_list)


    # Create categories for memory and time consumption
    df['memory_category'] = pd.cut(df['memoryConsumedKiloBytes'],
                                   bins=[0, 100, 1000, 5000, np.inf],
                                   labels=['0-100 KB', '101-1000 KB', '1001-5000 KB', '5000+ KB'])

    df['time_category'] = pd.cut(df['timeConsumedMillis'],
                                 bins=[0, 100, 150, 200, np.inf],
                                 labels=['0-100 ms', '101-150 ms', '151-200 ms', '200+ ms'])

    return df, tag_frequencies



### Step 4. Perform exploratory data analysis (EDA) on the data using Seaborn.
def perform_eda(df, tag_frequencies):

    # 1. Plot unique tags frequency Distribution
    plt.figure(figsize=(12, 8))

    # Convert Counter to DataFrame and sort by frequency
    tag_df = pd.DataFrame.from_dict(tag_frequencies, orient='index', columns=['count'])
    tag_df = tag_df.sort_values('count', ascending=False).head(15)  # Get top 15 tags

    # Create color palette
    colors = sns.color_palette("husl", n_colors=len(tag_df))

    # Create vertical bar plot
    bars = plt.bar(range(len(tag_df)), tag_df['count'], color=colors)

    # Customize the plot
    plt.xticks(range(len(tag_df)), tag_df.index, rotation=45, ha='right')
    plt.ylabel('Frequency')
    plt.xlabel('Tags')
    plt.title('Frequency of Tags')

    # Add gridlines
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    plt.show()

    # 2. Memory Consumption Distribution
    plt.figure(figsize=(10, 8))
    memory_counts = df['memory_category'].value_counts()
    plt.pie(memory_counts, labels=memory_counts.index, autopct='%1.1f%%')
    plt.title('Memory Consumption Distribution')
    plt.show()

    # 3. Time Consumption Distribution
    plt.figure(figsize=(10, 8))
    time_counts = df['time_category'].value_counts()
    plt.pie(time_counts, labels=time_counts.index, autopct='%1.1f%%')
    plt.title('Time Consumption Distribution')
    plt.show()

    # 4. Time vs Memory Scatter Plot
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='timeConsumedMillis', y='memoryConsumedKiloBytes')
    plt.title('Time vs Memory Consumption')
    plt.xlabel('Time (ms)')
    plt.ylabel('Memory (KB)')
    plt.show()

    # 5. Rating Distribution
    plt.figure(figsize=(12, 8))
    sns.histplot(data=df, x='rating', bins=30)
    plt.title('Problem Rating Distribution')
    plt.xlabel('Rating')
    plt.show()

    # 6. Verdict Distribution
    plt.figure(figsize=(12, 8))
    verdict_counts = df['verdict'].value_counts()
    verdict_colors = {
        'OK': '#32CD32',
        'WRONG_ANSWER': '#FA8072',
        'TIME_LIMIT_EXCEEDED': '#FFA500',
        'COMPILATION_ERROR': '#FFD700',
        'RUNTIME_ERROR': '#808080'
    }
    colors = [verdict_colors.get(verdict, '#808080') for verdict in verdict_counts.index]

    plt.pie(verdict_counts, autopct='%1.1f%%', colors=colors)
    plt.title('Verdict Distribution')

    legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor=color) for color in colors]
    plt.legend(legend_elements,
               ['ACCEPTED' if x == 'OK' else x.replace('_', ' ') for x in verdict_counts.index],
               loc='center left',
               bbox_to_anchor=(1, 0.5))
    plt.show()

    # 7. Distribution of Solving Times
    plt.figure(figsize=(12, 8))
    solving_times = df[df['timeConsumedMillis'] < df['timeConsumedMillis'].quantile(0.95)]
    sns.histplot(data=solving_times, x='timeConsumedMillis', bins=30)
    plt.title('Distribution of Solving Times')
    plt.xlabel('Time (milliseconds)')
    plt.show()

    # 8. Problems Solved by Index
    plt.figure(figsize=(12, 8))
    index_counts = df[df['verdict'] == 'OK']['index'].value_counts().sort_index()
    sns.barplot(x=index_counts.index, y=index_counts.values)
    plt.title('Problems Solved by Index')
    plt.xlabel('Problem Index')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

    # Print summary statistics
    print("\nSummary Statistics:")
    print("\nRating Statistics:")
    print(df['rating'].describe())
    print("\nTime Consumption (ms):")
    print(df['timeConsumedMillis'].describe())
    print("\nMemory Consumption (KB):")
    print(df['memoryConsumedKiloBytes'].describe())
    print("\nSolving Time Statistics (millisecond):")
    print(df['timeConsumedMillis'].describe())


def main():
    df = fetch_and_prepare_data()

    if df is not None:

        processed_df, tag_frequencies = preprocess_data(df)
        perform_eda(processed_df, tag_frequencies)

        print("\nMost Common Problem Types:")
        for tag, count in sorted(tag_frequencies.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"{tag}: {count}")

        print("\nProgramming Language Distribution:")
        print(processed_df['programmingLanguage'].value_counts().head())

        success_rate = (len(processed_df[processed_df['verdict'] == 'OK']) / len(processed_df)) * 100
        print(f"\nOverall Success Rate: {success_rate:.2f}%")

    cf_rating = CodeforcesRating("Md_Almizan")
    cf_rating.plot_rating_history()


if __name__ == "__main__":
    main()