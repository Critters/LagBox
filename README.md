A RaspberryPi-based device to test how your mobile games/app copes with lag and packet loss. The device bridges a WiFi connection with a wired connection and lets the user set the packet delay in ms and the loss as a percentage using a rotary encoder and an OLED display, housed in a 3D-printed enclosure

Setup:
Install Adafruit's OLED display lib and dependencies: https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black/usage

I followed thse guides on how to make a WiFi hotspot: 1) https://howtoraspberrypi.com/create-a-wi-fi-hotspot-in-less-than-10-minutes-with-pi-raspberry/ 2) https://www.raspberrypi.org/forums/viewtopic.php?t=132674

This is where I found out about how to add delay and loss to packets in Linux, the app uses these commands. If you want to skip over using an OLED and encoder and just hook the pi up to a monitor and keyboard you can use them to add the delay/loss using the command prompt: https://stackoverflow.com/questions/614795/simulate-delayed-and-dropped-packets-on-linux

The pinout for the rotary encoder is in the code, the OLED was wired using the instructions on the above Adafruit site