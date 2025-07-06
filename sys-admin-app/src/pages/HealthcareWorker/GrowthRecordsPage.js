import React, { useState } from "react";
import { Offcanvas, Button, ListGroup, Container, Modal, Form } from "react-bootstrap";
import { House, Person, People, Capsule, Bell, BarChart, BoxArrowRight } from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";

const GrowthRecordsPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [records, setRecords] = useState([]);

  const [form, setForm] = useState({
    child_name: "",
    date: "",
    weight: "",
    height: ""
  });

  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/healthcare-worker/login");
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setRecords([...records, { ...form, id: records.length + 1 }]);
    setShowModal(false);
    setForm({
      child_name: "",
      date: "",
      weight: "",
      height: ""
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
        <h3 className="mb-0">Growth Records</h3>
        <Button variant="light" onClick={() => setShowMenu(true)}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      {/* Content */}
      <Container className="py-4">
        <div className="d-flex justify-content-between mb-3">
          <h4>Growth History</h4>
          <Button onClick={() => setShowModal(true)}>Add Record</Button>
        </div>

        {/* Table */}
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Child</th>
              <th>Date</th>
              <th>Weight (kg)</th>
              <th>Height (cm)</th>
            </tr>
          </thead>
          <tbody>
            {records.map((r, idx) => (
              <tr key={idx}>
                <td>{r.child_name}</td>
                <td>{r.date}</td>
                <td>{r.weight}</td>
                <td>{r.height}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Container>

      {/* Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Add Growth Record</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-2">
              <Form.Label>Child Name</Form.Label>
              <Form.Control
                value={form.child_name}
                onChange={(e) => setForm({ ...form, child_name: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Date</Form.Label>
              <Form.Control
                type="date"
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Weight (kg)</Form.Label>
              <Form.Control
                type="number"
                step="0.1"
                value={form.weight}
                onChange={(e) => setForm({ ...form, weight: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Height (cm)</Form.Label>
              <Form.Control
                type="number"
                step="0.1"
                value={form.height}
                onChange={(e) => setForm({ ...form, height: e.target.value })}
                required
              />
            </Form.Group>
            <Button type="submit" variant="primary">Save Record</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default GrowthRecordsPage;
