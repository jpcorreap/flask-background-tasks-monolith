import { Grid } from "@mui/material";
import * as React from "react";
import NavBar from "../components/NavBar";

export default function AdminLayout({ children }) {
  return (
    <Grid>
      <NavBar />
      {children}
    </Grid>
  );
}
