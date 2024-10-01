ALLOWED_STATUSES = ('в процессе', 'отправлен', 'доставлен')
PRODUCT_NOT_FOUND = 'Такого продукта не существует!'
PRODUCT_EXISTS = 'Продукт с таким именем уже существует!'
EXAMPLE_PRODUCTS = {1: 10, 5: 1, 4: 5}
DESCRIPTION_PRODUCTS = 'Сопоставление идентификаторов продуктов с заказываемым количеством.'
REGEX = '^(' + '|'.join(ALLOWED_STATUSES) + ')$'
DESCRIPTION_AMOUNT_PRODUCTS = 'Продуктов должно быть больше или равно 1'
DESCRIPTION_STATUS = ', '.join(ALLOWED_STATUSES)
