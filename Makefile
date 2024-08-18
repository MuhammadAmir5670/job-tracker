test:
	docker compose exec web python -m coverage run manage.py test
	docker compose exec web python -m coverage html
