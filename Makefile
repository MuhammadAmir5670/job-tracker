run:
	docker compose exec -it web python manage.py runserver_plus 0.0.0.0:8000

shell:
	docker compose exec web python manage.py shell_plus

test:
	docker compose exec web python -m coverage run manage.py test
	docker compose exec web python -m coverage html
