PWD = $(shell pwd)
PORT = 5000
default: 
	make build
	make run
build:
	docker build -t flask .
run:
	docker run --rm -it \
		--name flask_cont \
		-v $(PWD)/python/:/wd/ \
		-p $(PORT):5000 \
	 	-e LANG=C.UTF-8 \
		-e FLASK_APP=application.py \
		-w /wd/ \
		flask /bin/bash \
		#-e LC_ALL=C.UTF-8 \                                                     
			
