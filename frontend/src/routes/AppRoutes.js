import { Routes, Route } from "react-router-dom";
import * as Pages from "../pages";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Pages.Home />} />
      <Route path="/user" element={<Pages.User />} />
      <Route path="/login" element={<Pages.Login />} />
      <Route path="/home" element={<Pages.Dashboard />} />
      <Route path="/cadastro" element={<Pages.Cadastro />} />
      <Route path="/cadastro-clinica" element={<Pages.CadastroClinica />} />
      <Route path="/quero-ser-cliente" element={<Pages.QueroSerCliente />} />
      <Route
        path="/cadastro-veterinario"
        element={<Pages.CadastroVeterinario />}
      />

      <Route path="*" element={<Pages.NotFound />} />
    </Routes>
  );
}
