import React, { useState } from "react";
import { Container, Row, Col, Card, Table, Button, Offcanvas, ListGroup } from "react-bootstrap";
import { House, People, FileText,BoxArrowRight } from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";

const FacilityAdminDashboard = () => {
  const [showMenu, setShowMenu] = useState(false);
  const navigate = useNavigate();

  const handleShowMenu = () => setShowMenu(true);
  const handleCloseMenu = () => setShowMenu(false);

  // mock data
  const workers = [
    { id: "A0001", name: "Dr. Sarah Johnson", status: "Active", lastLogin: "2025-07-05 09:30" },
    { id: "A0002", name: "Nurse Mike Chen", status: "Active", lastLogin: "2025-07-05 08:45" },
    { id: "A0002", name: "Dr. Emily Rodriguez", status: "Offline", lastLogin: "2025-07-04 17:20" }
  ];

  const handleLogout = () => {
    navigate("/facility-admin/login");
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

      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <h3 className="mb-0">Facility Information Dashboard</h3>
        <Button variant="light" onClick={handleShowMenu}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Container className="py-4">
        <Row className="mb-3">
          <Col md={6}>
            <Card>
              <Card.Body>
                <Card.Title>Total Healthcare Workers</Card.Title>
                <Card.Text>40</Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={6}>
            <Card>
              <Card.Body>
                <Card.Title>Active Today</Card.Title>
                <Card.Text>32</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        <Card>
          <Card.Header>Healthcare Workers</Card.Header>
          <Card.Body>
            <Table striped hover>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>ID</th>
                  <th>Status</th>
                  <th>Last Login</th>
                </tr>
              </thead>
              <tbody>
                {workers.map((w) => (
                  <tr key={w.id}>
                    <td>{w.name}</td>
                    <td>{w.id}</td>
                    <td>
                      <span className={`badge ${w.status === "Active" ? "bg-success" : "bg-secondary"}`}>
                        {w.status}
                      </span>
                    </td>
                    <td>{w.lastLogin}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Card.Body>
        </Card>
      </Container>
    </>
  );
};

export default FacilityAdminDashboard;
