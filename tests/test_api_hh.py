def test_get_data(api_hh):
    """ Тест получения данных с сайта - получаем словарь"""
    assert type(api_hh) is dict
    assert api_hh.get('items') is not None
