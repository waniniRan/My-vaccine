import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api/sysadmin";

// Create a function to dynamically get token each time
const getAuthHeaders = () => {
  const token = localStorage.getItem("accessToken");
  return {
    Authorization: `Bearer ${token}`,
  };
};

const getFacilityAdmins = () =>
  axios.get(`${API_BASE}/list-facility-admins/`, { headers: getAuthHeaders() });

const createFacilityAdmin = (data) =>
  axios.post(`${API_BASE}/create-facility-admin/`, data, { headers: getAuthHeaders() });

const updateFacilityAdmin = (admin_id, data) =>
  axios.put(`${API_BASE}/update-facility-admin/${admin_id}/`, data, { headers: getAuthHeaders() });

const deleteFacilityAdmin = (admin_id) =>
  axios.delete(`${API_BASE}/delete-facility-admin/${admin_id}/`, { headers: getAuthHeaders() });

export default {
  getFacilityAdmins,
  createFacilityAdmin,
  updateFacilityAdmin,
  deleteFacilityAdmin,
};
