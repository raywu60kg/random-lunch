from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask, jsonify, request
import json
import logging
import os
import random
import datetime

sched = BlockingScheduler()
package_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

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

    app.run(host='127.0.0.1', debug=True)
    sched.add_job(draw_lunch, 'date', run_date=DRAW_TIME)
    while True:
        sched.start()