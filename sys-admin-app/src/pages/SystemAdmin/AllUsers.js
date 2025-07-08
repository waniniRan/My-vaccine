import React, { useEffect, useState } from 'react';
import { getAllUsers, exportUsers } from '../../services/userService';
import { Card, Table, Button, Spinner, Alert, InputGroup, FormControl, Badge, Offcanvas, ListGroup } from 'react-bootstrap';
import { Download, Funnel, House, People, PlusSquare, FileText, List, Building, BoxArrowRight } from 'react-bootstrap-icons';

function AllUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [search, setSearch] = useState('');
  const [showMenu, setShowMenu] = useState(false);

  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getAllUsers();
      setUsers(data);
    } catch (err) {
      setError(err.toString());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleExport = async () => {
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const res = await exportUsers();
      const blob = await res.data.data;
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'users.csv');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      setSuccess('User list exported!');
    } catch (err) {
      setError(err.toString());
    } finally {
      setLoading(false);
    }
  };

  // Filter users by search
  const filteredUsers = users.filter(u =>
    (u.full_name && u.full_name.toLowerCase().includes(search.toLowerCase())) ||
    (u.username && u.username.toLowerCase().includes(search.toLowerCase())) ||
    (u.email && u.email.toLowerCase().includes(search.toLowerCase())) ||
    (u.role && u.role.toLowerCase().includes(search.toLowerCase()))
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
        <h3 className="mb-0">All Users</h3>
        <Button variant="light" onClick={() => setShowMenu(true)}>
          <span className="me-1">&#9776;</span> Menu
        </Button>
      </div>

      <Card className="my-4 shadow">
        <Card.Header as="h4">All Users</Card.Header>
        <Card.Body>
          <div className="d-flex justify-content-between align-items-center mb-3">
            <InputGroup style={{ maxWidth: 300 }}>
              <InputGroup.Text><Funnel /></InputGroup.Text>
              <FormControl
                placeholder="Search by name, username, email, or role"
                value={search}
                onChange={e => setSearch(e.target.value)}
              />
            </InputGroup>
            <Button
              variant="success"
              onClick={handleExport}
              disabled={exporting}
            >
              <Download className="me-1" />
              {exporting ? 'Exporting...' : 'Export Users (CSV)'}
            </Button>
          </div>
          {error && <Alert variant="danger">{error}</Alert>}
          {success && <Alert variant="success">{success}</Alert>}
          {loading ? (
            <div className="text-center"><Spinner animation="border" /></div>
          ) : filteredUsers.length === 0 ? (
            <div className="text-center text-muted my-4">
              <Download size={48} className="mb-2" />
              <div>No users found.</div>
            </div>
          ) : (
            <Table striped hover responsive>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Role</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map(u => (
                  <tr key={u.id}>
                    <td>{u.id}</td>
                    <td>{u.full_name || u.name || u.username}</td>
                    <td>{u.username}</td>
                    <td>{u.email}</td>
                    <td>
                      <Badge bg="info" className="text-uppercase">{u.role}</Badge>
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

export default AllUsers;
