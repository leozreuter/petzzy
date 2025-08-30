import { Routes, Route } from "react-router-dom";
import * as Pages from "../pages";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Pages.Home />} />
      <Route path="/user" element={<Pages.User />} />
      <Route path="/login" element={<Pages.Login />} />

      <Route path="*" element={<h2>Página não encontrada</h2>} />
    </Routes>
  );
}
