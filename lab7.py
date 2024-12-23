from flask import Blueprint, redirect, request

lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')


films = [
    {
        "title": "Shutter Island",
        "title_ru": "Остров проклятых",
        "year": 2009,
        "description": "Два американских судебных пристава отправляются на один из островов в штате Массачусетс, чтобы расследовать исчезновение пациентки клиники для умалишенных преступников. При проведении расследования им придется столкнуться с паутиной лжи, обрушившимся ураганом и смертельным бунтом обитателей клиники."
    },
    {
        "title": "Собачье сердце",
        "title_ru": "Собачье сердце",
        "year": 1988,
        "description": "Москва, 1924 год. В результате одного из сложнейших опытов профессор Филипп Филиппович Преображенский делает потрясающее открытие: после пересадки гипофиза человека пёс Шарик начинает приобретать человеческие черты. Сенсационная новость мгновенно разлетается по Москве и приносит мировому светилу очередную порцию признания. Однако радость оказывается недолгой: вопрос, что из Шарика — то есть гражданина Шарикова — может получиться «высокая психическая личность», очень быстро становится под сомнение."
    },
    {
        "title": "Harry Potter and the Sorcerer's Stone",
        "title_ru": "Гарри Поттер и философский камень",
        "year": 2001,
        "description": "Жизнь десятилетнего Гарри Поттера нельзя назвать сладкой: родители умерли, едва ему исполнился год, а от дяди и тёти, взявших сироту на воспитание, достаются лишь тычки да подзатыльники. Но в одиннадцатый день рождения Гарри всё меняется. Странный гость, неожиданно появившийся на пороге,  приносит письмо, из которого мальчик узнаёт, что на самом деле он - волшебник и зачислен в школу магии под названием Хогвартс. А уже через пару недель Гарри будет мчаться в поезде Хогвартс-экспресс навстречу новой жизни, где его ждут невероятные приключения, верные друзья и самое главное — ключ к разгадке тайны смерти его родителей."
    },
    {
        "title": "Lock, Stock and Two Smoking Barrels",
        "title_ru": "Карты, деньги, два ствола",
        "year": 1998,
        "description": "Четверо приятелей накопили по 25 тысяч фунтов, чтобы один из них мог сыграть в карты с опытным шулером и матерым преступником, известным по кличке Гарри Топор. Парень проиграл 500 тысяч, на выплату долга ему дали неделю, а в противном случае и ему и его друзьям каждый день будут отрубать по пальцу. Ребята решают ограбить бандитов, решивших ограбить трех ботаников, выращивающих марихуану для местного наркобарона."
    },
    {
        "title": "The Silence of the Lambs",
        "title_ru": "Молчание ягнят",
        "year": 1990,
        "description": "Психопат похищает и убивает молодых женщин по всему Среднему Западу. ФБР, уверенное, что все преступления совершены одним и тем же человеком, поручает агенту Клариссе Старлинг встретиться с заключенным-маньяком Ганнибалом Лектером, который мог бы помочь составить психологический портрет убийцы. Сам Лектер отбывает наказание за убийства и каннибализм. Он согласен помочь Клариссе лишь в том случае, если она попотчует его больное воображение подробностями своей личной жизни."
    },
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if 0 <= id < len(films):
        return films[id]
    else:
        return {'error': 'Film not found'}, 404


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if 0 <= id < len(films):
        del films[id]
        return '', 204
    else:
        return {'error': 'Film not found'}, 404