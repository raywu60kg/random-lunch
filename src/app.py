from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_apscheduler import APScheduler
import json
import logging
import os
import random
import datetime

class Config(object):
    SCHEDULER_API_ENABLED = True

scheduler = APScheduler()
package_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute", "1 per second"],
)


DRAW_TIME = os.environ.get('DRAW_TIME') or 'today'
if DRAW_TIME == 'today':
    DRAW_TIME = datetime.datetime.now().strftime('%Y-%m-%d') + ' 12:00:00'
else:
    DRAW_TIME = DRAW_TIME

@app.route('/time_info', methods=['GET'])
def get_time_info():
    if 'result.json' in os.listdir('src'):
        with open('src/result.json', 'r') as file:
            result = json.load(file)
        return 'Already drew {}\n'.format(result)
    
    return 'Gonna drow the meal at {}\nCurrent time: {}\n'.format(
        DRAW_TIME, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


@app.route('/lunch_candidate', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def lunch_candidate():
    if request.method == 'GET':
        try:
            with open('src/lunch_candidate.json', 'r') as file:
                lunch_candidate = json.load(file)
            return jsonify(lunch_candidate)
        except Exception as ex:
            logging.error(ex)
            return 'Some error happened: {0}\n'.format(ex)

    elif request.method == 'POST':
        if 'result.json' in os.listdir('src'):
            with open('src/result.json', 'r') as file:
                result = json.load(file)
            return 'Already drew {}\n'.format(result)

        data = request.get_json(force=True)
        logging.info('@@@ {}'.format(data))

        # return data
        name = data['name']
        proposal = data['proposal']

        try:
            with open('src/lunch_candidate.json', 'r') as file:
                lunch_candidate = json.load(file)
            lunch_candidate['name'].append(name)
            lunch_candidate['proposal'].append(proposal)

            with open('src/lunch_candidate.json', 'w') as file:
                json.dump(lunch_candidate, file)
            
            return 'Added candidate :{}\n'.format(data)

        except Exception as ex:
            logging.error(request.args)
            return 'Post failed: {0}'.format(ex)

@app.route('/result', methods=['GET'])
def get_draw_result():
    if 'result.json' in os.listdir('src'):
        with open('src/result.json', 'r') as file:
            result = json.load(file)
        return 'Already drew {}\n'.format(result)
    else:
        return 'Have not drow\n'

@app.route('/health', methods=['GET'])
def health_check():
    '''Check connection health

    Returns:
        str: 'OK' if works
    '''
    logging.info('health check')
    return 'OK\n'

@scheduler.task('date', id='draw_scheduler', run_date=DRAW_TIME)
def draw_lunch():
    if 'result.json' in os.listdir('src'):
        with open('src/result.json', 'r') as file:
            result = json.load(file)
        return 'Already drew {}\n'.format(result)

    else:
        with open('src/lunch_candidate.json', 'r') as file:
            lunch_candidate = json.load(file)
        name = lunch_candidate['name']
        proposal = lunch_candidate['proposal']

        index = random.choice(list(enumerate(proposal)))[0]

        result = {
            'name': name[index],
            'proposal': proposal[index]
        }
        with open('src/result.json', 'w') as file:
            json.dump(result, file)
        return 'Drew result: {}\n'.format(result)

@app.route('/draw', methods=['POST'])
def force_draw():
    if 'result.json' in os.listdir('src'):
        with open('src/result.json', 'r') as file:
            result = json.load(file)
        return 'Already drew {}\n'.format(result)
        
    else:
        with open('src/lunch_candidate.json', 'r') as file:
            lunch_candidate = json.load(file)
        name = lunch_candidate['name']
        proposal = lunch_candidate['proposal']

        index = random.choice(list(enumerate(proposal)))[0]

        result = {
            'name': name[index],
            'proposal': proposal[index]
        }
        with open('src/result.json', 'w') as file:
            json.dump(result, file)
        return 'Drew result: {}\n'.format(result)


if __name__ == '__main__':
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()

    app.run(host='127.0.0.1', debug=True)