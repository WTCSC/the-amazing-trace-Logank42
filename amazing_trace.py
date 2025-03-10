import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
import time
import os
import subprocess
import re

def execute_traceroute(destination):
    response = subprocess.run(["sudo", "traceroute", "-I", destination], capture_output=True) # Runs the command to traceroute
    return response # Returns the command

def parse_traceroute(traceroute_output):
    final_output = []
    lines = traceroute_output.split("\n") # Splits the whole trace_output into seprate lines for easy handeling
    for line in lines:
        match = re.match(r"^\s*(\d+)\s+([\w\.-]+)?\s*\(?([\d\.]+)?\)?\s*(\d+\.\d+ ms)?\s*(\d+\.\d+ ms)?\s*(\d+\.\d+ ms)?", line) # Paramaters for splitting the lines into hops, ip, name and time
        if match:
            hop_dict = {} # Dictonary for return
            hop_dict["hop"] = int(match.group(1)) # Checks in first (), to match for the number of hops
            hop_dict["ip"] = match.group(3) if match.group(3) else None # Checks in second (), to match for the number of hops, and returns None if it does not match
            hop_dict["hostname"] = match.group(2) if match.group(2) else None # Checks in third (), to match for the number of hops, and returns None if it does not match
            hop_dict["rtt"] = [
                float(match.group(4).split()[0]) if match.group(4) else None, # Uses float to handle decimals, and uses same group functionality as before
                float(match.group(5).split()[0]) if match.group(5) else None, # Uses float to handle decimals, and uses same group functionality as before
                float(match.group(6).split()[0]) if match.group(6) else None # Uses float to handle decimals, and uses same group functionality as before
                ]           
            final_output.append(hop_dict) # Adds the dictionary to final_output
    return final_output


# ============================================================================ #
#                    DO NOT MODIFY THE CODE BELOW THIS LINE                    #
# ============================================================================ #
def visualize_traceroute(destination, num_traces=3, interval=5, output_dir='output'):
    """
    Runs multiple traceroutes to a destination and visualizes the results.

    Args:
        destination (str): The hostname or IP address to trace
        num_traces (int): Number of traces to run
        interval (int): Interval between traces in seconds
        output_dir (str): Directory to save the output plot

    Returns:
        tuple: (DataFrame with trace data, path to the saved plot)
    """
    all_hops = []

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    print(f"Running {num_traces} traceroutes to {destination}...")

    for i in range(num_traces):
        if i > 0:
            print(f"Waiting {interval} seconds before next trace...")
            time.sleep(interval)

        print(f"Trace {i+1}/{num_traces}...")
        output = execute_traceroute(destination)
        hops = parse_traceroute(output)

        # Add timestamp and trace number
        timestamp = time.strftime("%H:%M:%S")
        for hop in hops:
            hop['trace_num'] = i + 1
            hop['timestamp'] = timestamp
            all_hops.append(hop)

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(all_hops)

    # Calculate average RTT for each hop (excluding timeouts)
    df['avg_rtt'] = df['rtt'].apply(lambda x: np.mean([r for r in x if r is not None]) if any(r is not None for r in x) else None)

    # Plot the results
    plt.figure(figsize=(12, 6))

    # Create a subplot for RTT by hop
    ax1 = plt.subplot(1, 1, 1)

    # Group by trace number and hop number
    for trace_num in range(1, num_traces + 1):
        trace_data = df[df['trace_num'] == trace_num]

        # Plot each trace with a different color
        ax1.plot(trace_data['hop'], trace_data['avg_rtt'], 'o-',
                label=f'Trace {trace_num} ({trace_data.iloc[0]["timestamp"]})')

    # Add labels and legend
    ax1.set_xlabel('Hop Number')
    ax1.set_ylabel('Average Round Trip Time (ms)')
    ax1.set_title(f'Traceroute Analysis for {destination}')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()

    # Make sure hop numbers are integers
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()

    # Save the plot to a file instead of displaying it
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    safe_dest = destination.replace('.', '-')
    output_file = os.path.join(output_dir, f"trace_{safe_dest}_{timestamp}.png")
    plt.savefig(output_file)
    plt.close()

    print(f"Plot saved to: {output_file}")

    # Return the dataframe and the path to the saved plot
    return df, output_file

# Test the functions
if __name__ == "__main__":
    # Test destinations
    destinations = [
        "google.com",
        "amazon.com",
        "bbc.co.uk"  # International site
    ]

    for dest in destinations:
        df, plot_path = visualize_traceroute(dest, num_traces=3, interval=5)
        print(f"\nAverage RTT by hop for {dest}:")
        avg_by_hop = df.groupby('hop')['avg_rtt'].mean()
        print(avg_by_hop)
        print("\n" + "-"*50 + "\n")
