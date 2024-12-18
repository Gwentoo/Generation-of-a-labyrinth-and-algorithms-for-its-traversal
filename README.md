___
# Информация
В данной работе на языке Python был реализован алгоритм создания лабиринтов, а также три алгоритма обхода лабиринта - DFS, BFS и A*. Также были построены графики для сравнения этих алгоритмов. 
___
# Лабиринт
Для построения лабиринта был использован алгоритм Recursive Backtracker, по своей сути это обход в глубину, но в матрице. <p> 
1. Случайным образом выбирается начальная точка и добавляется в стек
2. Цикл, пока стек не пустой
    * Достаём из стека клетку и считаем её текущей
    * Если среди смежных с ней клеток имеются непосещённые
        * Отправляем текущую клетку в стек
        * Выбираем случайную смежную клетку
        * Отмечаем клетку посещённой и убираем её в стек
    * Иначе удаляем клетку из стека

Данный алгоритм создает лабиринт без циклов, а значит путь от начальной до конечной точки существует только один. Более подробно про этот алгоритм можно почитать в [статье](https://habr.com/ru/articles/778202/) на хабре.

[1]: Функция choice_transition возвращает кортеж из координат следующей клетки (для  матрицы достижимости и матрицы переходов). Параметры mode и finish будут нужны позже для реализации алгоритмов.

<img src="maze.jpg" alt="Альтернативный текст" width="300" height="300"/>

Чтобы добавить в лабиринт циклы можно случайным образом убирать стены, у которых 2 смежные противоположные стороны одного цвета, а другие 2 смежные стороны другого.
После этого добавим начальную и конечную точку.

Тогда мы получим следующее:

<img src="maze2.jpg" alt="Альтернативный текст" width="300" height="300"/>

___ 
# Пример обохода [DFS](https://ru.wikipedia.org/wiki/Поиск_в_глубину)

![](Gifs/DFS/DFS2.gif)
___

# [AStar](https://ru.wikipedia.org/wiki/A*#:~:text=A%20star)
Эврестический алгоритм, в котором порядок обхода определяется какой-либо функцией. В данной работе в качестве метрики для определения следующей клетки было использовано евклидово расстояние между следующей клеткой и финишем. Приоритет отдается клетке с наименьшим расстоянием.

Примеры работы A*

![](Gifs/AStar/AStar1.gif)
![](Gifs/AStar/AStar3.gif)

Особенно хорошо он справляется с сильно разреженными лабиринтами (но не всегда)
___
# [BFS](https://ru.wikipedia.org/wiki/Поиск_в_ширину)
Главное отличие BFS от прошлых обходов в том, что он позволяет находить наилучший путь из всех возможных (либо один из лучших, если таких несколько).

Для его реализации нужно снова изменить функцию choice_transition, по итогу она будет выглядеть так:

Примеры работы BFS:

![](Gifs/BFS/BFS1.gif)
![](Gifs/BFS/BFS3.gif)

___
# Сравнение и графики
Я сделал 500 запусков алгоритмов, каждый раз генерируя новый лабиринт. На каждой итерации я сохранял затраченное время и длину пути, который нашел алгоритм.

Для лабиринта размером 79x79 он выглядит следующим образом:

<div style="text-align: center;">
    Графики длины и времени для лабиринта 79x79
</div>

![](Graphics/79x79.png)

Ожидаемо, что самые короткие пути находил BFS, так же можно увидеть, что в среднем A* находил более короткие пути, чем DFS. 

Если говорить о времени, то можно сказать, что самым долгим оказался DFS, однако были  лабиринты, в которых A* справлялся дольше.

Средняя длина пути для алгоритмов:
* DFS - 603
* AStar - 390
* BFS - 177

Похожая картина наблюдается и для лабиринтов поменьше

<div style="text-align: center;">
    Графики длины и времени для лабиринта 9x9
</div>

![](Graphics/9x9_5.png)

С длинами путей всё остаётся по-прежнему, а затраченное время настолько мало, что нет смысла его сравнивать.

Средние длины пути для алгоритмов:
* DFS - 16
* AStar - 10
* BFS - 9
___
# Итог
Наиболее эффективным оказался обход в ширину (BFS), самым неэффективным обход в глубину (DFS), но при помощи добавления функции выбора клетки получилось сократить путь почти в 2 раза (A*). Также, для лабиринтов небольшого размера длины путей BFS и AStar практически не отличаются 

### Код, а также графики и гифки лежат в репозитории.
___
