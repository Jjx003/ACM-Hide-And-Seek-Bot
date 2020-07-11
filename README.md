# ACM-Hide-And-Seek-Bot
My entry into the [UCSD ACM's Hide and Seek AI competition :)](https://ai.acmucsd.com/tournaments/a0Zlpa/ranks)\
This bot, which I named "top ten anime betrayals," managed to win second place 🥈

## Fellow Competing Bots <3
* 🥇 Joe Cai's first place "pizza" (Currently unavailable)
* 🥉 [Kevin He's third place "botpwner"] (https://github.com/kevin-he-01/hide-and-seek-bot)
* 🎉 [Ishaan Kavoori's fourth place "Ultron"](https://github.com/ishaanharry/ACM-AI-Competition-HideAndSeek)
* 🎉 [Stone Tao's fifth "breadbot"](https://github.com/acmucsd/hide-and-seek-ai/tree/master/breadbot)



### Disclaimer:
This repository is open-sourced and free to reference, though it is not very well written.
* *Beware: major undocumented, spaghetti code*
* *Featuring: many bugs*

## Seeker Idea
Instead of calculating the shortest path to some destination per iteration, I decided to use the Floyd-Warshall algorithm to calculate the shortest paths of all pairs of nodes during setup. This was done just for convenience purposes.

With this, all seeker bots start in a "bounce" state that tells them to wander to arbitrary points across the map while marking nodes they come across as visited. Slowly but surely, the bots narrow down cells that are not visited. Admittedly, this was not a very good implementation but it was good enough to almost always find hiders.

In the first instance that a hider is spotted, all seeker bots are called to "swarm" on that single target and chase them down. If at any point the target disappears, the bots are made to visit the last position that the target hider was seen. If nothing is found, bots will continue bouncing.

This bounce-and-chase logic is essentially all the seeker does.

## Hider Idea
I realized that to achieve higher scores, it was necessary to implement a good hider. Seekers, in general, followed the same sort of wander-and-chase logic, so it was the hider logic that mattered most. This is where I spent the majority of my time writing code.

* The first idea of my hider was to run in the opposite direction of the seeker. Implementing this basic avoidance was enough to bring my bot to first in the live leaderboard, but I knew that it would not be enough. This strategy was riddled with holes and my implementation was buggy too.
* The second idea of my hider was to identify "wall islands," connected components of walls, that my hider could run around in circles. In this fashion, seekers would run around the islands chasing my hider -- but would always be one step behind. Unlike my first idea, there would be no bad moves made that would bring my hiders to a dead-end (e.g. running into a bad corner). To implement this feature, I ran scipy's convex hull algorithm on wall islands to identify the smallest bound of such islands. The vertices of the hull would give my hiders waypoints to run around.

![Demo Video](assets/gameplay.gif)

## Future Improvements
"top ten anime betrayals" is by no means a smart/perfect bot. There were a lot of improvements that could have been made to both the bot and the code itself. Here are some ideas for the future:

Seeker
-------
* Instead of choosing random points, have all visible points marked as visited. Then within the range of vision, if there are any, choose points that are hidden as the next task to visit. Once all of these initially hidden points are all visited, choose the next set of points that remain invisible to you from your current position.
* When the hider suddenly disappears, keep track of it's last seen position. Then, for every step that the hider still isn't seen, extend the last seen position in a BFS fashion so that we have a growing list of possible positions that the hider moved to. This would give us better idea of the general position(s) to move to when hiders disappear from sight.

Hider
-------
* When threatened on both ends of an island, jump to a new island.
* Make hiders spread between different islands if possible. (Currently have a tendency of all sticking to same island).
* ????
* profit




