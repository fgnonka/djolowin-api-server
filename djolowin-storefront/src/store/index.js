import { createStore } from 'vuex'
import account from '@/modules/account/store/account';
import football from '@/modules/sports/football/store/football';

export default createStore({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    account,
    football,
  }
})
