import React from "react";
import { Button, Form, Card } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const SystemAdminLogin = () => {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // 👉 later, add token validation here
    navigate("/system-admin/dashboard");
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
      <Card style={{ width: "400px", padding: "20px" }}>
        <h3 className="text-center mb-4">System Admin Login</h3>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" placeholder="Enter username" />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Enter password" />
          </Form.Group>
          <Button variant="primary" type="submit" className="w-100 mt-2">
            Login
          </Button>
        </Form>
      </Card>
    </div>
  );
};

export default SystemAdminLogin;
