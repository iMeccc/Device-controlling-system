import axios from 'axios';

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

// --- Authentication Service ---
export const login = async (email, password) => {
  // ... (this function remains the same)
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
export const getUsers = async () => {
  try {
    const response = await apiClient.get('/users/');
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
  // ... (this function remains the same)
  try {
    const response = await apiClient.get('/instruments/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getInstrumentById = async (instrumentId) => {
  // ... (this function remains the same)
  try {
    const response = await apiClient.get(`/instruments/${instrumentId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// --- Reservation Service ---
export const getReservationsByInstrument = async (instrumentId) => {
  // ... (this function remains the same)
  try {
    const response = await apiClient.get(`/reservations/instrument/${instrumentId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// --- NEW: Create Reservation Service ---
export const createReservation = async (reservationData) => {
  // Thanks to the interceptor, the token will be added automatically!
  try {
    const response = await apiClient.post('/reservations/', reservationData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getMyReservations = async () => {
  // Thanks to the interceptor, the token is added automatically
  try {
    const response = await apiClient.get('/reservations/my-reservations');
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