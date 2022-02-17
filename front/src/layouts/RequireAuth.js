import { Grid } from "@mui/material";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function RequireAuth({ children }) {
  let { jwt } = useAuth();
  let location = useLocation();

  if (!jwt) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return (
    <Grid>
      <h1>This is a protected route!</h1>
      <p>{jwt}</p>
      {children}
    </Grid>
  );
}
