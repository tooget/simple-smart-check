import request from '@/utils/request'

export function fetchMembersList(query) {
  return request({
    url: '/resource/members/list',
    method: 'get',
    params: query
  })
}

export function fetchMembersListfile(query) {
  return request({
    url: '/resource/members/listfile',
    method: 'get',
    params: query,
    responseType: 'blob'
  })
}

export function updateMembersData(data) {
  const requestBody = new FormData()
  requestBody.append('phoneNo', data.phoneNo)
  requestBody.append('curriculumNo', data.curriculumNo)
  requestBody.append('attendancePass', data.attendancePass)
  requestBody.append('attendanceCheck', data.attendanceCheck)
  requestBody.append('curriculumComplete', data.curriculumComplete)
  requestBody.append('employment', data.employment)

  return request({
    url: '/resource/members',
    method: 'put',
    data: requestBody
  })
}
