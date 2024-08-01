from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Host, Port  # Import directly since models.py is now in the same directory

app = Flask(__name__)

DATABASE_URL = "postgresql://username:password123@db:5432/scanner"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route('/api/hosts', methods=['GET'])
def get_hosts():
    db = next(get_db())
    hosts = db.query(Host).all()
    result = []
    for host in hosts:
        result.append({
            'ip': host.ip,
            'ports': [port.port for port in host.ports]
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
