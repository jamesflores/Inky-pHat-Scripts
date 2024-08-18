# Inky-pHat-Scripts

A collection of Python scripts for displaying data on the Pimoroni Inky pHAT eInk Display (Black/White) using a Raspberry Pi Zero W.

## Requirements

- Raspberry Pi Zero W (or any other compatible Pi with GPIO pins)
- Pimoroni Inky pHAT - eInk Display (Black/White)
- Python 3.x

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/jamesflores/Inky-pHat-Scripts.git
   cd Inky-pHat-Scripts
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the desired script using Python. For example:

```
python script_name.py
```

## Scheduling with Cron

To schedule a script to run periodically, you can use cron:

1. Open the crontab file:
   ```
   crontab -e
   ```

2. Add a line to schedule your script. For example, to run a script every hour:
   ```
   0 * * * * /bin/bash -c 'source /home/pi/Inky-pHat-Scripts/venv/bin/activate && /home/pi/Inky-pHat-Scripts/script_name.py'
   ```

   Adjust the timing and path as needed.

3. Save and exit the crontab editor.

## Contributing

Feel free to open issues or submit pull requests with improvements or new scripts.

## License

MIT Licence
