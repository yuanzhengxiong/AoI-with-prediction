# AoI with Prediction

This is a project aming to minimize the AoI (Age of Information) with the help of prediction. 

# Requirements

- python: 3.5+

# Usage

```
$ git clone https://github.com/jasonyuan97/AoI-with-prediction.git

# For Bernoulli Arrival:
$ python3 AoI/main.py -a Bernoulli -av <number of sequences to averge from> -t <time range> -p <Bernoulli parameter> -w <window size> -sew <step size equals window size or not>

# For Markovian Arrival:
$ python3 AoI/main.py -a Markovian -av <number of sequences to averge from> -t <time range> -p1 <Markovian parameter> -p2 <Markovian parameter> -w <window size> -sew <step size equals window size or not>
```
