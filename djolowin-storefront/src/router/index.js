import {createRouter, createWebHistory} from 'vue-router';
import accountRoutes from '@/modules/account/routes.js';
import footballRoutes from '@/modules/sports/football/routes.js';
import store from '@/store/index.js';

const routes = [
  ...accountRoutes,
  ...footballRoutes,
  {
    path: '/',
    name: 'Welcome',
    component: () => import ('../views/WelcomeView.vue'),
  },
];

const router = createRouter ({
  history: createWebHistory (process.env.BASE_URL),
  routes,
});

router.beforeEach ((to, from, next) => {
  if (to.matched.some (record => record.meta.requiresAuth)) {
    if (!store.getters['account/isTokenActive']) {
      next ({
        name: 'Login',
        query: {redirect: to.fullPath},
      });
    } else {
      next ();
    }
  } else if (to.matched.some (record => record.meta.requiresLoggedOut)) {
    if (store.getters['account/isTokenActive']) {
      next ({ name: 'Home' });
    } else {
      next ();
    }
  } else {
    next ();
  }
});

export default router;
