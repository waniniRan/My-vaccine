import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
});

// Request interceptor to add Authorization header
api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));

// Helper to extract data from various response formats
export function extractData(response) {
  if (response?.data) {
    if (typeof response.data === 'object' && 'data' in response.data) {
      return response.data.data;
    }
    return response.data;
  }
  return response;
}

// Add response interceptor
api.interceptors.response.use(
  (response) => {
    response.data = extractData(response);
    return response;
  },
  async (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      await AsyncStorage.removeItem('accessToken');
      await AsyncStorage.removeItem('refreshToken');
      // Optionally, trigger navigation to login
    }
    return Promise.reject(error);
  }
);

export default api; 