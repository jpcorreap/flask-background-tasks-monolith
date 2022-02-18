import * as React from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { useAuth } from "../hooks/useAuth";
import { parseStringToDetailedDate } from "../utils/dateUtils";

export default function VoiceCard({ submission }) {
  const { jwt } = useAuth();

  return (
    <Card sx={{ maxWidth: 345 }}>
      <CardMedia
        component="img"
        height="140"
        image="https://previews.123rf.com/images/martialred/martialred1701/martialred170100048/70075273-sound-audio-wave-or-soundwave-line-art-vector-icon-for-music-apps-and-websites.jpg"
        alt="wave"
      />
      <audio
        controls
        src={`${process.env.REACT_APP_FETCH_URL}/submissions/${submission.id}`}
        type="audio/mpeg"
      ></audio>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          Submmited by user {submission.user_id}
        </Typography>
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
