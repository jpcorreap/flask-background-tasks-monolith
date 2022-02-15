import "./App.css";
import { Link, Route, Routes } from "react-router-dom";
import AdminLayout from "./layouts/AdminLayout";
import Contest from "./pages/ContestPage";
import { AuthProvider } from "./components/AuthProvider";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import LandingPage from "./pages/LandingPage";

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/test1" element={<h1>Test 1</h1>} />
        <Route path="/test2" element={<h1>Test 2</h1>} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/protected"
          element={
            <AdminLayout>
              <h3>Protected</h3>
            </AdminLayout>
          }
        />
        <Route
          path="/contest/:contestId"
          element={
            <AdminLayout>
              <Contest />
            </AdminLayout>
          }
        />
        <Route
          path="*"
          element={
            <main style={{ padding: "1rem" }}>
              <p>404 not found</p>
              <Link to={"/"}>Go to home</Link>
            </main>
          }
        />
      </Routes>
    </AuthProvider>
  );
}

export default App;
