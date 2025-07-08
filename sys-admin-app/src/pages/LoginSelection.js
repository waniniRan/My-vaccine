import React from "react";
import { Link } from "react-router-dom";

const cardStyle = {
  maxWidth: 400,
  margin: "60px auto",
  padding: 32,
  background: "#fff",
  borderRadius: 12,
  boxShadow: "0 2px 16px rgba(0,0,0,0.08)",
  textAlign: "center",
};

const titleStyle = {
  marginBottom: 24,
  fontWeight: 700,
  fontSize: 28,
  color: "#2c3e50",
};

const listStyle = {
  listStyle: "none",
  padding: 0,
  margin: 0,
};

const linkStyle = {
  display: "block",
  margin: "16px 0",
  padding: "12px 0",
  background: "#1976d2",
  color: "#fff",
  borderRadius: 6,
  textDecoration: "none",
  fontWeight: 500,
  fontSize: 18,
  transition: "background 0.2s",
};

const linkHoverStyle = {
  background: "#1565c0",
};

class LoginSelection extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hovered: null };
  }

  handleMouseEnter = (idx) => {
    this.setState({ hovered: idx });
  };

  handleMouseLeave = () => {
    this.setState({ hovered: null });
  };

  render() {
    const links = [
      { to: "/system-admin/login", label: "System Admin Login" },
      { to: "/facility-admin/login", label: "Facility Admin Login" },
      { to: "/healthcare-worker/login", label: "Healthcare Worker Login" },
      { to: "https://your-guardian-app-url/login", label: "Parent/Guardian Login", external: true },
    ];
    return (
      <div style={cardStyle}>
        <div style={titleStyle}>Select your login type</div>
        <ul style={listStyle}>
          {links.map((link, idx) => (
            <li key={link.to}>
              {link.external ? (
                <a
                  href={link.to}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={
                    this.state.hovered === idx
                      ? { ...linkStyle, ...linkHoverStyle }
                      : linkStyle
                  }
                  onMouseEnter={() => this.handleMouseEnter(idx)}
                  onMouseLeave={this.handleMouseLeave}
                >
                  {link.label}
                </a>
              ) : (
                <Link
                  to={link.to}
                  style={
                    this.state.hovered === idx
                      ? { ...linkStyle, ...linkHoverStyle }
                      : linkStyle
                  }
                  onMouseEnter={() => this.handleMouseEnter(idx)}
                  onMouseLeave={this.handleMouseLeave}
                >
                  {link.label}
                </Link>
              )}
            </li>
          ))}
        </ul>
      </div>
    );
  }
}

export default LoginSelection; 