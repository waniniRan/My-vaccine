// services/reportService.js

const API_BASE = "/api/system-reports/";

const getSystemReports = async () => {
  const res = await fetch(API_BASE, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      "Content-Type": "application/json",
    },
  });
  if (!res.ok) {
    throw new Error("Failed to fetch reports");
  }
  return res.json();
};

export default {
  getSystemReports,
};
