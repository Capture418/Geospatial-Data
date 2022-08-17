def transform_data(df_tourism):

    df_tourism['id'] = df_tourism['TIME'].astype(str) + '?' + df_tourism['GEO']
    df_pivot = df_tourism.pivot(index = 'id', columns = ['ACCOMUNIT','UNIT'], values = 'Value')
    new_names = ['_'.join(x) for x in df_pivot.columns]
    df_pivot.columns = new_names
    df_pivot['new_id'] = df_pivot.index.values
    new = df_pivot['new_id'].str.split('?', expand = True)
    df_pivot['nuts218nm'] = new[1].values
    df_pivot['year'] = new[0].values
    df_pivot.reset_index(inplace = True, drop = True)
    df_pivot.drop(['Bedrooms_Number','Bedrooms_Percentage change on previous period', 'new_id'], inplace = True, axis = 1)
    return df_pivot

def call2016():

    import geopandas as gpd
    import pandas as pd
    import funcs as tourism
    FILENAME1 = 'NUTS_Level_2_(January_2018)_Boundaries.geojson'
    FILENAME2 = 'tour_cap_nuts2_1_Data.csv'
    gdf = gpd.read_file(FILENAME1)
    df_tourism = pd.read_csv(FILENAME2)
    transformed_df = tourism.transform_data(df_tourism)
    df_2016 = transformed_df[transformed_df['year']=='2016']
    df_2016['true_loc'] = df_2016['nuts218nm']
    replacements = {
    'Northern Ireland (UK)':'Northern Ireland', 
    'Gloucestershire, Wiltshire and Bristol/Bath area':'Gloucestershire, Wiltshire and Bath/Bristol area',
    'West Wales and The Valleys':'West Wales'
    }
    df_2016['true_loc'].replace(replacements, inplace = True)

    df_scotland = pd.DataFrame(
    [
    [None,None,None,None,'Eastern_Scotland', '2016', 'Eastern Scotland'],
    [None,None,None,None,'West_Central_Scotland', '2016', 'West Central Scotland'],
    [None,None,None,None,'Southern_Scotland', '2016', 'Southern Scotland']
    ],
    columns = ['Establishments_Number', 'Establishments_Percentage change on previous period','Bedplaces_Number','Bedplaces_Percentage change on previous period','nuts218nm','year','true_loc']
    )
    df_2016 = pd.concat([df_2016,df_scotland], ignore_index= True)

    df_2016 = df_2016.rename({'nuts218nm':'old_nuts218nm','true_loc':'nuts218nm'}, axis = 1)
    return df_2016


