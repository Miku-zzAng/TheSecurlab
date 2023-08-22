function login() {
    var loginId = document.getElementById("login_id").value; // 입력한 아이디 변수에 저장
    var loginPw = document.getElementById("login_pw").value; // 입력한 패스워드 변수에 저장

    if (loginId === "your_valid_id" && loginPw === "your_valid_password") {  //입력한 아이디와 비밀번호 비교
        window.location.href = "메인페이지로 이동.html"; // 메인 페이지로 이동
    } else {
        alert("로그인 실패: 아이디 또는 비밀번호가 올바르지 않습니다."); // 일단 넣어 둠 알림창 말고 패스워드 인풋 박스 밑에 넣는게 더 예쁠 듯 함
    }
}