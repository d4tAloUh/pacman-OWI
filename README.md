



##
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
##### A test and A* uses different written algorithm (different heuristic)
### Tick was 60 fps
#### 1st map test

| Algorithm     | Time          | Memory usage  |  Pacman Moves| Algo Moves | Path |
| ------------- |:-------------:| -------------:| ------------:| --------:| ------:|
| DFS           |   4.666 sec    | 35.549 MB     | 281          | 166     | RRUURRRRRRDDRRUUUULLUULL + |
|               |               |               |              |         | + LLLLDDLLUUUULLLUURRRUULLL |
| BFS           | 17.957 sec     | 35.536 MB     | 1055          | 120     | UUUUUUUUUUUULLL |
| Greedy        | 0.240 sec     | 35.426 MB     | 15          | 16     | UUUUUUUUUUUULLL |
| A*            | 2.944 sec     | 35.512 MB     | 177          | 36     | UUUUUUUUUUUULLL |
| A* test       | 2.999 sec     | 35.606 MB     | 177         | 36     | UUUUUUUUUUUULLL |

#### 3rd map test
| Algorithm     | Time          | Memory usage  |  Pacman Moves| Algo Moves | Path |
| ------------- |:-------------:| -------------:| ------------:| --------:| ------:|
| DFS           |   0.634 sec    | 35.151 MB     | 39          | 40     | RRDLLLLDRRRRRRRRRRRR + |
|               |               |               |              |         | + RRRRULLLLLLLLLLURRR |
| BFS           | 6.305 sec     | 35.475 MB     | 377          | 57     | DDRRRRUURRR |
| Greedy        | 0.416 sec     | 35.999 MB     | 25          | 16     | RRDDRRUURRR |
| A*            | 1.011 sec     | 35.434 MB     | 61          | 26     | RRDDRRUURRR |
| A* test       | 1.697 sec     | 35.237 MB     | 103         | 32     | RRDDRRUURRR |


#### 2nd map test
| Algorithm     | Time          | Memory usage  |  Pacman Moves| Algo Moves | Path |
| ------------- |:-------------:| -------------:| ------------:| --------:| ------:|
| DFS           |   4.103 sec    | 35.368 MB     | 247          | 194     | RRDLLLLLLLLLLLDDLLUULLLURRRRRRULLLLLLUR + |
|               |                |               |              |       | + RRRRRULLLLLLURRRRRRRRRRRRRRRRULLLLLLLLLLLLLLLLU + |
|               |                |               |              |       | + RRRRRRRRRRRRRRRRULLLLLLLLLURRRRRRRRRULLLLLLLLLLLLLLLL |
| BFS           | 36.601 sec      | 35.516 MB     | 2171         | 217     | DLLLLLLLLUUUUUUURUUULLLLLLL |
| Greedy        | 3.573 sec      | 35.209 MB     | 215         | 63     | UULLLLLLDDDLLUUUUUUURUUULLLLLLL |
| A*            | 9.967 sec      | 35.377 MB     | 597         | 97     | LLLLLLDLLUUUUURUUUUULLLLLLL |
| A* test       | 12.388 sec     | 35.307 MB     | 725         | 107     | LLLLLLDLLUUUUUUURUUULLLLLLL |