import * as React from "react";
import { Link, useLocation, Navigate, Outlet } from "react-router-dom";
import AuthStatus from "../components/AuthStatus";
import { useAuth } from "../hooks/useAuth";

export default function AdminLayout({ children }) {
  return (
    <RequireAuth>
      <h1>Ruta protegida</h1>
      <AuthStatus />

      <ul>
        <li>
          <Link to="/">Public Page</Link>
        </li>
        <li>
          <Link to="/protected">Protected Page</Link>
        </li>
      </ul>
      {children}

      <Outlet />
    </RequireAuth>
  );
}

function RequireAuth({ children }) {
  let auth = useAuth();
  let location = useLocation();

  if (!auth.user) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
