
import pandas as pd
import os
import csv
import statistics as st
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# ____________ DIRICTORIES______________________
input_rewards_file = 'C:\\Users\\u201914\\Learning\\learning_criterias\\learning_criterias\\try\\reward.csv'
input_discrimination_file_active = 'C:\\Users\\u201914\\Learning\\learning_criterias\\learning_criterias\\try\\act.csv'
input_discrimination_file_inactive = 'C:\\Users\\u201914\\Learning\\learning_criterias\\learning_criterias\\try\\inact.csv'
output_folder = 'C:\\Users\\u201914\\Learning\\learning_criterias\\learning_criterias\\try\\out_temp_rewards'   # do not remove the last part
output_folder_disc = 'C:\\Users\\u201914\\Learning\\learning_criterias\\learning_criterias\\try\\out_temp_levers'   # do not remove the last part
output_folder_3_days = 'C:\\Users\\u201914\\Learning\\learning_criterias\\learning_criterias\\try\\3_days'   # do not remove the last part


os.makedirs(output_folder, exist_ok=True)
os.makedirs(output_folder_disc, exist_ok=True)
os.makedirs(output_folder_3_days, exist_ok=True)
#____________________________________________


#________________READ REWARD CSV_______________
df = pd.read_csv(input_rewards_file)
df_values = df.iloc[:,2:]
df.set_index(['Mice', 'Genotype'], inplace=True)
df_new = pd.DataFrame().reindex(index=df.index)

# loop through every column and add consecutive columns to the new dataframe
for i in range(df.shape[1]-2):
    df_temp = df.iloc[:, i:i+3].reindex(index=df.index)
    df_temp.columns = ['day'+str(i+1), 'day'+str(i+2), 'day'+str(i+3)]
    df_new = pd.concat([df_new, df_temp], axis=1)
df_trans = df_new.T

suffix = 1
for i in range(len(df_trans)):
    if i % 3 == 0:
        df_trans[i:i + 3].to_csv(os.path.join(output_folder, f"{suffix}.csv"),
                           sep='\t', index=True, header=True)
        suffix += 1
# _______________________________________________

#____________ READ DISCRIMINATION CSV_____________

# read the two csv tables
table1 = pd.read_csv(input_discrimination_file_active)
table2 = pd.read_csv(input_discrimination_file_inactive)
# check if column names are the same for levers
if set(table1.columns) != set(table2.columns):
    # raise an error with unique columns
    unique_cols = set(table1.columns) ^ set(table2.columns)
    raise ValueError(f"Columns for act and inact levers are not same. Unique columns are {unique_cols}")
# check if column names are the same for rewards and levers
if set(table1.columns) != set(df_values.columns):
    # raise an error with unique columns
    unique_cols = set(table1.columns) ^ set(df_values.columns)
    raise ValueError(f"Columns for rewards and levers are not same. Unique columns are {unique_cols}")


# fill gaps in tables with zeros
table1.fillna(0, inplace=True)
table2.fillna(0, inplace=True)
table1.astype(float)
table2.astype(float)
# create a new pandas table to store the comparison result
comp_table = pd.DataFrame(index=table1.index, columns=table1.columns)
# loop through each row and column of the tables and compare the values
for i in range(len(table1.index)):
    for j in range(len(table1.columns)):
        val1 = table1.iloc[i,j]
        val2 = table2.iloc[i,j]
        if val1 > 1.75 * val2:
            comp_table.iloc[i,j] = 1
        else:
            comp_table.iloc[i,j] = 0


df_new_div = pd.DataFrame()
for i in range(comp_table.shape[1]-2):
    df_temp = comp_table.iloc[:, i:i+3]
    df_new_div = pd.concat([df_new_div, df_temp], axis=1)
df_new_div_T = df_new_div.T

suffix_div = 1
for i in range(len(df_new_div_T)):
    if i % 3 == 0:
        df_new_div_T[i:i + 3].T.to_csv(os.path.join(output_folder_disc, f"{suffix_div}.csv"),
                           sep='\t', index=False, header=False)
        suffix_div += 1
# _________________________________________

# ___________FUNCTIONS_____________________
def stability(day1, day2, day3):
    """ counts the lower limit and upper limit of the
        3 days period; return 1 if all numbers in the range, 0 in all
        other cases. The result writes to the 'Stability' column

        - to change the limit -> change 'percent' variable """

    data_list = [day1, day2, day3]
    temp_list = []
    # ______Change the limit_______
    percent = 0.2
    # ______________________________
    minus_percent = st.mean(data_list) - (st.mean(data_list) * percent)
    plus_percent = st.mean(data_list) + (st.mean(data_list) * percent)

    for i in data_list:
        if plus_percent > i > minus_percent:
            temp_list.append(i)
    if len(temp_list) == 3:
        return 1
    else:
        return 0


def reward(day1, day2, day3):
    """ counts the number of rewards; prints 1 if all 3 days are more
    than the given minimum. If all three days acquire the criteria
    writes '1' to the column 'Reinforcement', if not '0'

    - to change the minimum of rewards -> change 'rewards' variable"""

    data_list = [day1, day2, day3]
    temp_list = []
    # ______Change the min rewards_______
    rewards = 10
    # ___________________________________

    for i in data_list:
        if i >= rewards:
            temp_list.append(i)
    if len(temp_list) == 3:
        return 1
    else:
        return 0


def acquisition(stability, reinforcement, discrimination):
    """ When 'Stability', 'Reinforcement' and 'Discrimination'
        columns == 1 - return 1 to 'Acquisition' column. If
        at least one criteria not equal 1 - returns 0 """

    data_list = [stability, reinforcement, discrimination]
    if data_list[0] == data_list[1] == data_list[2] == 1:
        return 1
    else:
        return 0
#__________________________________________

suffix2 = 1
i = 1
for file in os.listdir(output_folder):
    file_name = f"{i}.csv"

    source = pd.read_csv(os.path.join(output_folder, file_name), index_col='Mice', sep='\t')
    df_three_days = source.T
    df_three_days.iloc[:, 1] = df_three_days.iloc[:, 1].astype(int)
    df_three_days.iloc[:, 2] = df_three_days.iloc[:, 2].astype(int)
    df_three_days.iloc[:, 3] = df_three_days.iloc[:, 3].astype(int)


    discrim_file = os.path.join(output_folder_disc, file_name)
    discrim_list = []
    final_discrim_list = []

    """ to check for discrimination opens the given .csv, 
    where 0 - not acquire and 1 - acquire. If all three 
    days == 1. Discrimination column == 1
    
    - % change in the template .xlsx file"""

    with open(discrim_file, 'r', encoding='utf-8') as f:
        csv_file = csv.reader(f, delimiter='\t')
        for row in csv_file:
            discrim_list.append(row)

        for list1 in discrim_list:
            if list1[0] == list1[1] == list1[2] == '1':
                final_discrim_list.append(1)
            else:
                final_discrim_list.append(0)


    df_three_days['Stability'] = df_three_days.iloc[:, [1, 2, 3]].apply(lambda x: stability(*x), axis=1)
    df_three_days['Reinforcement'] = df_three_days.iloc[:, [1, 2, 3]].apply(lambda x: reward(*x), axis=1)
    df_three_days['Discrimination'] = final_discrim_list
    df_three_days['Acquisition'] = df_three_days.iloc[:, [4, 5, 6]].apply(lambda x: acquisition(*x), axis=1)


    df_three_days.to_csv(os.path.join(output_folder_3_days, f"{suffix2}.csv"), sep='\t', index=True, index_label='Mice')

    #os.remove(os.path.join(output_folder, file_name))
    #os.remove(os.path.join(output_folder_disc, file_name))
    suffix2 += 1
    i += 1

a = 1
df_samples = pd.read_csv(os.path.join(output_folder_3_days, "1.csv"), sep='\t')
diction = df_samples.set_index('Mice').to_dict()['Genotype']
df_stable_days = pd.DataFrame(list(diction.items()), columns=['Mice', 'Genotype'])
df_unstable_days = pd.DataFrame(list(diction.items()), columns=['Mice', 'Genotype'])

for file in os.listdir(output_folder_3_days):
    file_name = f'{a}.csv'
    df_three_days = pd.read_csv(os.path.join(output_folder_3_days, file_name), sep='\t')

    df_temporary = df_three_days.copy()
    df_temporary = df_temporary.loc[df_temporary['Acquisition'] != 0]
    df_temporary = df_temporary.drop(columns=['Stability',
                                              'Reinforcement', 'Discrimination',
                                              'Acquisition'])
    df_stable_days = df_stable_days.merge(df_temporary, on='Mice', how='left', suffixes=('', '_y'))
    df_stable_days.drop(df_stable_days.filter(regex='_y$').columns, axis=1, inplace=True)

    df_temporary = df_three_days.copy()
    df_temporary = df_temporary.loc[df_temporary['Acquisition'] == 0]
    df_temporary = df_temporary.drop(columns=['Stability',
                                              'Reinforcement', 'Discrimination',
                                              'Acquisition'])
    df_unstable_days = df_unstable_days.merge(df_temporary, on='Mice', how='left', suffixes=('', '_y'))
    df_unstable_days.drop(df_unstable_days.filter(regex='_y$').columns, axis=1, inplace=True)

    a += 1


df_stable_days.to_excel('stable_days.xlsx')    # Here you can change the name of the final table file
df_unstable_days.to_excel('unstable_days.xlsx')  # Here you can change the name of the final table file

print('done')