UI_DIR = smart_bookmarks/ui/

build:
	docker-compose build
up:
	docker-compose up -d
down:
	docker-compose down
stop:
	docker-compose stop
logs:
	docker-compose logs -f
start-db:
	docker-compose up -d database
stop-db:
	docker-compose stop database
dump-db:
	docker-compose exec database pg_dump -U dev -F p smart-bookmarks-dev
drop-db:
	docker-compose exec database dropdb -U dev smart-bookmarks-dev
create-db:
	docker-compose exec database createdb -U dev smart-bookmarks-dev
start-es:
	docker-compose up -d elasticsearch-head
start-app:
	docker-compose up -d app
setup-frontend:
	cd $(UI_DIR)frontend && yarn install
build-frontend:
	cd $(UI_DIR)frontend && yarn webpack
build-ui: build-frontend
	python manage.py collectstatic
clean-ui:
	rm -rf $(UI_DIR)frontend/node_modules/
	rm -rf $(UI_DIR)static/dist/
	rm -rf $(UI_DIR)static_root/
