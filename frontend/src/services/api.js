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