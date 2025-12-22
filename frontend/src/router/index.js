import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import InstrumentDetailView from '../views/InstrumentDetailView.vue'
import MyReservationsView from '../views/MyReservationsView.vue' // <-- 1. Import the new view

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ... (other routes remain the same) ...
    { path: '/', redirect: '/dashboard' },
    { path: '/login', name: 'login', component: LoginView },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/instrument/:id',
      name: 'instrument-detail',
      component: InstrumentDetailView,
      meta: { requiresAuth: true }
    },
    {
      path: '/my-reservations', // <-- 2. Add the new route
      name: 'my-reservations',
      component: MyReservationsView,
      meta: { requiresAuth: true }
    }
  ]
})

// ... (Navigation guard remains the same) ...
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('access_token');
  if (to.meta.requiresAuth && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router