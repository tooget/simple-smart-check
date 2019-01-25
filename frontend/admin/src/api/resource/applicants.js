import request from '@/utils/request'

export function createApplicantsBulk(data) {
  const requestBody = new FormData()
  requestBody.append('curriculumNo', data.curriculumNo)
  requestBody.append('applicantsBulkXlsxFile', data.applicantsBulkXlsxFile)
  return request({
    url: '/resource/applicants/bulk',
    method: 'post',
    data: requestBody
  })
}
