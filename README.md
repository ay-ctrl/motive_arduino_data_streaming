**Real-Time Position Transfer with OptiTrack**

This project was developed to transfer position data obtained from the OptiTrack motion tracking system to an Arduino, and from there to another Arduino via Bluetooth in real time.

At the core of the system, the position information of an object defined in the scene is obtained using Python and sent to the Arduino via the serial port. The first Arduino then transmits this data to the second Arduino over Bluetooth. This setup enables the sharing of position data in mobile or wireless systems.

To set up the system, you can refer to the Real-Time Position Sharing with OptiTrack Guide file.

In the project, instead of using OptiTrack’s official NatNet SDK directly, a Python wrapper developed by the community was preferred.

🔗 Reference GitHub repository: https://github.com/TimSchneider42/python-natnet-client
