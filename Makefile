TAG=random-lunch:dev
# DROW_TIME="1992-04-18 12:00:00"
DROW_TIME=today
port=5000
activate ::
	gunicorn -w 4 --log-config config/logging.conf -c config/gunicorn_config.py src.app:app

build-dev ::
	docker build -t=${TAG} ./

run-dev ::
	docker run --rm -it -e DROW_TIME=${DROW_TIME} -p ${port}:5000 random-lunch:dev

get_time_info ::
	curl localhost:5000/time_info

add-candidate ::
	curl -X POST -H "Content-Type: application/json" -d '${data}' localhost:5000/lunch_candidate

run :: 
	docker run --rm -it -e DROW_TIME=${DROW_TIME} -p ${port}:5000 random-lunch:latest 

	

