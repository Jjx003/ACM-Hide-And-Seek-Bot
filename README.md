# ACM-Hide-And-Seek-Bot
My entry into the [UCSD ACM's Hide and Seek AI compeition :)](https://ai.acmucsd.com/tournaments/a0Zlpa/ranks)\
The bot's name is "	top ten anime betrayals"...

### Disclaimer:
This repository is open-sourced and free to reference, though it is not very well written. 
*Beware: major undocumented, spaghetti code
*Featuring: a lot of bugs

## Seeker Idea
Instead of calculating the shortest path to some destination per iteration, I decided to use the Floyd-Warshall algorithm to calculate the shortest paths of all pairs of nodes during setup. This was done just for convenience purposes.

With this, all seeker bots start in a "bounce" state that tells them to wander to arbitrary points across the map while marking nodes they come across as visited. Slowly but surely, the bots narrow down cells that are not visited. Admitedly, this was not a very good imlementation but it was good enough to almost always find hiders.

In the first instance a hider is spotted, all seeker bots are called to "swarm" on that single target and chase them down. If at any point the target disappears from sight, the bots are made to visit the last position that target hider was seen. If nothing is found, bots will continue bouncing.

This bounce-and-chase logic is essentially all the seeker does.

## Hider Idea
I realized that in order to achieve higher scores, it was necessary to implement a good hider. Seekers in general followed the same sort of wander and chase logic, so it was the hider logic that mattered most. This is where I spent the majority of my time writing code.

* The first idea of my hider was to run in the opposite direction of the seeker. Implementing this basic avoidance was enough to bring my bot to first in the live leaderboard, but I knew that it would not be enough.
* The second idea of my hider was to identify "wall islands," connected components of walls, that my hider could run around in circles. In this fashion, seekers would run around the islands chasing my hider -- but would always be one step behind. There would be no bad moves that would bring me to a dead-end unlike my first idea. To implement this feature, I ran scipy's convex hull algorithm on wall islands to identify the smallest bound of such islands. The vertices of the hull then, give us waypoints that my hider can run around.
