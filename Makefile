.PHONY: migrations migrate all clean runserver populate superuser

migrations:
	python manage.py makemigrations accounts monitoring evolution prediction mathmodels dashboard report geolocation map

migrate:
	python manage.py migrate

runserver:
	python manage.py test
	python manage.py runserver 0.0.0.0:8000

all:
	python manage.py makemigrations accounts monitoring evolution prediction mathmodels dashboard report geolocation map
	python manage.py migrate
	python manage.py cadastrar_unidades_cnes
	python manage.py createsuperuser
	echo "from accounts.models import Account; su = Account.objects.get(id=1); su.health_center_id=1; su.user_profile='SS'; su.save()" | python manage.py shell
	#echo "import utils; utils.run_profiles(seed=None); utils.run_health_center_status()" | python manage.py shell
	python manage.py import_maragogi ~/maragogi.xlsx
	python manage.py runserver 0.0.0.0:8000

superuser:
	python manage.py createsuperuser
	echo "from accounts.models import Account; su = Account.objects.get(id=1); su.health_center_id=1; su.user_profile='SS'; su.save()" | python manage.py shell

populate:
	echo "import utils; utils.run_profiles(seed=None); utils.run_health_center_status()" | python manage.py shell
	#python manage.py import_maragogi ~/maragogi.xlsx

clean:
	rm -rf db.sqlite3
	find . ! -path "*env/*" -prune -path "*migrations/*" -delete

binaries:
	python3 setup.py build_ext -i -j12

remove_py: binaries
	find . -not -name "0*.py" -not -wholename "*venv*" -not -name "settings.py" -not -name "manage.py" -not -name "setup.py" -not -name "__init__.py" -not -name "wsgi.py" -name "*.py" -delete
	find . -not -name "0*.py" -not -wholename "*venv*" -not -name "settings.py" -not -name "manage.py" -not -name "setup.py" -not -name "__init__.py" -not -name "wsgi.py" -name "*.pyc" -delete
	find . -not -name "0*.py" -not -wholename "*venv*" -not -name "settings.py" -not -name "manage.py" -not -name "setup.py" -not -name "__init__.py" -not -name "wsgi.py" -name "*.c" -delete
	rm -rf build

remove_binaries:
	find . -not -name "0*.py" -not -wholename "*venv*" -not -name "settings.py" -not -name "manage.py" -not -name "setup.py" -not -name "__init__.py" -not -name "wsgi.py" -name "*.so" -delete
	rm -rf build
