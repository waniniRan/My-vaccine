import React, { useState, useEffect } from "react";
import {
  Container,
  Button,
  Table,
  Modal,
  Form,
  Offcanvas,
  ListGroup,
  Spinner,
  Alert,
} from "react-bootstrap";
import {
  House,
  People,
  FileText,
  BoxArrowRight,
  Trash,
  PencilSquare,
} from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const HealthcareWorkersPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [editingWorker, setEditingWorker] = useState(null);
  const [workers, setWorkers] = useState([]);
  const [facilities, setFacilities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const [form, setForm] = useState({
    worker_username: "",
    fullname: "",
    email: "",
    phone_number: "",
    position: "doctor",
    facility: "",
    temporary_password: "Kenya@2030",
    status: "active",
  });

  const handleShowMenu = () => setShowMenu(true);
  const handleCloseMenu = () => setShowMenu(false);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    navigate("/facility-admin/login");
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("accessToken");

      const [workersRes, facilitiesRes] = await Promise.all([
        axios.get(
          "http://127.0.0.1:8000/api/facilityadmin/list-healthcare-workers/",
          { headers: { Authorization: `Bearer ${token}` } }
        ),
        axios.get(
          "http://127.0.0.1:8000/api/sysadmin/list-facilities/",
          { headers: { Authorization: `Bearer ${token}` } }
        ),
      ]);

      setWorkers(workersRes.data.data);
      setFacilities(facilitiesRes.data.data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setError("Failed to load workers or facilities.");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("accessToken");
      if (editingWorker) {
        await axios.put(
          `http://127.0.0.1:8000/api/facilityadmin/update-healthcare-worker/${editingWorker}/`,
          form,
          { headers: { Authorization: `Bearer ${token}` } }
        );
      } else {
        await axios.post(
          "http://127.0.0.1:8000/api/facilityadmin/create-healthcare-worker/",
          form,
          { headers: { Authorization: `Bearer ${token}` } }
        );
      }
      fetchData();
      setShowModal(false);
      setEditingWorker(null);
      setForm({
        worker_username: "",
        fullname: "",
        email: "",
        phone_number: "",
        position: "doctor",
        facility: "",
        temporary_password: "Kenya@2030",
        status: "active",
      });
    } catch (err) {
      console.error(err);
      alert("Error saving worker. Check console for details.");
    }
  };

  const handleDelete = async (workerId) => {
    if (!window.confirm("Delete worker?")) return;
    try {
      const token = localStorage.getItem("accessToken");
      await axios.delete(
        `http://127.0.0.1:8000/api/facilityadmin/delete-healthcare-worker/${workerId}/`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchData();
    } catch (err) {
      console.error(err);
      alert("Error deleting worker.");
    }
  };

  const handleEdit = (w) => {
    setEditingWorker(w.worker_id);
    setForm({
      worker_username: w.worker_username,
      fullname: w.fullname,
      email: w.email,
      phone_number: w.phone_number,
      position: w.position,
      facility: w.facility,
      temporary_password: "Kenya@2030",
      status: w.status,
    });
    setShowModal(true);
  };

  return (
    <>
      <Offcanvas show={showMenu} onHide={handleCloseMenu}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Menu</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <ListGroup variant="flush">
            <ListGroup.Item action href="/facility-admin/dashboard">
              <House /> Home
            </ListGroup.Item>
            <ListGroup.Item action href="/facility-admin/healthcare-workers">
              <People /> Healthcare Workers
            </ListGroup.Item>
            <ListGroup.Item action href="/facility-admin/reports">
              <FileText /> Facility Reports
            </ListGroup.Item>
            <ListGroup.Item action onClick={handleLogout}>
              <BoxArrowRight /> Logout
            </ListGroup.Item>
          </ListGroup>
        </Offcanvas.Body>
      </Offcanvas>

      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <h3>Manage Healthcare Workers</h3>
        <Button variant="light" onClick={handleShowMenu}>
          &#9776; Menu
        </Button>
      </div>

      <Container className="py-4">
        <div className="d-flex justify-content-between mb-3">
          <h4>Healthcare Workers</h4>
          <Button
            onClick={() => {
              setEditingWorker(null);
              setForm({
                worker_username: "",
                fullname: "",
                email: "",
                phone_number: "",
                position: "doctor",
                facility: "",
                temporary_password: "Kenya@2030",
                status: "active",
              });
              setShowModal(true);
            }}
          >
            Add Worker
          </Button>
        </div>

        {loading && (
          <div className="text-center py-4">
            <Spinner animation="border" />
          </div>
        )}
        {error && <Alert variant="danger">{error}</Alert>}

        {!loading && !error && (
          <Table bordered hover>
            <thead>
              <tr>
                <th>Worker ID</th>
                <th>Full Name</th>
                <th>Username</th>
                <th>Facility</th>
                <th>Position</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {workers.map((w) => (
                <tr key={w.worker_id}>
                  <td>{w.worker_id}</td>
                  <td>{w.fullname}</td>
                  <td>{w.worker_username}</td>
                  <td>{w.facility}</td>
                  <td>{w.position}</td>
                  <td>{w.status}</td>
                  <td>
                    <Button
                      size="sm"
                      onClick={() => handleEdit(w)}
                      className="me-2"
                    >
                      <PencilSquare />
                    </Button>
                    <Button
                      size="sm"
                      variant="danger"
                      onClick={() => handleDelete(w.worker_id)}
                    >
                      <Trash />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        )}
      </Container>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{editingWorker ? "Edit" : "Add"} Healthcare Worker</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-2">
              <Form.Label>Username</Form.Label>
              <Form.Control
                required
                value={form.worker_username}
                onChange={(e) =>
                  setForm({ ...form, worker_username: e.target.value })
                }
                disabled={editingWorker !== null}
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Full Name</Form.Label>
              <Form.Control
                required
                value={form.fullname}
                onChange={(e) => setForm({ ...form, fullname: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Phone</Form.Label>
              <Form.Control
                value={form.phone_number}
                onChange={(e) => setForm({ ...form, phone_number: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Position</Form.Label>
              <Form.Select
                value={form.position}
                onChange={(e) => setForm({ ...form, position: e.target.value })}
              >
                <option value="doctor">Doctor</option>
                <option value="nurse">Nurse</option>
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Facility</Form.Label>
              <Form.Select
                required
                value={form.facility}
                onChange={(e) => setForm({ ...form, facility: e.target.value })}
              >
                <option value="">Select Facility</option>
                {facilities.map((f) => (
                  <option key={f.ID} value={f.ID}>
                    {f.name} ({f.ID})
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Status</Form.Label>
              <Form.Select
                value={form.status}
                onChange={(e) => setForm({ ...form, status: e.target.value })}
              >
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="suspended">Suspended</option>
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Temporary Password</Form.Label>
              <Form.Control
                type="password"
                value={form.temporary_password}
                onChange={(e) =>
                  setForm({ ...form, temporary_password: e.target.value })
                }
                disabled={editingWorker !== null}
              />
            </Form.Group>
            <Button type="submit" className="w-100 mt-2">
              {editingWorker ? "Update Worker" : "Save Worker"}
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default HealthcareWorkersPage;
