# Terminal weather

A lightweight command-line weather app that brings current conditions straight into your terminal. No extra UI, no bloated dependencies — just clean city lookup, temperature, wind speed, and weather descriptions from Open-Meteo.

## Why it exists

Because checking the weather should be as simple as typing one command.

## Features

- Search any city by name
- Fetch live weather from Open-Meteo
- Show temperature, wind, time, and condition
- Works in plain Windows terminal or PowerShell
- No install path changes required if you use `setup.py`

## Usage

Run from the project folder:

```bash
python Main.py London
```

Or just run:

```bash
python Main.py
```

Then type a city name when prompted.

## Install locally

To make the folder available on your user `PATH` and create a command wrapper:

```bash
python setup.py
```

After that, open a new terminal and run:

```bash
weather
```

## Notes

- `Main.py` is the core weather fetcher.
- `setup.py` adds the project folder to your user PATH and creates `weather.cmd`.
- The wrapper keeps your project where it is, so it never moves files into `C:\Windows`.
