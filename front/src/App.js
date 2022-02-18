import "./App.css";
import { Link, Route, Routes } from "react-router-dom";
import AdminLayout from "./layouts/AdminLayout";
import Contest from "./pages/ContestPage";
import { AuthProvider } from "./components/AuthProvider";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import LandingPage from "./pages/LandingPage";
import RequireAuth from "./layouts/RequireAuth";
import ContestsPage from "./pages/ContestsPage";

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/contests/:contestId"
          element={
            <AdminLayout>
              <Contest />
            </AdminLayout>
          }
        />
        <Route
          path="/contests/:contestId/submit"
          element={
            <AdminLayout>
              <p>Submit contest</p>
              <Contest />
            </AdminLayout>
          }
        />
        {/* Route for contests CRUD requires to be signed in */}
        <Route
          path="/contests/"
          element={
            <RequireAuth>
              <AdminLayout>
                <ContestsPage />
              </AdminLayout>
            </RequireAuth>
          }
        />
        {/* Edit a contest also requires to be signed in */}
        <Route
          path="/contests/:contestId/edit"
          element={
            <RequireAuth>
              <AdminLayout>
                <p>Edit contest</p>
                <Contest />
              </AdminLayout>
            </RequireAuth>
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
    </AuthProvider>
  );
}

export default App;
