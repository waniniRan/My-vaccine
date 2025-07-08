import React, { useState, useEffect } from "react";
import { Container, Table, Button, Modal, Form, Offcanvas, ListGroup, Alert } from "react-bootstrap";
import { House, People, PlusSquare, FileText, List, Building, BoxArrowRight } from "react-bootstrap-icons";
import {
  getFacilities,
  createFacility,
  updateFacility,
  deleteFacility
} from "../../services/facilityService";

const FacilitiesPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [facilities, setFacilities] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editing, setEditing] = useState(false);
  const [editId, setEditId] = useState(null);

  const handleCloseMenu = () => setShowMenu(false);
  const handleShowMenu = () => setShowMenu(true);

  const [form, setForm] = useState({
    name: "",
    facility_type: "HOSPITAL",
    location: "",
    phone: "",
    email: "",
  });

  useEffect(() => {
    getFacilities()
      .then((res) => {
        setFacilities(Array.isArray(res.data.data) ? res.data.data : []);
      })
      .catch((err) => {
        setFacilities([]);
        setError("Failed to load facilities.");
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await updateFacility(editId, form);
        setSuccess("Facility updated successfully!");
      } else {
        await createFacility(form);
        setSuccess("Facility created successfully!");
      }

      const response = await getFacilities();
      setFacilities(response.data.data);

      setShowModal(false);
      setEditing(false);
      setForm({
        name: "",
        facility_type: "HOSPITAL",
        location: "",
        phone: "",
        email: "",
      });
    } catch (err) {
      console.error(err);
      setError("Failed to save facility.");
    }
  };

  const handleEdit = (facility) => {
    setForm({
      name: facility.name,
      facility_type: facility.facility_type,
      location: facility.location,
      phone: facility.phone,
      email: facility.email,
    });
    setEditId(facility.ID);
    setEditing(true);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this facility?");
    if (!confirmDelete) return;
    try {
      await deleteFacility(id);
      setSuccess("Facility deleted successfully.");
      const response = await getFacilities();
      setFacilities(response.data.data);
    } catch (err) {
      console.error(err);
      setError("Failed to delete facility.");
    }
  };

  return (
    <>
      <Offcanvas show={showMenu} onHide={handleCloseMenu}>
        <Offcanvas.Header closeButton><Offcanvas.Title>Menu</Offcanvas.Title></Offcanvas.Header>
        <Offcanvas.Body>
          <ListGroup variant="flush">
            <ListGroup.Item action href="/system-admin/dashboard"><House /> Home</ListGroup.Item>
            <ListGroup.Item action href="/system-admin/facilities"><Building /> Facilities</ListGroup.Item>
            <ListGroup.Item action href="/system-admin/facility-admins"><People /> Facility Admins</ListGroup.Item>
            <ListGroup.Item action href="/system-admin/vaccines"><PlusSquare /> Vaccines</ListGroup.Item>
            <ListGroup.Item action href="/system-admin/reports"><FileText /> System Reports</ListGroup.Item>
            <ListGroup.Item action href="/system-admin/all-users"><List /> All Users</ListGroup.Item>
            <ListGroup.Item action href="/"><BoxArrowRight /> Logout</ListGroup.Item>
          </ListGroup>
        </Offcanvas.Body>
      </Offcanvas>

      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <h3 className="mb-0">Manage Facilities</h3>
        <Button variant="light" onClick={handleShowMenu}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Container className="py-4">
        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">{success}</Alert>}

        <div className="d-flex justify-content-between mb-3">
          <h4>Facilities List</h4>
          <Button onClick={() => { setShowModal(true); setEditing(false); }}>Add Facility</Button>
        </div>

        <Table bordered hover>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Type</th>
              <th>Location</th>
              <th>Phone</th>
              <th>Email</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {(facilities || []).map((f) => (
              <tr key={f.ID}>
                <td>{f.ID}</td>
                <td>{f.name}</td>
                <td>{f.facility_type}</td>
                <td>{f.location}</td>
                <td>{f.phone}</td>
                <td>{f.email}</td>
                <td>
                  <Button variant="warning" size="sm" onClick={() => handleEdit(f)} className="me-2">Edit</Button>
                  <Button variant="danger" size="sm" onClick={() => handleDelete(f.ID)}>Delete</Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton><Modal.Title>{editing ? "Edit Facility" : "Add Facility"}</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-2">
              <Form.Label>Facility Name</Form.Label>
              <Form.Control value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Facility Type</Form.Label>
              <Form.Select value={form.facility_type} onChange={(e) => setForm({ ...form, facility_type: e.target.value })}>
                <option>HOSPITAL</option>
                <option>CLINIC</option>
                <option>HEALTH_CENTER</option>
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Location</Form.Label>
              <Form.Control value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} required />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Phone</Form.Label>
              <Form.Control value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Email</Form.Label>
              <Form.Control type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            </Form.Group>
            <Button type="submit" variant="primary">{editing ? "Update" : "Save"}</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default FacilitiesPage;
