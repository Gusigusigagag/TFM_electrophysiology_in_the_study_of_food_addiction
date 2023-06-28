# -*- coding: utf-8 -*-

# def to reload data

def pickle_save_var(variable, path):
    with open(path, 'wb') as openfile:
        pickle.dump(variable, openfile)
    return None


def pickle_load_var(path):
    with open(path, 'rb') as openfile:
        variable = pickle.load(openfile)
    return variable

# lib
import puiglablib as pll
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle


# file selection
root_folder = os.path.normpath('C:\\Users\\u201914\\basal\\sygnal\\PFC2')
file_list = os.listdir(root_folder)
file_list = [os.path.join(root_folder, file) for file in file_list if '_d30' in file]

# dictionaries
animal_group_dict = {'Addicted': ['L-33', 'L-34', 'L-36', 'L-39', 'L-30',
        'L-15', 'L-10', 'L-37'], 'Not_Addicted' : ['L-05', 'L-07', 'L-11',
        'L-13', 'L-18', 'L-19', 'L-20', 'L-21', 'L-22', 'L-31', 'L-32']}




ch_labels_dict = {'8_11_4_15_1_19_28_22_25_65_66_67': ['PFC1', 'PFC2',
        'PFCREF1', 'PFCREF2', 'HPC1', 'HPC2', 'HPCREF1', 'HPCREF2', 'COMREF',
        'ACC1', 'ACC2', 'ACC3'],
        '56_58_53_62_50_33_45_37_42_68_69_70': ['PFC1', 'PFC2', 'PFCREF1',
        'PFCREF2', 'HPC1', 'HPC2', 'HPCREF1', 'HPCREF2', 'COMREF', 'ACC1',
        'ACC2', 'ACC3'],
        '55_56_52_61_48_37_44_42_41_68_69_70': ['PFC1', 'PFC2', 'PFCREF1',
        'PFCREF2', 'HPC1', 'HPC2', 'HPCREF1', 'HPCREF2', 'COMREF', 'ACC1',
        'ACC2', 'ACC3'],
        '7_9_5_13_2_17_28_21_27_65_66_67': ['PFC1', 'PFC2', 'PFCREF1',
        'PFCREF2', 'HPC1', 'HPC2', 'HPCREF1', 'HPCREF2', 'COMREF',
        'ACC1', 'ACC2', 'ACC3'],
        '39_41_36_46_33_49_62_53_58_68_69_70': ['PFC1', 'PFC2','PFCREF1',
        'PFCREF2', 'HPC1', 'HPC2', 'HPCREF1', 'HPCREF2', 'COMREF', 'ACC1',
        'ACC2', 'ACC3']}


band_dict = {'delta': (3, 5), 'ntheta': (8, 10), 'wtheta': (8, 12),
        'beta': (15, 25), 'lgamma': (30, 50), 'hgamma': (50, 100), 'fgamma': (120, 150),
            'hfo': (150, 200)}

df_animal_freq_power = pd.DataFrame({'Animal': [], 
                                    'Type': [], 
                                    'delta': [], 
                                    'ntheta': [], 
                                    'wtheta': [], 
                                    'beta': [],
                                    'lgamma': [],
                                    'hgamma': [],
                                    'fgamma': [],
                                    'hfo': []})


concat_file_dict = {}

for file in file_list:
    exp_name_full = os.path.splitext(file.split(os.path.sep)[-1])[0]
    exp_name_full = re.sub('_d[0-9]+', '', exp_name_full)
    exp = exp_name_full.split('_')[0]
    animal = exp_name_full.split('_')[1]
    rep = exp_name_full.split('_')[2]
    cond_full = exp_name_full.split('_')[3]
    cond_number = int(cond_full.split('-')[-1])
    exp_animal_rep = exp + '_' + animal + '_' + rep
    print('Processing: ' + exp_name_full, flush=True)
    if animal in animal_group_dict['Addicted']:
        addiction_type = 'Addicted'
    elif animal in animal_group_dict['Not_Addicted']:
        addiction_type = 'Not_Addicted'
    else:
        print(''.join(('The current animal doesn\'t have group ',
                'information: ', animal, '.')))
        continue
    if exp_animal_rep not in concat_file_dict.keys():
        concat_file_dict[exp_animal_rep] = {'exp_files': {}}
    concat_file_dict[exp_animal_rep]['exp_files'][cond_number] = file
    
print('end of concatinating')

for exp_animal_rep in concat_file_dict.keys():
    exp_files_dict = concat_file_dict[exp_animal_rep]['exp_files']
    sorted_keys = sorted(exp_files_dict.keys())
    sorted_files = [exp_files_dict[num] for num in sorted_keys]
    concat_file_dict[exp_animal_rep]['exp_files'] = sorted_files
    data_concat = []
    for file in sorted_files:
        fileload = pll.load_mat(file)
        selected_ch = fileload['selected_ch']
        samplingrate = int(fileload['sample_rate'])
        ch_labels = ch_labels_dict['_'.join([str(ch) for ch in selected_ch])]
        data_df = pd.DataFrame(fileload['data'], columns=ch_labels)
        data_concat.append(data_df)
    data_concat = pd.concat(data_concat, axis=0).reset_index(drop=True)
    
    
    animal = exp_animal_rep.split('_')[1]
    if animal in animal_group_dict['Addicted']:
        addiction_type = 'Addicted'
    elif animal in animal_group_dict['Not_Addicted']:
        addiction_type = 'Not_Addicted'

    data_f, data_p, connectivity = pll.power_multitaper(data_concat['PFC2'], samplingrate, time_halfbandwidth_product=5,
                time_window_duration=None, time_window_step=None,
                n_tapers=9, is_low_bias=True, axis=0, frequency_norm=True,
                return_connectivity=True)
    
    # If two electrodes
    # data_f1, data_p1, connectivity1 = pll.power_multitaper(data_concat['PFC2'],samplingrate, time_halfbandwidth_product=5,
    #             time_window_duration=None, time_window_step=None,
    #             n_tapers=9, is_low_bias=True, axis=0, frequency_norm=True,
    #             return_connectivity=True)
    

    # if np.array_equal(data_f, data_f1):
    #     print("Arrays are equal")
    # else:
    #     # find elements that are different
    #     diff_idx = np.where(data_f != data_f1)[0]
    #     print("Different elements:")
    #     print("data_f:", data_f[diff_idx])
    #     print("data_f1:", data_f1[diff_idx])
    # data_p2 = np.mean([data_p, data_p1], axis=0)
    

    band_power_values_dict = pll.bandfunction(data_f, data_p, np.mean, band_dict=band_dict)
    my_dick = {}
    my_dick['Animal'] = animal
    my_dick['Type'] = addiction_type
    my_dick.update(band_power_values_dict)
    
    print('animal ', animal, ' saved to the dick: ', my_dick, '    ')
    print('finish animal  ', animal)


    df_animal_freq_power = df_animal_freq_power.append(my_dick, ignore_index=True)
print(df_animal_freq_power)

out_file = 'C:\\Users\\u201914\\basal\\df_PFC2.csv'
df_animal_freq_power.to_csv(out_file, sep='\t', index=False)