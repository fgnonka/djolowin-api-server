import {createApp, h} from 'vue';
// import {ApolloClient, InMemoryCache} from '@apollo/client/core';
// import {createApolloProvider} from '@vue/apollo-option';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import vue3GoogleLogin from 'vue3-google-login';


const CLIENT_ID = '895349954455-07j550leaklcui189sq2q1sid013cdtu.apps.googleusercontent.com';
const app = createApp ({
  render: () => h (App),
  beforeCreate () {
    try{
      this.$store.dispatch ('wallet/pullWalletData');
    } catch (e) {
      console.log (e);
    }
  },
});


app.use (vue3GoogleLogin, {
  clientId: CLIENT_ID,
  scope: 'profile email',
});
app.use (router).use (store).mount ('#app');
