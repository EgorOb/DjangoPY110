import http.client

# Замените <значение ключа> и параметры запроса на конкретные значения
api_key = "54d73608-c8dd-4c98-b18f-d9a5056525ab"
lat = "55.75396"
lon = "37.620393"

# Создайте соединение с сервером
conn = http.client.HTTPSConnection("api.weather.yandex.ru")

# Формируйте URL запроса
url = f"/v2/informers?lat={lat}&lon={lon}"

# Создайте заголовок с ключом аутентификации
headers = {
    "X-Yandex-API-Key": api_key
}

# Отправьте GET-запрос
conn.request("GET", url, headers=headers)

# Получите ответ
response = conn.getresponse()

# Проверьте статус ответа
if response.status == 200:
    data = response.read()
    # Обработка данных о погоде (data содержит ответ в байтах)
    print(data.decode('utf-8'))  # Преобразование ответа в строку
else:
    print(f"Ошибка при запросе: {response.status} {response.reason}")

# Закройте соединение
conn.close()


