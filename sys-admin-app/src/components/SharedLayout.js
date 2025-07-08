import React, { useState } from 'react';
import OffcanvasSidebar from './OffcanvasSidebar';

const SharedLayout = ({ title, navItems, children, onLogout }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleMenuToggle = () => setSidebarOpen((open) => !open);

  return (
    <div className="shared-layout">
      <OffcanvasSidebar open={sidebarOpen} navItems={navItems} onClose={handleMenuToggle} onLogout={onLogout} />
      <header className="shared-header">
        <button onClick={handleMenuToggle} className="menu-btn">☰</button>
        <h1>{title}</h1>
        {onLogout && <button onClick={onLogout} className="logout-btn">Logout</button>}
      </header>
      <main className="shared-content">{children}</main>
    </div>
  );
};

export default SharedLayout; 