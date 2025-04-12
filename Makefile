build-local:
	docker compose build

prod-compose-bash:
	docker compose up -d && \
	docker compose exec river_flows /bin/bash && \
	docker compose down

flake8:
	flake8

test-compose-bash:
	docker compose -f tests/docker-compose.yml up -d && \
	docker compose -f tests/docker-compose.yml exec river_flows /bin/bash && \
	docker compose -f tests/docker-compose.yml down