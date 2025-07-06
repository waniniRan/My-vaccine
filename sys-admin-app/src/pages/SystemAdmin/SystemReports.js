import React, { useState, useEffect } from "react";
import { Container, Table, Offcanvas, ListGroup, Button, Spinner, Alert } from "react-bootstrap";
import { House, People, PlusSquare, FileText, List, Building, BoxArrowRight, Download } from "react-bootstrap-icons";
import reportService from "../../services/reportService";

const SystemReportsPage = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCloseMenu = () => setShowMenu(false);
  const handleShowMenu = () => setShowMenu(true);

  useEffect(() => {
    const fetchReports = async () => {
    try {
      setLoading(true);
      const data = await reportService.getSystemReports();
      setReports(data); // or data.data depending on your Django response
    } catch (err) {
      console.error(err);
      setError("Could not fetch reports");
    } finally {
      setLoading(false);
    }
  };
  fetchReports();
  }, []);

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
        {error && <Alert variant="danger">{error}</Alert>}
        {loading ? (
          <div className="text-center"><Spinner animation="border" /></div>
        ) : (
          <>
            <h4>Available Reports</h4>
            <Table bordered hover>
              <thead>
                <tr>
                  <th>Report Name</th>
                  <th>Date</th>
                  <th>Download</th>
                </tr>
              </thead>
              <tbody>
                {reports.map((r) => (
                  <tr key={r.id}>
                    <td>{r.name}</td>
                    <td>{r.date}</td>
                    <td>
                      <a
                        href={r.file_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-primary btn-sm"
                      >
                        <Download /> Download
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </>
        )}
      </Container>
    </>
  );
};

export default SystemReportsPage;
