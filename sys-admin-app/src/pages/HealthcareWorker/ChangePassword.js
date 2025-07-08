import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import healthcareWorkerService from '../../../../../myVaccine/sys-admin-app/src/services/healthcareWorkerService';

const HealthcareWorkerChangePassword = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    old_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    if (!formData.old_password || !formData.new_password || !formData.confirm_password) {
      setError('Please fill in all fields');
      setLoading(false);
      return;
    }

    if (formData.new_password !== formData.confirm_password) {
      setError('New passwords do not match');
      setLoading(false);
      return;
    }

    if (formData.new_password.length < 8) {
      setError('New password must be at least 8 characters long');
      setLoading(false);
      return;
    }

    try {
      await healthcareWorkerService.changePassword({
        old_password: formData.old_password,
        new_password: formData.new_password
      });
      setSuccess('Password changed successfully');
      setFormData({
        old_password: '',
        new_password: '',
        confirm_password: ''
      });
      setTimeout(() => {
        navigate('/healthcare-worker/dashboard');
      }, 2000);
    } catch (err) {
      setError(err.detail || 'Password change failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-header">
              <h3 className="text-center">Change Password</h3>
            </div>
            <div className="card-body">
              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}
              {success && (
                <div className="alert alert-success" role="alert">
                  {success}
                </div>
              )}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="old_password" className="form-label">Current Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="old_password"
                    name="old_password"
                    value={formData.old_password}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="new_password" className="form-label">New Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="new_password"
                    name="new_password"
                    value={formData.new_password}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="confirm_password" className="form-label">Confirm New Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="confirm_password"
                    name="confirm_password"
                    value={formData.confirm_password}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="d-flex gap-2">
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={loading}
                  >
                    {loading ? 'Changing Password...' : 'Change Password'}
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => navigate('/healthcare-worker/dashboard')}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HealthcareWorkerChangePassword; 