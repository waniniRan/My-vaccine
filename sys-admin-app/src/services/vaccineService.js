import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api/sysadmin";

const getAuthHeaders = () => {
  const token = localStorage.getItem("accessToken");
  return {
    Authorization: `Bearer ${token}`,
  };
};

const getVaccines = () =>
  axios.get(`${API_BASE}/list-vaccines/`, { headers: getAuthHeaders() });

const createVaccine = (data) =>
  axios.post(`${API_BASE}/create-vaccine/`, data, { headers: getAuthHeaders() });

const updateVaccine = (v_ID, data) =>
  axios.put(`${API_BASE}/update-vaccine/${v_ID}/`, data, { headers: getAuthHeaders() });

const deleteVaccine = (v_ID) =>
  axios.delete(`${API_BASE}/delete-vaccine/${v_ID}/`, { headers: getAuthHeaders() });

export default {
  getVaccines,
  createVaccine,
  updateVaccine,
  deleteVaccine,
};
