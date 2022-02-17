import { Grid } from "@mui/material";
import { Box } from "@mui/system";
import { useParams } from "react-router-dom";
import VoiceCard from "../components/VoiceCard";

export default function Contest() {
  let params = useParams();

  return (
    <Grid style={{ padding: 10 }}>
      <h2>Contest {params.contestId}</h2>
      <Grid item>
        <Box sx={{ flexGrow: 1 }} style={{ marginTop: 20 }}>
          <Grid container spacing={2}>
            {[
              {
                id: 1,
                name: "Voice 1",
                image: "ruta imagen",
              },
              {
                id: 2,
                name: "Voice 2",
                image: "ruta imagen",
              },
              {
                id: 3,
                name: "Voice 3",
                image: "ruta imagen",
              },
              {
                id: 4,
                name: "Voice 4",
                image: "ruta imagen",
              },
              {
                id: 5,
                name: "Voice 5",
                image: "ruta imagen",
              },
              {
                id: 6,
                name: "Voice 6",
                image: "ruta imagen",
              },
            ].map((voice, id) => (
              <Grid container item xs={2}>
                <VoiceCard name={voice.name} />
              </Grid>
            ))}
          </Grid>
        </Box>
      </Grid>
    </Grid>
  );
}
