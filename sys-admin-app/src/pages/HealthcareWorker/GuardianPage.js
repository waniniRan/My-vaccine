import React, { useState } from "react";
import { Offcanvas, Button, ListGroup, Container, Form, Modal } from "react-bootstrap";
import { House, Person, People, Capsule, Bell, BarChart, BoxArrowRight } from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";

const GuardianPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [guardians, setGuardians] = useState([]);

  const [form, setForm] = useState({
    national_id: "",
    fullname: "",
    email: "",
    phone_number: "",
    temporary_password: ""
  });

  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/healthcare-worker/login");
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setGuardians([...guardians, { ...form }]);
    setShowModal(false);
    setForm({
      national_id: "",
      fullname: "",
      email: "",
      phone_number: "",
      temporary_password: ""
    });
  };

  return (
    <>
      {/* Offcanvas Menu */}
      <Offcanvas show={showMenu} onHide={() => setShowMenu(false)}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Menu</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <ListGroup variant="flush">
            <ListGroup.Item action href="/healthcare-worker/dashboard"><House /> Home</ListGroup.Item>
            <ListGroup.Item action href="/healthcare-worker/guardian"><Person /> Guardian</ListGroup.Item>
            <ListGroup.Item action href="/healthcare-worker/children"><People /> Children</ListGroup.Item>
            <ListGroup.Item action href="/healthcare-worker/vaccination-records"><Capsule /> Vaccinations</ListGroup.Item>
            <ListGroup.Item action href="/healthcare-worker/growth-records"><BarChart /> Growth Records</ListGroup.Item>
            <ListGroup.Item action href="/healthcare-worker/notifications"><Bell /> Notifications</ListGroup.Item>
            <ListGroup.Item action onClick={handleLogout}><BoxArrowRight /> Logout</ListGroup.Item>
          </ListGroup>
        </Offcanvas.Body>
      </Offcanvas>

      {/* Header */}
      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <h3 className="mb-0">Manage Guardians</h3>
        <Button variant="light" onClick={() => setShowMenu(true)}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      {/* Content */}
      <Container className="py-4">
        <div className="d-flex justify-content-between mb-3">
          <h4>Guardians</h4>
          <Button onClick={() => setShowModal(true)}>Add Guardian</Button>
        </div>

        {/* Guardians table */}
        <table className="table table-striped">
          <thead>
            <tr>
              <th>National ID</th>
              <th>Full Name</th>
              <th>Email</th>
              <th>Phone</th>
            </tr>
          </thead>
          <tbody>
            {guardians.map((g, idx) => (
              <tr key={idx}>
                <td>{g.national_id}</td>
                <td>{g.fullname}</td>
                <td>{g.email}</td>
                <td>{g.phone_number}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Container>

      {/* Modal to add */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Add Guardian</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-2">
              <Form.Label>National ID</Form.Label>
              <Form.Control
                type="text"
                value={form.national_id}
                onChange={(e) => setForm({ ...form, national_id: e.target.value })}
                pattern="\d+"
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Full Name</Form.Label>
              <Form.Control
                value={form.fullname}
                onChange={(e) => setForm({ ...form, fullname: e.target.value })}
                required
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
              <Form.Label>Phone Number</Form.Label>
              <Form.Control
                value={form.phone_number}
                onChange={(e) => setForm({ ...form, phone_number: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Temporary Password</Form.Label>
              <Form.Control
                type="text"
                value={form.temporary_password}
                onChange={(e) => setForm({ ...form, temporary_password: e.target.value })}
                required
              />
            </Form.Group>
            <Button type="submit" variant="primary">Save Guardian</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default GuardianPage;
