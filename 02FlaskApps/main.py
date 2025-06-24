# HTML파일을 템플릿으로 사용하기 위한 모듈 임포트
from flask import Flask, render_template
# 폼값 처리를 위한 모듈 임포트
from flask import request
# 화면이동, 세션처리 등을 위한 모듈 임포트
from flask import redirect, session, url_for
# 문자열 깨짐 방지를 위한 인코딩 처리를 위한 모듈 임포트
from markupsafe import escape

# 플라스크 앱 초기화
app = Flask(__name__)

# 앱을 최초로 실행했을때의 화면. 주로 index화면이라고 한다.
@app.route('/')
def root():
  return "Hello Flask Apps"

# 이미지 사용을 위한 static 폴더 확인용
# 요청명과 함수명은 보통 동일하게 작성한다.(필수사항은 아님)
@app.route('/image')
def image():
  # render_templates() 함수로 템플릿으로 사용할 HTML 파일을 렌더링한다.
  # 프로젝트에 생성된 templates 폴더 하위로 경로가 자동으로 지정된다. 
  return render_template('static.html')

'''
Jinja2는 플라스크에서 사용하는 템플릿 엔진으로, 웹개발에서 사용되는 
HTML 문서에 동적인 데이터를 삽입할 수 있게 해준다. 
즉 HTML 문서에 Python 코드를 사용할 수 있게 해주는 엔진이다. 
'''
@app.route('/jinja2')
def jinja2():
  '''
  함수에서 처리한 내용을 템플릿 파일로 전달하기 위해 여러개의 인수를
  아래와 같이 추가할 수 있다. 문자열과 리스트를 전달하고 있다. 
  '''
  return render_template('jinja2.html',
                  title = 'Jinja2',
                  home_str = 'Jinja2를 알아봅시다',
                  home_list=  [1,2,3,4,5])
  
# 폼값을 입력하고 전송하기 위한 페이지
@app.route('/form')
def info():
  return render_template('form.html')

# 라우팅 설정시 methods 속성에 사용할 방식을 리스트로 설정
@app.route('/method', methods=['GET', 'POST'])
def method():
  if request.method == 'GET':
    # GET방식 : form 데이터를 request.args로 받음
    args_dict=request.args.to_dict()
    # 전송된 폼값 전체를 딕셔너리로 변환 후 출력
    print("args_dict(GET):", args_dict)
    userid = request.args["userid"] #방식1
    # 함수의 인수로 접근하여 사용
    name = request.args.get("name") #방식2
    email = request.args.get("email")
    # POST 방식에서 사용하는 form은 사용할 수 없으므로 None으로 출력됨
    fail = request.form.get("name") #의도적 오류(None)
    print("실패 예시 request.form.get(name):", fail)
    # 템플릿을 렌더링하면서 필요한 변수는 인수로 전달
    return render_template(
      'get.html',
      userid=userid,
      name=name,
      email=email,
      fail=fail
    )
  else:
    # POST 방식 : form 데이터를 request.form 으로 받음
    form_dict = request.form.to_dict()
    print("form_dict(POST):", form_dict)
    userid = request.form["userid"]
    name = request.form.get("name")
    email = request.form.get("email")
    fail = request.args.get("name")
    print("실패 예시 request.args.get(name):", fail)
    return render_template(
      'post.html',
      userid=userid,
      name=name,
      email=email,
      fail=fail
    )

# URL 패스 Variable 1
@app.route('/hello/<name>')
def hello(name):
  return "내 이름은 {}".format(name)

# URL 패스 Variable 2
@app.route('/input/<int:num>')
def input(num):
  name=''
  if num == 1:
    name="홍길동"
  elif num == 2:
    name="전우치"
  elif num == 3:
    name="손오공"
  return "내 선택은 {}".format(name)
     
def hello(name):
  return "내 이름은 {}".format(name)

# session 사용시 필수사항인 시크릿키
app.secret_key = "wbcat3232"

# 예시 사용자(실제 DB 연결 대신 하드코딩)
users = {
  'admin' : '1234',
  'user' : '9876'
}

# 세션 정보가 필요한 마이페이지를 가정
@app.route('/mypage')
def mypage():
  # 페이지로 진입시 세션정보가 있는지 확인(로그인 되었는지 확인)
  if 'username' in session:
    # 로그인 된 상태라면 welcome페이지를 렌더링한다. 
    # 템플릿으로 회원의 아이디를 전달
    return render_template('welcome.html',
                           username=escape(session['username']))
  # 로그인이 안된 상태라면 login 페이지로 이동한다.  
  # url_for() 함수의 인수는 실행할 함수명을 기술한다. 
  return redirect(url_for('login'))

# 로그인 페이지
@app.route('/login', methods=["GET", "POST"])
def login():
  # 폼값을 입력후 submit(전송)했을때의 실행코드
  if request.method == "POST":
    # POST 방식의 전송이므로 form을 이용해서 값 받음
    input_id = request.form['username']
    input_pw = request.form['password']
    # 사용자 인증. 입력한 정보와 일치하는지 확인
    if input_id in users and users[input_id] == input_pw:
      # 정보가 일치하면 세션에 사용자의 아이디를 입력해서 생성
      session['username'] = input_id
      # 마이페이지로 이동
      return redirect(url_for('mypage'))
    else:
      # 사용자 정보가 일치하지 않는 경우에는 다시 로그인 페이지로 이동.
      # 이때 error라는 변수에 메시지를 전달한다. 
      return render_template('login.html',
                            error='아이디 또는 비밀번호가 틀렸습니다.')
  # 첫 진입시에는 메뉴 클릭을 통해 이동하게 되므로 GET 방식의 요청임
  # 따라서 로그인 폼을 보여준다. 
  return render_template('login.html')

# 로그아웃 처리
@app.route('/logout')
def logout():
  # 세션에 저장된 사용자 정보를 삭제한다. 
  session.pop('username', None)
  # 삭제가 완료되면 index 화면으로 이동한다. 
  return redirect(url_for('root'))
    
# 요청시 외부페이지로 이동한다. 
@app.route('/daum')
def daum():
  return redirect("https://daum.net/")
@app.route('/naver')
def naver():
  return redirect("https://naver.com/")

# Page not found 에러 발생시 핸들링
@app.errorhandler(404)
def page_not_found(error):
  # 실제 서비스에서는 Parking 페이지를 만들어서 보여줌(네이버, 다음 참조)
  print("오류 로그:", error) #서버 콘솔에 출력
  # return "페이지가 없습니다. URL을 확인하세요"
  return "페이지가 없습니다. URL을 확인하세요", 404
# return문 마지막에 404 파라미터가 없으면 Status code가 200으로 반환되므로
# 반드시 추가하는 것이 좋다.

# 플라스크 애플리케이션 작성시 모든 함수를 정의한 후 app.run()을 실행해야 한다.
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)
# 만약 아래쪽에 함수가 정의되어 있으면 오류가 발생한다. 