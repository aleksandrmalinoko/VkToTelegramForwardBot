from flask import Flask, json, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = json.loads(request.data)
    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return '5c003175'
    return 'index.html'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
