import pandas as pd
import plotly.graph_objects as go

# Load the data from the CSV file. Format should be: timestamp,private (MiB),shared (MiB),total (MiB),program,num_processes
file_path = './ps_mem.csv'
data = pd.read_csv(file_path)

# Convert timestamp to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Aggregate data by timestamp and program to get the total memory usage at each timestamp
aggregated_data = data.groupby(['timestamp', 'program']).sum().reset_index()

# Sort data by total memory consumption in descending order and select the top num_top_processes processes
sorted_data = aggregated_data.groupby('program')['total (MiB)'].max().sort_values(ascending=False)

num_top_processes = 10

top_programs = sorted_data.head(num_top_processes).index

# Filter the aggregated data to include only the top 2 processes
filtered_data = aggregated_data[aggregated_data['program'].isin(top_programs)]

# Create an interactive plot using Plotly with WebGL
fig = go.Figure()

for program in filtered_data['program'].unique():
    program_data = filtered_data[filtered_data['program'] == program]
    fig.add_trace(go.Scattergl(
        x=program_data['timestamp'],
        y=program_data['total (MiB)'],
        mode='lines',
        name=program,
        hovertemplate='<b>Program:</b> %{text}<br>' +
                      '<b>Timestamp:</b> %{x}<br>' +
                      '<b>Total Memory (MiB):</b> %{y}<br>' +
                      '<b>Num Processes:</b> %{customdata}',
        text=program_data['program'],
        customdata=program_data['num_processes']
    ))

# Update layout with dropdown menu to select which processes to show
buttons = [
    {
        'label': 'All Programs', 
        'method': 'update', 
        'args': [{'visible': [True] * len(filtered_data['program'].unique())}]
    }
]
buttons += [
    {
        'label': program, 
        'method': 'update', 
        'args': [{'visible': [program == p for p in filtered_data['program']]}]
    } 
    for program in filtered_data['program'].unique()
]

fig.update_layout(
    title='Memory Consumption Over Time',
    xaxis_title='Timestamp',
    yaxis_title='Total Memory Consumption (MiB)',
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'showactive': True,
    }]
)

# Save the plot to an HTML file, so that it can be opened in any browser. This is important because my Firefox install does not support WebGL for some reason.
html_file = 'memory_consumption_plot.html'
fig.write_html(html_file)