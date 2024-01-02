Contingency Core 1A6F
by Draconas
for Stellaris ModJam 2024

Contributers
Draconas

This mod requires Synthetic Dawn to operate.  Attempting to run it without SD is a violation of PDX terms of use.

Acknowledgements
While all the work is mine, I must acknowledge those that have gone before that inspired bits of it, either concepts, or code.
Gigastructural Engineering by Elowiny and the team, which is my go to source for "that is bats**t crazy, I wonder if it's possible?" at which point some searching though the code usually finds that 1. Gigas does it, and 2. they are doing it in a surprisingly elegant way that I had no idea was possible.
Machine and Robot Expansion by XVCV, which first did Synth -> Machine Intelligence many years ago, which meant I knew that the core concept for this mod was at least theoretically possible, without knowing that it had been done I probably wouldn't have tried given the time constraints as its such a massive shift.


Code style:
All files are prefixed with condan_ (required by PDX, but good practice)
All things added by the mod are prefixed with condan_ except things that have a defined vanilla prefix (e.g. deposits being d_) in which case condan_ will be the first thing after the prefix.
Scripted triggers are all condan_[questioning word]
Scripted effects should be condan_[verb]
Sometimes I broke the above prefix guide and went [verb]_condan_ especally on things being done to condan itself, because it read better.  Everything has condan in it somewhere thought to prevent clashes.