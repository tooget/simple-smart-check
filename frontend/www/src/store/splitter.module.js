export const splitter = {
    strict: true,
    namespaced: true,
    state: {
    open: false
    },
    mutations: {
        toggle(state, shouldOpen) {
            if (typeof shouldOpen === 'boolean') {
                state.open = shouldOpen;
            } else {
                state.open = !state.open;
            }
        }
    }
}