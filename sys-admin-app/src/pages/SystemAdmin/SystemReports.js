import React, { useEffect, useState } from 'react';
import { getSystemReports, exportSystemReport, downloadReport } from '../../services/reportService';
import { Card, Table, Button, Spinner, Alert, InputGroup, FormControl, Badge, Offcanvas, ListGroup } from 'react-bootstrap';
import { Download, FileEarmarkArrowDown, Funnel, House, People, PlusSquare, FileText, List, Building, BoxArrowRight } from 'react-bootstrap-icons';

function SystemReports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [search, setSearch] = useState('');
  const [showMenu, setShowMenu] = useState(false);

  const fetchReports = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getSystemReports();
      setReports(data);
    } catch (err) {
      setError(err.toString());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleExport = async (type = 'all', format = 'csv') => {
    setGenerating(true);
    setError('');
    setSuccess('');
    try {
      const res = await exportSystemReport({ report_type: type, format });
      if (res && res.data && res.data.data && res.data.data.download_url) {
        window.open(res.data.data.download_url, '_blank');
        setSuccess('Report generated and download started!');
      }
    } catch (err) {
      setError(err.toString());
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = async (reportId) => {
    setError(null);
    setSuccess('');
    try {
      const blob = await downloadReport(reportId);
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${reportId}.csv`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      setSuccess('Report downloaded!');
    } catch {
      setError('Failed to download report');
    }
  };

  // Filter reports by search
  const filteredReports = reports.filter(r =>
    r.report_type.toLowerCase().includes(search.toLowerCase()) ||
    (r.generated_by && r.generated_by.toLowerCase().includes(search.toLowerCase()))
  );

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
        <h3 className="mb-0">System Reports</h3>
        <Button variant="light" onClick={() => setShowMenu(true)}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Card className="my-4 shadow">
        <Card.Header as="h4">System Reports</Card.Header>
        <Card.Body>
          <div className="d-flex justify-content-between align-items-center mb-3">
            <InputGroup style={{ maxWidth: 300 }}>
              <InputGroup.Text><Funnel /></InputGroup.Text>
              <FormControl
                placeholder="Filter by type or user"
                value={search}
                onChange={e => setSearch(e.target.value)}
              />
            </InputGroup>
            <div>
              <Button
                variant="success"
                className="me-2"
                onClick={() => handleExport('all', 'csv')}
                disabled={generating}
              >
                <FileEarmarkArrowDown className="me-1" />
                {generating ? 'Generating...' : 'Export CSV'}
              </Button>
              <Button
                variant="info"
                onClick={() => handleExport('all', 'pdf')}
                disabled={generating}
              >
                <FileEarmarkArrowDown className="me-1" />
                {generating ? 'Generating...' : 'Export PDF'}
              </Button>
            </div>
          </div>
          {error && <Alert variant="danger">{error}</Alert>}
          {success && <Alert variant="success">{success}</Alert>}
          {loading ? (
            <div className="text-center"><Spinner animation="border" /></div>
          ) : filteredReports.length === 0 ? (
            <div className="text-center text-muted my-4">
              <Download size={48} className="mb-2" />
              <div>No reports found.</div>
            </div>
          ) : (
            <Table striped hover responsive>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Type</th>
                  <th>Generated At</th>
                  <th>Generated By</th>
                  <th>Download</th>
                </tr>
              </thead>
              <tbody>
                {filteredReports.map(r => (
                  <tr key={r.id}>
                    <td>{r.id}</td>
                    <td>
                      <Badge bg="secondary">{r.report_type}</Badge>
                    </td>
                    <td>{new Date(r.generated_at).toLocaleString()}</td>
                    <td>{r.generated_by}</td>
                    <td>
                      <Button
                        variant="outline-primary"
                        size="sm"
                        onClick={() => handleDownload(r.id)}
                        title="Download"
                      >
                        <Download />
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Card.Body>
      </Card>
    </>
  );
}

export default SystemReports;
