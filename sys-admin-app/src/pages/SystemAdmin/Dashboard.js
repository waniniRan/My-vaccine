import React, { useState } from "react";
import { Offcanvas, Button, ListGroup, Container, Row, Col, Card } from "react-bootstrap";
import { House, People, PlusSquare, FileText, List, Building,BoxArrowRight } from "react-bootstrap-icons";


const SystemAdminDashboard = () => {
  const [showMenu, setShowMenu] = useState(false);

  const handleClose = () => setShowMenu(false);
  const handleShow = () => setShowMenu(true);

  return (
    <>
      {/* Offcanvas sidebar */}
      <Offcanvas show={showMenu} onHide={handleClose}>
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
              <PlusSquare/> Vaccines
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

      {/* Header */}
      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <h3 className="mb-0">System Admin Dashboard</h3>
        <h4 className="mb-0">Welcome, Admin</h4>
        <Button variant="light" onClick={handleShow}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Container className="my-4">
        {/* Metrics */}
        <Row className="mb-4">
          <Col md={4}>
            <Card className="text-center">
              <Card.Body>
                <h5>Total Facilities</h5>
                <h2>15</h2>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4}>
            <Card className="text-center">
              <Card.Body>
                <h5>Active Admins</h5>
                <h2>13</h2>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4}>
            <Card className="text-center">
              <Card.Body>
                <h5>Total Vaccines</h5>
                <h2>30</h2>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        {/* Recent Activity */}
        <Row>
          <Col md={8}>
            <Card>
              <Card.Header>Recent Activity</Card.Header>
              <ListGroup variant="flush">
                <ListGroup.Item>New facility registered (2 hours ago)</ListGroup.Item>
                <ListGroup.Item>Admin account activated (4 hours ago)</ListGroup.Item>
                <ListGroup.Item>Vaccine inventory updated (6 hours ago)</ListGroup.Item>
              </ListGroup>
            </Card>
          </Col>
          <Col md={4}>
            <Card>
              <Card.Header>System Status</Card.Header>
              <ListGroup variant="flush">
                <ListGroup.Item>Database: Online</ListGroup.Item>
                <ListGroup.Item>API Services: Active</ListGroup.Item>
                <ListGroup.Item>Security: Secure</ListGroup.Item>
              </ListGroup>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default SystemAdminDashboard;
