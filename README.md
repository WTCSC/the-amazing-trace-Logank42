[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=18567569)
# The Amazing Trace
This is a simple traceroute program. To run it, you'll need to run `python3 amazing_trace.py`. Once run, you may need to enter your password for sudo commands. 

The output of this script will look like this:

    Running 3 traceroutes to google.com...
    Trace 1/3...
    Waiting 5 seconds before next trace...
    Trace 2/3...
    Waiting 5 seconds before next trace...
    Trace 3/3...
    Plot saved to: output/trace_google-com_20250310-152454.png

    Average RTT by hop for google.com:
    hop
    1     0.461167
    2     3.220167
    3          NaN
    4          NaN
    5     5.588000
    6     4.679556
    7     4.461222
    8     4.091222
    9     5.694111
    10    4.046667
    11    4.755889
    Name: avg_rtt, dtype: float64

    ------------------------------------------

This script only traces to google.com, amazon.com and bbc.co.uk, however you can change that to any website you want in the destionations list (line 119).

Enjoy!