# flask 모듈 임포트
from flask import Flask
# Flask 객체 생성
app = Flask(__name__)

# 데코레이터를 이용해서 요청명에 대한 매핑을 한다. 이때 실행할 함수를 엔드포인트로 등록한다. 
@app.route('/')
def root():
  # 이 부분이 웹브라우저에 출력(렌더링)된다.
  return "Hello Flask(python Main.py)"

# 이 파일 자체를 python 명령으로 실행했을때 아래 지정한 옵션이 적용된 상태로 플라스크앱이 실행된다. 
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)
  
# 실행
# python Main.py 