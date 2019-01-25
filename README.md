## Project Info
 1. 프로젝트명 : simple-smart-check
 2. 내용 : KISA 교육과정 서명 및 출결관리 웹서비스
    - 핵심기능
      - backend (API 서버, https://backend.smartcheck.ml)
      - frontend
        - www (서명 페이지, https://www.smartcheck.ml)
          - 전자서명 및 저장
        - admin (관리자 페이지, https://admin.smartcheck.ml)
          - 수업 목록 관리(추가/삭제)
          - 수업별/참여자별 출석부 관리 및 엑셀파일 다운로드
          - 엑셀파일을 통한 신청자 일괄 업로드
          - 신청자 상태(선정, 참석, 수료, 취직) 업데이트 및 개인정보 조회
      
    - 주요 리소스 및 아키텍쳐
      - Serverless: AWS(S3, Route53, Certificate Manager, CloudFront, Lambda, API Gateway, RDS)
      - Frontend1 : Vue.js / OnsenUI
      - Frontend2 : Vue.js / vue-element-admin(Element UI)
      - Backend : Python / Flask, Zappa, Sqlalchemy(ORM), pandas, Swagger UI

## Prerequsite
- NPM : https://nodejs.org
- YARN : https://yarnpkg.com/lang/en/
- PIPENV : https://github.com/pypa/pipenv

## Licensing
[MIT License](LICENSE.md)
