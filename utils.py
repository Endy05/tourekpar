def round_price(price, decimals=6):
    """Округлює ціну до вказаної кількості знаків після коми."""
    return round(price, decimals)


def chunk_list(lst, chunk_size):
    """Розбиває список на підсписки заданого розміру."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def handle_error(error):
    """Обробляє помилки та повертає їх у вигляді рядка."""
    return f"Помилка: {str(error)}"
