# python-raspberry-alarm
A python script that can be used with a Raspberry Pi, PIR Sensor and Pi Camera as an alarm.

For the application to run there needs to be a "imgMail/" folder right next to the python file, this folder is used to store the images from the camera.

The Pi camera also has to work, use the raspi-config command to enable it.

Make sure to connect the PIR sensor correctly, one pin requires voltage (usually 5v), another is the mass, and the third is usually the data pin, the "GPIO_PIR" variable is used to define this pin.
