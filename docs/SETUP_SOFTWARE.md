Software Setup
----

### Debian

This tutorial assumes [Debian](http://elinux.org/BeagleBoardDebian) or Ubuntu is installed on your Beaglebone (older revisions may use Angstrom Linux)! If you are not using one of these distributions, it is recommended that you re-flash to ease the installation process.

### LEDscape

Install [LEDscape](https://github.com/osresearch/LEDscape/) on the Beaglebone and copy the device tree overlay to `/lib/firmware/`

    git clone https://github.com/osresearch/LEDscape/
    cd LEDscape
    make
    sudo cp ./dts/CAPE-BONE-OCTO-00A0.dtbo /lib/firmware

Setup your matrix layout in `default.config` (in our case we have 4 panels in a 64x32 matrix). You specify the channel 0-7, and can chain up to 8 boards on each channel. Then the orientation (N,L,R,U) and x,y offset.

	matrix16
	0,6 N 0,0
	0,7 N 32,0
	1,6 N 0,16
	1,7 N 32,16

You can test things with:

	sudo ./bin/run-ledscape default.config
    sudo ./bin/identify default.config
	sudo ./bin/opc-rx 

If things aren't working:

* Adjust height and width values  in [./src/net/opc-rx.c](https://github.com/osresearch/LEDscape/blob/master/src/net/opc-rx.c#L64
) and settings at the bottom of [./src/ledscape/ledscape.c](https://github.com/osresearch/LEDscape/blob/master/src/ledscape/ledscape.c#L622)
* If you're seeing errors about PRU or Device Tree, follow the [instructions here](https://github.com/Yona-Appletree/LEDscape/#installation-and-usage) about disabling the built-in HDMI capes and replacing your device tree (am335x-boneblack.dtb). 

* Take a look at LEDscape's newly written [setup guide](https://github.com/osresearch/LEDscape/blob/master/Setup.md)
* Older [LEDscape setup guide](http://trmm.net/LEDscape/Setup)
* [Google Group](https://groups.google.com/forum/#!forum/ledscape)


### LED-bot

Make sure your system has these packages installed, libfreetype and libjpeg are needed so [Pillow](https://pillow.readthedocs.org/en/latest/) will build with support for JPG and TrueType Font rendering:

    sudo apt-get install build-essential python-dev libfreetype6-dev libjpeg-dev git


Download [LED-bot](https://github.com/marqsm/LED-bot).

    git clone https://github.com/marqsm/LED-bot

You can install the led bot software by:

    python setup.py install 

If you wish to install a development version, so you can test your changes, use

    python setup.py develop

To run the bot, run

    led-bot

To edit the default config file, you can use your favorite text editor:

    vim ~/.led-bot.conf
    nano ~/.led-bot.conf

If you'd like to make an adjustment to which listeners launch at start-up, take a look at [main()](https://github.com/marqsm/LED-bot/blob/master/LEDBot/bot_scheduler.py#L222) in `bot_scheduler.py` 

### Debian start-up script

This start-up script will run LED-bot and LEDscape when your Beaglebone boots. To install it follow these steps:

Copy the [start-up script](https://github.com/marqsm/LED-bot/blob/master/startup/ledbot.sh) to `/etc/init.d/`

    sudo cp ~/LED-Bot/startup/ledbot.sh /etc/init.d
    sudo chmod +x /etc/init.d/ledbot.sh`
    sudo update-rc.d ledbot.sh defaults