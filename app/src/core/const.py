base_buttons = (('Каталог', 'catalog'), ('Корзина', 'bucket'))

empty_bucket = (('Каталог', 'catalog'),)

start_callback = ('catalog', 'bucket', 'faq', 'group_subscription',
                 'channel_subscription', 'subscribe')

subscriptions = ('group_subscription',
                 'channel_subscription', 'subscribe')

show_image_buttons = (('Добавить в корзину', 'add_to_bucket'),
                      ('Вернуться к выбору товаров', 'back_to_item'),
                      ('Корзина', 'bucket'))

empty_items = (('Вернуться к выбору подкатегории', 'back_to_subcategory'),
                ('Корзина', 'bucket'))

empty_subcategoty = (('Вернуться к выбору категории', 'catalog'),
                    ('Корзина', 'bucket'))

add_quantity_buttons = (('Вернуться к выбору товаров', 'back_to_item'),
                        ('Корзина', 'bucket'))

all_items_deleted_from_bucket = (('Вернуться к выбору товаров', 'back_to_item'),
                                 ('Каталог', 'catalog'))

confirm_buttons = (('Добавить товар в корзину', 'yes'),
                   ('Вернуться к выбору товаров', 'back_to_item'),
                   ('Просмотр корзины', 'bucket'))

bucket_buttons = (('Оформить заказ', 'order'),
                  ('Удалить товар из корзины', 'delete_item'),
                  ('Очистить корзину', 'clear_bucket'),
                  ('Каталог', 'catalog'))

payment_gates = (('Оплата тинькофф', 'payment'),
                 ('Оплата юкасса', 'payment'),
                 ('Вернуться в корзину', 'bucket'),
                 ('Каталог', 'catalog'))

payment_gates_change_adress = (
    ('Изменить адрес доставки', 'change_adress'),
    ('Оплата тинькофф', 'payment'),
    ('Оплата юкасса', 'payment'),
    ('Вернуться в корзину', 'bucket'),
    ('Каталог', 'catalog'))