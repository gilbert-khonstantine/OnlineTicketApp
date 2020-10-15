import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy(app)

# put this class in main app
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    tag = db.Column(db.String(255), nullable=False)
    subtag = db.Column(db.String(255), nullable=False)
    image_link = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.id

# then run these to add to db
df = pd.read_csv('final_result.csv', index_col=[0])
print(df)

engine = create_engine('sqlite:///ticketapp.db')
db.Model.metadata.create_all(engine)
df.to_sql(con=engine, index_label='id', name=Product.__tablename__, if_exists='replace')
print('Done')
