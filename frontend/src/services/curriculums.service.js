import request from '../backend'

export const curriculumsService = {
    fetchCurriculmList
};

function fetchCurriculmList(query) {
    return request({
        url: '/resource/curriculums/filter',
        method: 'get',
        params: query
    })
}