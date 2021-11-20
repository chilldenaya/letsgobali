precommit:
	which pre-commit || (python3.7 -m pip install pre-commit==2.0.1 && pre-commit install)
	which autoflake || python3.7 -m pip install autoflake==1.3.1
	autoflake --in-place \
		--remove-all-unused-imports \
		--remove-duplicate-keys \
		--remove-unused-variables \
		-r .
	git ls-files -- . | xargs pre-commit run --files

build:
	chmod a+rw -R .
	chmod a+x -R dags
	docker-compose down || true
	make up

up:
	docker-compose up -d
	make prune
	make logs

stop:
	docker-compose stop

start:
	docker-compose start
	make prune
	make logs

prune:
	docker system prune -af --volumes
