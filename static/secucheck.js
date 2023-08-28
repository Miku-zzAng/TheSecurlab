document.addEventListener('DOMContentLoaded', function () { // 문서가 모두 열리면 함수를 실행하는 이벤트리스너
    let targetPosition = 200;
    let currentPosition = 200;
    const navbar = document.querySelector(".navbar2"); // 해당 class 가진 태그를 각각의 변수에 할당
    const navbarCover = document.querySelector(".navbar-cover");

    function smoothFollow() { // current를 target 방향으로 부드럽게 움직이게 하는 함수.
        currentPosition += (targetPosition - currentPosition) * 0.9; // currentPosition 값이 실시간으로 바뀌며 부드럽게 움직여짐.
        navbar.style.top = currentPosition + "px"; // 네비바와 커버 css의 top 속성을 현재위치 값으로 동적으로 바꿔감.
        navbarCover.style.top = currentPosition + "px";
        requestAnimationFrame(smoothFollow);
    }

    window.addEventListener("scroll", function () {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        const navbarHeight = navbar.offsetHeight;
    
        // 스크롤 가능한 최대 위치
        const maxScrollPosition = documentHeight - windowHeight;
    
        // 네비바가 완전히 보일 수 있는 최대 스크롤 위치
        const maxNavbarPosition = maxScrollPosition + 200 - navbarHeight;
    
        targetPosition = Math.min(window.scrollY + 200, maxNavbarPosition);
    });
    

    smoothFollow();
});

document.addEventListener('DOMContentLoaded', function () {
    const topics = document.querySelectorAll('.topic-wrapper');

    topics.forEach(topic => {
        let tree = topic.querySelector('.tree-wrapper');

        topic.addEventListener('click', function () {
            // 다른 모든 tree-wrapper를 닫음
            topics.forEach(innerTopic => {
                if (innerTopic !== topic) { // 현재 클릭된 주제를 제외하고
                    let innerTree = innerTopic.querySelector('.tree-wrapper');
                    innerTree.style.height = '0px';
                }
            });

            if (tree.style.height === '0px' || tree.style.height === '') {
                tree.style.height = tree.scrollHeight + 'px';
            } else {
                tree.style.height = '0px';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // navbar2 내부의 모든 <a> 태그에 이벤트 리스너 추가
    document.querySelectorAll('.navbar2 a').forEach(function (link) {
        link.addEventListener('click', function (e) {
            e.preventDefault(); // 기본 동작 중지
            const targetId = this.getAttribute('href'); // 연결된 요소의 ID 가져오기
            const targetElement = document.querySelector(targetId); // 해당 요소 선택
            if (targetElement) {
                const rect = targetElement.getBoundingClientRect();
                const offset = rect.top + window.pageYOffset - (window.innerHeight / 2) + (rect.height / 2);
                window.scrollTo({
                    top: offset,
                    behavior: 'smooth'
                });
            }
        });
    });
});

// 해당 로직을 함수로 분리
function adjustTopicVisibility() {
    const topics = document.querySelectorAll('.topic-wrapper');
    const middle = window.innerHeight * 0.4;

    let closest = null;
    let closestDistance = Infinity;

    topics.forEach(topic => {
        const box = topic.getBoundingClientRect();
        const focusPoint = box.top + (box.height * 0.95);
        const distance = Math.abs(middle - focusPoint);

        if (distance < closestDistance) {
            closestDistance = distance;
            closest = topic;
        }

        topic.classList.remove('active');
        topic.classList.remove('nearby1');
        topic.classList.remove('nearby2');
    });

    if (closest) {
        closest.classList.add('active');
        const prevElement = closest.previousElementSibling;
        const nextElement = closest.nextElementSibling;

        if (prevElement) prevElement.classList.add('nearby1');
        if (nextElement) nextElement.classList.add('nearby1');

        const prevElement2 = prevElement ? prevElement.previousElementSibling : null;
        const nextElement2 = nextElement ? nextElement.nextElementSibling : null;

        if (prevElement2) prevElement2.classList.add('nearby2');
        if (nextElement2) nextElement2.classList.add('nearby2');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    adjustTopicVisibility();
    window.addEventListener('scroll', adjustTopicVisibility);
});