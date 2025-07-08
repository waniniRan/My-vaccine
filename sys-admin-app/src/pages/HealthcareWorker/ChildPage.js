import React, { useState, useEffect } from 'react';
import healthcareWorkerService from '../../services/healthcareWorkerService';

const ChildPage = () => {
  const [children, setChildren] = useState([]);
  const [guardians, setGuardians] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingChild, setEditingChild] = useState(null);
  const [formData, setFormData] = useState({
    child_id: '',
    first_name: '',
    last_name: '',
    date_of_birth: '',
    gender: '',
    birth_weight: '',
    birth_height: '',
    national_id: ''
  });

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const [childrenData, guardiansData] = await Promise.all([
        healthcareWorkerService.getChildren(),
        healthcareWorkerService.getGuardians()
      ]);
      setChildren(childrenData);
      setGuardians(guardiansData);
    } catch (err) {
      setError(err.detail || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (editingChild) {
        await healthcareWorkerService.updateChild(editingChild.child_id, formData);
      } else {
        await healthcareWorkerService.createChild(formData);
      }
      setShowForm(false);
      setEditingChild(null);
      resetForm();
      fetchData();
    } catch (err) {
      setError(err.detail || 'Failed to save child');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (childId) => {
    if (window.confirm('Are you sure you want to delete this child?')) {
      setLoading(true);
      setError('');
      try {
        await healthcareWorkerService.deleteChild(childId);
        fetchData();
      } catch (err) {
        setError(err.detail || 'Failed to delete child');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleEdit = (child) => {
    setEditingChild(child);
    setFormData({
      child_id: child.child_id,
      first_name: child.first_name,
      last_name: child.last_name,
      date_of_birth: child.date_of_birth,
      gender: child.gender,
      birth_weight: child.birth_weight,
      birth_height: child.birth_height,
      national_id: child.guardian_national_id
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({
      child_id: '',
      first_name: '',
      last_name: '',
      date_of_birth: '',
      gender: '',
      birth_weight: '',
      birth_height: '',
      national_id: ''
    });
  };

  const handleAddNew = () => {
    setEditingChild(null);
    resetForm();
    setShowForm(true);
  };

  if (loading && children.length === 0) {
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
        <h2>Child Management</h2>
        <button className="btn btn-primary" onClick={handleAddNew}>
          Add New Child
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
            <h5>{editingChild ? 'Edit Child' : 'Add New Child'}</h5>
          </div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="row">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Child ID</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.child_id}
                      onChange={(e) => setFormData({...formData, child_id: e.target.value})}
                      required
                      disabled={editingChild}
                    />
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Guardian</label>
                    <select
                      className="form-control"
                      value={formData.national_id}
                      onChange={(e) => setFormData({...formData, national_id: e.target.value})}
                      required
                    >
                      <option value="">Select Guardian</option>
                      {guardians.map((guardian) => (
                        <option key={guardian.national_id} value={guardian.national_id}>
                          {guardian.full_name} ({guardian.national_id})
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
              <div className="row">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">First Name</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.first_name}
                      onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                      required
                    />
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Last Name</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.last_name}
                      onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                      required
                    />
                  </div>
                </div>
              </div>
              <div className="row">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Date of Birth</label>
                    <input
                      type="date"
                      className="form-control"
                      value={formData.date_of_birth}
                      onChange={(e) => setFormData({...formData, date_of_birth: e.target.value})}
                      required
                    />
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Gender</label>
                    <select
                      className="form-control"
                      value={formData.gender}
                      onChange={(e) => setFormData({...formData, gender: e.target.value})}
                      required
                    >
                      <option value="">Select Gender</option>
                      <option value="M">Male</option>
                      <option value="F">Female</option>
                    </select>
                  </div>
                </div>
              </div>
              <div className="row">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Birth Weight (kg)</label>
                    <input
                      type="number"
                      step="0.01"
                      className="form-control"
                      value={formData.birth_weight}
                      onChange={(e) => setFormData({...formData, birth_weight: e.target.value})}
                      required
                    />
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Birth Height (cm)</label>
                    <input
                      type="number"
                      step="0.01"
                      className="form-control"
                      value={formData.birth_height}
                      onChange={(e) => setFormData({...formData, birth_height: e.target.value})}
                      required
                    />
                  </div>
                </div>
              </div>
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
          <h5>Children List</h5>
        </div>
        <div className="card-body">
          {children.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Child ID</th>
                    <th>Name</th>
                    <th>Date of Birth</th>
                    <th>Age</th>
                    <th>Gender</th>
                    <th>Guardian</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {children.map((child) => (
                    <tr key={child.child_id}>
                      <td>{child.child_id}</td>
                      <td>{child.full_name}</td>
                      <td>{child.date_of_birth}</td>
                      <td>{child.age}</td>
                      <td>{child.gender}</td>
                      <td>{child.guardian_national_id}</td>
                      <td>
                        <button
                          className="btn btn-sm btn-outline-primary me-2"
                          onClick={() => handleEdit(child)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => handleDelete(child.child_id)}
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
            <p className="text-muted">No children found</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChildPage; 