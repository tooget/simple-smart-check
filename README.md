## Project Info
 1. 이름: Smart Check
 2. 내용 : Blockchain을 활용한 출결관리 dApp
    - 핵심기능
      - Smart Contract를 활용한 _출석부_ 생성 및 관리
      - 수업별 출결 현황 조회 
      - 참여자별 해당 수업에 대한 출석여부 확인  
    - 구현형태 : Hybrid App
    - 주요 리소스 및 아키텍쳐
      - Serverless: AWS(S3, Route53, Certificate Manager, CloudFront, Lambda, API Gateway)
      - Blockchain Network: AWS(EC2, ECS Cluster)
      - Front-End : Vue.js, OnsenUI, Javascript, CSS
      - Back-End : Flask, Zappa, Web3.py, Python
      
![](https://github.com/yunsu246/smart-check/blob/master/docs/Smart-Check%20Architecture.png)

## Prerequsite
- OS: Ubuntu 18.04.1 LTS
- NPM : https://nodejs.org
- YARN : https://yarnpkg.com/lang/en/
- PIPENV : https://github.com/pypa/pipenv
- WEB3.PY : https://github.com/ethereum/web3.py
  
- IDE: (eg. Intelij, Eclipse, WinStorm, Visual Studio etc.)
- (Optional) IDE에 맞는 Solidity 플러그인 추가 
- Metamask : https://metamask.io/

## Licensing

[MIT License](LICENSE.md)
