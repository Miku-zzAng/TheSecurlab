document.addEventListener("click", function (event) { //클릭 이벤트 감지
    const navbar = document.querySelector(".navbar");
    const submenu = document.querySelectorAll(".submenu");

    if (!navbar.contains(event.target)) { //navbar 이외에 요소에서 클릭 이벤트 발생했을 경우
        submenu.forEach(function (item) {
            item.style.display = "none"; //sub메뉴 요소 숨김
        });
    }
});