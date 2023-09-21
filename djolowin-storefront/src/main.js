import {createApp, h} from 'vue';
import { createPinia } from 'pinia';
// import {ApolloClient, InMemoryCache} from '@apollo/client/core';
// import {createApolloProvider} from '@vue/apollo-option';
import App from './App.vue';
import router from './router';
import { useWalletStore } from './stores/wallet';

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import vue3GoogleLogin from 'vue3-google-login';
import VueCountdown from '@chenfengyuan/vue-countdown';

const CLIENT_ID = '895349954455-07j550leaklcui189sq2q1sid013cdtu.apps.googleusercontent.com';
const pinia = createPinia ();
const app = createApp ({
  render: () => h (App),
  beforeCreate () {
    const walletStore = useWalletStore ();
    try{
      walletStore.pullWalletData ();
    } catch (e) {
      console.log (e);
    }
  },
});

app.component (VueCountdown.name, VueCountdown);
app.use (vue3GoogleLogin, {
  clientId: CLIENT_ID,
  scope: 'profile email',
});
app.use (router).use (pinia).mount ('#app');
