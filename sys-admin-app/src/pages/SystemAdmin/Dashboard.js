import React, { useState, useEffect } from "react";
import { Offcanvas, Button, ListGroup, Container, Row, Col, Card, Alert } from "react-bootstrap";
import { House, People, PlusSquare, FileText, List, Building, BoxArrowRight } from "react-bootstrap-icons";
import { getFacilities } from "../../services/facilityService";
import { getFacilityAdmins } from "../../services/facilityAdminService";
import { getVaccines } from "../../services/vaccineService";
import { useNavigate } from "react-router-dom";

const SystemAdminDashboard = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [facilities, setFacilities] = useState([]);
  const [admins, setAdmins] = useState([]);
  const [vaccines, setVaccines] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleClose = () => setShowMenu(false);
  const handleShow = () => setShowMenu(true);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setError("You are not logged in.");
      return;
    }

    getFacilities()
      .then((response) => {
        setFacilities(Array.isArray(response.data.data) ? response.data.data : []);
      })
      .catch((err) => {
        setFacilities([]);
        setError("Failed to fetch facilities.");
      });

    getFacilityAdmins()
      .then((response) => {
        setAdmins(Array.isArray(response.data.data) ? response.data.data : []);
      })
      .catch((err) => {
        setAdmins([]);
        setError("Failed to fetch facility admins.");
      });

    getVaccines()
      .then((response) => {
        setVaccines(Array.isArray(response.data.data) ? response.data.data : []);
      })
      .catch((err) => {
        setVaccines([]);
        setError("Failed to fetch vaccines.");
      });
  }, []);

  return (
    <>
      <Offcanvas show={showMenu} onHide={handleClose}>
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
        <h3 className="mb-0">System Admin Dashboard</h3>
        <h4 className="mb-0">Welcome, System Admin</h4>
        <Button variant="light" onClick={handleShow}><span className="me-1">&#9776;</span> Menu</Button>
      </div>

      <Container className="my-4">
        {error && <Alert variant="danger">{error}</Alert>}

        <Row className="mb-4">
          <Col md={4}>
            <Card className="text-center"><Card.Body><h5>Total Facilities</h5><h2>{(facilities || []).length}</h2></Card.Body></Card>
          </Col>
          <Col md={4}>
            <Card className="text-center"><Card.Body><h5>Active Admins</h5><h2>{(admins || []).length}</h2></Card.Body></Card>
          </Col>
          <Col md={4}>
            <Card className="text-center"><Card.Body><h5>Total Vaccines</h5><h2>{(vaccines || []).length}</h2></Card.Body></Card>
          </Col>
        </Row>

        <Row>
          <Col md={8}>
            <Card>
              <Card.Header>Recent Activity</Card.Header>
              <ListGroup variant="flush">
                <ListGroup.Item>New facility registered</ListGroup.Item>
                <ListGroup.Item>Admin account activated</ListGroup.Item>
                <ListGroup.Item>Vaccine inventory updated</ListGroup.Item>
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
