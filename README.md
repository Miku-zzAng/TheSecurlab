# TheSecurlab
### OWASP Top 10 기반 웹 애플리케이션 보안 사이트 설계 및 구현
- **2023 ANU yANUs 보안셀 개발2팀 산학협력 프로젝트**<br>
- **2023 ANU SW중심대학 성과발표회 발표작**<br>
- **2023 한국정보기술학회 추계종합학술대회 제출 논문**
- **2023 ANU SW융합학과 졸업작품전시회 전시작품**

## 참여 인원 
- 김선혁 (팀장)
- 전보경
- 최태용
- 김유진
- 김선민
- 안수윤
  
## Stacks
- JavaScript
- Python
  - BeautifulSoup
- Django
- ZAP (Zad Attack Proxy) - https://github.com/zaproxy/zap-api-python

---

## 추진 배경
**웹 개발자 및 운영자가 웹 사이트의 보안 취약점을 쉽게 확인하고 개선할 수 있는 자체 플랫폼 제공**
- 최근 웹 기술의 발전과 더불어 웹 사이트들이 여러 유형의 데이터와 많은 정보를 다루기 때문에 웹 보안에 대한 이해와 인식이 매우 중요해졌기에, 웹 개발자에게 웹 애플리케이션 보안 취약점을 식별하고 대비할 수 있도록 카테고리 별로 묶어 제시하여 웹 보안에 대한 이해와 인식을 향상시켜 안전한 웹 서비스 상태를 도모
- **OWASP Top 10**에 명시된 웹 어플리케이션 보안 취약점들로 작성된 **Security CheckList를 제작**하고, 사이트의 취약점을 스스로 파악하며, **공격 루트와 진단 방안 및 대응 방안**을 카테고리 별로 묶어 제시하여 웹 보안에 대한 이해와 인식 향상

## 주요 기능
1. **취약점 자동화 분석**
- Python을 활용하여 ZAP Proxy의 API를 호출한 후 프록시 설정을 조정, 로컬 웹 서버에서 ZAP 프록시 서버와 통신
- URL에 연결된 모든 페이지와 리소스를 크롤링하며, 이후 Passive Scan과 Active Scan을 실행하여 웹 어플리케이션 보안 취약점을 탐색
2. **취약점 분석 결과 제공**
- 스캔을 통해 얻은 웹 애플리케이션 보안 취약점 결과 정보는 High, Medium, Low, Informational의 네 가지 단계로 분류
- 발견한 취약점 목록을 상위 단계 유형의 취약점부터 내림차순으로 정렬 후 표시하며 종류 수, 스캔 과정에서 전송한 통합 요청(request) 횟수와 함께 제공
3. **관련 실제 보안 피해사례 제공**
- 실제로 발생한 관련 웹 보안 피해 사례 기사를 제공하기 위해 웹 크롤링(Crawling) 기술을 채택
- Python과 BeautifulSoup 라이브러리를 사용하여 NAVER 뉴스 기사 중 한국어로 작성된 기사의 이미지, 본론, 작성자 등의 정보를 수집
4. **Web Crawling Process**
- NAVER 사이트 URL에 대하여 생성 방식을 활용하여 특정 키워드에 대한 기사를 이중 필터링을 적용하여 자동으로 수집
- 지정된 페이지 수만큼 URL을 생성하여 각 기사의 HTML 요소를 이용하여 기사의 제목, 본문, 작성자, 사진 URL, 그리고 날짜를 수집한 후 DataFrame화 하여 DB에 연결

## 기대 효과
- 본 서비스에서 자체 제공하는 Security CheckList를 통하여 공통적인 웹 어플리케이션 보안 요구사항에 대한 표준화 제시 가능
- 웹 애플리케이션 보안에 대한 일반 사용자의 접근성과 이해도를 높이고, 웹 사이트의 안전성 향상 도모 가능
- 웹 개발자들이 웹 애플리케이션의 보안 상태를 자체적으로 진단하고 점검할 수 있는 자동화 취약점 분석 서비스 제공

---

## More Info

- [yANUs 보안팀 보안 체크리스트 개발계획서 종합.pdf](https://github.com/OuserDev/TheSecurlab/files/13651132/yANUs.pdf) (초안)
- [TheSeculab 보안셀 2팀 성과조사 발표 PPT.pdf](https://github.com/OuserDev/TheSecurlab/files/13651145/TheSeculab.2.PPT.pdf) (SW중심대학 성과발표회)
- [TheSeculab 보안셀 2팀 성과조사 발표 판넬.pptx](https://github.com/OuserDev/TheSecurlab/files/13651147/TheSeculab.2.pptx) (SW중심대학 성과발표회)
- [OWASP Top 10 웹 애플리케이션 보안 종합 포털사이트 구축 - 논문.pdf](https://github.com/OuserDev/TheSecurlab/files/13651159/OWASP.Top.10.-.pdf) (한국정보기술학회 추계종합학술대회 제출 논문)


