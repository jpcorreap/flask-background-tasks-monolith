import "./App.css";
import {
  Link,
  Route,
  Routes,
  useLocation,
  useNavigate,
} from "react-router-dom";
import AdminLayout from "./layouts/AdminLayout";
import Contest from "./pages/Contest";
import AuthProvider from "./components/AuthProvider";
import { useAuth } from "./hooks/useAuth";

function LoginPage() {
  let navigate = useNavigate();
  let location = useLocation();
  let auth = useAuth();

  let from = location.state?.from?.pathname || "/";

  function handleSubmit(event) {
    event.preventDefault();

    let formData = new FormData(event.currentTarget);
    let username = formData.get("username");

    auth.signin(username, () => {
      // Send them back to the page they tried to visit when they were
      // redirected to the login page. Use { replace: true } so we don't create
      // another entry in the history stack for the login page.  This means that
      // when they get to the protected page and click the back button, they
      // won't end up back on the login page, which is also really nice for the
      // user experience.
      navigate(from, { replace: true });
    });
  }

  return (
    <div>
      <p>You must log in to view the page at {from}</p>

      <form onSubmit={handleSubmit}>
        <label>
          Username: <input name="username" type="text" />
        </label>{" "}
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<h1>Landing</h1>} />
        <Route path="/test1" element={<h1>Test 1</h1>} />
        <Route path="/test2" element={<h1>Test 2</h1>} />
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
