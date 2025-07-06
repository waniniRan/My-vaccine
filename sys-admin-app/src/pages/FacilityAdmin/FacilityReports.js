import React, { useState } from "react";
import { Container, Table, Offcanvas, ListGroup, Button } from "react-bootstrap";
import { House, People, FileText, BoxArrowRight } from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";

const FacilityReportsPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const navigate = useNavigate();

  const handleShowMenu = () => setShowMenu(true);
  const handleCloseMenu = () => setShowMenu(false);

  const handleLogout = () => {
    navigate("/facility-admin/login");
  };

  // mock reports data
  const reports = [
    { id: 1, name: "Weekly Vaccination Summary", date: "2025-07-05", status: "Downloaded" },
    { id: 2, name: "Stock Usage Report", date: "2025-07-01", status: "Available" }
  ];

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

      {/* header */}
      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <h3 className="mb-0">Facility Reports</h3>
        <Button variant="light" onClick={handleShowMenu}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Container className="py-4">
        <h4 className="mb-3">Reports</h4>
        <Table bordered hover>
          <thead>
            <tr>
              <th>Report Name</th>
              <th>Date</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((r) => (
              <tr key={r.id}>
                <td>{r.name}</td>
                <td>{r.date}</td>
                <td>{r.status}</td>
                <td>
                  <Button size="sm" variant="primary">
                    Download
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
    </>
  );
};

export default FacilityReportsPage;
