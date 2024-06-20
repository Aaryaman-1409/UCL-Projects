This program can find the shortest path through a maze, and can also figure out if no possible path to the goal exists. 

## Usage

- Compile with `gcc -o main main.c graphics.c`
- Run `./main | java -jar drawapp.jar`

## Notes

How to organize parameter.txt file:

Line 1: Starting X position, Starting Y position
Line 2: Goal X position, Goal Y position 
Line 3-...: Obstacle i X position, Obstacle i Y position (one pair per line)

Example file:
3, 0
13, 19
1, 1
2, 5
3, 9

