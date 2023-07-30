import {createApp, h} from 'vue';
import {ApolloClient, InMemoryCache} from '@apollo/client/core';
import {createApolloProvider} from '@vue/apollo-option';

import App from './App.vue';
import router from './router';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const cache = new InMemoryCache ();

const apolloClient = new ApolloClient ({
    cache,
    uri: 'http://localhost:8000/graphql/',
});

const apolloProvider = createApolloProvider ({
  defaultClient: apolloClient,
});

const app = createApp ({
  render: () => h (App),
});

app.use(router)
app.use (apolloProvider)
app.mount ('#app')
