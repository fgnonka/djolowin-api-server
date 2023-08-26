import { createStore } from 'vuex'
import account from '@/modules/account/store/account';
import auction from '@/modules/auction/store/auction';
import card from '@/modules/card/store/card';
import football from '@/modules/sports/football/store/football';
import wallet from '@/modules/wallet/store/wallet';

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
    auction,
    card,
    football,
    wallet,
  }
})
