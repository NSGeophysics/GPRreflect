# GPRreflect
Python program to simulate zero-offset profile arrivals from hand-drawn reflectors

## Requirements
Python with numpy, scipy, matplotlib

Once you have python installed (https://www.python.org/) you can add packages using `pip`
Alternatively you can install Python with many packages from Anaconda (www.anaconda.com)

## How to run it 
Once you have python and all the required packages installed, run in the command line
`python GPRreflect.py`

## Instructions
Click on the canvas to add points for your first reflector. Once you are done, close the figure.

The program will smoothly interpolate your clicked positions (using a running mean) and will show you the result.

You can now add a second reflector by clicking again on the canvas. Close the figure when you are done.

Repeat until you have added all of your reflectors.

When you have no more reflectors to add, simply close the figure without clicking on the canvas.

A new figure will pop up showing the zero-offset profile together with a smooth version of your reflectors.
