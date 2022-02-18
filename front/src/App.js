import "./App.css";
import { Link, Route, Routes } from "react-router-dom";
import AdminLayout from "./layouts/AdminLayout";
import ContestPage from "./pages/ContestPage";
import SubmitPage from "./pages/SubmitPage";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import LandingPage from "./pages/LandingPage";
import ContestsPage from "./pages/ContestsPage";
import { useEffect } from "react";
import { useAuth } from "./hooks/useAuth";

function App() {
  const { validateLoggedAccount } = useAuth();

  useEffect(() => validateLoggedAccount(), [validateLoggedAccount]);

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/signup" element={<SignUpPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/contests/:contestId"
        element={
          <AdminLayout>
            <ContestPage />
          </AdminLayout>
        }
      />
      <Route
        path="/contests/:contestId/submit"
        element={
          <AdminLayout>
            <SubmitPage />
          </AdminLayout>
        }
      />
      {/* Route for contests CRUD requires to be signed in */}
      <Route
        path="/contests/"
        element={
          <AdminLayout>
            <ContestsPage />
          </AdminLayout>
        }
      />
      {/* Edit a contest also requires to be signed in */}
      <Route
        path="/contests/:contestId/edit"
        element={
          <AdminLayout>
            <p>Edit contest</p>
            <SubmitPage />
          </AdminLayout>
        }
      />
      {/* Generic fallback for unknown routes */}
      <Route
        path="*"
        element={
          <main style={{ padding: "1rem" }}>
            <h1>404 not found</h1>
            <Link to={"/"}>Go to home</Link>
          </main>
        }
      />
    </Routes>
  );
}

export default App;
