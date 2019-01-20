import request from '@/utils/request'

export function fetchAttendanceLogsListfile(query) {
  return request({
    url: '/resource/attendancelogs/listfile',
    method: 'get',
    params: query,
    responseType: 'blob' // important
  })
}
