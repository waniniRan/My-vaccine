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
import facilityAdminService from "../../services/facilityAdminService";

const FacilityAdminsPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [admins, setAdmins] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [form, setForm] = useState({
    fullname: "",
    username: "",
    email: "",
    facility: "",
    temporary_password: "",
  });

  const [editForm, setEditForm] = useState({
    admin_id: "",
    email: "",
  });

  const handleCloseMenu = () => setShowMenu(false);
  const handleShowMenu = () => setShowMenu(true);

  const fetchAdmins = async () => {
    try {
      setError("");
      const res = await facilityAdminService.getFacilityAdmins();
      setAdmins(res.data.data);
    } catch (error) {
      console.error(error);
      setError("Failed to load facility admins");
    }
  };

  useEffect(() => {
    fetchAdmins();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError("");
      await facilityAdminService.createFacilityAdmin({
        fullname: form.fullname,
        admin_username: form.username,
        email: form.email,
        facility: form.facility,
        temporary_password: form.temporary_password || "ChangeMe123",
      });
      setSuccess("Facility admin created successfully");
      setForm({
        fullname: "",
        username: "",
        email: "",
        facility: "",
        temporary_password: "",
      });
      setShowModal(false);
      fetchAdmins();
    } catch (error) {
      console.error(error);
      setError("Failed to create facility admin");
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (admin) => {
    setEditForm({
      admin_id: admin.admin_id,
      email: admin.email,
    });
    setShowEditModal(true);
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await facilityAdminService.updateFacilityAdmin(editForm.admin_id, {
        email: editForm.email,
      });
      setSuccess("Facility admin updated successfully");
      setShowEditModal(false);
      fetchAdmins();
    } catch (error) {
      console.error(error);
      setError("Failed to update facility admin");
    }
  };

  const handleDelete = async (admin_id) => {
    if (!window.confirm("Delete this facility admin?")) return;
    try {
      await facilityAdminService.deleteFacilityAdmin(admin_id);
      setSuccess("Facility admin deleted successfully");
      fetchAdmins();
    } catch (error) {
      console.error(error);
      setError("Failed to delete facility admin");
    }
  };

  return (
    <>
      {/* side menu */}
      <Offcanvas show={showMenu} onHide={handleCloseMenu}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Menu</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <ListGroup variant="flush">
            <ListGroup.Item action href="/system-admin/dashboard">
              <House /> Home
            </ListGroup.Item>
            <ListGroup.Item action href="/system-admin/facilities">
              <Building /> Facilities
            </ListGroup.Item>
            <ListGroup.Item action href="/system-admin/facility-admins">
              <People /> Facility Admins
            </ListGroup.Item>
            <ListGroup.Item action href="/system-admin/vaccines">
              <PlusSquare /> Vaccines
            </ListGroup.Item>
            <ListGroup.Item action href="/system-admin/reports">
              <FileText /> System Reports
            </ListGroup.Item>
            <ListGroup.Item action href="/system-admin/all-users">
              <List /> All Users
            </ListGroup.Item>
            <ListGroup.Item action href="/">
              <BoxArrowRight /> Logout
            </ListGroup.Item>
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
        {error && <Alert variant="danger">{error}</Alert>}
        {success && <Alert variant="success">{success}</Alert>}

        <div className="d-flex justify-content-between mb-3">
          <h4>Facility Admins</h4>
          <Button onClick={() => setShowModal(true)}>Add Facility Admin</Button>
        </div>

        <Table bordered hover>
          <thead>
            <tr>
              <th>Full Name</th>
              <th>Username</th>
              <th>Email</th>
              <th>Facility</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {admins.map((a) => (
              <tr key={a.admin_id}>
                <td>{a.fullname}</td>
                <td>{a.admin_username}</td>
                <td>{a.email}</td>
                <td>{a.facility}</td>
                <td>
                  <Button
                    variant="secondary"
                    size="sm"
                    className="me-2"
                    onClick={() => handleEdit(a)}
                  >
                    <PencilSquare />
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => handleDelete(a.admin_id)}
                  >
                    <Trash />
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>

      {/* create modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Add Facility Admin</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleCreate}>
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
              <Form.Label>Facility (ID)</Form.Label>
              <Form.Control
                value={form.facility}
                onChange={(e) => setForm({ ...form, facility: e.target.value })}
                placeholder="e.g. A0001"
                required
              />
            </Form.Group>
            <Form.Group className="mb-2">
              <Form.Label>Temporary Password</Form.Label>
              <Form.Control
                value={form.temporary_password}
                onChange={(e) =>
                  setForm({ ...form, temporary_password: e.target.value })
                }
                placeholder="Leave blank for ChangeMe123"
              />
            </Form.Group>
            <Button type="submit" disabled={loading} variant="primary">
              {loading ? "Saving..." : "Save"}
            </Button>
          </Form>
        </Modal.Body>
      </Modal>

      {/* edit modal */}
      <Modal show={showEditModal} onHide={() => setShowEditModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Update Admin Email</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleUpdate}>
            <Form.Group className="mb-2">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                value={editForm.email}
                onChange={(e) =>
                  setEditForm({ ...editForm, email: e.target.value })
                }
                required
              />
            </Form.Group>
            <Button type="submit" variant="primary">
              Update
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default FacilityAdminsPage;
