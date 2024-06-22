# Server Memory Logging Utility

This repo uses [https://github.com/pixelb/ps_mem](ps_mem.py) to get the actual memory consumption of each program, parse its output and then save the data to a csv.

The csv format is not optimal due to the structure of the saved data but it's a quick script to troubleshoot out of memory server crashes.

The ``visualize-memory-consumption.py`` script saves an html file with an interactive plot using plotly.

Install requirements.txt and run to get the plot. It expects the file in ./ps_mem.csv and by default prints the top 10 processes by max momentary memory consumption. This is an important bit, if a memory consumes 1MiB for ages and once spikes up to 1GiB, it will be included which might not be desirable. You can adjust this in the code though.