import axios from 'axios'

const HTTP = axios.create({
    baseURL: `http://localhost:5000/api`,
    timeout: 5000,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  })

export const attendanceLogService = {
    checkInOut
};

function checkInOut(requestBody) {
    return HTTP.post(`/resource/attendance/log`, requestBody)
        .then(response => {
            return response;
        });
}