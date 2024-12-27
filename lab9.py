from flask import Blueprint, render_template

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')


@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        session['age'] = request.form['age']
        return redirect(url_for('lab9.gender'))
    return render_template('lab9/age.html')

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'POST':
        session['gender'] = request.form['gender']
        return redirect(url_for('lab9.preference'))
    return render_template('lab9/gender.html')

@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def preference():
    if request.method == 'POST':
        session['preference'] = request.form['preference']
        return redirect(url_for('lab9.sub_preference'))
    return render_template('lab9/preference.html')

@lab9.route('/lab9/sub_preference', methods=['GET', 'POST'])
def sub_preference():
    if request.method == 'POST':
        session['sub_preference'] = request.form['sub_preference']
        return redirect(url_for('lab9.final'))
    return render_template('lab9/sub_preference.html')

@lab9.route('/lab9/final')
def final():
    name = session.get('name')
    age = session.get('age')
    gender = session.get('gender')
    preference = session.get('preference')
    sub_preference = session.get('sub_preference')

    # Логика для выбора поздравления и картинки
    if gender == 'male':
        gender_pronoun = 'ты'
        gift = 'мешочек конфет'
        if preference == 'вкусное':
            if sub_preference == 'сладкое':
                message = f"Поздравляю тебя, {name}, желаю, хорошо встретить новый год. Вот тебе подарок — {gift}."
                image = 'candy.jpg'  # Путь к картинке с конфетами
            else:
                message = f"Поздравляю тебя, {name}, желаю, хорошо встретить новый год. Вот тебе подарок — сытное угощение."
                image = 'savory.jpg'  # Путь к картинке с сытным
        else:
            message = f"Поздравляю тебя, {name}, желаю, хорошо встретить новый год. Вот тебе подарок — что-то красивое."
            image = 'beautiful.jpg'  # Путь к картинке с красивым
    else:
        gender_pronoun = 'ты'
        gift = 'тортик'
        if preference == 'вкусное':
            if sub_preference == 'сладкое':
                message = f"Поздравляю тебя, {name}, желаю, хорошо встретить новый год. Вот тебе подарок — {gift}."
                image = 'cake.jpg'  # Путь к картинке с тортом
            else:
                message = f"Поздравляю тебя, {name}, желаю, хорошо встретить новый год. Вот тебе подарок — сытное угощение."
                image = 'savory.jpg'  # Путь к картинке с сытным
        else:
            message = f"Поздравляю тебя, {name}, желаю, хорошо встретить новый год. Вот тебе подарок — что-то красивое."
            image = 'beautiful.jpg'  # Путь к картинке с красивым

    return render_template('lab9/final.html', message=message, image=image)

@lab9.route('/lab9/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('index'))