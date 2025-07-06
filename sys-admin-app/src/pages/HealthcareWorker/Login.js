import React from "react";
import { Card, Button, Form } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const HealthcareWorkerLogin = () => {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: hook up real login logic
    navigate("/healthcare-worker/dashboard");
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
      <Card style={{ width: "400px", padding: "20px" }}>
        <h3 className="text-center mb-4">Healthcare Worker Login</h3>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" placeholder="Enter your username" required />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Enter your password" required />
          </Form.Group>
          <Button type="submit" className="w-100 mt-2" variant="primary">
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

export default HealthcareWorkerLogin;
