import axios from 'axios';
import { ElMessage } from 'element-plus';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Axios Request Interceptor ---
// This function will be called before every request is sent.
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      // If a token exists, add it to the Authorization header
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => {
    // Any status code that lie within the range of 2xx cause this function to trigger
    return response;
  },
  (error) => {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    if (error.response && error.response.status === 401) {
      // This is a specific check for "Unauthorized" errors
      console.error("Authentication Error: ", error.response.data);
      // Remove the invalid token
      localStorage.removeItem('access_token');
      // Show a message to the user
      ElMessage.error('您的登录已过期，请重新登录。');
      // Redirect to the login page after a short delay
      setTimeout(() => {
        window.location.href = '/login';
      }, 1500);
    }
    // Return a rejected promise to be caught by the original caller
    return Promise.reject(error);
  }
);

// --- Authentication Service ---
export const login = async (email, password) => {
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);
  try {
    const response = await apiClient.post('/users/login/access-token', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

// --- User Management Service ---
export const getUsers = async (params) => { // <-- Accept a 'params' object
  try {
    const response = await apiClient.get('/users/', { params }); // <-- Pass params to the request
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createUser = async (userData) => {
  try {
    const response = await apiClient.post('/users/', userData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteUser = async (userEmail) => {
  try {
    const response = await apiClient.delete(`/users/${userEmail}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// --- Instrument Service ---
export const getInstruments = async () => {
  try {
    const response = await apiClient.get('/instruments/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getInstrumentById = async (instrumentId) => {
  try {
    const response = await apiClient.get(`/instruments/${instrumentId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// --- Reservation Service ---
export const getReservationsByInstrument = async (instrumentId) => {
  try {
    const response = await apiClient.get(`/reservations/instrument/${instrumentId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// --- Create Reservation Service ---
export const createReservation = async (reservationData) => {
  // Thanks to the interceptor, the token will be added automatically!
  try {
    const response = await apiClient.post('/reservations/', reservationData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getMyReservations = async (params) => { // Accept params
  try {
    const response = await apiClient.get('/reservations/my-reservations', { params }); // Pass params
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const cancelReservation = async (reservationId) => {
  // Thanks to the interceptor, the token is added automatically
  try {
    const response = await apiClient.delete(`/reservations/${reservationId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getCurrentUser = async () => {
  // The interceptor will automatically add the token
  try {
    const response = await apiClient.get('/users/me');
    return response.data;
  } catch (error) {
    // If the token is invalid, the backend will return a 401, which will be caught here
    throw error;
  }
};

export const bulkCreateUsers = async (usersData) => {
  try {
    const response = await apiClient.post('/users/bulk-create', usersData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateUser = async (userEmail, userData) => {
  try {
    // We'll create a PUT /users/{user_email} endpoint in the backend
    const response = await apiClient.put(`/users/${userEmail}`, userData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// --- Instrument Management Service ---
export const createInstrument = async (instrumentData) => {
  try {
    const response = await apiClient.post('/instruments/', instrumentData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const updateInstrument = async (instrumentId, instrumentData) => {
  try {
    const response = await apiClient.put(`/instruments/${instrumentId}`, instrumentData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteInstrument = async (instrumentId) => {
  try {
    const response = await apiClient.delete(`/instruments/${instrumentId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// --- Permission Management Service ---
export const grantPermission = async (permissionData) => {
  // The backend expects user_email, not user_id. We need to construct it.
  // Or, better, we modify the backend to accept user_id.
  // Let's assume we will modify the backend for simplicity.
  try {
    const response = await apiClient.post('/permissions/grant', permissionData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const revokePermission = async (permissionData) => {
  try {
    const response = await apiClient.post('/permissions/revoke', permissionData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getAllReservations = async (params) => {
  try {
    // Pass the 'params' object to the request config.
    // Axios will automatically convert it to URL query parameters.
    const response = await apiClient.get('/reservations/all', { params });
    return response.data;
  } catch (error) {
    throw error;
  }
};