build:
	docker-compose build
up:
	docker-compose up
down:
	docker-compose down
stop:
	docker-compose stop
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
