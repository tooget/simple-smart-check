import request from '../backend'

export const curriculumsService = {
    fetchCurriculmList
};

function fetchCurriculmList(query) {
    return request({
        url: '/resource/curriculums',
        method: 'get',
        params: query
    })
}