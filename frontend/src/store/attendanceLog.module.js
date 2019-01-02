import { attendanceLogService } from '../services';

export const attendanceLog = {
    namespaced: true,
    state: {
        checkInOut: {}
    },
    actions: {
        checkInOut({ commit }, { requestBody }) {
            commit('postCheckInOutRequest');

            attendanceLogService.checkInOut(requestBody)
                .then(
                    response => {
                        commit('postCheckInOutSuccess', response.data);
                    }
                )
                .catch(
                    error => {
                        commit('postCheckInOutFailure', error.response.data);
                    }
                );
        }
    },
    mutations: {
        postCheckInOutRequest(state) {
            state.checkInOut = { loading: true };
        },
        postCheckInOutSuccess(state, attendanceLog) {
            state.checkInOut = { items: attendanceLog };
        },
        postCheckInOutFailure(state, error) {
            state.checkInOut = { error };
        }
    }
}