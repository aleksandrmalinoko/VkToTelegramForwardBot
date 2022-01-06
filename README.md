# VkToTelegramForwardBot
Данный бот работает с VK и Telegram и репостит записи из сообщеста вк в группу telegram
## Возможности
Бот может репостить записи содержащие только текст или текст и изображения
## Настройка
Для конфигурации бота необходимо добавить свои токены и ссылки на сообщества в файл config.ini
### VK токен
Для работы с сообществом вконтакте используется Long Poll API. В настройках сообщества для типов событий Long Poll должно быть разрешение на тип события "Записи на стене" - "Добавление"
Для получение токена ВК необходимо создать ключ с дотсупом к стене сообщества
### Telegram токен
Необходимо создать бота черз BotFather. После создание бота, BotFather пришлет его токен. Бот должен быть добавлен в сообщество telegram как администратор
## Запуск
Запуск бота может быть как на самом устройстве, так и в Docker контейнере.
### Запуск без использования контейнеров
`python app.py`
### Запуск в контейнере
`docker build -t vk-forwarding-bot .`
`docker run --network host --name vk-recender-bot -d vk-recender-bot`
