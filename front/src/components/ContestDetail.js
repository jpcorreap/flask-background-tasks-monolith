import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Modal from "@mui/material/Modal";
import { Grid, TextField } from "@mui/material";
import { useContestService } from "../services/useContestService";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export default function ContestDetail({ open, setOpen, contestUrl }) {
  const { createContest, getContestDetail, updateContest } =
    useContestService();
  const [isLoading, setIsLoading] = React.useState(false);
  const [data, setData] = React.useState({
    name: "",
    url: "",
    prize: "",
    script: "",
    advices: "",
    start_date: "",
    end_date: "",
  });
  const [bannerImg, setBannerImg] = React.useState(null);

  const handleRefresh = React.useCallback(() => {
    getContestDetail(
      contestUrl,
      (d) => setData(d),
      () => {}
    );
  }, [contestUrl, getContestDetail]);

  React.useEffect(() => {
    if (contestUrl) {
      handleRefresh();
    }
  }, [contestUrl]);

  const onFileChange = (event) => {
    // Update the state
    console.info("AAAAAAAH", event.target.files[0]);
    setBannerImg(event.target.files[0]);
  };

  const handleChange = (e) => {
    setData({ ...data, [e.currentTarget.id]: e.currentTarget.value });
  };

  const handleSubmit = () => {
    // Create an object of formData
    const formData = new FormData();
    // Update the formData object
    formData.append("file", bannerImg, bannerImg.name);
    Object.keys(data).forEach((key) => {
      formData.append(key, data[key]);
    });
    // Details of the uploaded file
    // console.log(this.state.selectedFile);
    // console.table(formData);
    createContest(
      formData,
      () => {
        setOpen(false);
        handleRefresh();
        window.location.assign("/");
      },
      () => {}
    );
  };

  const handleClose = () => setOpen(false);

  const handleUpdate = () => {
    // Create an object of formData
    const formData = new FormData();
    // Update the formData object
    if (bannerImg) formData.append("file", bannerImg, bannerImg.name);

    Object.keys(data).forEach((key) => {
      console.info("Iterando ando", key, data[key]);
      if (data[key]) {
        formData.append(key, data[key]);
      }
    });

    updateContest(
      contestUrl,
      formData,
      () => {
        setOpen(false);
        handleRefresh();
        window.location.assign("/contests");
      },
      () => {
        setOpen(false);
        handleRefresh();
        window.location.assign("/contests");
      }
    );
  };

  return (
    <div>
      <Button onClick={() => window.location.assign("/contests")}>
        Refresh
      </Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style} style={{ width: 750, height: "90vh" }}>
          <Grid
            container
            direction="column"
            justifyContent="center"
            alignItems="center"
          >
            {isLoading ? (
              <p>Cargando...</p>
            ) : (
              [
                { id: "name", label: "Name" },
                { id: "url", label: "URL" },
                { id: "script", label: "Script" },
                { id: "prize", label: "Prize" },
                { id: "advices", label: "Advices" },
              ].map((val) => (
                <Grid
                  container
                  direction="row"
                  justifyContent="space-between"
                  alignItems="center"
                  style={{ marginBottom: 22 }}
                >
                  <p style={{ fontSize: 15, fontWeight: "bolder" }}>
                    {val.label}
                  </p>
                  <TextField
                    id={val.id}
                    label={val.label}
                    defaultValue={data[val.id]}
                    value={data[val.id]}
                    style={{ width: 500 }}
                    onChange={handleChange}
                    type={val.id === "prize" ? "number" : "text"}
                  />
                </Grid>
              ))
            )}
            {/* START DATE */}
            <Grid
              container
              direction="row"
              justifyContent="space-between"
              alignItems="center"
              style={{ marginBottom: 22 }}
            >
              <p style={{ fontSize: 15, fontWeight: "bolder" }}>Start date</p>
              <TextField
                type={"datetime-local"}
                id={"start_date"}
                style={{ width: 500 }}
                onChange={(event) => {
                  console.info(event);
                  handleChange(event);
                }}
                value={data["start_date"]}
              />
            </Grid>
            <Grid
              container
              direction="row"
              justifyContent="space-between"
              alignItems="center"
              style={{ marginBottom: 22 }}
            >
              <p style={{ fontSize: 15, fontWeight: "bolder" }}>End date</p>
              <TextField
                type={"datetime-local"}
                id={"end_date"}
                style={{ width: 500 }}
                onChange={handleChange}
                value={data["end_date"]}
              />
            </Grid>
            <Grid
              container
              direction="row"
              justifyContent="space-between"
              alignItems="center"
              style={{ marginBottom: 22 }}
            >
              <p style={{ fontSize: 15, fontWeight: "bolder" }}>Banner file</p>
              <TextField
                type={"file"}
                id={"file"}
                style={{ width: 500 }}
                onChange={onFileChange}
              />
            </Grid>
            {contestUrl ? (
              <Button variant="contained" onClick={() => handleUpdate()}>
                Update
              </Button>
            ) : (
              <Button variant="contained" onClick={() => handleSubmit()}>
                Submit
              </Button>
            )}
          </Grid>
        </Box>
      </Modal>
    </div>
  );
}
