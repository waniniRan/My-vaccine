import React, { useState } from "react";
import { Offcanvas, Button, ListGroup, Container, Form, Modal } from "react-bootstrap";
import { House, Person, People, Capsule, Bell, BarChart, BoxArrowRight } from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";

const ChildPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [children, setChildren] = useState([]);

  const [form, setForm] = useState({
    fullname: "",
    date_of_birth: "",
    gender: "",
    guardian_national_id: ""
  });

  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/healthcare-worker/login");
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setChildren([...children, { ...form, id: children.length + 1 }]);
    setShowModal(false);
    setForm({
      fullname: "",
      date_of_birth: "",
      gender: "",
      guardian_national_id: ""
    });
  };

  return (
    <>
      {/* Offcanvas */}
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
        <h3 className="mb-0">Manage Children</h3>
        <Button variant="light" onClick={() => setShowMenu(true)}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      {/* Content */}
      <Container className="py-4">
        <div className="d-flex justify-content-between mb-3">
          <h4>Children</h4>
          <Button onClick={() => setShowModal(true)}>Add Child</Button>
        </div>

        {/* Table */}
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Full Name</th>
              <th>Date of Birth</th>
              <th>Gender</th>
              <th>Guardian National ID</th>
            </tr>
          </thead>
          <tbody>
            {children.map((c, idx) => (
              <tr key={idx}>
                <td>{c.fullname}</td>
                <td>{c.date_of_birth}</td>
                <td>{c.gender}</td>
                <td>{c.guardian_national_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Container>

      {/* Add Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Add Child</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-2">
              <Form.Label>Full Name</Form.Label>
              <Form.Control
                value={form.fullname}
                onChange={(e) => setForm({ ...form, fullname: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Date of Birth</Form.Label>
              <Form.Control
                type="date"
                value={form.date_of_birth}
                onChange={(e) => setForm({ ...form, date_of_birth: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Gender</Form.Label>
              <Form.Select
                value={form.gender}
                onChange={(e) => setForm({ ...form, gender: e.target.value })}
                required
              >
                <option value="">Select gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Guardian National ID</Form.Label>
              <Form.Control
                value={form.guardian_national_id}
                onChange={(e) => setForm({ ...form, guardian_national_id: e.target.value })}
                pattern="\d+"
                required
              />
            </Form.Group>
            <Button type="submit" variant="primary">Save Child</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default ChildPage;
