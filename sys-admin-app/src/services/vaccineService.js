import api, { extractData } from './api';

export async function getVaccines() {
  try {
    const response = await api.get('/api/sysadmin/vaccines/');
    return extractData(response);
  } catch (err) {
    throw err.response?.data?.message || 'Failed to fetch vaccines.';
  }
}

export const createVaccine = async (data) => {
  try {
    const res = await api.post('/api/sysadmin/create-vaccine/', data);
    return res.data;
  } catch (error) {
    throw error;
  }
};

export const updateVaccine = async (id, data) => {
  try {
    const res = await api.put(`/api/sysadmin/update-vaccine/${id}/`, data);
    return res.data;
  } catch (error) {
    throw error;
  }
};

export const deleteVaccine = async (id) => {
  try {
    const res = await api.delete(`/api/sysadmin/delete-vaccine/${id}/`);
    return res.data;
  } catch (error) {
    throw error;
  }
};
