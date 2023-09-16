import { createStore } from 'vuex'
import account from '@/modules/account/store/account';
import auction from '@/modules/auction/store/auction';
import card from '@/modules/card/store/card';
import football from '@/modules/sports/football/store/football';
import settings from '@/modules/settings/store/settings';
import wallet from '@/modules/wallet/store/wallet';

export default createStore({
  state: {
    successMessages: null,
    errorMessages: null,
  },
  getters: {
    getSuccessMessages: (state) => state.successMessages,
    getErrorMessages: (state) => state.errorMessages,
  },
  mutations: {
    setSuccessMessages(state, messages) {
      state.successMessages = messages;
    },
    setErrorMessages(state, messages) {
      state.errorMessages = messages;
    },
    clearLogMessages(state) {
      state.successMessages = null;
      state.errorMessages = null;
    }
  },
  actions: {
    setSuccessMessages({ commit }, messages) {
      commit('setSuccessMessages', messages);
    },
    setErrorMessages({ commit }, messages) {
      commit('setErrorMessages', messages);
    }
  },
  modules: {
    account,
    auction,
    card,
    football,
    settings,
    wallet,
  }
})
