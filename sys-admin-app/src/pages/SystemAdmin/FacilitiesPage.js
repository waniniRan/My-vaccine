import React, { useState } from "react";
import { Container, Table, Button, Modal, Form, Offcanvas, ListGroup } from "react-bootstrap";
import { House, People, PlusSquare, FileText, List, Building, BoxArrowRight } from "react-bootstrap-icons";


const FacilitiesPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const handleCloseMenu = () => setShowMenu(false);
  const handleShowMenu = () => setShowMenu(true);

  const [facilities, setFacilities] = useState([
    { id: 1, name: "Nairobi General", type: "HOSPITAL", location: "Nairobi" },
    { id: 2, name: "Mombasa Clinic", type: "CLINIC", location: "Mombasa" }
  ]);

  const [form, setForm] = useState({ name: "", type: "HOSPITAL", location: "" });

  const handleSubmit = (e) => {
    e.preventDefault();
    setFacilities([...facilities, { ...form, id: facilities.length + 1 }]);
    setShowModal(false);
  };

  return (
    <>
      {/* offcanvas menu */}
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
        <h3 className="mb-0">Manage Facilities</h3>
        <Button variant="light" onClick={handleShowMenu}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Container className="py-4">
        <div className="d-flex justify-content-between mb-3">
          <h4>Facilities List</h4>
          <Button onClick={() => setShowModal(true)}>Add Facility</Button>
        </div>

        <Table bordered hover>
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Location</th>
            </tr>
          </thead>
          <tbody>
            {facilities.map((f) => (
              <tr key={f.id}>
                <td>{f.name}</td>
                <td>{f.type}</td>
                <td>{f.location}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>

      {/* modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Add Facility</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-2">
              <Form.Label>Facility Name</Form.Label>
              <Form.Control
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Facility Type</Form.Label>
              <Form.Select
                value={form.type}
                onChange={(e) => setForm({ ...form, type: e.target.value })}
              >
                <option>HOSPITAL</option>
                <option>CLINIC</option>
                <option>HEALTH_CENTER</option>
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Location</Form.Label>
              <Form.Control
                value={form.location}
                onChange={(e) => setForm({ ...form, location: e.target.value })}
                required
              />
            </Form.Group>
            <Button type="submit" variant="primary">Save</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default FacilitiesPage;
