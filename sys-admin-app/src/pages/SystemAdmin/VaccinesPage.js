import React, { useEffect, useState } from "react";
import {
  Container,
  Table,
  Button,
  Modal,
  Form,
  Offcanvas,
  ListGroup,
  Alert,
} from "react-bootstrap";
import {
  House,
  People,
  PlusSquare,
  FileText,
  List,
  Building,
  BoxArrowRight,
  PencilSquare,
  Trash,
} from "react-bootstrap-icons";
import {
  getVaccines,
  createVaccine,
  updateVaccine,
  deleteVaccine
} from "../../services/vaccineService";

const VaccinesPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [vaccines, setVaccines] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editModal, setEditModal] = useState(false);
  const [editingVaccine, setEditingVaccine] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [form, setForm] = useState({
    name: "",
    v_ID: "",
    description: "",
    dosage: "",
    diseasePrevented: "",
    recommended_age: "",
  });

  const loadVaccines = async () => {
    try {
      const res = await getVaccines();
      setVaccines(res.data.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load vaccines");
    }
  };

  useEffect(() => {
    loadVaccines();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createVaccine(form);
      setSuccess("Vaccine created successfully");
      setShowModal(false);
      setForm({
        name: "",
        v_ID: "",
        description: "",
        dosage: "",
        diseasePrevented: "",
        recommended_age: "",
      });
      loadVaccines();
    } catch (err) {
      console.error(err);
      setError("Failed to create vaccine");
    }
  };

  const handleEdit = (vaccine) => {
    setEditingVaccine(vaccine);
    setForm({
      name: vaccine.name,
      v_ID: vaccine.v_ID,
      description: vaccine.description,
      dosage: vaccine.dosage,
      diseasePrevented: vaccine.diseasePrevented,
      recommended_age: vaccine.recommended_age,
    });
    setEditModal(true);
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await updateVaccine(editingVaccine.v_ID, {
        description: form.description,
        dosage: form.dosage,
      });
      setSuccess("Vaccine updated successfully");
      setEditModal(false);
      loadVaccines();
    } catch (err) {
      console.error(err);
      setError("Failed to update vaccine");
    }
  };

  const handleDelete = async (v_ID) => {
    if (!window.confirm("Are you sure you want to delete this vaccine?")) return;
    try {
      await deleteVaccine(v_ID);
      setSuccess("Vaccine deleted successfully");
      loadVaccines();
    } catch (err) {
      console.error(err);
      setError("Failed to delete vaccine");
    }
  };

  return (
    <>
      <Offcanvas show={showMenu} onHide={() => setShowMenu(false)}>
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

      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <h3 className="mb-0">Manage Vaccines</h3>
        <Button variant="light" onClick={() => setShowMenu(true)}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Container className="py-4">
        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">{success}</Alert>}

        <div className="d-flex justify-content-between mb-3">
          <h4>Vaccines List</h4>
          <Button onClick={() => setShowModal(true)}>Add Vaccine</Button>
        </div>

        <Table bordered hover>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Disease Prevented</th>
              <th>Dosage</th>
              <th>Recommended Age</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {vaccines.map((v) => (
              <tr key={v.v_ID}>
                <td>{v.v_ID}</td>
                <td>{v.name}</td>
                <td>{v.diseasePrevented}</td>
                <td>{v.dosage}</td>
                <td>{v.recommended_age}</td>
                <td>{v.description}</td>
                <td>
                  <Button
                    size="sm"
                    variant="secondary"
                    className="me-2"
                    onClick={() => handleEdit(v)}
                  >
                    <PencilSquare />
                  </Button>
                  <Button
                    size="sm"
                    variant="danger"
                    onClick={() => handleDelete(v.v_ID)}
                  >
                    <Trash />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>

      {/* Create Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton><Modal.Title>Add Vaccine</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            {["name", "v_ID", "description", "dosage", "diseasePrevented", "recommended_age"].map((field) => (
              <Form.Group key={field} className="mb-2">
                <Form.Label>{field.replace("_", " ").toUpperCase()}</Form.Label>
                <Form.Control
                  value={form[field]}
                  onChange={(e) => setForm({ ...form, [field]: e.target.value })}
                  required
                />
              </Form.Group>
            ))}
            <Button type="submit" variant="primary">Save</Button>
          </Form>
        </Modal.Body>
      </Modal>

      {/* Edit Modal */}
      <Modal show={editModal} onHide={() => setEditModal(false)}>
        <Modal.Header closeButton><Modal.Title>Edit Vaccine</Modal.Title></Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleUpdate}>
            <Form.Group className="mb-2">
              <Form.Label>Description</Form.Label>
              <Form.Control
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Dosage</Form.Label>
              <Form.Control
                value={form.dosage}
                onChange={(e) => setForm({ ...form, dosage: e.target.value })}
                required
              />
            </Form.Group>
            <Button type="submit" variant="primary">Update</Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default VaccinesPage;
