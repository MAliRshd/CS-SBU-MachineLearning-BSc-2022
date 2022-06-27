from flask import Flask, request
from utils.common import response_message, read_json_time_series, read_json_normal
from utils.interpolation_methods import interpolate
from utils.outlier_detection_methods import outlier_detector
from utils.imbalanced_data_management_methods import balanced_data
from khayyam import JalaliDatetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def isup():
    return response_message('API is active')


@app.route('/service1', methods=['GET', 'POST'])
def interpolation():
    try:
        req = request.get_json()
        config = req['config']
        data = read_json_time_series(req['data'], config['type'] == 'shamsi')

        result = interpolate(data, config)

        if config['type'] == 'shamsi':
            result.time = result.time.map(lambda d: JalaliDatetime(d).strftime('%Y-%m-%d-%H-%M-%S-%f'))
        result = result.to_json()

        return response_message(dict({"data": result}))
    except Exception as e:
        print(e)
        return response_message(dict({"data":"400 Bad Request"}), status=400)

@app.route('/service2', methods=['GET', 'POST'])
def shamsiInterpolation():
    try:
        req = request.get_json()
        config = req['config']
        data = read_json_time_series(req['data'], False)

        result = interpolate(data, config)

        result.time = result.time.map(lambda d: JalaliDatetime(d).strftime('%Y-%m-%d-%H-%M-%S-%f'))
        result = result.to_json()

        return response_message(dict({"data": result}))
    except Exception as e:
        print(e)
        return response_message(dict({"data":"400 Bad Request"}), status=400)

@app.route('/service3', methods=['GET', 'POST'])
def outlier_detection():
    try:
        req = request.get_json()
        config = req['config']
        data = read_json_time_series(req['data'], False) if config['time_series'] else read_json_normal(req['data'])

        result = outlier_detector(data, config)

        result = result.to_json()

        return response_message(dict({"data": result}))
    except Exception as e:
        print(e)
        return response_message(dict({"data":"400 Bad Request"}), status=400)

@app.route('/service4', methods=['GET', 'POST'])
def imbalanced_data():
    try:
        req = request.get_json()
        config = req['config']
        data = read_json_normal(req['data'])

        result = balanced_data(data, config)

        result = result.to_json()

        return response_message(dict({"data": result}))
    except Exception as e:
        print(e)
        return response_message(dict({"data":"400 Bad Request"}), status=400)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
