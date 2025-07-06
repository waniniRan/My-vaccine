import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api/sysadmin";

const getAuthHeaders = () => {
  const token = localStorage.getItem("accessToken");
  return {
    Authorization: `Bearer ${token}`,
  };
};

const getFacilities = () =>
  axios.get(`${API_BASE}/list-facilities/`, { headers: getAuthHeaders() });

const createFacility = (data) =>
  axios.post(`${API_BASE}/create-facility/`, data, { headers: getAuthHeaders() });

const updateFacility = (id, data) =>
  axios.put(`${API_BASE}/update-facility/${id}/`, data, { headers: getAuthHeaders() });

const deleteFacility = (id) =>
  axios.delete(`${API_BASE}/delete-facility/${id}/`, { headers: getAuthHeaders() });

export default {
  getFacilities,
  createFacility,
  updateFacility,
  deleteFacility,
};
