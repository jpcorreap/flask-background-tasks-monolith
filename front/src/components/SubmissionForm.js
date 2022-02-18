import { useState } from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import PublishIcon from "@mui/icons-material/Publish";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Copyright from "../components/Copyright";
import { useAuth } from "../hooks/useAuth";
import { Alert } from "@mui/material";
import { useSubmissionForm } from "../services/useSubmissionForm";
import { useParams } from "react-router-dom";

export default function SubmissionForm() {
  const { signup } = useAuth();
  const { contestId } = useParams();
  const [audioFile, setAudioFile] = useState(null);
  const onFileChange = (event) => {
    // Update the state
    console.info("AAAAAAAH", event.target.files[0]);
    setAudioFile(event.target.files[0]);
  };

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
  const { createSubmission } = useSubmissionForm();

  const handleSubmit = (event) => {
    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    formData.append("file", audioFile, audioFile.name);

    Object.keys(data).forEach((key) => {
      formData.append(key, data[key]);
    });

    event.preventDefault();

    createSubmission(
      contestId,
      formData,
      () => {
        setDisplaySuccess(true);
      },
      () => {}
    );
  };

  const handleChange = (event) => {
    setData((prevValue) => ({
      ...prevValue,
      [event.target.name]: event.target.value,
    }));
  };

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
          <PublishIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Submit your voice!
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
                id="observations"
                value={data.observations}
                label="Observations"
                name="observations"
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                name="file"
                type="file"
                id="file"
                onChange={onFileChange}
              />
            </Grid>
          </Grid>
          <Button
            fullWidth
            variant="contained"
            // disabled={displaySuccess}
            sx={{ mt: 3, mb: 2 }}
            onClick={handleSubmit}
          >
            Submit voice
          </Button>
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
            We have received your voice and we are processing it so that it can
            be published in the page and can then be reviewed by our team. As
            soon as the voice is published on the contest page, we will notify
            you by email
          </Alert>
        ) : (
          <></>
        )}
      </Box>
      <Copyright sx={{ mt: 5 }} />
    </Container>
  );
}
