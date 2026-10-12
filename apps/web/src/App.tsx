import { Link, Route, Routes } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Receipts from "./pages/Receipts";

export default function App() {
  return (
    <>
      <nav>
        <Link to="/">Dashboard</Link> | <Link to="/receipts">Receipts</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/receipts" element={<Receipts />} />
      </Routes>
    </>
  );
}
