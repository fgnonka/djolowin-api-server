import {createRouter, createWebHistory} from 'vue-router';
import accountRoutes from '@/modules/account/routes.js';
import auctionRoutes from '@/modules/auction/routes.js';
import cardRoutes from '@/modules/card/routes.js';
import collectionRoutes from '@/modules/collections/routes.js';
import settingsRoutes from '@/modules/settings/routes.js';
import footballRoutes from '@/modules/sports/football/routes.js';
import walletRoutes from '@/modules/wallet/routes.js';

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

import {useAccountStore} from '@/stores/account';
router.beforeEach (async (to, from, next) => {
  const accountStore = useAccountStore ();
  accountStore.onStoreInit (); // Ensure the user is logged in before navigating to any route
  if (to.matched.some (record => record.meta.requiresAuth)) {
    if (!accountStore.isTokenActive) {
      try {
        await accountStore.refreshToken (); // Ensure refreshToken returns a promise

        if (!accountStore.isTokenActive) {
          // Token is still not active after refresh
          next (); // Allow navigation (e.g., go to login page)
        } else {
          next (); // Token is active; continue to the desired route
        }
      } catch (error) {
        console.error ('Error in refresh action:', error);
        // Handle errors if necessary
        next (); // Call next here to ensure the navigation continues even on error
      }
    } else {
      next (); // Token is already active; continue to the desired route
    }
  } else if (to.matched.some (record => record.meta.requiresLoggedOut)) {
    if (accountStore.isTokenActive) {
      next ({name: 'Home'}); // Redirect authenticated users to the "Home" route
    } else {
      next (); // Allow navigation for logged-out users
    }
  } else {
    next (); // For routes with no access control requirements
  }
});

export default router;
