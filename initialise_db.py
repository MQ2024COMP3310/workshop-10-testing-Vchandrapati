from project import db, create_app, models

if __name__ == '__main__':
  app = create_app()
  with app.app_context():
    db.create_all()
  print("Intialisation finished!")
