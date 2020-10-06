
# Pacman game with Algorithms

### [Project Link](https://github.com/d4tAloUh/pacman-OWI)

#### Used pacman from [github](https://github.com/hbokmann/Pacman)

## This project was done by Karmeliuk Kostiantyn, Kupchyk Daryna, Myronovych Oleksandr.
#### Karmeliuk - made base for project
#### Myronovych - added parsing levels from files
#### Kupchyk - written bfs with team
____
**To start up the project do the following commands**<br>
Requires python 3.6+
```
1. python -m venv myvenv
2. cd myvenv/Scripts/
3. activate
cd ../..
4. pip install -r requirements.txt
5. python pacman.py
```
---
# Results   
### Tick was 60 fps
| Algorithm     | Time          | Memory usage  |  Pacman Moves| Algo Moves | Path |
| ------------- |:-------------:| -------------:| ------------:| --------:| ------:|
| DFS           |   4.67 sec    | 35.405 MB     | 281          | 166     | RRUURRRRRRDDRRUUUULLUULLL + |
|               |               |               |              |         | + LLLDDLLUUUULLLUURRRUULLL |
| BFS           | 17.58 sec     | 35.241 MB     | 1055         | 120     | UUUUUUUUUUUULLL |
