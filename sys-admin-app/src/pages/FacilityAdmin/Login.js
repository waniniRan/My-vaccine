import React from "react";
import { Button, Form, Card } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const FacilityAdminLogin = () => {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // TODO: add API call
    navigate("/facility-admin/dashboard");
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
      <Card style={{ width: "400px", padding: "20px" }}>
        <h3 className="text-center mb-3">Facility Admin Login</h3>
        <Form onSubmit={handleLogin}>
          <Form.Group className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" placeholder="Enter username" required />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Enter password" required />
          </Form.Group>
          <Button type="submit" variant="primary" className="w-100 mt-2">
            Login
          </Button>
        </Form>
        <div className="text-center mt-3">
          <a href="#">Forgot password?</a>
        </div>
      </Card>
    </div>
  );
};

export default FacilityAdminLogin;
