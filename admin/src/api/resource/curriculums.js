import request from '@/utils/request'

export function fetchCurriculumList(query) {
  return request({
    url: '/resource/curriculums',
    method: 'get',
    params: query
  })
}

export function createCurriculumData(data) {
  const requestBody = new FormData()
  requestBody.append('curriculumCategory', data.curriculumCategory)
  requestBody.append('ordinalNo', data.ordinalNo)
  requestBody.append('curriculumName', data.curriculumName)
  requestBody.append('curriculumType', data.curriculumType)
  requestBody.append('startDate', data.startDate)
  requestBody.append('endDate', data.endDate)

  return request({
    url: '/resource/curriculums',
    method: 'post',
    data: requestBody
  })
}

export function updateCurriculumData(data) {
  const requestBody = new FormData()
  requestBody.append('curriculumNo', data.curriculumNo)
  requestBody.append('curriculumCategory', data.curriculumCategory)
  requestBody.append('ordinalNo', data.ordinalNo)
  requestBody.append('curriculumName', data.curriculumName)
  requestBody.append('curriculumType', data.curriculumType)
  requestBody.append('startDate', data.startDate)
  requestBody.append('endDate', data.endDate)

  return request({
    url: '/resource/curriculums',
    method: 'put',
    data: requestBody
  })
}

export function deleteCurriculumData(curriculumNo) {
  const requestBody = new FormData()
  requestBody.append('curriculumNo', curriculumNo)

  return request({
    url: '/resource/curriculums',
    method: 'delete',
    data: requestBody
  })
}

export function fetchCurriculumWithMemberCountList(query) {
  return request({
    url: '/resource/curriculums/withmembercount',
    method: 'get',
    params: query
  })
}
