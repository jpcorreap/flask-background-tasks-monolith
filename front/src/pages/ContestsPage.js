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
  Typography,
} from "@mui/material";
import ContestDetail from "../components/ContestDetail";
import { useContestsService } from "../services/useContestsService";
import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useContestService } from "../services/useContestService";
import useFetchRequest from "../hooks/useFetchRequest";

function ContestsPage() {
  const [hasLoggedIn, setHasLoggedIn] = useState(true);
  const [rows, setRows] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [modalDetailId, setModalDetailId] = useState();
  const { validateLoggedAccount } = useAuth();
  const { getContests } = useContestsService();
  const { deleteContest } = useContestService();
  const { get } = useFetchRequest();

  useEffect(() => {
    setIsLoading(true);
    getContests(
      (contests) => {
        setRows(contests);
        setIsLoading(false);
      },
      (error) => {
        setError(error);
        setIsLoading(false);
      }
    );
  }, []);
  useEffect(() => {
    if (validateLoggedAccount()) {
      getContests(
        (contests) => setRows(contests),
        (error) => setError(error)
      );
    } else {
      setHasLoggedIn(false);
    }
  }, [getContests, validateLoggedAccount]);

  const handleRefresh = () => {
    getContests(
      (contests) => setRows(contests),
      (error) => setError(error)
    );
  };

  const onClick = useCallback(
    (action, id) => {
      if (action === "delete") {
        deleteContest(
          id,
          () =>
            getContests(
              (contests) => setRows(contests),
              (error) => setError(error)
            ),
          () =>
            getContests(
              (contests) => setRows(contests),
              (error) => setError(error)
            )
        );
      } else {
        setModalDetailId(id);
        setShowModal(true);
      }
    },
    [deleteContest, handleRefresh]
  );

  const handleNewEvent = () => {
    setShowModal(true);
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
        field: "prize",
        headerName: "Contest Prize",
      },
      {
        field: "start_date",
        headerName: "Contest Start Date",
      },
      {
        field: "end_date",
        headerName: "Contest End Date",
      },
      {
        field: "actions",
        headerName: "Actions",
        onClick: onClick,
      },
    ],
    [onClick]
  );

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
                      <Tooltip title="Go to contest page">
                        <Link to={`/contests/${row.url}`}>
                          <IconButton>
                            <VisibilityIcon />
                          </IconButton>
                        </Link>
                      </Tooltip>
                      <Tooltip title="Edit contest">
                        <IconButton onClick={() => onClick("edit", row.url)}>
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Delete contest">
                        <IconButton onClick={() => onClick("delete", row.url)}>
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

  const tableContent = useMemo(() => {
    if (isLoading)
      return (
        <TableRow hover={true} role="checkbox" tabIndex={-1}>
          <TableCell colSpan={8}>
            <p>Loading...</p>
          </TableCell>
        </TableRow>
      );

    if (rows.length)
      return rows
        .slice(pagination[0], pagination[1])
        .map((row) => createRow(row));

    if (!isLoading && rows.length)
      return (
        <TableRow hover={true} role="checkbox" tabIndex={-1}>
          <TableCell colSpan={8}>
            <p>No data</p>
          </TableCell>
        </TableRow>
      );

    return <></>;
  }, [createRow, isLoading, pagination, rows]);

  if (!hasLoggedIn) {
    return <Navigate to="/login" state={{ from: "/contests" }} replace />;
  }

  return (
    <div>
      <div style={{ margin: 20 }}>
        <Typography variant={"h6"}>Contests</Typography>

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
                {tableContent}
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
              `Page ${page + 1}: displaying from ${from} to ${to} registers ${
                count !== -1 ? count : 0
              }`
            }
          />
        </Paper>
      </div>
      <ContestDetail
        contestUrl={modalDetailId}
        open={showModal}
        setOpen={setShowModal}
        refresh={handleRefresh}
      />
    </div>
  );
}

export default ContestsPage;
