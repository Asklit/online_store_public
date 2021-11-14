from work_with_db import get_data_for_receipt


def save_in_txt_file(index_place_of_receipt, index_payment_method, order_id):
    with open(f'receipt #{order_id}.txt', "w") as f:
        f.write('Добро пожаловать\n')
        f.write('Интернет магазин\n')
        f.write('Angels\n')
        f.write('\n')
        f.write('Кассовый чек для получения товара в магазине\n')
        f.write('Адрес получения:\n')
        if index_place_of_receipt == 0:
            place_of_receipt = "It-куб, ул. Чернышевского, 28, Пермь (эт. 3)\n"
        else:
            place_of_receipt = "Муравейник, ул. Пушкина, 76, Пермь\n"
        f.write(f"{place_of_receipt}\n")
        data = get_data_for_receipt(order_id)
        f.write('Место расчетов\n')
        list_items = [f'{elem[0]} {elem[2][:-2]} x {elem[1]} = {int(elem[2][:-2]) * int(elem[1])}' for elem in data]
        max_len = -1
        for elem in list_items:
            if max_len < len(elem):
                max_len = len(elem)
        list_index = []
        for elem in list_items:
            list_index.append(max_len - len(elem))
        amount = 0
        for index, elem in enumerate(data):
            name, count, price = elem
            amount_price = int(price[:-2]) * int(count)
            amount += amount_price
            f.write(f'{name} {" " * list_index[index]}{price[:-2]} x {count} = {amount_price}\n')
        f.write(f'Итого: {amount}')
        if index_payment_method == 0:
            payment_method = "Заказ оплачен онлайн\n"
        else:
            payment_method = "Оплата заказа при получении\n"
        f.write('\n')
        f.write(f'{payment_method}\n')


