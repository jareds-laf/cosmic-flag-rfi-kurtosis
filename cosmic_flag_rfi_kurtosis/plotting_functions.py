import matplotlib.pyplot as plt
import numpy as np
import os
from analysis_functions import get_kurtosis


# TODO: Make it so that these functions access the table that
# was created by the write_output_table() function!
# TODO: Add output file functionality for different file types

def plot_tavg_power(wf_in,
                    f_start=0, f_stop=6000,
                    p_start=0, p_stop=5*10**10, n_divs=256, threshold=50,
                    show_filtered_bins=True,
                    output_file='', output_type='png'):
    # Plot the time-averaged power spectrum for a given blimpy waterfall object
    # Inputs:
        # wf: The desired input waterfall object
        # t: The integration number
        # f_start: Lower bound for frequency (horizontal) axis
        # f_stop: Upper bound for frequency (horizontal) axis
        # p_start: Lower bound for time-averaged power (veritcal) axis
        # p_start: Lower bound for time-averaged power (veritcal) axis
        # show_filtered: If true, mark high RFI channels with a vertical red box
        # output_dest: Location (including filename) to save output file
        # output_type: Filetype of output

    # Time average the power
    wf_pwr_mean_arr = np.mean(wf_in.data, axis=0)
    wf_pwr_mean = wf_pwr_mean_arr[0]
   
    # Plot time-averaged power
    fig, ax = plt.subplots()
    
    ax.set_xlim(f_start, f_stop)
    ax.set_ylim(p_start, p_stop)
    
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Time-Averaged Power (Counts)')

    ax.plot(wf_in.get_freqs(), wf_pwr_mean,
            label='Time-averaged power spectrum',
            c='#1f1f1f')

    # Grab info for RFI masking
    bins, kurts, pows_mean, flagged_bins, flagged_kurts, masked_kurts, masked_freqs, bin_mask, freq_mask = get_kurtosis(wf_in, n_divs, threshold)

    # Plot frequency bins that were flagged as RFI
    if show_filtered_bins == True:
        full_freq_range = np.amax(wf_in.get_freqs()) - np.amin(wf_in.get_freqs())
        bin_width = full_freq_range / n_divs

        for rfi_bin in flagged_bins:
            xmin = rfi_bin
            xmax = rfi_bin + bin_width
            flagged_line = plt.axvspan(xmin=xmin, xmax=xmax, ymin=0, ymax=1, color='red', alpha=0.5)

        flagged_line.set_label('RFI-flagged channels')
        ax.legend(fancybox=True,shadow=True, loc='lower center', bbox_to_anchor=(1, 1), ncols=1)
    else:
        ax.legend(fancybox=True,shadow=True, loc='lower center', bbox_to_anchor=(1, 1), ncols=1)
    
    plt.savefig(output_file, type=output_type)

def plot_mask_kurtosis(wf_in, n_divs=256, threshold=50,
                       unfiltered=True, clean_chnls=True, rfi=False,
                      f_start=2000, f_stop=4000,
                      k_start=-5, k_stop=500,
                      output_file='', output_type='png'):
    # This function plots the kurtosis of each frequency channel for a specified waterfall object.
    # Inputs:
        # wf_in: See get_kurtosis() function definition
        # n_divs: See get_kurtosis() function definition
        # threshold: See get_mask_kurtosis() function definition
        # unfiltered: If true, plot the data before any RFI filtering has occurred
        # clean_chnls: If true, plot the data after RFI has been filtered out
        # rfi: If true, plot the channels that have been marked as RFI
        # output_dest: Location (including filename) to save output file
        # output_type: Filetype of output
    
    bins, kurts, pows_mean, flagged_bins, flagged_kurts, masked_kurts, masked_freqs, bin_mask, freq_mask = get_kurtosis(wf_in, n_divs, threshold)
    
    fig, ax = plt.subplots()
    
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Kurtosis')
    
    if unfiltered:
        ax.plot(bins, kurts, 'o', c='black', label='Unfiltered data') # Color is a nice black
    if clean_chnls:
        ax.plot(bins, masked_kurts, '.', c='#43cc5c', label='Clean channels') # Color is a nice green
    if rfi:
        ax.plot(flagged_bins, flagged_kurts, '.', c='red', label='Heavy RFI') # Color is a nice red
    
    # TODO: Change this condition... :)
    if np.any([f_start, f_stop, k_start, k_stop]) != 0:
        ax.set_xlim(f_start, f_stop)
        ax.set_ylim(k_start, k_stop)
    
        ax.legend(fancybox=True,shadow=True, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncols=3)
    else:
        ax.legend(fancybox=True,shadow=True, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncols=3)

    plt.savefig(output_file, type=output_type)