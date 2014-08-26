LED Screen Build Notes
=========

Hardware
----
After some fussing we found Trammell Hudson's really excellent [Octoscroller](http://trmm.net/Octoscroller) and LEDscape project to interface with our low-level hardware.

### Adafruit

Buy a [BeagleBone Black](https://www.adafruit.com/product/1876), some [LED Panels](https://www.adafruit.com/product/420) and a nice [5V power supply](https://www.adafruit.com/products/658). 

### OSH Park

We also need an [Octoscroller cape](https://oshpark.com/shared_projects/7mSHNZcD). You can order the cape circuit board in sets of 3 from OSH Park! Share with a friend! The process takes two or three weeks.

### Digikey

Make a [DigiKey](http://www.digikey.com) order. Here are the parts you want:

| Quantity   | Part Number  | Description |
|---|---|---|
| 1  | 296-8503-5-ND  | 8-bit bus transceiver |
|  8 | S9171-ND  | 16 pin ribbon connector |
|  4 | S1012E-36-ND | Breakable header pins | 

### Soldering


Solder your hardware. The buffer IC goes on the underside of the circuit board. The hole in the ribbon cable connectors face towards the bottom of the PCB.

These LED panels use a lot of power. Make sure you have an adequate power supply or you may experience funny issues!


Software
----

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

Download [LED-bot](https://github.com/marqsm/LED-bot).

    git clone https://github.com/marqsm/LED-bot

You can install the python dependencies using the `requirements.txt` file

    pip install -r requirements.txt
