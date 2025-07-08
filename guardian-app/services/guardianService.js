import api from './api';

/**
 * Login for guardian
 * @param {Object} credentials - { national_id, password }
 * @returns {Promise<Object>} JWT tokens and password_change_required
 */
async function login(credentials) {
  try {
    const response = await api.post('/api/healthcare/guardian/login/', credentials);
    return response.data;
  } catch (err) {
    throw err.response?.data?.message || 'Login failed.';
  }
}

const guardianService = {
  // Authentication
  login,
  changePassword: async (passwordData) => {
    try {
      const response = await api.post('/api/healthcare/guardian/change-password/', passwordData);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Password change failed' };
    }
  },
  // Profile
  getProfile: async () => {
    try {
      const response = await api.get('/api/healthcare/guardian/me/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch profile' };
    }
  },
  // Children
  getChildren: async () => {
    try {
      const response = await api.get('/api/healthcare/guardian/children/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch children' };
    }
  },
  getChildDetail: async (childId) => {
    try {
      const response = await api.get(`/api/healthcare/guardian/children/${childId}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch child detail' };
    }
  },
  // Growth Records
  getChildGrowthRecords: async (childId) => {
    try {
      const response = await api.get(`/api/healthcare/guardian/children/${childId}/growth/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch growth records' };
    }
  },
  // Vaccination Records
  getChildVaccinationRecords: async (childId) => {
    try {
      const response = await api.get(`/api/healthcare/guardian/children/${childId}/vaccines/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch vaccination records' };
    }
  },
  // Notifications
  getNotifications: async () => {
    try {
      const response = await api.get('/api/healthcare/guardian/notifications/');
      return response.data;
    } catch (error) {
      throw error.response?.data || { detail: 'Failed to fetch notifications' };
    }
  },
};

export default guardianService; 