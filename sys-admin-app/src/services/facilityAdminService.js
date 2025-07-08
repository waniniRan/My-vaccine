import api, { extractData } from './api';

export async function getFacilityAdmins() {
  try {
    const response = await api.get('/api/sysadmin/facility-admins/');
    return extractData(response);
  } catch (err) {
    throw err.response?.data?.message || 'Failed to fetch facility admins.';
  }
}

export const createFacilityAdmin = async (data) => {
  try {
    const res = await api.post('/api/sysadmin/create-facility-admin/', data);
    return res.data;
  } catch (error) {
    throw error;
  }
};

export const updateFacilityAdmin = async (id, data) => {
  try {
    const res = await api.put(`/api/sysadmin/update-facility-admin/${id}/`, data);
    return res.data;
  } catch (error) {
    throw error;
  }
};

export const deleteFacilityAdmin = async (id) => {
  try {
    const res = await api.delete(`/api/sysadmin/delete-facility-admin/${id}/`);
    return res.data;
  } catch (error) {
    throw error;
  }
};
