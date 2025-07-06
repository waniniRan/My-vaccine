import React, { useState } from "react";
import { Container, Table, Offcanvas, ListGroup, Button } from "react-bootstrap";
import { House, People, PlusSquare, FileText, List, Building, BoxArrowRight } from "react-bootstrap-icons";

const SystemReportsPage = () => {
  const [showMenu, setShowMenu] = useState(false);

  const handleCloseMenu = () => setShowMenu(false);
  const handleShowMenu = () => setShowMenu(true);

  const reports = [
    { id: 1, name: "System Audit Report", date: "2025-07-01" },
    { id: 2, name: "User Activity Report", date: "2025-07-02" },
  ];

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

      <div className="bg-primary text-white p-3 d-flex justify-content-between align-items-center">
        <h3 className="mb-0">System Reports</h3>
        <Button variant="light" onClick={handleShowMenu}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Container className="py-4">
        <h4>Available Reports</h4>
        <Table bordered hover>
          <thead>
            <tr>
              <th>Report Name</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((r) => (
              <tr key={r.id}>
                <td>{r.name}</td>
                <td>{r.date}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
    </>
  );
};

export default SystemReportsPage;
