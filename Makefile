TAG="random-lunch:dev"
# DROW_TIME="1992-04-18T12:00"
DROW_TIME="today"
activate ::
	gunicorn -w 4 --log-config .config/logging.conf -c .config/gunicorn_config.py src/app.py
build-dev ::
	docker build -t=${TAG} ./
run-dev ::
	docker run --rm -it -e DROW_TIME=${DROW_TIME} random-lunch:dev
get_time_info ::
	curl localhost:5000/time_info
run :: 
	docker run --rm -it -e DROW_TIME=${DROW_TIME} random-lunch:latest 

	

