import request from '@/utils/request'

export function fetchAttendanceLogsList(query) {
  return request({
    url: '/resource/attendancelogs/list',
    method: 'get',
    params: query
  })
}

export function fetchAttendanceLogsListfile(query) {
  return request({
    url: '/resource/attendancelogs/listfile',
    method: 'get',
    params: query,
    responseType: 'blob'
  })
}
