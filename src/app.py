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

global DREW 
DREW = False
global result
result = {}
DROW_TIME = os.environ.get('DROW_TIME') or 'today'
if DROW_TIME == 'today':
    DROW_TIME = datetime.datetime.now().strftime('%Y-%m-%d') + ' 12:00:00'
else:
    DROW_TIME = DROW_TIME

@app.route('/time_info', methods=['GET'])
def get_time_info():
    if DREW is True:
        return 'Already drew {}\n'.format(result)
    
    return 'Gonna drow the meal at {}\nCurrent time: {}'.format(
        DROW_TIME, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


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
        if DREW is True:
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
def get_drow_result():
    if DREW is True:
        return 'Result {}\n'.format(result)
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

def drow_lunch():
    if DREW is True:
        return 'Already drew {}\n'.format(result)
    DREW = True
    with open('src/lunch_candidate.json', 'r') as file:
        lunch_candidate = json.load(file)
    name = lunch_candidate['name']
    proposal = lunch_candidate['proposal']

    index = random.choice(list(enumerate(proposal)))[0]

    result = {
        'name': name[index],
        'proposal': proposal[index]
    }
    return 'Drew result: {}\n'.format(result)

@app.route('/drow', methods=['POST'])
def force_drow():
    DREW = True
    with open('src/lunch_candidate.json', 'r') as file:
        lunch_candidate = json.load(file)
    name = lunch_candidate['name']
    proposal = lunch_candidate['proposal']

    index = random.choice(list(enumerate(proposal)))[0]

    result = {
        'name': name[index],
        'proposal': proposal[index]
    }
    return 'Drew result: {}\n'.format(result)
     

if __name__ == '__main__':

    app.run(host='127.0.0.1', debug=True)
    sched.add_job(drow_lunch, 'date', run_date=DROW_TIME)
    while True:
        sched.start()