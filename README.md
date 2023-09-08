# Developing a Raycasting screensaver (Windows 3.x / 95 labyrinth style) 

## How to run it?

With Python installed, run:

```bash
pip install -r requirements.txt
python main.py
```

## Scenery

![Labyrinth](https://s11.gifyu.com/images/S42IR.gif)

## Introduction

I had idea how to do this kind of screensaver for a long time, but I didn't have enough knowledge to do it. 
Now I have it, so I decided to do it.

## What is Raycasting?

Raycasting is a rendering technique to create a 3D perspective in a 2D map. 
It's used in games like Wolfenstein 3D, Doom, Duke Nukem 3D, etc.
It's the way that these games can render 3D environments in a 386 processor.

## How does it work?

The idea is to cast a ray from the player position to the direction that the player is looking. 

Then, the ray is casted again, but this time, it's casted to the next column of the screen.

The ray is casted until it hits a wall. 

When it hits a wall, the distance between the player and the wall is calculated. 

Then, the height of the wall is calculated using the distance and the height of the screen.

You can move it manually with the arrow keys, or just let it run.

## How to do it?

I use Python to do it. PyGame is your friend.

First, we need to create a map.

The map is a 2D array of integers.

The map is something like this:

```python
[
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]
```

Next, we need to create a player/camera. The player/camera is an object with a position and a direction.

And finally, we need to cast the rays.

The rays are casted from the player position to the direction that the player is looking. 
Then, the ray is casted again, but this time, it's casted to the next column of the screen.

Also we have a minimap. The minimap is a 2D array of integers with the position of the player and the walls.

## License

This project is licensed under GPL-3.0 Licensed by @bitstuffing with love.

## References

- [Raycasting](https://en.wikipedia.org/wiki/Ray_casting)
- [Lode's Computer Graphics Tutorial](https://lodev.org/cgtutor/raycasting.html)
- [Wolfenstein 3D](https://en.wikipedia.org/wiki/Wolfenstein_3D)
- [Doom](https://en.wikipedia.org/wiki/Doom_(1993_video_game))
- [Duke Nukem 3D](https://en.wikipedia.org/wiki/Duke_Nukem_3D)
