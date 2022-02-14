import './App.css';
import { Link, Route, Routes } from 'react-router-dom';
import AdminLayout from './layouts/AdminLayout';
import Contest from './pages/Contest';

function App() {
  return (
    <Routes>
      <Route path="/" element={<h1>Landing</h1>} />
      <Route path="/test1" element={<h1>Test 1</h1>} />
      <Route path="/test2" element={<h1>Test 2</h1>} />
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
  );
}

export default App;
