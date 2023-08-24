from django.shortcuts import render,redirect
from users.forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from users.models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST": # 로그인 템플릿에서 요청온 것이 POST 형태라면
        receiveLoginForm = LoginForm(data=request.POST)
        if receiveLoginForm.is_valid():
            receiveUsername = receiveLoginForm.cleaned_data["username"]
            receivePassword = receiveLoginForm.cleaned_data["password"]

            search_user = authenticate(username=receiveUsername, password=receivePassword) # DB의 아이디와 비번이 일치하는 사용자가 있는지 검사

            if search_user:
                login(request, search_user) # 로그인 처리
                print(f"{receiveUsername}님이 로그인 했습니다.")
                return redirect("/")
            else:
                print("로그인에 실패했습니다. 입력값:", receiveUsername)
                receiveLoginForm.add_error(None, "아이디 또는 비밀번호가 일치하지 않습니다.")
        # 데이터 검증 또는 사용자 일치에서 둘다 틀린 경우, 로그인 창에 로그인 폼 띄움
        context = {"LoginForm": receiveLoginForm}
        return render(request, "users/login.html", context)

    else: # 로그인 창에 로그인 폼만 보내는 경우.
        createLoginForm = LoginForm() # 로그인 폼 인스턴스 생성
        context = {"LoginForm" : createLoginForm}
        return render(request, "users/login.html", context)
    


def logout_view(request):
    if request.user.is_authenticated:
        connect_username = request.user.username
        print(f"{connect_username}님이 로그아웃 했습니다.")
    else:
        connect_username = "Unknown User"
    logout(request) # 요청받음에 따라 로그아웃 수행
    return redirect("/")



def signup(request):
    if request.method == "POST":
        receiveSignupForm = SignupForm(data=request.POST, files=request.FILES)
        if receiveSignupForm.is_valid():
            receive_username = receiveSignupForm.cleaned_data["username"]
            receive_password1 = receiveSignupForm.cleaned_data["password1"]
            receive_password2 = receiveSignupForm.cleaned_data["password2"]
            receive_nickname = receiveSignupForm.cleaned_data["nickname"]
            receive_short_description = receiveSignupForm.cleaned_data["short_description"]
            if not receiveSignupForm.cleaned_data["profile_image"]:
                receive_profile_image = 'default_profile_image.png'
            else:
                receive_profile_image = receiveSignupForm.cleaned_data["profile_image"]
            
            if len(receive_nickname) > 8:
                receiveSignupForm.add_error("nickname", "닉네임의 최대 길이 제한은 8자입니다.")

            if receive_password1 != receive_password2 :
                receiveSignupForm.add_error("password2", "비밀번호와 비밀번호 확인란의 입력이 일치하지 않습니다.")
            
            if receive_password1 == receive_username:
                receiveSignupForm.add_error("password1", "아이디와 비밀번호는 동일하게 설정할 수 없습니다.")

            if User.objects.filter(username = receive_username).exists(): # DB의 조건에 해당하는 객체가 있다면 exists()
                receiveSignupForm.add_error("username", "이미 중복된 ID가 존재합니다.")

            if User.objects.filter(nickname = receive_nickname).exists(): # DB의 조건에 해당하는 객체가 있다면 exists()
                receiveSignupForm.add_error("nickname", "이미 중복된 닉네임이 존재합니다.") 

            if receiveSignupForm.errors:    # 에러가 났다면 에러를 포함한 폼을 사용해 회원가입 페이지 다시 렌더링
                print(f"가입자가 에러나서 다시 렌더링, 닉네임:{receive_nickname}, 아이디: {receive_username}")
                context = {"SignupForm": receiveSignupForm}
                return render(request, "users/signup.html", context)

            else:
                createUser = User.objects.create_user(
                    username = receive_username,
                    nickname = receive_nickname,
                    password = receive_password1,
                    profile_image = receive_profile_image,
                    short_description = receive_short_description,
                )
                login(request, createUser)
                print("성공 렌더")
                return redirect("/")

    else: # 회원가입 창에서 POST 요청이 따로 없다면, 빈 회원가입 창 보여준다.
        createSignupForm = SignupForm()
        context = {"SignupForm": createSignupForm}
        print("무반응 렌더")
        return render(request, "users/signup.html", context)