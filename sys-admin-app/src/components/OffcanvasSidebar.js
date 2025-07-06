import React, { useState } from "react";
import { Offcanvas, Nav, Navbar, Container } from "react-bootstrap";
import { House, Building, PersonBadge, Capsule, FileEarmarkText, People } from "react-bootstrap-icons";

const OffcanvasSidebar = () => {
  const [show, setShow] = useState(false);

  const toggleShow = () => setShow((s) => !s);

  return (
    <>
      <Navbar bg="dark" variant="dark" expand="lg" fixed="top">
        <Container>
          <Navbar.Brand>System Admin</Navbar.Brand>
          <Navbar.Toggle onClick={toggleShow} />
        </Container>
      </Navbar>

      <Offcanvas show={show} onHide={toggleShow} className="bg-dark text-white">
        <Offcanvas.Header closeButton closeVariant="white">
          <Offcanvas.Title>Navigation</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <Nav className="flex-column">
            <Nav.Link href="/system-admin/dashboard" className="text-white mb-2">
              <House className="me-2" /> Home
            </Nav.Link>
            <Nav.Link href="/system-admin/facilities" className="text-white mb-2">
              <Building className="me-2" /> Health Facilities
            </Nav.Link>
            <Nav.Link href="/system-admin/facility-admins" className="text-white mb-2">
              <PersonBadge className="me-2" /> Facility Admins
            </Nav.Link>
            <Nav.Link href="/system-admin/vaccines" className="text-white mb-2">
              <Capsule className="me-2" /> Vaccines
            </Nav.Link>
            <Nav.Link href="/system-admin/reports" className="text-white mb-2">
              <FileEarmarkText className="me-2" /> System Reports
            </Nav.Link>
            <Nav.Link href="/system-admin/all-users" className="text-white mb-2">
              <People className="me-2" /> All Users
            </Nav.Link>
          </Nav>
        </Offcanvas.Body>
      </Offcanvas>
    </>
  );
};

export default OffcanvasSidebar;
