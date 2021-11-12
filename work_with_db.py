import sqlite3

NAME_DATABASE = "online_store_database.sqlite"


def save_db(basket, current_id):
    con = sqlite3.connect(NAME_DATABASE)
    cur = con.cursor()
    order_verification = cur.execute(f"""SELECT status FROM orders
                                         WHERE id_client = {current_id}""").fetchall()
    flag = True
    if len(order_verification) >= 1:
        for i in order_verification:
            if i[0] == 'not paid':
                flag = False
    if flag:
        cur.execute(f"""INSERT INTO orders(status, id_client) VALUES('not paid', {current_id})""").fetchall()

        con.commit()
    id_order = cur.execute(f"""SELECT id FROM orders
                               WHERE id_client = {current_id} and status = 'not paid'""").fetchall()
    cur.execute(f"""DELETE from order_items
                            WHERE id_order = {id_order[0][0]}""").fetchall()
    con.commit()
    for elem in basket.keys():
        id_product = cur.execute(f"""SELECT id FROM price_list
                                                WHERE title = '{elem}'""").fetchall()
        cur.execute(f"""INSERT INTO order_items(id_product, id_order, count_product)
                        VALUES({id_product[0][0]}, {id_order[0][0]}, {basket[elem]})""").fetchall()
        con.commit()


def get_result_from_db(current_id):
    con = sqlite3.connect(NAME_DATABASE)
    cur = con.cursor()
    order_verification = cur.execute(f"""SELECT
                                        price_list.title,
                                        order_items.count_product
                                        FROM
                                        order_items
                                        INNER JOIN price_list
                                        ON price_list.id = order_items.id_product
                                        WHERE order_items.id_order=(SELECT id from orders 
                                        WHERE id_client = {current_id} and status = 'not paid')""").fetchall()
    data = {}
    for i in order_verification:
        data[i[0]] = i[1]
    return data


def make_status_paid(current_id, index):
    con = sqlite3.connect(NAME_DATABASE)
    cur = con.cursor()
    if index == 0:
        update_db = cur.execute(f"""UPDATE orders
                                    SET status = 'paid'
                                    WHERE id_client = {current_id} and status = 'not paid'""").fetchall()
    else:
        update_db = cur.execute(f"""UPDATE orders
                                    SET status = 'payment in the store'
                                    WHERE id_client = {current_id} and status = 'not paid'""").fetchall()
    con.commit()


def get_order_id(current_id):
    con = sqlite3.connect(NAME_DATABASE)
    cur = con.cursor()
    id_order = cur.execute(f"""SELECT id from orders
                                WHERE id_client = {current_id} and status = 'not paid'""").fetchall()
    return id_order[0]


def get_data_for_receipt(id_order):
    con = sqlite3.connect(NAME_DATABASE)
    cur = con.cursor()
    data = cur.execute(f"""SELECT
                            price_list.title,
                            order_items.count_product,
                            price_list.price
                            FROM
                            order_items
                            INNER JOIN price_list
                            ON price_list.id = order_items.id_product
                            WHERE order_items.id_order = {id_order}""").fetchall()
    return data
