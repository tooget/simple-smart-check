import CURRICULUMS_ALL from '../../graphql/AllCurriculums.gql'
import CURRICULUMS_CREATE from '../../graphql/CreateCurriculumsData.gql'
import { apolloClient } from '../../utils/apollo'
import request from '@/utils/request'

export function fetchCurriculumsList(query) {
  return request({
    url: '/resource/curriculums',
    method: 'get',
    params: query
  })
}

export async function fetchCurriculumsListGql(variables) {
  return await apolloClient.query({
    query: CURRICULUMS_ALL,
    variables: variables
  })
}

export async function createCurriculumsData(variables) {
  return await apolloClient.mutate({
    mutation: CURRICULUMS_CREATE,
    variables: variables
  })
}

export function updateCurriculumsData(data) {
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

export function deleteCurriculumsData(curriculumNo) {
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
