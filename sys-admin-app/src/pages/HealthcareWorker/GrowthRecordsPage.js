import React, { useState, useEffect } from 'react';
import healthcareWorkerService from '../../services/healthcareWorkerService';

const GrowthRecordsPage = () => {
  const [growthRecords, setGrowthRecords] = useState([]);
  const [children, setChildren] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingRecord, setEditingRecord] = useState(null);
  const [formData, setFormData] = useState({
    child_id: '',
    weight: '',
    height: '',
    date_recorded: '',
    notes: '',
    recorded_by: ''
  });

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const [recordsData, childrenData] = await Promise.all([
        healthcareWorkerService.getGrowthRecords(),
        healthcareWorkerService.getChildren()
      ]);
      setGrowthRecords(recordsData);
      setChildren(childrenData);
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
      if (editingRecord) {
        await healthcareWorkerService.updateGrowthRecord(editingRecord.id, formData);
      } else {
        await healthcareWorkerService.createGrowthRecord(formData);
      }
      setShowForm(false);
      setEditingRecord(null);
      resetForm();
      fetchData();
    } catch (err) {
      setError(err.detail || 'Failed to save growth record');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (recordId) => {
    if (window.confirm('Are you sure you want to delete this growth record?')) {
      setLoading(true);
      setError('');
      try {
        await healthcareWorkerService.deleteGrowthRecord(recordId);
        fetchData();
      } catch (err) {
        setError(err.detail || 'Failed to delete growth record');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleEdit = (record) => {
    setEditingRecord(record);
    setFormData({
      child_id: record.child_id,
      weight: record.weight,
      height: record.height,
      date_recorded: record.date_recorded,
      notes: record.notes,
      recorded_by: record.recorded_by
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({
      child_id: '',
      weight: '',
      height: '',
      date_recorded: '',
      notes: '',
      recorded_by: ''
    });
  };

  const handleAddNew = () => {
    setEditingRecord(null);
    resetForm();
    setShowForm(true);
  };

  if (loading && growthRecords.length === 0) {
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
        <h2>Growth Records Management</h2>
        <button className="btn btn-primary" onClick={handleAddNew}>
          Add New Growth Record
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
            <h5>{editingRecord ? 'Edit Growth Record' : 'Add New Growth Record'}</h5>
          </div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="row">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Child</label>
                    <select
                      className="form-control"
                      value={formData.child_id}
                      onChange={(e) => setFormData({...formData, child_id: e.target.value})}
                      required
                    >
                      <option value="">Select Child</option>
                      {children.map((child) => (
                        <option key={child.child_id} value={child.child_id}>
                          {child.full_name} ({child.child_id})
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Date Recorded</label>
                    <input
                      type="date"
                      className="form-control"
                      value={formData.date_recorded}
                      onChange={(e) => setFormData({...formData, date_recorded: e.target.value})}
                      required
                    />
                  </div>
                </div>
              </div>
              <div className="row">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Weight (kg)</label>
                    <input
                      type="number"
                      step="0.01"
                      className="form-control"
                      value={formData.weight}
                      onChange={(e) => setFormData({...formData, weight: e.target.value})}
                      required
                    />
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Height (cm)</label>
                    <input
                      type="number"
                      step="0.01"
                      className="form-control"
                      value={formData.height}
                      onChange={(e) => setFormData({...formData, height: e.target.value})}
                      required
                    />
                  </div>
                </div>
              </div>
              <div className="mb-3">
                <label className="form-label">Notes</label>
                <textarea
                  className="form-control"
                  rows="3"
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Recorded By</label>
                <input
                  type="text"
                  className="form-control"
                  value={formData.recorded_by}
                  onChange={(e) => setFormData({...formData, recorded_by: e.target.value})}
                  required
                />
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
          <h5>Growth Records List</h5>
        </div>
        <div className="card-body">
          {growthRecords.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Child</th>
                    <th>Date</th>
                    <th>Weight (kg)</th>
                    <th>Height (cm)</th>
                    <th>BMI</th>
                    <th>Recorded By</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {growthRecords.map((record) => {
                    const bmi = record.weight && record.height ? 
                      ((record.weight / Math.pow(record.height / 100, 2)).toFixed(2)) : 'N/A';
                    return (
                      <tr key={record.id}>
                        <td>{record.child_id}</td>
                        <td>{record.date_recorded}</td>
                        <td>{record.weight}</td>
                        <td>{record.height}</td>
                        <td>{bmi}</td>
                        <td>{record.recorded_by}</td>
                        <td>
                          <button
                            className="btn btn-sm btn-outline-primary me-2"
                            onClick={() => handleEdit(record)}
                          >
                            Edit
                          </button>
                          <button
                            className="btn btn-sm btn-outline-danger"
                            onClick={() => handleDelete(record.id)}
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-muted">No growth records found</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default GrowthRecordsPage; 