Software Setup
----

### Debian

This tutorial assumes [Debian](http://elinux.org/BeagleBoardDebian) or Ubuntu is installed on your Beaglebone (older revisions may use Angstrom Linux)! If you are not using one of these distros, it is recommended that you re-flash to ease the installation process.

If things are not working or you find you're having PRU/Device Tree wonkiness, follow the [instructions here](https://github.com/Yona-Appletree/LEDscape/#installation-and-usage) about replacing your am335x-boneblack.dtb

### LEDscape

Install [LEDscape](https://github.com/osresearch/LEDscape/) on the Beaglebone.

    git clone https://github.com/osresearch/LEDscape/
    cd LEDscape
    make

Setup your matrix layout in `default.config` (in our case we have 4 panels in a 64x32 matrix). You specify the channel 0-7, and can chain up to 8 boards on each channel. Then the orientation (N,L,R,U) and x,y offset.

	matrix16
	0,6 N 0,0
	0,7 N 32,0
	1,6 N 0,16
	1,7 N 32,16

You can test things with:

	sudo ./bin/run-ledscape default.config
    sudo ./bin/identify default.config
	sudo ./bin/opc-rx default.config

If things aren't working:

* Take a look at LEDscape's newly written [setup guide](https://github.com/osresearch/LEDscape/blob/master/Setup.md)
* Muck around with `./src/net/opc-rx.c` and settings at the bottom of `./src/ledscape/ledscape.c`
* Older [LEDscape setup guide](http://trmm.net/LEDscape/Setup)
* [Google Group](https://groups.google.com/forum/#!forum/ledscape)

### LED-bot

Make sure your system has these packages installed so [Pillow](https://pillow.readthedocs.org/en/latest/) will build with support for JPG and TTF rendering:

    sudo apt-get install build-essential libfreetype6-dev libjpeg-dev


Download [LED-bot](https://github.com/marqsm/LED-bot).

    git clone https://github.com/marqsm/LED-bot

You can install the led bot software by:

    python setup.py install 

If you wish to install a development version, so you can test your changes, use

    python setup.py develop

To run the bot, run

    led-bot

### Debian start-up script

Copy the [start-up script](https://github.com/marqsm/LED-bot/blob/master/startup/ledbot.sh) to `/etc/init.d/`

`sudo chmod +x ledbot.sh`

`sudo update-rc.d ledbot.sh defaults`