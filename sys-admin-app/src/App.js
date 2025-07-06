//import logo from './logo.svg';
import './App.css';
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

//System Admin Pages
import SystemAdminLogin from "./pages/SystemAdmin/Login";
import SystemAdminDashboard from "./pages/SystemAdmin/Dashboard";
import FacilitiesPage from "./pages/SystemAdmin/FacilitiesPage";
import FacilityAdminsPage from "./pages/SystemAdmin/FacilityAdminsPage";
import VaccinesPage from "./pages/SystemAdmin/VaccinesPage";
import SystemReportsPage from "./pages/SystemAdmin/SystemReports";   
import AllUsersPage from "./pages/SystemAdmin/AllUsers";             

//Facility Admin Pages
import FacilityAdminLogin from "./pages/FacilityAdmin/Login";
import FacilityAdminDashboard from "./pages/FacilityAdmin/Dashboard";
import HealthcareWorkersPage from "./pages/FacilityAdmin/HealthcareWorkers";
import FacilityReportsPage from "./pages/FacilityAdmin/FacilityReports";

//Healthcare Worker Pages
import HealthcareWorkerLogin from "./pages/HealthcareWorker/Login";
import HealthcareWorkerDashboard from "./pages/HealthcareWorker/Dashboard";
import GuardianPage from "./pages/HealthcareWorker/GuardianPage";
import ChildPage from "./pages/HealthcareWorker/ChildPage";
import VaccinationRecordsPage from "./pages/HealthcareWorker/VaccinationRecordsPage";
import GrowthRecordsPage from "./pages/HealthcareWorker/GrowthRecordsPage";
import NotificationPage from "./pages/HealthcareWorker/NotificationPage";


function App() {
  return (
    <Router>
      <Routes>
        {/* System Admin Routes */}
        <Route path="/" element={<SystemAdminLogin />} />
        <Route path="/system-admin/dashboard" element={<SystemAdminDashboard />} />
        <Route path="/system-admin/facilities" element={<FacilitiesPage />} />
        <Route path="/system-admin/facility-admins" element={<FacilityAdminsPage />} />
        <Route path="/system-admin/vaccines" element={<VaccinesPage />} />
        <Route path="/system-admin/reports" element={<SystemReportsPage />} />
        <Route path="/system-admin/all-users" element={<AllUsersPage />} />

        {/* Facility Admin Routes */}
        <Route path="/facility-admin/login" element={<FacilityAdminLogin />} />
        <Route path="/facility-admin/dashboard" element={<FacilityAdminDashboard />} />
        <Route path="/facility-admin/healthcare-workers" element={<HealthcareWorkersPage />} />
        <Route path="/facility-admin/reports" element={<FacilityReportsPage />} />
        

        {/*Hea}lthcare Worker Routes */}
        <Route path="/healthcare-worker/login" element={<HealthcareWorkerLogin />} />
        <Route path="/healthcare-worker/dashboard" element={<HealthcareWorkerDashboard />} />
        <Route path="/healthcare-worker/guardian" element={<GuardianPage />} />
        <Route path="/healthcare-worker/children" element={<ChildPage />} />
        <Route path="/healthcare-worker/vaccination-records" element={<VaccinationRecordsPage />} />
        <Route path="/healthcare-worker/growth-records" element={<GrowthRecordsPage />} />
        <Route path="/healthcare-worker/notifications" element={<NotificationPage />} />
        

      </Routes>
    </Router>
  );
}

export default App;
