import { reactive } from 'vue';

export const authState = reactive({
  user: null, // Holds the current user object
  isAuthenticated: false, // Is the user logged in?
  isAdmin: false, // Is the user an admin?
});

export const authMethods = {
  setUser(user) {
    authState.user = user;
    authState.isAuthenticated = !!user;
    authState.isAdmin = user ? user.role === 'admin' : false;
  },
  logout() {
    localStorage.removeItem('access_token');
    this.setUser(null);
  }
};