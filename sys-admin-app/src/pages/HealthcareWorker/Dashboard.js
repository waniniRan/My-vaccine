import React, { useState } from "react";
import { Offcanvas, Button, ListGroup, Container, Row, Col, Card, Table } from "react-bootstrap";
import { House, Person, People, Capsule, Bell, BarChart, BoxArrowRight } from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";

const HealthcareWorkerDashboard = () => {
  const [showMenu, setShowMenu] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/healthcare-worker/login");
  };

  // demo hardcoded data for testing
  const registeredData = [
    {
      guardian: "Mary Wanjiru",
      child: "James Mwangi",
      registered_on: "2025-07-01",
      registered_by: "Nurse Anne",
      active: true
    },
    {
      guardian: "Ali Hassan",
      child: "Fatma Hassan",
      registered_on: "2025-07-03",
      registered_by: "Nurse Anne",
      active: false
    }
  ];

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
        <h3 className="mb-0">Healthcare Worker Dashboard</h3>
        <Button variant="light" onClick={() => setShowMenu(true)}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      {/* Summary */}
      <Container className="py-4">
        <Row>
          <Col md={6}>
            <Card className="mb-3">
              <Card.Body>
                <Card.Title>Total Guardians</Card.Title>
                <h2>25</h2>
              </Card.Body>
            </Card>
          </Col>
          <Col md={6}>
            <Card className="mb-3">
              <Card.Body>
                <Card.Title>Total Children</Card.Title>
                <h2>40</h2>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Registered guardian+child list */}
        <h4 className="mt-4">Registered Parents + Children</h4>
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Guardian</th>
              <th>Child</th>
              <th>Registered On</th>
              <th>Registered By</th>
              <th>Active</th>
            </tr>
          </thead>
          <tbody>
            {registeredData.map((entry, idx) => (
              <tr key={idx}>
                <td>{entry.guardian}</td>
                <td>{entry.child}</td>
                <td>{entry.registered_on}</td>
                <td>{entry.registered_by}</td>
                <td>{entry.active ? "Yes" : "No"}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
    </>
  );
};

export default HealthcareWorkerDashboard;
