import { useEffect, useState } from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { Link, useNavigate } from "react-router-dom";
import Copyright from "../components/Copyright";
import { useAuth } from "../hooks/useAuth";
import { Alert } from "@mui/material";

export default function SignUpPage() {
  const { signup, validateLoggedAccount } = useAuth();
  const navigate = useNavigate();

  useEffect(() => validateLoggedAccount(), []);

  const [data, setData] = useState({
    names: "",
    last_names: "",
    email: "",
    company_name: "",
    password: "",
    confirm_password: "",
  });
  const [error, setError] = useState(false);
  const [displaySuccess, setDisplaySuccess] = useState(false);

  const handleSubmit = (event) => {
    setError(undefined);
    setDisplaySuccess(false);
    event.preventDefault();
    // eslint-disable-next-line no-console
    console.info("CONECTANDO AL ENDPOINT");
    console.table(data);
    signup(
      data,
      () => {
        setDisplaySuccess(true);
        setInterval(() => {
          window.location.assign("/");
        }, 5000);
      },
      (error) => setError(error)
    );
  };

  const handleChange = (event) => {
    setData((prevValue) => ({
      ...prevValue,
      [event.target.name]: event.target.value,
    }));
  };

  /* if (jwt) {
    return <Navigate to="/" /*state={{ from: location }} replace />;
  } */

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign up
        </Typography>
        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                autoComplete="given-name"
                name="names"
                value={data.names}
                required
                fullWidth
                id="names"
                label="Name(s)"
                onChange={handleChange}
                autoFocus
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                fullWidth
                id="last_names"
                value={data.last_names}
                label="Last name(s)"
                name="last_names"
                onChange={handleChange}
                autoComplete="family-name"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                id="email"
                value={data.email}
                label="Email address"
                name="email"
                onChange={handleChange}
                autoComplete="email"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                id="companyName"
                value={data.company_name}
                label="Company name"
                name="company_name"
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                value={data.password}
                onChange={handleChange}
                autoComplete="new-password"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                name="confirm_password"
                label="Confirm password"
                value={data.confirm_password}
                type="password"
                onChange={handleChange}
                id="confirm_password"
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={displaySuccess}
            sx={{ mt: 3, mb: 2 }}
          >
            Sign Up
          </Button>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link to="/login">Already have an account? Sign in</Link>
            </Grid>
          </Grid>
        </Box>
        <div style={{ height: "30px" }}></div>
        {error ? (
          <Alert severity="error">
            Error creating the account, please try with new credentials
          </Alert>
        ) : (
          <></>
        )}
        {displaySuccess ? (
          <Alert severity="success">
            Account created successfully! Sign in automatically 5 seconds...
          </Alert>
        ) : (
          <></>
        )}
      </Box>
      <Copyright sx={{ mt: 5 }} />
    </Container>
  );
}
