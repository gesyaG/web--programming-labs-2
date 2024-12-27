from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, session,  current_app, Flask, flash, jsonify
from functools import wraps
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

RGZ = Blueprint('RGZ', __name__)

ADMIN_USER = 'gesya'


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        try:
            conn = psycopg2.connect(
                dbname="cinema",
                user="gesya",
                password="212121",
                host="127.0.0.1"
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(f"Ошибка подключения к PostgreSQL: {e}")
            return None, None
    else:
        try:
            dir_path = path.dirname(path.realpath(__file__))
            db_path = path.join(dir_path, "database.db")
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
        except Exception as e:
            print(f"Ошибка подключения к SQLite: {e}")
            return None, None

    return conn, cur

def db_close(conn, cur):
    if conn and cur:
        conn.commit()
        cur.close()
        conn.close()


@RGZ.route('/RGZ/login')
def log():
    return render_template('/RGZ/login.html')


@RGZ.route('/RGZ/register')
def reg():
    return render_template('/RGZ/register.html')


@RGZ.route('/api/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return jsonify({"message": "Вы вышли из системы!"}), 200


@RGZ.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    login = data.get('login')
    name = data.get('name')
    password = data.get('password')

    if not (login and name and password):
        return jsonify({"error": "Заполните все поля"}), 400

    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        # Проверка на существующий логин
        query_check_login = (
            "SELECT login FROM users WHERE login = %s;"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "SELECT login FROM users WHERE login = ?;"
        )
        cur.execute(query_check_login, (login,))
        if cur.fetchone():
            return jsonify({"error": "Такой пользователь уже существует"}), 400

        # Хэширование пароля
        password_hash = generate_password_hash(password)

        # Вставка нового пользователя
        query_insert_user = (
            "INSERT INTO users (login, name, password) VALUES (%s, %s, %s);"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "INSERT INTO users (login, name, password) VALUES (?, ?, ?);"
        )
        cur.execute(query_insert_user, (login, name, password_hash))
        conn.commit()
    except Exception as e:
        db_close(conn, cur)
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500

    db_close(conn, cur)
    return jsonify({"message": "Регистрация прошла успешно"}), 201


@RGZ.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    if not (login and password):
        return jsonify({"error": "Заполните поля"}), 400

    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        # Выполняем запрос на получение пользователя
        query = "SELECT * FROM users WHERE login=%s;" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT * FROM users WHERE login=?;"
        cur.execute(query, (login,))
        user = cur.fetchone()

        # Проверяем, найден ли пользователь и совпадает ли пароль
        if not user or not check_password_hash(user['password'], password):
            return jsonify({"error": "Логин и/или пароль неверны"}), 401

        # Сохраняем данные пользователя в сессии
        session['user_id'] = user['id']  # Добавляем user_id в сессию
        session['login'] = user['login']
        session['role'] = 'admin' if user['login'] == ADMIN_USER else 'user'

    except Exception as e:
        db_close(conn, cur)
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500

    db_close(conn, cur)

    # Определяем URL перенаправления в зависимости от роли
    redirect_url = url_for('RGZ.admin') if session['role'] == 'admin' else url_for('RGZ.sessions')

    return jsonify({"message": "Вы успешно вошли в систему!", "redirect": redirect_url}), 200



@RGZ.route('/admin')
def admin():
    return render_template('/RGZ/admin.html')


# Декоратор для проверки роли администратора
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({"error": "Доступ запрещён. Необходима роль администратора."}), 403
        return f(*args, **kwargs)
    return decorated_function


# Роут для создания нового сеанса
@RGZ.route('/api/sessions', methods=['POST'])
@admin_required
def create_session():
    data = request.get_json()
    movie_name = data.get('movie_name')
    session_date = data.get('session_date')
    session_time = data.get('session_time')

    if not (movie_name and session_date and session_time):
        return jsonify({"error": "Заполните все поля"}), 400

    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        # Проверка на уникальность сеанса
        query_check_session = (
            "SELECT * FROM sessions WHERE movie_name = %s AND session_date = %s AND session_time = %s;"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "SELECT * FROM sessions WHERE movie_name = ? AND session_date = ? AND session_time = ?;"
        )
        cur.execute(query_check_session, (movie_name, session_date, session_time))
        if cur.fetchone():
            return jsonify({"error": "Такой сеанс уже существует"}), 400

        # Вставка нового сеанса
        query_insert_session = (
            "INSERT INTO sessions (movie_name, session_date, session_time) VALUES (%s, %s, %s) RETURNING id;"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "INSERT INTO sessions (movie_name, session_date, session_time) VALUES (?, ?, ?);"
        )
        cur.execute(query_insert_session, (movie_name, session_date, session_time))
        session_id = cur.fetchone()['id'] if current_app.config['DB_TYPE'] == 'postgres' else cur.lastrowid

        # Генерация мест для нового сеанса
        query_insert_seats = (
            "INSERT INTO seats (session_id, seat_number) VALUES (%s, %s);"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "INSERT INTO seats (session_id, seat_number) VALUES (?, ?);"
        )
        for seat_number in range(1, 31):
            cur.execute(query_insert_seats, (session_id, seat_number))

        conn.commit()

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500

    finally:
        conn.close()

    return jsonify({"message": "Сеанс успешно создан с 30 местами"}), 201


# Роут для удаления сеанса
@RGZ.route('/api/sessions/<int:session_id>', methods=['DELETE'])
@admin_required
def delete_session(session_id):
    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        # Удаление сеанса
        query_delete_session = (
            "DELETE FROM sessions WHERE id = %s RETURNING *;"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "DELETE FROM sessions WHERE id = ?;"
        )
        cur.execute(query_delete_session, (session_id,))
        deleted_session = cur.fetchone() if current_app.config['DB_TYPE'] == 'postgres' else cur.rowcount

        if not deleted_session:
            return jsonify({"error": "Сеанс не найден"}), 404

        # Удаление связанных с сеансом мест
        query_delete_seats = (
            "DELETE FROM seats WHERE session_id = %s;"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "DELETE FROM seats WHERE session_id = ?;"
        )
        cur.execute(query_delete_seats, (session_id,))

        # Удаление связанных с сеансом бронирований
        query_delete_bookings = (
            "DELETE FROM bookings WHERE session_id = %s;"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "DELETE FROM bookings WHERE session_id = ?;"
        )
        cur.execute(query_delete_bookings, (session_id,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500

    finally:
        conn.close()

    return jsonify({"message": "Сеанс и все связанные с ним данные успешно удалены"}), 200


# Роут для снятия брони с места
@RGZ.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
@admin_required
def remove_booking(booking_id):
    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        # Удаление бронирования
        query_delete_booking = (
            "DELETE FROM bookings WHERE id = %s RETURNING seat_id;"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "DELETE FROM bookings WHERE id = ?;"
        )
        cur.execute(query_delete_booking, (booking_id,))
        deleted_booking = cur.fetchone() if current_app.config['DB_TYPE'] == 'postgres' else cur.rowcount

        if not deleted_booking:
            return jsonify({"error": "Бронирование не найдено"}), 404

        seat_id = deleted_booking['seat_id'] if current_app.config['DB_TYPE'] == 'postgres' else None

        # Снимаем бронь с места
        query_update_seat = (
            "UPDATE seats SET is_taken = FALSE, taken_by = NULL WHERE id = %s;"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "UPDATE seats SET is_taken = FALSE, taken_by = NULL WHERE id = ?;"
        )
        cur.execute(query_update_seat, (seat_id,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500

    finally:
        conn.close()

    return jsonify({"message": "Бронирование успешно удалено и место освобождено"}), 200


def fetch_sessions():
    """Получает список всех сеансов из базы данных."""
    conn, cur = db_connect()
    if conn is None or cur is None:
        return None, "Ошибка подключения к базе данных"

    try:
        query_sessions = "SELECT id, movie_name, session_date, session_time FROM sessions;"
        cur.execute(query_sessions)
        sessions = cur.fetchall()

        current_time = datetime.now()
        formatted_sessions = [
            {
                "id": session["id"],
                "movie_name": session["movie_name"],
                "session_date": session["session_date"].isoformat(),  # Преобразование даты в строку
                "session_time": session["session_time"].isoformat(),  # Преобразование времени в строку
                "is_editable": datetime.combine(session["session_date"], session["session_time"]) > current_time
            }
            for session in sessions
        ]
        return formatted_sessions, None

    except Exception as e:
        return None, f"Ошибка выполнения запроса: {e}"

    finally:
        db_close(conn, cur)


@RGZ.route('/api/sessions', methods=['GET'])
def api_get_sessions():
    """REST API: возвращает список всех сеансов."""
    sessions, error = fetch_sessions()
    if error:
        return jsonify({"error": error}), 500
    return jsonify(sessions), 200


@RGZ.route('/sessions', methods=['GET'])
def sessions():
    """Отображает страницу со списком сеансов, используя REST API."""
    sessions, error = fetch_sessions()
    if error:
        abort(500, description=error)
    return render_template('/RGZ/sessions.html', sessions=sessions)


# Получение списка мест для сеанса и названия фильма
@RGZ.route('/api/sessions/<int:session_id>/seats', methods=['GET'])
def get_seats(session_id):
    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        # Проверка существования сессии
        session_check_query = (
            "SELECT id FROM sessions WHERE id = %s"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "SELECT id FROM sessions WHERE id = ?"
        )
        cur.execute(session_check_query, (session_id,))
        session_exists = cur.fetchone()
        if not session_exists:
            return jsonify({"error": "Сеанс не найден"}), 404

        # Запрос мест
        seats_query = (
            """
            SELECT seats.id AS seat_id, seats.seat_number, seats.is_taken, users.name AS taken_by
            FROM seats
            LEFT JOIN users ON seats.taken_by = users.id
            WHERE seats.session_id = %s
            """
            if current_app.config['DB_TYPE'] == 'postgres'
            else """
            SELECT seats.id AS seat_id, seats.seat_number, seats.is_taken, users.name AS taken_by
            FROM seats
            LEFT JOIN users ON seats.taken_by = users.id
            WHERE seats.session_id = ?
            """
        )
        cur.execute(seats_query, (session_id,))
        seats = [dict(seat) for seat in cur.fetchall()]

        if not seats:
            return jsonify({"error": "Нет мест для указанного сеанса"}), 404

        # Запрос названия фильма
        movie_query = (
            "SELECT movie_name FROM sessions WHERE id = %s"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "SELECT movie_name FROM sessions WHERE id = ?"
        )
        cur.execute(movie_query, (session_id,))
        movie = cur.fetchone()
        movie_name = movie['movie_name'] if movie else "Неизвестно"

        # Формирование результата
        result = {
            "movie_name": movie_name,
            "seats": seats
        }
        return jsonify(result), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Ошибка выполнения запроса"}), 500
    finally:
        db_close(conn, cur)


# Бронирование мест
@RGZ.route('/api/sessions/<int:session_id>/book', methods=['POST'])
def book_seats(session_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Вы не авторизованы"}), 403

    data = request.get_json()
    seat_ids = data.get('seat_ids', [])
    if not isinstance(seat_ids, list) or not all(isinstance(seat, int) for seat in seat_ids):
        return jsonify({"error": "Неверный формат seat_ids"}), 400

    if len(seat_ids) > 5:
        return jsonify({"error": "Нельзя бронировать более 5 мест"}), 400

    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        # Проверяем существование сеанса
        session_check_query = (
            "SELECT id FROM sessions WHERE id = %s"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "SELECT id FROM sessions WHERE id = ?"
        )
        cur.execute(session_check_query, (session_id,))
        session_exists = cur.fetchone()
        if not session_exists:
            return jsonify({"error": "Сеанс не найден"}), 404

        # Проверяем доступность мест
        seats_query = (
            "SELECT id, is_taken FROM seats WHERE id = ANY(%s) AND session_id = %s FOR UPDATE;"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "SELECT id, is_taken FROM seats WHERE id IN ({}) AND session_id = ?;".format(",".join(["?"] * len(seat_ids)))
        )
        cur.execute(seats_query, (*seat_ids, session_id) if current_app.config['DB_TYPE'] == 'sqlite' else (seat_ids, session_id))
        seats = cur.fetchall()

        if len(seats) != len(seat_ids):
            return jsonify({"error": "Одно или несколько мест не существуют"}), 400

        for seat in seats:
            if seat['is_taken']:
                return jsonify({"error": f"Место {seat['id']} уже занято"}), 400

        # Бронируем места и добавляем записи в таблицу бронирований
        update_seats_query = (
            "UPDATE seats SET is_taken = TRUE, taken_by = %s WHERE id = %s AND session_id = %s;"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "UPDATE seats SET is_taken = TRUE, taken_by = ? WHERE id = ? AND session_id = ?;"
        )
        insert_booking_query = (
            "INSERT INTO bookings (user_id, session_id, seat_id) VALUES (%s, %s, %s);"
            if current_app.config['DB_TYPE'] == 'postgres'
            else "INSERT INTO bookings (user_id, session_id, seat_id) VALUES (?, ?, ?);"
        )
        for seat_id in seat_ids:
            cur.execute(update_seats_query, (user_id, seat_id, session_id))
            cur.execute(insert_booking_query, (user_id, session_id, seat_id))

        conn.commit()
        return jsonify({"message": "Места успешно забронированы"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500
    finally:
        db_close(conn, cur)


@RGZ.route('/api/sessions/<int:session_id>/unbook', methods=['POST'])
def unbook_seats(session_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Вы не авторизованы"}), 403

    data = request.get_json()
    seat_ids = data.get('seat_ids', [])

    conn, cur = db_connect()
    if conn is None or cur is None:
        return jsonify({"error": "Ошибка подключения к базе данных"}), 500

    try:
        for seat_id in seat_ids:
            # Проверяем, принадлежит ли бронь текущему пользователю
            query_check = (
                "SELECT taken_by FROM seats WHERE id = %s AND session_id = %s;"
                if current_app.config['DB_TYPE'] == 'postgres'
                else "SELECT taken_by FROM seats WHERE id = ? AND session_id = ?;"
            )
            cur.execute(query_check, (seat_id, session_id))
            seat = cur.fetchone()

            if not seat or seat[0] != user_id:
                return jsonify({"error": f"Место {seat_id} не забронировано вами или не существует"}), 400

            # Снимаем бронь
            query_update = (
                "UPDATE seats SET is_taken = FALSE, taken_by = NULL WHERE id = %s AND session_id = %s;"
                if current_app.config['DB_TYPE'] == 'postgres'
                else "UPDATE seats SET is_taken = FALSE, taken_by = NULL WHERE id = ? AND session_id = ?;"
            )
            cur.execute(query_update, (seat_id, session_id))

            # Удаляем запись из таблицы бронирований
            query_delete = (
                "DELETE FROM bookings WHERE user_id = %s AND session_id = %s AND seat_id = %s;"
                if current_app.config['DB_TYPE'] == 'postgres'
                else "DELETE FROM bookings WHERE user_id = ? AND session_id = ? AND seat_id = ?;"
            )
            cur.execute(query_delete, (user_id, session_id, seat_id))

        conn.commit()
        return jsonify({"message": "Бронь успешно снята"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка выполнения запроса: {e}"}), 500
    finally:
        db_close(conn, cur)


@RGZ.route('/sessions/<int:session_id>/seats', methods=['GET'])
def seats(session_id):
    """Отображает страницу с местами для конкретного сеанса."""
    return render_template('/RGZ/seats.html', session_id=session_id)

