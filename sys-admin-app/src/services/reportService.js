// services/reportService.js

import api from './api';

export const getSystemReports = async () => {
  try {
    const res = await api.get('/api/sysadmin/system-reports/');
    return res.data && res.data.data ? res.data.data : res.data;
  } catch (error) {
    throw error;
  }
};

export const exportSystemReport = async () => {
  try {
    const res = await api.get('/api/sysadmin/export-system-reports/', { responseType: 'blob' });
    return res;
  } catch (error) {
    throw error;
  }
};

export const downloadReport = async (reportId) => {
  try {
    const res = await api.get(`/api/sysadmin/download-report/${reportId}/`, { responseType: 'blob' });
    return res;
  } catch (error) {
    throw error;
  }
};
