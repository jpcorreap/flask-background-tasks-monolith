import {
  AppBar,
  Button,
  Link as MaterialLink,
  Toolbar,
  Typography,
} from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const NavBar = () => {
  const { email, signout } = useAuth();
  const navigate = useNavigate();

  return (
    <AppBar
      position="static"
      color="default"
      elevation={0}
      sx={{ borderBottom: (theme) => `1px solid ${theme.palette.divider}` }}
    >
      <Toolbar sx={{ flexWrap: "wrap" }}>
        <Typography
          variant="h6"
          color="inherit"
          noWrap
          sx={{ flexGrow: 1, fontWeight: "bolder" }}
        >
          SuperVoices
        </Typography>
        {email ? (
          <p>{email}</p>
        ) : (
          <nav>
            <MaterialLink
              variant="button"
              color="text.primary"
              sx={{ my: 1, mx: 1.5 }}
            >
              <Link to="/login">Login</Link>
            </MaterialLink>
          </nav>
        )}
        {email ? (
          <>
            {" "}
            <Button
              variant="outlined"
              sx={{ my: 1, mx: 1.5 }}
              onClick={() => signout(() => navigate("/"))}
            >
              Sign out
            </Button>
            <Link to="/contests" style={{ textDecoration: "none" }}>
              <Button variant="contained" sx={{ my: 1, mx: 1.5 }}>
                View contests
              </Button>
            </Link>
          </>
        ) : (
          <Link to="/signup" style={{ textDecoration: "none" }}>
            <Button variant="contained" sx={{ my: 1, mx: 1.5 }}>
              Sign up
            </Button>
          </Link>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
