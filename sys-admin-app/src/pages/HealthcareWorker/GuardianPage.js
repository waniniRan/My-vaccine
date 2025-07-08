import React, { useState, useEffect } from 'react';
import healthcareWorkerService from '../../services/healthcareWorkerService';

const GuardianPage = () => {
  const [guardians, setGuardians] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingGuardian, setEditingGuardian] = useState(null);
  const [formData, setFormData] = useState({
    national_id: '',
    full_name: '',
    email: '',
    phone_number: '',
    temporary_password: ''
  });

  const fetchGuardians = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await healthcareWorkerService.getGuardians();
      setGuardians(data);
    } catch (err) {
      setError(err.detail || 'Failed to fetch guardians');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGuardians();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (editingGuardian) {
        await healthcareWorkerService.updateGuardian(editingGuardian.national_id, formData);
      } else {
        await healthcareWorkerService.createGuardian(formData);
      }
      setShowForm(false);
      setEditingGuardian(null);
      resetForm();
      fetchGuardians();
    } catch (err) {
      setError(err.detail || 'Failed to save guardian');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (nationalId) => {
    if (window.confirm('Are you sure you want to delete this guardian?')) {
      setLoading(true);
      setError('');
      try {
        await healthcareWorkerService.deleteGuardian(nationalId);
        fetchGuardians();
      } catch (err) {
        setError(err.detail || 'Failed to delete guardian');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleEdit = (guardian) => {
    setEditingGuardian(guardian);
    setFormData({
      national_id: guardian.national_id,
      full_name: guardian.full_name,
      email: guardian.email,
      phone_number: guardian.phone_number,
      temporary_password: ''
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({
      national_id: '',
      full_name: '',
      email: '',
      phone_number: '',
      temporary_password: ''
    });
  };

  const handleAddNew = () => {
    setEditingGuardian(null);
    resetForm();
    setShowForm(true);
  };

  if (loading && guardians.length === 0) {
    return (
      <div className="container mt-5">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Guardian Management</h2>
        <button className="btn btn-primary" onClick={handleAddNew}>
          Add New Guardian
        </button>
      </div>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {showForm && (
        <div className="card mb-4">
          <div className="card-header">
            <h5>{editingGuardian ? 'Edit Guardian' : 'Add New Guardian'}</h5>
          </div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="row">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">National ID</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.national_id}
                      onChange={(e) => setFormData({...formData, national_id: e.target.value})}
                      required
                      disabled={editingGuardian}
                    />
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Full Name</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.full_name}
                      onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                      required
                    />
                  </div>
                </div>
              </div>
              <div className="row">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      required
                    />
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Phone Number</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.phone_number}
                      onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
                      required
                    />
                  </div>
                </div>
              </div>
              {!editingGuardian && (
                <div className="mb-3">
                  <label className="form-label">Temporary Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={formData.temporary_password}
                    onChange={(e) => setFormData({...formData, temporary_password: e.target.value})}
                    required
                  />
                </div>
              )}
              <div className="d-flex gap-2">
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Saving...' : 'Save'}
                </button>
                <button type="button" className="btn btn-secondary" onClick={() => setShowForm(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-header">
          <h5>Guardians List</h5>
        </div>
        <div className="card-body">
          {guardians.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>National ID</th>
                    <th>Full Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {guardians.map((guardian) => (
                    <tr key={guardian.national_id}>
                      <td>{guardian.national_id}</td>
                      <td>{guardian.full_name}</td>
                      <td>{guardian.email}</td>
                      <td>{guardian.phone_number}</td>
                      <td>
                        <span className={`badge ${guardian.is_active ? 'bg-success' : 'bg-danger'}`}>
                          {guardian.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn btn-sm btn-outline-primary me-2"
                          onClick={() => handleEdit(guardian)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => handleDelete(guardian.national_id)}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-muted">No guardians found</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default GuardianPage; 