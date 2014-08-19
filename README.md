hs-screen
=========

Currently pipeline is working, supports to commands.

| command                              | parameters         | 
| ------------------------------------ | ------------------ |
| ```led-bot show-image <imagename>``` | image needs to be on the same server & directory where bot is running.  |
| ```led-bot show-text <text>```       | text supports currently only 1 word.  |

TODO:
- Fix to support longer texts for "show-text"
- add support to animated gifs
- Add fetching of remote images, if imagename is an URL
- Add commands for sampling / scrolling images, if they are too big for the screen
- Add possibility to move an image across the screen (like immobile pacman) - of course way cooler with animated gifs


DONE:  
x Hardware soldering  
x Figure out software dependencies on beagleBone for OpenPixel  
x Learn OpenPixel file format  
x Build Zulip bot  
x Get communication from server to hardware  
x Figure out conversion from raw data to OpenPixel format  

Goal:

(done) 1. Reference app running from network to HW

