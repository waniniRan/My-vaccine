import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
  timeout: 10000,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

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
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      window.location.href = '/';
    }
    return Promise.reject(
      error.response && error.response.data && error.response.data.detail
        ? error.response.data.detail
        : error.message || 'Network error'
    );
  }
);

export default api; 