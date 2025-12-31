import { createRouter, createWebHistory } from 'vue-router'
import { authState, authMethods } from '../store/auth'; // Import state and methods
import { getCurrentUser } from '../services/api'; // Import the api call

// Import views
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import InstrumentDetailView from '../views/InstrumentDetailView.vue'
import MyReservationsView from '../views/MyReservationsView.vue'
import AdminLayout from '../layouts/AdminLayout.vue';
import UserManagement from '../views/admin/UserManagement.vue';
import InstrumentManagement from '../views/admin/InstrumentManagement.vue';
import PermissionManagement from '../views/admin/PermissionManagement.vue';
import ReservationManagement from '../views/admin/ReservationManagement.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ... (routes array remains the same)
    { path: '/', redirect: '/dashboard' },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } },
    { path: '/instrument/:id', name: 'instrument-detail', component: InstrumentDetailView, meta: { requiresAuth: true } },
    { path: '/my-reservations', name: 'my-reservations', component: MyReservationsView, meta: { requiresAuth: true } },
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        { path: '', redirect: '/admin/users' },
        { path: 'users', name: 'admin-users', component: UserManagement },
        { path: 'instruments', name: 'admin-instruments', component: InstrumentManagement },
        { path: 'permissions', name: 'admin-permissions', component: PermissionManagement },
        { path: 'reservations', name: 'admin-reservations', component: ReservationManagement },
      ]
    }
  ]
})

// --- NEW, ROBUST Navigation Guard ---
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('access_token');

  // If we don't have user info but have a token, it's the first navigation.
  // We MUST fetch user info before proceeding.
  if (token && !authState.isAuthenticated) {
    try {
      const user = await getCurrentUser();
      authMethods.setUser(user);
    } catch (error) {
      // Token is invalid, force logout.
      authMethods.logout();
      // If the target route requires auth, redirect to login. Otherwise, let them be.
      if (to.meta.requiresAuth) {
        return next({ name: 'login' });
      }
    }
  }
  
  // Now, we can safely check the auth state.

  // 1. Check if route requires admin
  if (to.meta.requiresAdmin && !authState.isAdmin) {
    // Redirect to dashboard if not an admin
    return next({ name: 'dashboard' });
  }

  // 2. Check if route requires auth
  if (to.meta.requiresAuth && !authState.isAuthenticated) {
    // Redirect to login if not authenticated
    return next({ name: 'login' });
  }
  
  // 3. Prevent logged-in users from accessing the login page again
  if (to.name === 'login' && authState.isAuthenticated) {
    return next({ name: 'dashboard' });
  }

  // All checks passed, proceed.
  next();
});

export default router