# SoFiA

 1. 재무항목 Up & Down 컨센서스 서비스
 2. 코드 템플릿(simple-smart-check)
    - 핵심기능
      - backend (API 서버, https://backend.smartcheck.gq)
      - frontend
        - www (서명 페이지, https://www.smartcheck.gq)
          - 전자서명 및 저장
        - admin (관리자 페이지, https://admin.smartcheck.gq)
          - 수업 목록 관리(추가/삭제)
          - 수업별/참여자별 출석부 관리 및 엑셀파일 다운로드
          - 엑셀파일을 통한 신청자 일괄 업로드
          - 신청자 상태(선정, 참석, 수료, 취직) 업데이트 및 개인정보 조회
      
    - 주요 리소스
      - Frontend1 : Vue.js / OnsenUI
      - Frontend2 : Vue.js / vue-element-admin(Element UI)
      - Backend : Python / Flask, Zappa, Sqlalchemy(ORM), pandas, Swagger UI

## Prerequsite
- NPM : https://nodejs.org
- YARN : https://yarnpkg.com/lang/en/
- PIPENV : https://github.com/pypa/pipenv

## Licensing
[Apache License 2.0](LICENSE.md)
