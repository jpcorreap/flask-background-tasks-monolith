import React, { useCallback, useEffect, useMemo, useState } from "react";
import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import AddCircleIcon from "@mui/icons-material/AddCircle";
import {
  Button,
  Grid,
  IconButton,
  LinearProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  Tooltip,
} from "@mui/material";
import ContestDetail from "../components/ContestDetail";

function ContestsPage() {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const fetchRequests = {
    get: () => {},
    delete: () => {},
  };
  const [rows, setRows] = useState([
    {
      id: 1,
      url: "https:alguna_cosa",
      name: "Mi Concurso",
      image: "ruta imagen",
    },
  ]);

  const [isLoading, setIsLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [modalMode, setModalMode] = useState("read_only");
  const [modalDetailId, setModalDetailId] = useState();

  const handleRefresh = useCallback(() => {
    setIsLoading(true);
  }, []);

  const deleteEvent = useCallback((event_id) => {}, []);

  const onClick = useCallback(
    (action, id) => {
      if (action === "delete") deleteEvent(id);
      else if (action === "read_only") {
        setModalDetailId(id);
        setShowModal(true);
        setModalMode("read_only");
      } else {
        setModalDetailId(id);
        setModalMode("edit");
        setShowModal(true);
      }
    },
    [deleteEvent]
  );

  const handleNewEvent = () => {
    setShowModal(true);
    setModalMode("new_event");
  };

  const [currentPage, setCurrentPage] = useState(0);
  const [pagination, setPagination] = useState([0, 7]);
  const columns = useMemo(
    () => [
      {
        field: "id",
        headerName: "Contest ID",
      },
      {
        field: "url",
        headerName: "Contest URL",
      },
      {
        field: "name",
        headerName: "Contest Name",
      },
      {
        field: "image",
        headerName: "Contest Image",
      },
      {
        field: "actions",
        headerName: "Actions",
        onClick: onClick,
      },
    ],
    [onClick]
  );

  useEffect(() => {
    setIsLoading(true);
  }, [fetchRequests]);

  const handleChangePage = (event, newPage) => {
    setPagination([newPage * 7, (newPage + 1) * 7]);
    setCurrentPage(newPage);
  };

  const createRow = useCallback(
    (row) => {
      return (
        <TableRow hover={true} role="checkbox" tabIndex={-1} key={row.code}>
          {columns.map((column) => {
            const value = row[column.field];

            return (
              <TableCell>
                <Grid
                  container
                  direction="row"
                  justifyContent="space-between"
                  alignItems="center"
                >
                  {column.onClick ? (
                    <>
                      <Tooltip title="Ver evento">
                        <IconButton
                          onClick={() => onClick("read_only", row.id)}
                        >
                          <VisibilityIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Editar evento">
                        <IconButton onClick={() => onClick("edit", row.id)}>
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Eliminar evento">
                        <IconButton onClick={() => onClick("delete", row.id)}>
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </>
                  ) : (
                    <p>
                      {column.valueParser ? column.valueParser(value) : value}
                    </p>
                  )}
                </Grid>
              </TableCell>
            );
          })}
        </TableRow>
      );
    },
    [columns, onClick]
  );

  return (
    <div>
      <div style={{ margin: 20 }}>
        <Paper
          style={{
            width: "100%",
          }}
        >
          <div style={{ height: "5px" }}>
            {isLoading ? <LinearProgress /> : <></>}
          </div>
          <TableContainer
            style={{
              width: "100%",
              minHeight: 465,
              "& > * + *": {
                marginTop: 20,
              },
            }}
          >
            <Table stickyHeader aria-label="sticky table" size="small">
              <colgroup>
                {columns.map((column, i) => (
                  <col key={"colWidth_" + i} width={400} />
                ))}
              </colgroup>
              <TableHead>
                <TableRow>
                  {columns.map((column) => (
                    <TableCell key={column.id}>{column.headerName}</TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {!isLoading ? (
                  rows.length ? (
                    rows
                      .slice(pagination[0], pagination[1])
                      .map((row) => createRow(row))
                  ) : (
                    <TableRow hover={true} role="checkbox" tabIndex={-1}>
                      <TableCell colSpan={8}>
                        <p>No se encontraron resultados</p>
                      </TableCell>
                    </TableRow>
                  )
                ) : (
                  <TableRow hover={true} role="checkbox" tabIndex={-1}>
                    <TableCell colSpan={8}>
                      <p>Cargando...</p>
                    </TableCell>
                  </TableRow>
                )}
                {/*error && (
              <TableRow hover={true} role="checkbox" tabIndex={-1}>
                <TableCell colSpan={5}>
                  <p>{error}</p>
                </TableCell>
              </TableRow>
            )*/}
              </TableBody>
            </Table>
          </TableContainer>
          <Button
            variant="outlined"
            fullWidth
            startIcon={<AddCircleIcon />}
            onClick={handleNewEvent}
          >
            Create a new contest
          </Button>
          <TablePagination
            rowsPerPageOptions={[]}
            component={"div"}
            count={rows?.length}
            rowsPerPage={7}
            backIconButtonText={"Anterior"}
            nextIconButtonText={"Siguiente"}
            page={currentPage}
            onPageChange={handleChangePage}
            labelDisplayedRows={({ from, to, count, page }) =>
              `Página ${
                page + 1
              }: mostrando de ${from} a ${to} registros de un total de ${
                count !== -1 ? count : 0
              }`
            }
          />
        </Paper>
      </div>
      <ContestDetail
        mode={modalMode}
        event_id={modalDetailId}
        open={showModal}
        setOpen={setShowModal}
        refresh={handleRefresh}
      />
    </div>
  );
}

export default ContestsPage;
