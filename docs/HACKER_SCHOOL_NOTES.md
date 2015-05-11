Installation Notes
----

### Current Setup

Recurse Center's LEDBot is awesome, though at present our cord situation is a little quirky (we have 3 cords).

* Large 5V Power Adapter - Goes to connector LED panel's barrel connector
* Small 5V Power Adapter - Connects to the Beaglebone Black's barrel connector
* Ethernet Cable - Connects to the Beaglebone Black's Ethernet port

### Possible Improvements

* Consolidate power to a single line
* Move from ethernet to [USB wifi adapter](https://wiki.debian.org/WiFi/HowToUse#Command_Line)

Notes:

We tried to use a single power adapter for the Beaglebone and the LEDs but ran into stability issues. If we put a [capacitor](https://www.adafruit.com/products/1589) on the power we could probably run a single line.

When we tried to connect via wifi we noticed:

1. Lag when streaming OPC packets over the network
2. Periodic trouble getting a DHCP lease

### Connecting to the Beaglebone

The beaglebone lives at `ledbone.local` on the Recurse Center network. If you can't find it here is another way you can conncet.

Find your IP Address with `ifconfig` or sometimes `ip addr`

You should see something like `	inet 10.0.0.100 netmask 0xffff0000 broadcast 10.0.255.255`

Lets say our IP is 10.0.0.100
#### Use nmap to scan the local network

On Linux:
> sudo apt-get install nmap

Or Mac:
> brew install nmap

Search the local network
> sudo nmap -sP 10.0.0.0/24

Look for a result that contains `Texas Instruments` like:
>Nmap scan report for 10.0.0.102

>Host is up (0.0048s latency).

>MAC Address: 1C:BA:DE:AD:BE:EF (Texas Instruments)

SSH into it
> ssh debian@10.0.0.102
