import { Outlet, Link } from "react-router-dom";

export default function AdminLayout() {
  // TODO: protéger si pas loggé (JWT) → sinon redirect login
  return (
    <div style={{ maxWidth: 1100, margin: "2rem auto" }}>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h2>Admin ATS</h2>
        <nav style={{ display: "flex", gap: 12 }}>
          <Link to="/admin">Jobs</Link>
          <Link to="/admin/jobs/new">Créer un job</Link>
        </nav>
      </header>
      <hr />
      <Outlet />
    </div>
  );
}
