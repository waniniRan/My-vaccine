import React, { useState } from "react";
import { Container, Table, Button, Modal, Form, Offcanvas, ListGroup } from "react-bootstrap";
import { House, People, PlusSquare, FileText, List, Building,BoxArrowRight } from "react-bootstrap-icons";

const FacilityAdminsPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const handleCloseMenu = () => setShowMenu(false);
  const handleShowMenu = () => setShowMenu(true);

  const [admins, setAdmins] = useState([
    { id: 1, fullname: "Jane Doe", username: "jane.admin", email: "jane@health.org", facility: "Nairobi General" },
  ]);

  const [form, setForm] = useState({ fullname: "", username: "", email: "", facility: "" });

  const handleSubmit = (e) => {
    e.preventDefault();
    setAdmins([...admins, { ...form, id: admins.length + 1 }]);
    setShowModal(false);
  };

  return (
    <>
      <Offcanvas show={showMenu} onHide={handleCloseMenu}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Menu</Offcanvas.Title>
        </Offcanvas.Header>
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

      {/* header */}
      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <h3 className="mb-0">Manage Facility Admins</h3>
        <Button variant="light" onClick={handleShowMenu}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Container className="py-4">
        <div className="d-flex justify-content-between mb-3">
          <h4>Facility Admins List</h4>
          <Button onClick={() => setShowModal(true)}>Add Facility Admin</Button>
        </div>

        <Table bordered hover>
          <thead>
            <tr>
              <th>Full Name</th>
              <th>Username</th>
              <th>Email</th>
              <th>Facility</th>
            </tr>
          </thead>
          <tbody>
            {admins.map((a) => (
              <tr key={a.id}>
                <td>{a.fullname}</td>
                <td>{a.username}</td>
                <td>{a.email}</td>
                <td>{a.facility}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>

      {/* modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Add Facility Admin</Modal.Title>
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
              <Form.Label>Username</Form.Label>
              <Form.Control
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Facility</Form.Label>
              <Form.Control
                value={form.facility}
                onChange={(e) => setForm({ ...form, facility: e.target.value })}
                required
              />
            </Form.Group>
            <Button type="submit" variant="primary">Save Admin</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default FacilityAdminsPage;
