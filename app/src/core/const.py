base_buttons = (('Каталог', 'catalog'), ('Корзина', 'bucket'),
                ('FAQ', 'faq'))

empty_bucket = (('Каталог', 'catalog'),
                ('FAQ', 'faq'))

start_callback = ('catalog', 'bucket', 'faq', 'group_subscription',
                 'channel_subscription', 'subscribe')

subscriptions = ('group_subscription',
                 'channel_subscription', 'subscribe')

show_image_buttons = (('Добавить в корзину', 'add_to_bucket'),
                      ('Вернуться к выбору товаров', 'back_to_item'),
                      ('Корзина', 'bucket'))

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