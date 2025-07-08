import React, { useState, useEffect } from 'react';
import healthcareWorkerService from '../../services/healthcareWorkerService';

const VaccinationRecordsPage = () => {
  const [vaccinationRecords, setVaccinationRecords] = useState([]);
  const [children, setChildren] = useState([]);
  const [vaccines, setVaccines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingRecord, setEditingRecord] = useState(null);
  const [formData, setFormData] = useState({
    child_id: '',
    v_ID: '',
    dose_number: '',
    administration_date: '',
    side_effects: '',
    remarks: '',
    administered_by: ''
  });

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const [recordsData, childrenData, vaccinesData] = await Promise.all([
        healthcareWorkerService.getVaccinationRecords(),
        healthcareWorkerService.getChildren(),
        healthcareWorkerService.getVaccines()
      ]);
      setVaccinationRecords(recordsData);
      setChildren(childrenData);
      setVaccines(vaccinesData);
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
        await healthcareWorkerService.updateVaccinationRecord(editingRecord.recordID, formData);
      } else {
        await healthcareWorkerService.createVaccinationRecord(formData);
      }
      setShowForm(false);
      setEditingRecord(null);
      resetForm();
      fetchData();
    } catch (err) {
      setError(err.detail || 'Failed to save vaccination record');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (recordId) => {
    if (window.confirm('Are you sure you want to delete this vaccination record?')) {
      setLoading(true);
      setError('');
      try {
        await healthcareWorkerService.deleteVaccinationRecord(recordId);
        fetchData();
      } catch (err) {
        setError(err.detail || 'Failed to delete vaccination record');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleEdit = (record) => {
    setEditingRecord(record);
    setFormData({
      child_id: record.child_id,
      v_ID: record.v_ID,
      dose_number: record.dose_number,
      administration_date: record.administration_date,
      side_effects: record.side_effects,
      remarks: record.remarks,
      administered_by: record.administered_by
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({
      child_id: '',
      v_ID: '',
      dose_number: '',
      administration_date: '',
      side_effects: '',
      remarks: '',
      administered_by: ''
    });
  };

  const handleAddNew = () => {
    setEditingRecord(null);
    resetForm();
    setShowForm(true);
  };

  if (loading && vaccinationRecords.length === 0) {
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
        <h2>Vaccination Records Management</h2>
        <button className="btn btn-primary" onClick={handleAddNew}>
          Add New Vaccination Record
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
            <h5>{editingRecord ? 'Edit Vaccination Record' : 'Add New Vaccination Record'}</h5>
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
                    <label className="form-label">Vaccine</label>
                    <select
                      className="form-control"
                      value={formData.v_ID}
                      onChange={(e) => setFormData({...formData, v_ID: e.target.value})}
                      required
                    >
                      <option value="">Select Vaccine</option>
                      {vaccines.map((vaccine) => (
                        <option key={vaccine.v_ID} value={vaccine.v_ID}>
                          {vaccine.name} ({vaccine.v_ID})
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
              <div className="row">
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Dose Number</label>
                    <input
                      type="number"
                      min="1"
                      className="form-control"
                      value={formData.dose_number}
                      onChange={(e) => setFormData({...formData, dose_number: e.target.value})}
                      required
                    />
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="mb-3">
                    <label className="form-label">Administration Date</label>
                    <input
                      type="date"
                      className="form-control"
                      value={formData.administration_date}
                      onChange={(e) => setFormData({...formData, administration_date: e.target.value})}
                      required
                    />
                  </div>
                </div>
              </div>
              <div className="mb-3">
                <label className="form-label">Side Effects</label>
                <textarea
                  className="form-control"
                  rows="3"
                  value={formData.side_effects}
                  onChange={(e) => setFormData({...formData, side_effects: e.target.value})}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Remarks</label>
                <textarea
                  className="form-control"
                  rows="3"
                  value={formData.remarks}
                  onChange={(e) => setFormData({...formData, remarks: e.target.value})}
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Administered By</label>
                <input
                  type="text"
                  className="form-control"
                  value={formData.administered_by}
                  onChange={(e) => setFormData({...formData, administered_by: e.target.value})}
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
          <h5>Vaccination Records List</h5>
        </div>
        <div className="card-body">
          {vaccinationRecords.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Child</th>
                    <th>Vaccine</th>
                    <th>Dose</th>
                    <th>Date</th>
                    <th>Side Effects</th>
                    <th>Administered By</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {vaccinationRecords.map((record) => (
                    <tr key={record.recordID}>
                      <td>{record.child_id}</td>
                      <td>{record.vaccine_name || record.v_ID}</td>
                      <td>{record.dose_number}</td>
                      <td>{record.administration_date}</td>
                      <td>{record.side_effects || 'None'}</td>
                      <td>{record.administered_by}</td>
                      <td>
                        <button
                          className="btn btn-sm btn-outline-primary me-2"
                          onClick={() => handleEdit(record)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => handleDelete(record.recordID)}
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
            <p className="text-muted">No vaccination records found</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default VaccinationRecordsPage; 