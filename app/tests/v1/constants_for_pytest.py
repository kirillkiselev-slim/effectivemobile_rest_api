CREATE_INCORRECT_ORDER = {
  'status': 'в процессе',
  'products': {
    '1': 3,
    '2': 3,
  }
}

INSUFFICIENT_STOCK_MESSAGE = (f'Нет кол-во для LowStockProduct '
                              f'(ID: 1). '
                              f'Доступно: 1,'
                              f' Запрошено: 3')

CREATE_ORDER_ID = 1
CREATE_ORDER_AMOUNT = 2
CREATE_ORDER = {
  'status': 'в процессе',
  'products': {
    '1': CREATE_ORDER_AMOUNT,
  }
}
PORT_TEST = 5434
