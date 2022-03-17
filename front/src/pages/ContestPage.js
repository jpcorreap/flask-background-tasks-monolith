import { Button, Grid, Typography } from "@mui/material";
import { Box } from "@mui/system";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import VoiceCard from "../components/VoiceCard";
import { useContestService } from "../services/useContestService";
import { parseStringToDetailedDate } from "../utils/dateUtils";

export default function ContestPage() {
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
    <Grid container direction="row">
      <Grid
        container
        direction="column"
        justifyContent="center"
        alignItems="center"
        xs={12}
        md={3}
        style={{
          backgroundColor: "#41464a",
          padding: 20,
          minHeight: "100vh",
        }}
      >
        <img width={"100%"} src={banner} alt={`Contest ${contestId}`} />
        <p
          style={{
            textAlign: "center",
            fontSize: "2em",
            padding: 0,
            margin: 0,
          }}
        >
          <span style={{ fontWeight: "bolder", color: "white" }}>
            Contest {contest.name}
          </span>
        </p>

        <Grid
          container
          direction="row"
          justifyContent="flex-start"
          alignItems="flex-start"
          style={{ padding: 10 }}
        >
          <p style={{ fontSize: "1.2em", color: "white" }}>
            <span style={{ fontWeight: "bolder" }}>Prize: </span>{" "}
            {contest.prize} USD
            <br />
            <span style={{ fontWeight: "bolder" }}> Start date: </span>{" "}
            {parseStringToDetailedDate(contest.start_date)}
            <br />
            <span style={{ fontWeight: "bolder" }}>End date: </span>{" "}
            {parseStringToDetailedDate(contest.end_date)}
            <br />
            <span style={{ fontWeight: "bolder" }}>Advices: </span>{" "}
            {contest.advices}
            <br />
            <span style={{ fontWeight: "bolder" }}>Script: </span>{" "}
            {contest.script}
          </p>
        </Grid>
        {contest.prize ? (
          <Link to={`submit`} style={{ textDecoration: "none" }}>
            <Button variant="contained" color={"secondary"}>
              Submit your voice!
            </Button>
          </Link>
        ) : (
          <p style={{ color: "white" }}>This contest does not exist</p>
        )}
      </Grid>
      <Grid style={{ padding: 10 }} container xs={12} md={9}>
        <Box sx={{ flexGrow: 1 }}>
          <Grid container spacing={2}>
            {contest.submissions?.map((submission, id) => (
              <Grid container item xs={4}>
                <VoiceCard submission={submission} />
              </Grid>
            ))}
          </Grid>
        </Box>
      </Grid>
    </Grid>
  );
}
