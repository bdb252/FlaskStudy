from flask import Flask
app = Flask(__name__)

@app.route('/')
def root():
  return "Hello Flask(Main.py)"

# 실행
# FLASK_APP=Main.py FLASK_DEBUG=1