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
root_folder = os.path.normpath('/Users/tatiana/Documents/laura/basal/data')
file_list = os.listdir(root_folder)
file_list = [os.path.join(root_folder, file) for file in file_list if '_d30' in file]

# dictionaries
animal_group_dict = {'Addicted': ['L-33', 'L-34', 'L-36', 'L-39', 'L-30',
        'L-15', 'L-10', 'L-37'], 'Not_Addicted' : ['L-05', 'L-07', 'L-11',
        'L-13', 'L-18', 'L-19', 'L-20', 'L-21', 'L-22', 'L-31', 'L-32']}


animal_box_dict = {'L-33': '4R', 'L-34': '1L', 'L-36': '3L', 'L-39': '4R',
                   'L-30': '2R', 'L-15': '4R', 'L-10': '2R', 'L-37': '4R',
                   'L-05': '2R', 'L-07': '1L', 'L-11': '1L', 'L-13': '4R',
                   'L-18': '3L', 'L-19': '2R', 'L-20': '1L', 'L-21': '3L',
                   'L-22': '2R', 'L-31': '3L', 'L-32': '2R'}


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



"""
********* 1)a) SPECTROGRAMS (ALL SESSION) *****
"""
#INDIVIDUAL SPECTROGRAMS

spectro_windowlength = 1
individual_spectro_plot = True
spectro_vmin = 0
spectro_vmax = 50
spectro_ylim = (0, 100)

output_folder = '/Users/tatiana/Documents/laura/basal/Spectrograms'

#plt.ioff()

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

# concatenate events of the whole FR5 session

    # events_concat = []
    # active_events_dict = {}
    # previous_points = 0
    # previous_points_list = []
    # for file in sorted_files:
    #     fileload = pll.load_mat(file)
    #     events = fileload['adjusted_events']
    #     if len(events) > 0 and type(events[0]) != np.ndarray:
    #         events = events[np.newaxis, ...]
    #     for event in events:
    #         if event[0] == 'None':
    #             if event[2] in active_events_dict.keys():
    #                 events_concat.append([active_events_dict[event[2]],
    #                         event[1] + previous_points, event[2], True])
    #                 del active_events_dict[event[2]]
    #         elif event[1] == 'None':
    #             active_events_dict[event[2]] = event[0] + previous_points
    #         else:
    #             events_concat.append([event[0] + previous_points,
    #                     event[1] + previous_points, event[2], False])
    #     previous_points += fileload['data'].shape[0]
    #     previous_points_list.append(previous_points)

    #     # Para ordenar eventos desde punto de inicio
    # events_concat = [list(event) for event in pd.DataFrame(
    #         events_concat).sort_values(0).values]

    # animal = exp_animal_rep.split('_')[1]
    # if animal in animal_group_dict['Addicted']:
    #     addiction_type = 'Addicted'
    # elif animal in animal_group_dict['Not_Addicted']:
    #     addiction_type = 'Not_Addicted'
    # else:
    #     print(''.join(('The current animal doesn\'t have group ',
    #             'information: ', animal, '.')))
        # continue
# spectrograms of the whole FR5 session with events
    data_ch_list = [ch for ch in list(data_concat) if not 'ACC' in ch and not\
            'REF' in ch]
    for ch_name in data_ch_list:
        ch_data = data_concat[ch_name]
        data_f, data_t, data_s = pll.spectrogram(ch_data, samplingrate,
                spectro_windowlength)
        fig, axarr = plt.subplots(nrows=3, ncols=2, gridspec_kw={
                'width_ratios': [1, 0.03], 'height_ratios': [0.1, 0.1, 1],
                'wspace': 0.05, 'hspace': 0}, sharex='col')
        axarr[0][0].plot((np.array(range(ch_data.shape[0])) / samplingrate) / 60, ch_data)
        # SPECTROGRAM AXIS
        adjusted_data_s = 10 * np.log10(data_s)
        adjusted_data_t = data_t / 60
        im = axarr[2][0].imshow(adjusted_data_s, cmap='jet', aspect='auto',
                interpolation='gaussian', vmin=spectro_vmin, vmax=spectro_vmax,
                origin='lower', extent=(0, adjusted_data_t[-1], 0, data_f[-1]))
        axarr[2][0].set_ylim(spectro_ylim)
        axarr[2][0].set_xlabel('Time (min)')
        axarr[2][0].set_ylabel('Frequency (Hz)')
        # COLORBAR AXIS
        plt.colorbar(im, cax=axarr[2][1])
        # BORRAR EJES
        axarr[1][1].set_axis_off()
        axarr[0][1].set_axis_off()
        # DIBUJAR INFO DE EVENTOS EN EL EJE (0, 0)
        rec_length_min = ch_data.shape[0] / samplingrate / 60
        # for previous_points in previous_points_list:
        #     axarr[1][0].vlines((previous_points / samplingrate / 60), 0 , 1,
        #         color='grey' , linestyle = [':'] , label = 'File Concatenation')
        # for event in events_concat:
        #     if event[2] == ttls_box_dict[animal_box_dict[animal]]['ActLev'] and not event[3]:
        #         axarr[1][0].scatter((event[0]/samplingrate/60), 0.8, s=2,
        #                  color='black', label='Active Lever')
        #     if event[2] == ttls_box_dict[animal_box_dict[animal]]['InactLev'] and not event[3]:
        #         axarr[1][0].scatter((event[0]/samplingrate/60), 0.8, s=2,
        #                  color='grey', label='Inactive Lever')
        #     if event[2] == ttls_box_dict[animal_box_dict[animal]]['Reward'] and not event[3]:
        #         axarr[1][0].vlines((event[0]/samplingrate/60), 0, 1,
        #                  colors='red', linestyles='solid', linewidth=0.7,
        #                  label='Reward')
        #     if event[2] == ttls_box_dict[animal_box_dict[animal]]['Houselight']:
        #         light_start_min = event[0] / samplingrate / 60
        #         lignt_end_min = event[1] / samplingrate / 60
        #         axarr[1][0].hlines(0.2, light_start_min, lignt_end_min,
        #                  colors='orange', lw=6, label='LightHouse' )
        axarr[1][0].set_xlim((0, rec_length_min))
        axarr[1][0].set_ylim((0, 1))
        axarr[1][0].get_yaxis().set_ticks([])
        plot_name = '_'.join((exp_animal_rep, ch_name, addiction_type))
        axarr[0][0].set_title(plot_name)
        # FIG SAVE
        fig.savefig(os.path.join(output_folder, ''.join((plot_name, '.png'))))
        # plt.close(fig)
    plt.ion()
