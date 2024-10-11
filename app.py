from flask import Flask, redirect, url_for, render_template
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)


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
        <a href="/lab2">Вторая лабораторная</a>

        <footer>
            &copy; Александр Герасимов, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
"""


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


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
     return f'''
     <!doctype html>
     <html>
        <body>
              {a} + {b} = { a + b }<br>
              {a} - {b} = { a - b }<br>
              {a} * {b} = { a * b }<br>
              {a} / {b} = { a / b }<br>
              {a}<sup>{b}</sup> = { a ** b }
        </body>
     </html>
'''


@app.route('/lab2/calc/')
def calcWithoutNum():
    return redirect("/lab2/calc/1/1", code=302)


@app.route('/lab2/calc/<int:a>/')
def calcWithOneNum(a):
 return redirect(f"/lab2/calc/{a}/1", code=302)


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


@app.route('/lab2/filters/')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


@app.route('/lab2/books/')
def books():
    books = [
         {'author': 'Виктор Пелевин', 'name': 'Круть', 'genre': 'Триллер', 'pages': 344},
         {'author': 'Алексей Небоходов', 'name': 'Месть-дело семейное', 'genre': 'Любовный роман', 'pages': 34},
         {'author': 'Роман прокофьев', 'name': 'Звездная Кровь – 7. Дикая Охота', 'genre': 'Боевая фантастика', 'pages': 330},
         {'author': 'Кирилл Клеванский', 'name': 'Матабар', 'genre': 'Героическое фэнтэзи', 'pages': 714},
         {'author': 'Ян Бадевский', 'name': 'Мастер ножей', 'genre': 'Стимпанк', 'pages': 310},
         {'author': 'Ян Бадевский', 'name': 'Предельные Чертоги', 'genre': 'Боевая фантастика', 'pages': 320},
         {'author': 'Cyberdawn', 'name': 'Потапыч', 'genre': 'Юмористическое фэнтэзи', 'pages': 450},
         {'author': 'Евгений Астахов', 'name': 'Путь водного дракона', 'genre': 'Боевое фэнтэзи', 'pages': 357},
         {'author': 'Юрий Винокуров', 'name': 'Убивать, чтобы жить 3', 'genre': 'Героичкская фантастика', 'pages': 260},
         {'author': 'Евгений Астахов', 'name': 'Пробуждение силы. Том 2', 'genre': 'Боевое фэнтэзи', 'pages': 287},
    ]
    return render_template('books.html', books=books)


@app.route('/lab2/vegetables/')
def vegetables():
    vegetables = [
        {'image': url_for('static', filename='beet.png'), 'name': 'Свекла', 'description': 'Свекла полезный овощь с ним делают борщ'},
        {'image': url_for('static', filename='cabbage.png'), 'name': 'Капуста', 'description': 'Если много кушать капусту будешь здоровый!'},
        {'image': url_for('static', filename='carrot.png'), 'name': 'Морковка', 'description': 'Длинный продолговатый овощь оранджевого цвета, говорят улучшает зрение'},
        {'image': url_for('static', filename='radish.png'), 'name': 'Редис', 'description': 'Не самый вкусный овощ, но один из полезных'},
        {'image': url_for('static', filename='tomato.png'), 'name': 'Томат', 'description': 'Самый вкусный здесь овощ, можно с ним сделать много вкусных вещей'},
    ]
    return render_template('vegetables.html', vegetables=vegetables)




