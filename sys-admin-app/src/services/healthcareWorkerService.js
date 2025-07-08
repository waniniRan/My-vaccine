import api, { extractData } from './api';

const healthcareWorkerService = {
  // Authentication
  login: async (credentials) => {
    try {
      const response = await api.post('/api/healthcare/login/', credentials);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Login failed.';
    }
  },
  changePassword: async (passwordData) => {
    try {
      const response = await api.post('/api/healthcare/change-password/', passwordData);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Password change failed.';
    }
  },
  // Guardian Management
  getGuardians: async () => {
    try {
      const response = await api.get('/api/healthcare/guardian/list/');
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to fetch guardians.';
    }
  },
  createGuardian: async (guardianData) => {
    try {
      const response = await api.post('/api/healthcare/guardian/create/', guardianData);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to create guardian.';
    }
  },
  updateGuardian: async (nationalId, guardianData) => {
    try {
      const response = await api.put(`/api/healthcare/guardian/update/${nationalId}/`, guardianData);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to update guardian.';
    }
  },
  deleteGuardian: async (nationalId) => {
    try {
      const response = await api.delete(`/api/healthcare/guardian/delete/${nationalId}/`);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to delete guardian.';
    }
  },
  // Child Management
  getChildren: async () => {
    try {
      const response = await api.get('/api/healthcare/child/list/');
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to fetch children.';
    }
  },
  createChild: async (childData) => {
    try {
      const response = await api.post('/api/healthcare/child/create/', childData);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to create child.';
    }
  },
  updateChild: async (childId, childData) => {
    try {
      const response = await api.put(`/api/healthcare/child/update/${childId}/`, childData);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to update child.';
    }
  },
  deleteChild: async (childId) => {
    try {
      const response = await api.delete(`/api/healthcare/child/delete/${childId}/`);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to delete child.';
    }
  },
  // Growth Record Management
  getGrowthRecords: async () => {
    try {
      const response = await api.get('/api/healthcare/growth-record/list/');
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to fetch growth records.';
    }
  },
  createGrowthRecord: async (recordData) => {
    try {
      const response = await api.post('/api/healthcare/growth-record/create/', recordData);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to create growth record.';
    }
  },
  updateGrowthRecord: async (recordId, recordData) => {
    try {
      const response = await api.put(`/api/healthcare/growth-record/update/${recordId}/`, recordData);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to update growth record.';
    }
  },
  deleteGrowthRecord: async (recordId) => {
    try {
      const response = await api.delete(`/api/healthcare/growth-record/delete/${recordId}/`);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to delete growth record.';
    }
  },
  // Vaccination Record Management
  getVaccinationRecords: async () => {
    try {
      const response = await api.get('/api/healthcare/vaccination-record/list/');
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to fetch vaccination records.';
    }
  },
  createVaccinationRecord: async (recordData) => {
    try {
      const response = await api.post('/api/healthcare/vaccination-record/create/', recordData);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to create vaccination record.';
    }
  },
  updateVaccinationRecord: async (recordId, recordData) => {
    try {
      const response = await api.put(`/api/healthcare/vaccination-record/update/${recordId}/`, recordData);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to update vaccination record.';
    }
  },
  deleteVaccinationRecord: async (recordId) => {
    try {
      const response = await api.delete(`/api/healthcare/vaccination-record/delete/${recordId}/`);
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to delete vaccination record.';
    }
  },
  // Vaccine Management
  getVaccines: async () => {
    try {
      const response = await api.get('/api/sysadmin/vaccines/');
      return extractData(response);
    } catch (err) {
      throw err.response?.data?.message || 'Failed to fetch vaccines.';
    }
  },
};

export default healthcareWorkerService; 