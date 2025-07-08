import api from './api';

export const getAllUsers = async () => {
  try {
    const res = await api.get('/api/sysadmin/users/');
    return res.data && res.data.data ? res.data.data : res.data;
  } catch (error) {
    throw error;
  }
};

export const exportUsers = async () => {
  try {
    const res = await api.get('/api/sysadmin/export-users/', { responseType: 'blob' });
    return res;
  } catch (error) {
    throw error;
  }
};
