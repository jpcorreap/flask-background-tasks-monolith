import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { Chip, Grid, IconButton } from "@mui/material";
import { useAuth } from "../hooks/useAuth";
import { parseStringToDetailedDate } from "../utils/dateUtils";
import waveSpectrum from "../assets/img/audio_spectrum_line_animation.gif";
import HelpIcon from "@mui/icons-material/Help";
import { useUsersService } from "../services/useUsersService";
import { useState } from "react";

import { FETCH_URL } from "../config";

export default function VoiceCard({ submission }) {
  const { jwt } = useAuth();
  const { getUserInfo } = useUsersService();
  const [user, setUser] = useState();

  const handleClick = () => {
    getUserInfo(
      submission.user_id,
      (user) => setUser(user),
      (error) => {}
    );
  };

  return (
    <Card>
      <CardMedia
        component="img"
        height="140"
        width="auto"
        image={waveSpectrum}
        alt="wave"
      />

      {jwt ? (
        <>
          <p>Raw:</p>
          <audio
            controls
            src={`${FETCH_URL}/submissions/raw/${submission.id}`}
          ></audio>

          <p>Converted:</p>
          <audio
            controls
            src={`${FETCH_URL}/submissions/${submission.id}`}
            type="audio/mpeg"
          ></audio>
        </>
      ) : (
        <audio
          controls
          src={`${FETCH_URL}/submissions/${submission.id}`}
          type="audio/mpeg"
        ></audio>
      )}

      <CardContent>
        {jwt ? (
          submission.status === "converted" ? (
            <Chip label="Converted" color="secondary" />
          ) : (
            <Chip label="In progress" color="primary" />
          )
        ) : (
          <></>
        )}

        <Grid
          container
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          style={{ marginTop: 5 }}
        >
          <Grid item xs>
            <Typography gutterBottom variant="h5" component="span">
              Submitted by user {submission.user_id}
            </Typography>
          </Grid>
          <Grid item xs={2}>
            <IconButton aria-label="info" onClick={handleClick}>
              <HelpIcon />
            </IconButton>
          </Grid>
        </Grid>
        {user ? (
          <p style={{ margin: 0, padding: 0, marginBottom: 20 }}>
            <span
              style={{ fontWeight: "bolder" }}
            >{`${user.names} ${user.last_names}`}</span>{" "}
            <br />
            {`${user.email}`}
          </p>
        ) : (
          <></>
        )}
        <Typography gutterBottom variant="body" component="div">
          Uploaded at {parseStringToDetailedDate(submission.upload_date)}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          <span style={{ fontWeight: "bolder" }}>Observations: </span>
          {submission.observations}
        </Typography>
      </CardContent>
      {jwt ? (
        <CardActions>
          <Button size="small">Share</Button>
          <Button size="small">Learn More</Button>
        </CardActions>
      ) : (
        <></>
      )}
    </Card>
  );
}