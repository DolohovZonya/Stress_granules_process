The order of using the files and the parameters that are currently set in every step:
1) make_tiff_from_czi - used as a plugin in Fiji
2) count_granules_in_Icy.js - used as a plugin in Icy, current parameters: intensity 30, 3 pixels
3) make_nucleus_from_dir - I launch it in Spyder so it's kinda divided into pieces. Current parameters: area 400, block_size = 101
4) map_granules_on_nuclei_big_ellipse.py - the last file for mapping I used. here the radius of nucleus is set as 40
5) collect_statistics - gets different parameters per image
6) make_merged_file - merges results of statistics script into a single file
7) divide_by_anumal_and_struct - clusters the files
8) some_stats_script - calculates the statistics for further imaging
9) plot_sg - plot the dynamics :) I manually set tthe parameters I want to see, but I have a broader file where in makes figures for all parameters for all structures (currently I work only with OB so I plot only OB)
