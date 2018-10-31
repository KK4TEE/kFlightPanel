# kFlightPanel
A Navbal and indicator readout for your 2nd monitor, using Python and Telemachus for Kerbal Space Program

![kFlightPanel Screenshot](doc/img/2018-10-31-kFlightPanel.jpg?raw=true "kFlightPanel Screenshot")

Based on the spirit of the [Control-Panel](https://github.com/KK4TEE/Control-Panel) application, this is a near complete rewrite using PyGame instead of nCurses. Calls to [Telemachus](https://github.com/KSP-Telemachus/Telemachus) are streamlined, a nav ball is operational, and performance is above 5 fps on my test computer. Time to start getting your ship's data on another computer screen!

To use:
  * In [config.py](config.py) - Edit the IP address of your computer running Kerbal Space Program with the Telemachus mod installed 
  * Optionally configure the fullscreen or windowed mode by commenting ("#") out the appropriate line
  * Launch the program using "python kFlightPanel.py"
  
If the application is unable to connect to Telemachus/KSP, it will enter a demo mode where the navball rotates in place. If this happens, check your IP address in [config.py](config.py) as well as your firewall on both computers.
  
Requirements:
  * This application requires [PyGame](https://www.pygame.org/) libraries, and is only tested on Python 2.7.6 on Ubuntu Linux
  * [Telemachus](https://github.com/KSP-Telemachus/Telemachus) mod for Kerbal Space Program
  * IPv4 Networking (localhost and remote are both supported)
  
Future Plans:
  * Update to Python 3
  * Better handling of different screen sizes
  * Connection stability improvements and error handling
