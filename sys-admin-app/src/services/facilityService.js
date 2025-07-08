import api, { extractData } from './api';

export async function getFacilities() {
  try {
    const response = await api.get('/api/sysadmin/list-facilities/');
    return response;
  } catch (err) {
    throw err.response?.data?.message || 'Failed to fetch facilities.';
  }
}

export const createFacility = async (data) => {
  try {
    const res = await api.post('/api/sysadmin/create-facility/', data);
    return res.data;
  } catch (error) {
    throw error;
  }
};

export const updateFacility = async (id, data) => {
  try {
    const res = await api.put(`/api/sysadmin/update-facility/${id}/`, data);
    return res.data;
  } catch (error) {
    throw error;
  }
};

export const deleteFacility = async (id) => {
  try {
    const res = await api.delete(`/api/sysadmin/delete-facility/${id}/`);
    return res.data;
  } catch (error) {
    throw error;
  }
};
