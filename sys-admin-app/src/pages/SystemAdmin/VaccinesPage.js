import React, { useState } from "react";
import { Container, Table, Button, Modal, Form, Offcanvas, ListGroup } from "react-bootstrap";
import { House, People, PlusSquare, FileText, List, Building,BoxArrowRight } from "react-bootstrap-icons";

const VaccinesPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const handleCloseMenu = () => setShowMenu(false);
  const handleShowMenu = () => setShowMenu(true);

  const [vaccines, setVaccines] = useState([
    { id: 1, name: "BCG", disease: "Tuberculosis", schedule: "At birth" },
    { id: 2, name: "OPV", disease: "Polio", schedule: "6, 10, 14 weeks" }
  ]);

  const [form, setForm] = useState({ name: "", disease: "", schedule: "" });

  const handleSubmit = (e) => {
    e.preventDefault();
    setVaccines([...vaccines, { ...form, id: vaccines.length + 1 }]);
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
        <h3 className="mb-0">Manage Vaccines</h3>
        <Button variant="light" onClick={handleShowMenu}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Container className="py-4">
        <div className="d-flex justify-content-between mb-3">
          <h4>Vaccine Catalog</h4>
          <Button onClick={() => setShowModal(true)}>Add Vaccine</Button>
        </div>

        <Table bordered hover>
          <thead>
            <tr>
              <th>Name</th>
              <th>Disease</th>
              <th>Schedule</th>
            </tr>
          </thead>
          <tbody>
            {vaccines.map((v) => (
              <tr key={v.id}>
                <td>{v.name}</td>
                <td>{v.disease}</td>
                <td>{v.schedule}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>

      {/* modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Add Vaccine</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-2">
              <Form.Label>Name</Form.Label>
              <Form.Control
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Disease</Form.Label>
              <Form.Control
                value={form.disease}
                onChange={(e) => setForm({ ...form, disease: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Schedule</Form.Label>
              <Form.Control
                value={form.schedule}
                onChange={(e) => setForm({ ...form, schedule: e.target.value })}
                required
              />
            </Form.Group>
            <Button type="submit" variant="primary">Save Vaccine</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default VaccinesPage;
