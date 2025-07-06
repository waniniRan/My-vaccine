import React, { useState } from "react";
import { Container, Button, Table, Modal, Form, Offcanvas, ListGroup } from "react-bootstrap";
import { House, People, FileText, BoxArrowRight } from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";

const HealthcareWorkersPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();

  const handleShowMenu = () => setShowMenu(true);
  const handleCloseMenu = () => setShowMenu(false);

  const handleLogout = () => {
    navigate("/facility-admin/login");
  };

  // mock data
  const [workers, setWorkers] = useState([
    { id: "HW001", name: "Dr. Sarah Johnson", status: "Active", lastLogin: "2025-07-05 09:30" },
    { id: "HW002", name: "Nurse Mike Chen", status: "Active", lastLogin: "2025-07-05 08:45" }
  ]);

  const [form, setForm] = useState({
    name: "",
    id: "",
    status: "Active"
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setWorkers([...workers, form]);
    setShowModal(false);
    setForm({ name: "", id: "", status: "Active" });
  };

  return (
    <>
      <Offcanvas show={showMenu} onHide={handleCloseMenu}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Menu</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <ListGroup variant="flush">
            <ListGroup.Item action href="/facility-admin/dashboard"><House /> Home</ListGroup.Item>
            <ListGroup.Item action href="/facility-admin/healthcare-workers"><People /> Healthcare Workers</ListGroup.Item>
            <ListGroup.Item action href="/facility-admin/reports"><FileText /> Facility Reports</ListGroup.Item>
            <ListGroup.Item action onClick={handleLogout}><BoxArrowRight /> Logout</ListGroup.Item>
          </ListGroup>
        </Offcanvas.Body>
      </Offcanvas>

      {/* header */}
      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <h3 className="mb-0">Manage Healthcare Workers</h3>
        <Button variant="light" onClick={handleShowMenu}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Container className="py-4">
        <div className="d-flex justify-content-between mb-3">
          <h4>Healthcare Workers</h4>
          <Button onClick={() => setShowModal(true)}>Add Worker</Button>
        </div>

        <Table bordered hover>
          <thead>
            <tr>
              <th>Name</th>
              <th>ID</th>
              <th>Status</th>
              <th>Last Login</th>
            </tr>
          </thead>
          <tbody>
            {workers.map((w, idx) => (
              <tr key={idx}>
                <td>{w.name}</td>
                <td>{w.id}</td>
                <td>
                  <span className={`badge ${w.status === "Active" ? "bg-success" : "bg-secondary"}`}>
                    {w.status}
                  </span>
                </td>
                <td>{w.lastLogin || "-"}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>

      {/* modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Add Healthcare Worker</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-2">
              <Form.Label>Full Name</Form.Label>
              <Form.Control
                required
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>ID</Form.Label>
              <Form.Control
                required
                value={form.id}
                onChange={(e) => setForm({ ...form, id: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Status</Form.Label>
              <Form.Select
                value={form.status}
                onChange={(e) => setForm({ ...form, status: e.target.value })}
              >
                <option>Active</option>
                <option>Inactive</option>
              </Form.Select>
            </Form.Group>
            <Button type="submit" variant="primary">Save Worker</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default HealthcareWorkersPage;
