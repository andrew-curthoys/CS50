# CS50 Final Project: *Dick or <span>Don.c</span>om*

## Andrew Curthoys

## Who said it: Richard Nixon or Donald Trump?

### Youtube link to project description and demonstration: https://youtu.be/3XlUdsQGuy4

## Background

The impetus for this project was born 2 years ago while I was listening to
season 1 of the *Slow Burn* podcast. The season took an in-depth look at
Richard Nixon and the Watergate investigation. It was fascinating to hear how
the investigation unfolded as someone who didn't live through it, because it
always seemed like a foregone conclusion to me looking at it through a
historical lens. However, stepping through all the reports, bombshells, and the
releasing of the White House tapes in "real time" gave me an all new perspective
on the incident.

Concurrent with my listening to the podcast was the Mueller investigation of
Donald Trump. Some of the things that Nixon said about the Watergate
investigation, most specifically regarding the media and a "conspiracy" out to
get him, were eerily similar to many of the things Trump was saying at the time.
I thought it would be a funny/interesting exercise to see if people could tell
the difference between quotes from the two. At the time I had no idea how to
build a website/webapp, but I came up with the name DickOrDon.com and I couldn’t
stop thinking about it. With the skills I learned in CS50, I became comfortable
with building a webapp and decided to finally give it a shot.

I tried to pick quotes that would make people think, and not the most obvious
ones. There are some off color quotes with elements of racism and misogyny,
which I have chosen to include because I want to paint the full picture of what
these men believe(d) and what they might have said behind closed doors.

## Webapp Structure and Operation

I have populated a SQLite database with nearly 100 quotes, half from Nixon, half
from Trump. Each quote has a quote ID and when the webapp is launched, a random
number is generated using the **random** module in Python. This random number is
then used to pull a quote from the SQLite DB, which is then presented to the
user. The user has two buttons to choose whether they think it was Nixon or
Trump who said it. The buttons are stylized using CSS and an assortment of
randomly selected photos of each man. Each template utilizes Bootstrap custom
media queries to adjust font size based on device type to allow easy usage on
mobile and laptop/desktop devices alike.

Once the user makes a selection, the Python script checks the answer against who
actually said the quote and returns a template with either a correct or
incorrect message. I have selected another set of photos for each man looking
happy or disappointed, which are randomly selected depending on a correct or
incorrect guess. A JavaScript script counts down from 5 to automatically load a
new quote. Alternatively, there is a button that can be pushed to load a new
quote before the timer runs out, or the user can click the DickorDon.com
header to load a new quote as well. The JavaScript also displays the user’s
stats, i.e. how many they have gotten correct and their % correct.

The quote IDs that have been used each session are stored in a list and excluded
from the next time a user is prompted to guess. If the user goes through all
quotes in the set, the list of used quote IDs is reset and the user is presented
with a random quote from the entire set of quotes and the process begins anew.


## Future Plans

I plan to publish the webapp to DickOrDon.com, the domain of which I have
purchased through AWS. I have experience publishing a static website through
AWS Route 53 with the use of an S3 bucket, so I hope to expand on that with this
webapp. I am planning to take the CS50 Web Programming edX class, where I hope
to learn skills that can add features or functionality to this webapp and build
many, many more web programs.

Finally, I want to thank David Malan and the entire CS50 staff for their hard
work and dedication. The passion that professor Malan displays during the
lectures is infectious and has fed my interest in computer science. I can say
without a doubt this was one of the most enjoyable (and challenging!) courses I
have ever taken. I cannot recommend this class highly enough, and I plan to
point anybody who is interested in coding and wondering where to start directly
to this course.

Thank you again for everything, and have a Happy New Year!
