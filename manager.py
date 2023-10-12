
def deploy():
	"""Run deployment tasks."""
	from app import create_app,db
	from models import User, Order, Publisher, Author, Comic, Order_comic, Genre, Genre_comic

	app = create_app()
	app.app_context().push()
	db.drop_all()
	db.create_all()
	
deploy()