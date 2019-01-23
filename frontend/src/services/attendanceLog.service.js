import request from '../backend'

export const attendanceLogService = {
    checkInOut
};

function checkInOut(phoneNo, curriculumNo, checkInOut, signature) {
    const requestBody = new FormData();
    requestBody.append('phoneNo', phoneNo);
    requestBody.append('curriculumNo', curriculumNo);
    requestBody.append('checkInOut', checkInOut);
    requestBody.append('signature', signature);
    
    return request({
        url: '/resource/attendancelogs',
        method: 'post',
        data: requestBody
    });
}