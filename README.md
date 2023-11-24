# ipchain_test

## Запуск
Скачиваем проект
```shell
git clone git@github.com:BudjakovDmitry/ipchain_test.git
cd ipchain_test
```

Запуск тестов
```shell
python3 test.py
```

Расчет операторов
```shell
python3 main.py
```



## Общее описание
Класс `TimeLine` представляет собой временную ось, разделенную на дискретные промежутки в 1 минуту. На этой оси
отмечаются звонки. У каждого звонка (класс `Call`) есть дата начала и дата окончания. Когда звонок попадает на ось,
на всем его интервале ставится отметка, что требуется один оператор. Если у другой звонок попадает в этот же промежуток,
на пересечении их интервалов количество операторов увеличивается.

Уже перед самой отправкой пришла в голову идея, что можно сделать эффективнее по памяти: если предварительно
отсортировать лог в хронологическом порядке. В этом случае у нас получилась бы очередь: входящий звонок добавляется в
очередь, завершающийся звонок покидает очередь. Минимальное число операторов определяется как максимальная длинна
очереди.
