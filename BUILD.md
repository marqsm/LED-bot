LED Screen Build Notes
=========

Hardware
----
After some fussing we found Trammell Hudson's really excellent [Octoscroller](http://trmm.net/Octoscroller) project to interface with our low-level hardware.

Buy a [BeagleBone Black](https://www.adafruit.com/product/1876) and a [Octoscroller Cape](https://oshpark.com/shared_projects/7mSHNZcD), you can order them in sets of 3 from OSH Park. It takes two-three weeks.

Make a [DigiKey](http://www.digikey.com) order. Here are the parts you want

| Quantity   | Part Number  | Description |
|---|---|---|
| 1  | 296-8503-5-ND  | 8-bit bus transceiver |
|  8 | S9171-ND  | 16 pin ribbon connector |
|  4 | S1012E-36-ND | Breakable header pins | 


Solder your hardware. The buffer IC goes on the underside of the circuit board. The hole in the ribbon cable connectors face towards the bottom of the PCB.

Software
----

First you need to install [LEDscape](https://github.com/osresearch/LEDscape/) on the Beaglebone.

Follow their [newly written, setup instructions](https://github.com/osresearch/LEDscape/blob/master/Setup.md). 

Download [LED-bot](https://github.com/marqsm/LED-bot). 

You'll probably need some python dependencies

* zulip
* Pillow