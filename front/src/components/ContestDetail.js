import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import { Grid, TextField } from "@mui/material";
import useFetchRequest from "../hooks/useFetchRequest";

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

export default function ContestDetail({
  open,
  setOpen,
  token,
  refresh,
  handleLogout,
  event_id,
  mode,
}) {
  const handleClose = () => setOpen(false);
  const [isLoading, setIsLoading] = React.useState(false);
  const [state, setState] = React.useState({
    name: "",
    category: "",
    place: "",
    address: "",
    start: "",
    end: "",
    modality: "",
  });

  const fetchRequest = useFetchRequest();

  const handleChange = (e) => {
    setState({ ...state, [e.currentTarget.id]: e.currentTarget.value });
  };

  React.useEffect(() => {
    if (event_id) {
      setIsLoading(true);
      fetchRequest
        .get("/events/" + event_id, token)
        .then((res) => res.json())
        .then((data) => {
          console.info("Entróó", data);
          setState({
            name: data.name,
            category: data.category,
            place: data.place,
            address: data.address,
            start: data.start,
            end: data.end,
            modality: data.modality,
          });
          setIsLoading(false);
        });
    }
  }, [event_id, fetchRequest, token]);

  const handleSubmit = () => {
    if (mode === "edit") {
      if (event_id) {
        if (!/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.test(state.start)) {
          alert("Fecha de inicio inválida, siga el formato DD/MM/AAAA");
        } else {
          if (!/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.test(state.end)) {
            alert("Fecha de inicio inválida, siga el formato DD/MM/AAAA");
          } else {
            fetchRequest
              .put("/events/" + event_id, state, token)
              .then((res) => {
                if (res.status === 400) {
                  res.text().then((mes) => alert(mes));
                } else if (res.status === 401) {
                  handleLogout();
                } else {
                  handleClose();
                  refresh();
                }
              })
              .catch((e) => alert(e));
          }
        }
      }
    } else if (mode === "new_event") {
      fetchRequest
        .post("/events", state, token)
        .then((res) => {
          if (res.status === 400) {
            res.text().then((mes) => alert(mes));
          } else if (res.status === 401) {
            handleLogout();
          } else {
            handleClose();
            refresh();
          }
        })
        .catch((e) => alert(e));
    }
  };

  return (
    <div>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style} style={{ width: 750, height: 570 }}>
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
                { id: "name", label: "Nombre" },
                { id: "category", label: "Categoría" },
                { id: "place", label: "Lugar" },
                { id: "address", label: "Dirección" },
                { id: "start", label: "Fecha inicio (DD/MM/AAAA)" },
                { id: "end", label: "Fecha fin (DD/MM/AAAA)" },
                { id: "modality", label: "Modalidad" },
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
                    defaultValue={state[val.id]}
                    value={state[val.id]}
                    style={{ width: 500 }}
                    onChange={handleChange}
                    disabled={mode === "read_only"}
                  />
                </Grid>
              ))
            )}
            <Button
              variant="contained"
              onClick={mode === "read_only" ? handleClose : handleSubmit}
            >
              {mode === "read_only" ? "Regresar" : "Guardar"}
            </Button>
          </Grid>
        </Box>
      </Modal>
    </div>
  );
}
