# Programming vacancies compared

Python3 project that can perform following things:
1. Download top 10 programming languages vacancies in Moscow, Russia from [hh.ru](https://hh.ru/)
1. Download top 10 programming languages vacancies in Moscow, Russia from [superjob.ru](https://www.superjob.ru/)
3. Print statistics for found vacancies, processed vacancies and average salary in RUB for top 10 programming languages

## How to install

1. Register your app on [superjob.ru](https://api.superjob.ru/register) (Fill form with random info, they are not checking).
3. Create file ```.env``` in the directory with this script and put there your secret key, which can be found [here](https://api.superjob.ru/info/) ```.env``` file should look like this
```
SUPERJOB_APP_KEY=v3.r.130579387.1c87a178bb1c0dba3d4625093647117eab63d840.6780321530564ee19a2eecab8dde17a9b0666417
```
but with your data instead of presented above.

4. Python3 should be already installed. The script was made using `Python 3.7.3`. This version or higher should be fine.

5. Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

## How to use

Just start the script and wait a little.
```
$ python3 main.py
```
While data is downloading you will see something like this:
```
Python
Downloading page 0
Downloading page 1
Downloading page 2
C#
Downloading page 0
Downloading page 1
Downloading page 2
Downloading page 3
```
When data is downloaded you will see pretty tables with info:
```
+HeadHunter Moscow-------------+---------------------+----------------+
| language   | vacancies_found | vacancies_processed | average_salary |
+------------+-----------------+---------------------+----------------+
| Python     | 876             | 256                 | 148101         |
| JavaScript | 2217            | 736                 | 135870         |
| Java       | 1357            | 350                 | 167124         |
| Ruby       | 149             | 58                  | 156767         |
| PHP        | 967             | 476                 | 121693         |
| C++        | 775             | 231                 | 150619         |
| C#         | 873             | 269                 | 147652         |
| C          | 1246            | 454                 | 145001         |
| Go         | 244             | 72                  | 174222         |
+------------+-----------------+---------------------+----------------+
+SuperJob Moscow---------------+---------------------+----------------+
| language   | vacancies_found | vacancies_processed | average_salary |
+------------+-----------------+---------------------+----------------+
| Python     | 11              | 4                   | 128250         |
| JavaScript | 57              | 38                  | 109478         |
| Java       | 20              | 12                  | 153250         |
| Ruby       | 0               | 0                   | 0              |
| PHP        | 43              | 29                  | 105541         |
| C++        | 22              | 10                  | 123690         |
| C#         | 23              | 13                  | 125653         |
| C          | 16              | 6                   | 126400         |
| Go         | 1               | 1                   | 47500          |
+------------+-----------------+---------------------+----------------+
```

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
