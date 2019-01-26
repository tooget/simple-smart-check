export default {
  route: {
    dashboard: 'Dashboard',
    manage: 'Manage',
    curriculums: 'curriculums',
    members: 'members',
    attendanceLogs: 'attendanceLogs'
  },
  navbar: {
    logOut: '로그아웃',
    dashboard: 'Dashboard'
  },
  login: {
    title: 'Login Form',
    logIn: 'Log in',
    username: 'Username',
    password: 'Password',
    any: 'any',
    thirdparty: 'Or connect with',
    thirdpartyTips: 'Can not be simulated on local, so please combine you own business simulation! ! !'
  },
  table: {
    browse: '파일찾기',
    search: '검색',
    add: '입력',
    export: 'Export',
    status: 'Status',
    actions: 'Actions',
    edit: '수정',
    publish: 'Publish',
    draft: 'Draft',
    delete: '삭제',
    download: '다운로드',
    cancel: '취소',
    confirm: '확인',
    dashboard: {
      name: 'Dashboard',
      curriculumNo: '과정ID',
      curriculumName: '과정명',
      curriculumCategory: '과정분류',
      ordinalNo: '기수',
      curriculumPeriod: '기간',
      curriculumType: '유형',
      ApplicantCount: '지원자(명)',
      MemberCount: '수강자(명)',
      MemberCompleteCount: '수료자(명)',
      MemberEmploymentCount: '취업자(명)'
    },
    curriculums: {
      name: '교육과정',
      delete: '데이터(전체) 삭제',
      donwnloadAtendanceLogs: '출석부 다운로드',
      curriculumNo: '과정ID',
      curriculumCategory: '과정분류',
      ordinalNo: '기수',
      curriculumName: '과정명',
      curriculumType: '유형',
      startDate: '시작일',
      endDate: '종료일',
      applicantsBulkInserted: '명단(EXCEL) 입력',
      insertedTimestamp: '입력시간',
      updatedTimestamp: '수정시간'
    },
    members: {
      name: '수강자',
      phoneNo: '전화번호',
      curriculumNo: '과정ID',
      attendancePass: {
        name: '선발여부',
        status: {
          Y: '선발',
          N: '탈락',
          null: '알수없음'
        }
      },
      attendanceCheck: {
        name: '참석여부',
        status: {
          Y: '참석',
          N: '불참',
          null: '알수없음'
        }
      },
      curriculumComplete: {
        name: '수료여부',
        status: {
          Y: '수료',
          N: '미수료',
          null: '알수없음'
        }
      },
      employment: {
        name: '취업여부',
        status: {
          Y: '취업',
          N: '미취업',
          null: '알수없음'
        }
      },
      ordinalNo: '기수',
      curriculumName: '과정명',
      curriculumCategory: '과정분류',
      startDate: '시작일',
      endDate: '종료일',
      applicantName: '지원자명',
      birthDate: '생년월일',
      email: '이메일',
      affiliation: '소속(회사/학교)',
      department: '부서(전공)',
      position: '직급(학년)',
      job: '지원자 상태',
      purposeSelection: '수강목적',
      careerDuration: '개발경력(기간)',
      agreeWithPersonalinfo: '개인정보 제공동의',
      agreeWithMktMailSubscription: '핀테크 기술지원센터 소식 수신여부',
      operationMemo: '비고'
    },
    attendanceLogs: {
      name: '출석부',
      phoneNo: '전화번호',
      applicantName: '지원자명',
      signatureTimestamp: '서명',
      attendanceDate: '출석일',
      In: '입실',
      Out: '퇴실',
      curriculumCategory: '과정분류',
      noSignature: '서명없음'
    }
  }
}
