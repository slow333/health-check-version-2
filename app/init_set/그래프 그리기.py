# pip install pandas matplotlib

# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
db = SQLAlchemy(app)


class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    product_a = db.Column(db.Integer)
    product_b = db.Column(db.Integer)
    product_c = db.Column(db.Integer)

import pandas as pd

def get_sales_data():
    # SQLAlchemy ORM → Pandas DataFrame
    query = db.session.query(Sales).all()
    data = [{
        'date': row.date,
        'product_a': row.product_a,
        'product_b': row.product_b,
        'product_c': row.product_c
    } for row in query]
    return pd.DataFrame(data)    

import matplotlib.pyplot as plt

def plot_sales(df):
    plt.figure(figsize=(10, 6))
    # - y축에 여러 값을 넣는다는 건 여러 컬럼을 동시에 시각화한다는 의미입니다. plt.plot()을 여러 번 호출하면 됩니다.

    plt.plot(df['date'], df['product_a'], label='Product A')
    plt.plot(df['date'], df['product_b'], label='Product B')
    plt.plot(df['date'], df['product_c'], label='Product C')

    plt.title('Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    with app.app_context():
        df = get_sales_data()
        plot_sales(df)    