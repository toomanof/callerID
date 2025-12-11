KEYS_CSV = {
    '\ufeffАВС/ DEF': 'abc_def',
    'От': 'range_from',
    'До': 'range_to',
    'Емкость': 'capacity',
    'Оператор': 'operator',
    'Регион': 'region',
    'Территория ГАР': 'territory',
    'ИНН': 'inn'
}

FIELD_FOR_HASH = ('abc_def', 'range_from', 'range_to', 'capacity')
UPDATE_FIELDS_REGISTRY_MODEL = ('operator', 'region', 'territory', 'inn')

URLS_REGISTRY = (
    'https://opendata.digital.gov.ru/downloads/ABC-3xx.csv',
    'https://opendata.digital.gov.ru/downloads/ABC-4xx.csv',
    'https://opendata.digital.gov.ru/downloads/ABC-8xx.csv',
    'https://opendata.digital.gov.ru/downloads/DEF-9xx.csv',
)


HEAD_REQUEST = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
