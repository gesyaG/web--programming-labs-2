from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)
@app.route("/menu")
def menu():
    return """
<!DOCTYPE html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список Лабораторных
        </header>

        <a href="/lab1">Первая лабораторная</a>

        <footer>
            &copy; Александр Герасимов, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""
@app.route("/lab1")
def lab1():
    return '''
<!DOCTYPE html>
<html>
    <head>
        <title>Герасимов Александр Александрович, лабораторная работа 1</title>
        <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') +'''">
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>web-сервер на flask</h1>

        <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.
        </p>
        <a href="/menu">Меню</a>

        <h2>Реализованные роуты</h2>
        <div>
            <ul>
                <li>
                    <a href="/lab1/oak">Дуб</a>
                </li>
                <li>
                    <a href="/lab1/student">Студент</a>
                </li>
                <li>
                    <a href="/lab1/python">Python</a>
                </li>
                 <li>
                    <a href="/lab1/gesya">Личный роут</a>
                </li>
            </ul>
        </div>

        <footer>
            &copy; Александр Герасимов, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''

@app.route('/lab1/oak')
def oak():
    return '''
<!doctype html>
    <head>
       <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') +'''">
    </head>
<html>
    <header>
            НГТУ, ФБ, Лабораторная работа 1
    </header>

    <body>
        <h1>Дуб</h1>
        <img class="oak" src="''' + url_for('static', filename='oak.png') + '''">
    </body>

    <footer>
            &copy; Александр Герасимов, ФБИ-23, 3 курс, 2024
    </footer>
</html>
'''

@app.route('/lab1/student')
def student():
        return '''
<!doctype html>
    <head>
       <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') +'''">
    </head>
<html>
    <header>
            НГТУ, ФБ, Лабораторная работа 1
    </header>
    <body>
        <h2>Герасимов Александр Александрович</h2>
        <img class="logo" src="''' + url_for('static', filename='logo.png') + '''">
    </body>

    <footer>
            &copy; Александр Герасимов, ФБИ-23, 3 курс, 2024
    </footer>
</html>
'''

@app.route('/lab1/python')
def python():
        return '''
<!doctype html>
    <head>
       <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') +'''">
    </head>
<html>
    <header>
            НГТУ, ФБ, Лабораторная работа 1
    </header>
    <body>
        <p>
            Python — это высокоуровневый язык программирования, 
            отличающийся эффективностью, простотой и универсальностью
            использования. Он широко применяется в разработке веб-приложений
            и прикладного программного обеспечения, а также в машинном обучении и обработке больших данных. За счет простого и интуитивно понятного синтаксиса является одним из распространенных языков для обучения программированию. 
        </p>
        <p>
            Data Science и машинное обучение. Эти два направления IT 
            тесно связаны друг с другом. Наука о данных заключается в 
            обработке больших массивов информации из базы данных, а 
            машинное обучение — в разработке компьютерных алгоритмов, 
            способных учиться на ней и делать точные прогнозы.
        </p>
        <p>
            Веб-разработка. Многие крупные интернет-компании, такие
            как Google, Facebook*, программируют на Python свои самые
            известные проекты, например, Instagram*, YouTube, Dropbox
            и т.д. Этот язык позволяет вести веб-разработку на стороне 
            сервера, потому что его обширная библиотека включает 
            множество решений как раз для реализации сложных серверных 
            функций.
        </p>
        <img class="python-image" src="''' + url_for('static', filename='python.png') + '''">
    </body>

    <footer>
            &copy; Александр Герасимов, ФБИ-23, 3 курс, 2024
    </footer>
</html>
'''

@app.route('/lab1/gesya')
def gesya():
        return '''
<!doctype html>
    <head>
       <link rel="stylesheet" href="''' + url_for('static', filename='lab1.css') +'''">
    </head>
<html>
    <header>
            НГТУ, ФБ, Лабораторная работа 1
    </header>
    <body>
        <h1 class="gesya-title">Грустный киберспортсмен</h1>
        <div class="gesya-text">
            <p class="gesya-text-1">Я мог стать легендой, а стал разработчиком, и я рад!!! Название с подвохом</p>
            <p>
                Нет, — и, наверное, не было никогда в мире, — человека, который не хотел бы быть счастливым. Но вот вечный человеческий вопрос, самый простой и самый загадочный: что такое счастье?
                Для Франциска Ассизского и Альберта Швейцера счастье заключалось в полноте благоговения перед жизнью. Для Юлия Цезаря и Наполеона — в полноте обладания властью. Для Галилея и Альберта Эйнштейна — в полноте обладания научной истиной. Я назвал великие имена и великие судьбы. Но то же многообразие возможных вариантов счастья мы найдем в любой, самой обыкновенной и рядовой, человеческой судьбе. Даже беглое сопоставление этих вариантов показывает, что ответ на вопрос «Что такое счастье?» зависит от системы ценностей человека, зависит от того, что в этой иерархии помещается на верхние, что на нижние ступеньки. Но ответ на вопрос «Что такое счастье?» зависит в огромной степени и от системы ценностей всего общества. Эта система, разумеется, не есть нечто неизменное, неподвижное, замкнутое в себе. Она, как и само общество, живет, то есть меняется.
                В наш динамический век это особенно очевидно. Но даже меняясь, система ценностей в чем-то, вероятно, в основном, остается верной себе, иначе она бы была не системой, а хаосом.
                Что осталось неизменным? Что изменилось в системе жизненных ценностей сегодняшнего советского социалистического общества? Это не социологическое исследование, не научный труд, а наблюдения и заметки писателя. Поэтому, как и любые заметки, они носят в какой-то степени субъективный характер. Я делюсь моими частными соображениями, основанными в какой-то степени на моих наблюдениях, а в какой-то — на наблюдениях моих современников. В качестве завязки я избрал разговор о проходившей на страницах «Литературной газеты», где я работаю обозревателем, дискуссии «Успех в жизни — подлинный и мнимый». По-моему, эта дискуссия, несмотря на все издержки полемики, а может быть, именно благодаря неизбежным в полемике крайностям, показала вечное и сегодняшнее в нашей системе жизненных ценностей.
            </p>
        </div>
        <img class="gesya-image" src="''' + url_for('static', filename='major.png') + '''">
    </body>

    <footer>
            &copy; Александр Герасимов, ФБИ-23, 3 курс, 2024
    </footer>
</html>
'''

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого цветка нет", 404
    else:
        return f'''
        <!doctype html>
        <html>
            <body>
                <div>цветок: '''  + flower_list[flower_id] + '''</div>
                <a href="/lab2/flowersList/">Все цветы</a>
            </body>
        </html>
        '''

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
    <!doctype html>
    <html>
        <body>
         <h1>Добавлен цветок</h1>
         <p>Название нового цветка: {name} </p>
         <p>Всего цветов: {len(flower_list)} </p>
         <p>Полный список: {flower_list} </p>
        </body>
    </html>
'''

@app.route('/lab2/flowersListClear/')
def flowersListClear():
    flower_list.clear()
    return f'''
    <!doctype html>
    <html>
        <body>
            <a href="/lab2/flowersList/">Все цветы</a>
        </body>
    </html>
'''

@app.route('/lab2/flowersList/')
def flowersList():
    return f'''
    <!doctype html>
    <html>
        <body>
         <p>Всего цветов: {len(flower_list)} </p>
         <p>Полный список: {flower_list} </p>
        </body>
    </html>
'''

@app.route('/lab2/add_flower/')
def without_flower():
    return "вы не задали имя цветка", 400


@app.route('/lab2/example')
def example():
    name = 'Александр Герасимов'
    labNumber = '2'
    group = 'ФБИ-23'
    courseNumber = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
    ]
    return render_template('example.html',
                            name=name, labNumber=labNumber, group=group,
                             courseNumber=courseNumber, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)