import axios from 'axios'

const HTTP = axios.create({
    baseURL: `https://backend.smartcheck.ml/api`,
    timeout: 5000,
    headers: {
      'Content-Type': 'multipart/form-data',
      'Access-Control-Allow-Origin': '*'
    }
  })

export const attendanceLogService = {
    checkInOut
};

function checkInOut(phoneNo, curriculumNo, checkInOut, signature) {
    const requestBody = new FormData();
    requestBody.append('phoneNo', phoneNo);
    requestBody.append('curriculumNo', curriculumNo);
    requestBody.append('checkInOut', checkInOut);
    requestBody.append('signature', signature);
    
    return HTTP.post(`/resource/attendancelogs/new`, requestBody)
        .then(response => {
            return response;
        });
}