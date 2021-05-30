# Dynamixel_Python_TD
Using Dynamixel servos with TouchDesigner
You need to install this Python libraries (the best is with pip install)
Be sure you install in the proper folder for the right Python installation
- pythonosc https://pypi.org/project/python-osc/
- dynamixel python sdk https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/library_setup/python_windows/#python-windows
Install the .py and the .toe in the same folder. If you want that the D mapping works, install also the .fbx and .png files
Some settings are in the .py file:
- serial port
- osc port
- baudrate (better to leave at 1000000)
- and some other but for the begining, use defaults
In the .toe file, you can edit the dynamixelTable Dat with three cues:
- goal position
- speed
- acceleration
- treshold (if its too low, you have the risk to block the Python script, I search for a way to kill the process...)
- index of the motor
Pressing one of the buttons, you go to the cue
There is two outputs, one for the position in degrees, the other one for the movement.

Feel free to test it and change it for your usage.
A virtual beer for the person who find a way to kill the process.
I have prepared a script with the name of the process but its not working.
