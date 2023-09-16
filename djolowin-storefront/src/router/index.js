import {createRouter, createWebHistory} from 'vue-router';
import accountRoutes from '@/modules/account/routes.js';
import auctionRoutes from '@/modules/auction/routes.js';
import cardRoutes from '@/modules/card/routes.js';
import collectionRoutes from '@/modules/collections/routes.js';
import settingsRoutes from '@/modules/settings/routes.js';
import footballRoutes from '@/modules/sports/football/routes.js';
import walletRoutes from '@/modules/wallet/routes.js';
import store from '@/store/index.js';

const routes = [
  ...accountRoutes,
  ...auctionRoutes,
  ...collectionRoutes,
  ...settingsRoutes,
  ...footballRoutes,
  ...cardRoutes,
  ...walletRoutes,
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

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters['account/isTokenActive']) {
      try {
        store.dispatch('account/refreshToken').then(() => {
          if (!store.getters['account/isTokenActive']) {
            next();
          } else {
            next();
          }
        }).catch(error => {
          console.error('Error in refresh action:', error);
          // Handle errors if necessary
          next(); // Call next here to ensure the navigation continues even on error
        });
      } catch (error) {
        console.error('Error in refresh action:', error);
        // Handle errors if necessary
        next(); // Call next here to ensure the navigation continues even on error
      }
    } else {
      next();
    }
  } else if (to.matched.some(record => record.meta.requiresLoggedOut)) {
    if (store.getters['account/isTokenActive']) {
      next({ name: 'Home' });
    } else {
      next();
    }
  } else {
    next();
  }
});



export default router;
