import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import InstrumentDetailView from '../views/InstrumentDetailView.vue' // <-- 1. Import the new view

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/login', name: 'login', component: LoginView },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/instrument/:id', // <-- 2. Add the new DYNAMIC route
      name: 'instrument-detail',
      component: InstrumentDetailView,
      meta: { requiresAuth: true }
    }
  ]
})

// ... (The router.beforeEach navigation guard remains the same) ...
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('access_token');
  if (to.meta.requiresAuth && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router