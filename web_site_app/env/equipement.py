from datetime import datetime
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def cluster_meter_data(merged_meter_data):
    # Extract relevant columns for clustering
    test_merged_meter = merged_meter_data[['METER_CODE','FOLIO_NUMBER','GROSS_UNACCOUNTED']]
    # Convert data types
    test_merged_meter.loc[:, 'FOLIO_NUMBER'] = pd.to_datetime(test_merged_meter['FOLIO_NUMBER'])
    test_merged_meter.loc[:, 'GROSS_UNACCOUNTED'] = test_merged_meter['GROSS_UNACCOUNTED'].astype(int)

    test_merged_meter = test_merged_meter.sort_values(by ='METER_CODE')
    test_merged_meter.reset_index(inplace=True)
     
    # Group by 'METER_CODE'
    grouped_meter = test_merged_meter.groupby('METER_CODE')
    

    # Initialize variables
    result_data = []
    original_indices = set()

    # Iterate over groups
    for meter_code, group_data in grouped_meter:
        # Find the row with the maximum FOLIO_NUMBER where GROSS_UNACCOUNTED is greater than 20
        max_folio_row = group_data[(group_data['GROSS_UNACCOUNTED'] > 20) | (group_data['GROSS_UNACCOUNTED'] < -20)]['FOLIO_NUMBER'].idxmax()

        if pd.notnull(max_folio_row):
            
 
            days_since_last_non_zero = (datetime.now() - group_data.loc[max_folio_row, 'FOLIO_NUMBER']).days

            # Calculate successive non-zero count
            successive_non_zero_count = 1
            successive_non_zero_sum = abs(group_data.loc[max_folio_row, 'GROSS_UNACCOUNTED'])
            print(group_data)
            for idx in range(max_folio_row - 1, -1, -1):
                print(idx)
                if group_data.loc[idx, 'GROSS_UNACCOUNTED'] > 20 or group_data.loc[idx, 'GROSS_UNACCOUNTED'] < -20:
                    
                    successive_non_zero_count += 1
                    successive_non_zero_sum += abs(group_data.loc[idx, 'GROSS_UNACCOUNTED'])
                else:
                    break
                    
            repaired = 1 if days_since_last_non_zero > 30 else 0

            result_data.append({
                'METER_CODE': meter_code,
                'successive_non_zero': successive_non_zero_count,
                'successive_non_zero_abs_sum': successive_non_zero_sum,
                'last_date_non_zero': days_since_last_non_zero,
                'repaired': repaired
            })
            current_indices = set(group_data.index)
            original_indices.update(current_indices)
        else:
            result_data.append({
                'METER_CODE': meter_code,
                'successive_non_zero': 0,
                'successive_non_zero_abs_sum': 0,
                'last_date_non_zero': 'No non-zero values found',
                'repaired': 0
            })

    # Create DataFrame from the result data
    result_df = pd.DataFrame(result_data)

    # Extract relevant columns for clustering
    cluster_data = result_df[['successive_non_zero', 'successive_non_zero_abs_sum', 'repaired', 'last_date_non_zero']]

    # Normalize features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(cluster_data)

    # Apply PCA
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(scaled_data)

    # Apply k-means clustering with k=4 on PCA components
    kmeans = KMeans(n_clusters=4, random_state=0)
    kmeans.fit(pca_components)

    # Add cluster labels to the DataFrame
    result_df['cluster'] = kmeans.labels_

    # Plot the data points with cluster labels and annotations
    plt.figure(figsize=(10, 6))
    for cluster_label in range(4):
        cluster_data2 = pca_components[result_df['cluster'] == cluster_label]
        plt.scatter(cluster_data2[:, 0], cluster_data2[:, 1], label=f'Cluster {cluster_label}')
        for i, (x, y) in enumerate(zip(cluster_data2[:, 0], cluster_data2[:, 1])):
            meter_code = result_df.loc[result_df['cluster'] == cluster_label].iloc[i]['METER_CODE']
            plt.annotate(meter_code, (x, y), textcoords="offset points", xytext=(0,10), ha='center')

    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('K-Means Clustering with PCA')
    plt.legend()
    plt.grid(True)
    plt.savefig('meter_clustering_result.png')  # Save the plot
    plt.close()  # Close the plot to prevent displaying it in the console

    # Save the clustering result DataFrame
    result_df.to_csv('meter_clustering_result.csv', index=False)

    return result_df

def cluster_injector_data(merged_injector_data):

    test_merged_injector = merged_injector_data[['INJECTOR_CODE','FOLIO_NUMBER','FRAC_UNACCOUNTED']]
    # Convert data types
    test_merged_injector.loc[:, 'FOLIO_NUMBER'] = pd.to_datetime(test_merged_injector['FOLIO_NUMBER'])
    test_merged_injector.loc[:, 'FRAC_UNACCOUNTED'] = test_merged_injector['FRAC_UNACCOUNTED'].astype(int)

    test_merged_injector = test_merged_injector.sort_values(by ='INJECTOR_CODE')
    test_merged_injector.reset_index(inplace=True)

    # Group by 'INJECTOR_CODE'
    grouped_injector = test_merged_injector.groupby('INJECTOR_CODE')

    # Initialize variables
    result_data_inj = []
    original_indices_inj = set()

    # Iterate over groups
    for injector_code, group_data in grouped_injector:
        # Find the row with the maximum FOLIO_NUMBER where FRAC_UNACCOUNTED is greater than 20 or less than -20
        filtered_group_data = group_data[(group_data['FRAC_UNACCOUNTED'] > 20) | (group_data['FRAC_UNACCOUNTED'] < -20)]
        if not filtered_group_data.empty:
           max_folio_row_inj = filtered_group_data['FOLIO_NUMBER'].idxmax()
           days_since_last_non_zero = (datetime.now() - group_data.loc[max_folio_row_inj, 'FOLIO_NUMBER']).days
    

           # Calculate successive non-zero count and sum
           successive_non_zero_count = 1
           successive_non_zero_sum = abs(group_data.loc[max_folio_row_inj, 'FRAC_UNACCOUNTED'])
           for idx in range(max_folio_row_inj - 1, -1, -1):
               if group_data.loc[idx, 'FRAC_UNACCOUNTED'] > 20 or group_data.loc[idx, 'FRAC_UNACCOUNTED'] < -20:
                  successive_non_zero_count += 1
                  successive_non_zero_sum += abs(group_data.loc[idx, 'FRAC_UNACCOUNTED'])
               else:
                  break
                
           # Determine if repaired
           repaired = 1 if days_since_last_non_zero > 30  else 0

           result_data_inj.append({
            'INJECTOR_CODE': injector_code,
            'successive_non_zero': successive_non_zero_count,
            'successive_non_zero_abs_sum': successive_non_zero_sum,
            #'last_date_non_zero': f"{datetime.now().strftime('%Y-%m-%d')} - {last_non_zero_date.strftime('%Y-%m-%d')} = {days_since_last_non_zero} days",
            'last_date_non_zero': days_since_last_non_zero,
            'repaired': repaired
           })
        
           current_indices = set(group_data.index)
           original_indices_inj.update(current_indices)
        else:
           result_data_inj.append({
            'INJECTOR_CODE': injector_code,
            'successive_non_zero': 0,
            'successive_non_zero_abs_sum': 0,
            'last_date_non_zero': 0,
            'repaired': 1
           })
    
    # Create DataFrame from the result data
    result_df_inj = pd.DataFrame(result_data_inj)
    
    # Extract relevant columns for clustering
    cluster_data_inj2 = result_df_inj[['successive_non_zero', 'successive_non_zero_abs_sum', 'repaired', 'last_date_non_zero']]

    # Normalize features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(cluster_data_inj2)
    print("Shape of scaled_data:", scaled_data.shape)

    # Apply PCA
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(scaled_data)

    # Apply k-means clustering with k=4 on PCA components
    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(pca_components)

    # Add cluster labels to the DataFrame
    result_df_inj['cluster'] = kmeans.labels_

    # Plot the data points with cluster labels and annotations
    plt.figure(figsize=(10, 6))
    for cluster_label in range(4):
        cluster_data_inj2 = pca_components[result_df_inj['cluster'] == cluster_label]
        plt.scatter(cluster_data_inj2[:, 0], cluster_data_inj2[:, 1], label=f'Cluster {cluster_label}')
        for i, (x, y) in enumerate(zip(cluster_data_inj2[:, 0], cluster_data_inj2[:, 1])):
            injector_code = result_df_inj.loc[result_df_inj['cluster'] == cluster_label].iloc[i]['INJECTOR_CODE']
            plt.annotate(injector_code, (x, y), textcoords="offset points", xytext=(0,10), ha='center')


    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('K-Means Clustering with PCA')
    plt.legend()
    plt.grid(True)
    plt.savefig('injector_clustering_result.png')  # Save the plot
    plt.close()  # Close the plot to prevent displaying it in the console

    # Save the clustering result DataFrame
    result_df_inj.to_csv('injector_clustering_result.csv', index=False)

    return result_df_inj

def cluster_tanks_data(tanks_data):

    test_merged_leaks_thefts = tanks_data[['TANK_CODE','FOLIO_NUMBER','NET_QUANTITY','RACK_DISPOSALS','quantity_difference']]

    test_merged_leaks_thefts['FOLIO_NUMBER'] = pd.to_datetime(test_merged_leaks_thefts['FOLIO_NUMBER'])
    test_merged_leaks_thefts['quantity_difference'] = test_merged_leaks_thefts['quantity_difference'].astype(int)

    grouped_leaks_thefts = test_merged_leaks_thefts.groupby('TANK_CODE')

    # Initialize variables
    result_data = []
    original_indices = set()

   # Iterate over groups
    for tank_code, group_data in grouped_leaks_thefts:
        if (group_data['quantity_difference'] < -20).any():
            # Find the row with the maximum FOLIO_NUMBER where quantity_difference indicates a leak or theft
            max_folio_row = group_data[group_data['quantity_difference'] < -20]['FOLIO_NUMBER'].idxmax()
        
            if pd.notnull(max_folio_row) and max_folio_row in group_data.index:
               # Calculate days since last non-zero value
               timestamp_str = str(group_data.loc[max_folio_row, 'FOLIO_NUMBER'])

               timestamp = timestamp_str[-8:]

               year = timestamp[:4]
               month = timestamp[4:6]
               day = timestamp[6:]
 
               formatted_date_str = f"{year}-{month}-{day}"


               last_less_minus20_date = datetime.strptime(formatted_date_str, "%Y-%m-%d")
               days_since_last_less_minus20 = (datetime.now() - last_less_minus20_date).days

               # Calculate successive non-zero count
               successive_non_zero_count = 1
               successive_less_minus20_sum = abs(group_data.loc[max_folio_row, 'quantity_difference'])
               for idx in range(max_folio_row - 1, -1, -1):
                   if idx in group_data.index and group_data.loc[idx, 'quantity_difference'] < -20:
                       successive_non_zero_count += 1
                       successive_less_minus20_sum += abs(group_data.loc[idx, 'quantity_difference'])
                   else:
                       break
                    
               repaired = 1 if days_since_last_less_minus20 > 30 else 0

               result_data.append({
                'TANK_CODE': tank_code,
                'successive_less_minus20': successive_non_zero_count,
                'successive_less_minus20_abs_sum': successive_less_minus20_sum,
                'last_date_less_minus20': days_since_last_less_minus20,
                'max_folio_date': last_less_minus20_date.date(),
                'repaired': repaired
                })
               current_indices = set(group_data.index)
               original_indices.update(current_indices)
            else:
               result_data.append({
                'TANK_CODE': tank_code,
                'successive_less_minus20': 0,
                'successive_less_minus20_abs_sum': 0,
                'last_date_less_minus20': 0,
                'max_folio_date': 'No less than -20 values found',
                'repaired': 0
                })
        else:
            result_data.append({
            'TANK_CODE': tank_code,
            'successive_less_minus20': 0,
            'successive_less_minus20_abs_sum': 0,
            'last_date_less_minus20': 0,
            'max_folio_date': 'No less than -20 values found',
            'repaired': 0
            })

    # Create DataFrame from the result data
    result_df = pd.DataFrame(result_data)

   
    # Extract relevant columns for clustering
    cluster_data2 = result_df[['successive_less_minus20', 'successive_less_minus20_abs_sum', 'repaired', 'last_date_less_minus20']]

    # Normalize features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(cluster_data2)

    # Apply PCA
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(scaled_data)

    # Apply k-means clustering with k=4 on PCA components
    kmeans = KMeans(n_clusters=5, random_state=0)
    kmeans.fit(pca_components)

    # Add cluster labels to the DataFrame
    result_df['cluster'] = kmeans.labels_

    # Plot the data points with cluster labels and annotations
    plt.figure(figsize=(10, 6))
    for cluster_label in range(5):
        cluster_data2 = pca_components[result_df['cluster'] == cluster_label]
        plt.scatter(cluster_data2[:, 0], cluster_data2[:, 1], label=f'Cluster {cluster_label}')
        for i, (x, y) in enumerate(zip(cluster_data2[:, 0], cluster_data2[:, 1])):
           meter_code = result_df.loc[result_df['cluster'] == cluster_label].iloc[i]['TANK_CODE']
           plt.annotate(meter_code, (x, y), textcoords="offset points", xytext=(0,10), ha='center')

    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('K-Means Clustering with PCA')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Save the clustering result DataFrame
    result_df.to_csv('tanks_clustering_result.csv', index=False)

    return result_df