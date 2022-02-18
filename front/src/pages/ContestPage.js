import { Grid, Typography } from "@mui/material";
import { Box } from "@mui/system";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import VoiceCard from "../components/VoiceCard";
import { useContestService } from "../services/useContestService";

export default function Contest() {
  const { contestId } = useParams();
  const { getContestDetail, getBanner } = useContestService();

  const [isContestDetailLoading, setIsContestDetailLoading] = useState(true);
  const [contest, setContest] = useState();

  const [isBannerLoading, setIsBannerLoading] = useState(true);
  const [banner, setBanner] = useState();

  const [error, setError] = useState();

  useEffect(() => {
    getContestDetail(
      contestId,
      (c) => {
        setContest(c);
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
        <Typography variant={"h3"}>
          <span style={{ fontWeight: "bolder" }}>Contest {contest.name}</span>
        </Typography>
      </Grid>
      <Grid style={{ padding: 10 }}>
        <Grid item>
          <Box sx={{ flexGrow: 1 }} style={{ marginTop: 20 }}>
            <Grid container spacing={2}>
              {contest.submissions.map((submission, id) => (
                <Grid container item xs={2}>
                  <VoiceCard submission={submission} />
                </Grid>
              ))}
            </Grid>
          </Box>
        </Grid>
      </Grid>
    </Grid>
  );
}
