import { Grid } from "@mui/material";
import { Box } from "@mui/system";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import VoiceCard from "../components/VoiceCard";
import { useContestService } from "../services/useContestService";

export default function Contest() {
  const { contestId } = useParams();
  const { getContestDetail, getBanner } = useContestService();

  const [isContestDetailLoading, setIsContestDetailLoading] = useState(true);
  const [contestDetail, setContestDetail] = useState();

  const [isBannerLoading, setIsBannerLoading] = useState(true);
  const [banner, setBanner] = useState();

  const [error, setError] = useState();

  useEffect(() => {
    getContestDetail(
      contestId,
      (c) => {
        setContestDetail(c);
        setIsContestDetailLoading(false);
      },
      (error) => {
        setError(error);
      }
    );
    getBanner(
      contestId,
      (bannerBlob) => {
        setBanner(URL.createObjectURL(bannerBlob));
        setIsBannerLoading(false);
      },
      (error) => {
        setError(error);
      }
    );
  }, []);

  if (isContestDetailLoading || isBannerLoading) {
    return <p>Loading...</p>;
  }

  return (
    <Grid>
      <Grid
        container
        direction="column"
        justifyContent="center"
        alignItems="center"
      >
        <img height={400} src={banner} alt={`Contest ${contestId}`} />
        <h2>Contest {contestId}</h2>
      </Grid>
      <Grid style={{ padding: 10 }}>
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
    </Grid>
  );
}
