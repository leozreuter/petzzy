import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import Logo from "../../components/logo/Logo";

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Login com:", form);
    try {
      await fakeApiLogin();
      toast.success("Login realizado com sucesso!");
    } catch {
      setError("Verifique as credenciais digitadas!");
      setForm({ password: "" });
      toast.error("Usuário ou senha inválidos!");
    }
  };

  function fakeApiLogin() {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        Math.random() > 0.5 ? resolve() : reject();
      }, 1000);
    });
  }

  return (
    <div className="min-h-screen flex items-center flex-col justify-center bg-gradient-to-br from-blue-50 to-blue-100 p-4">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-md"
      >
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <div className="flex flex-col items-center mb-6">
            <Logo size="xlarge" className="w-15 h-15" />
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                E-mail
              </label>
              <input
                type="email"
                name="email"
                placeholder="seuemail@exemplo.com"
                value={form.email}
                onChange={handleChange}
                required
                className={`mt-1 w-full rounded-lg shadow-sm focus:outline-none ring-1 ring-petzzy-blue focus:ring-2 focus:ring-offset-1 p-2 ${
                  error
                    ? "border-red-500 focus:border-red-500 focus:ring-red-600 bg-red-200"
                    : "border-gray-300 focus:border-petzzy-blue focus:ring-petzzy-blue2"
                }`}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Senha
              </label>
              <input
                type="password"
                name="password"
                placeholder="********"
                value={form.password}
                onChange={handleChange}
                required
                className={`mt-1 w-full rounded-lg shadow-sm focus:outline-none ring-1 ring-petzzy-blue focus:ring-2 focus:ring-offset-1 p-2 
                ${
                  error
                    ? "border-red-500 focus:border-red-500 focus:ring-red-600 bg-red-200"
                    : "border-gray-300 focus:border-petzzy-blue focus:ring-petzzy-blue2"
                }`}
              />
            </div>

            <button
              type="submit"
              className="w-full rounded-xl bg-petzzy-blue hover:bg-petzzy-blue2 text-white font-medium py-2 transition"
            >
              Entrar
            </button>
            {error && (
              <p className="text-red-500 font-medium text-sm mt-1 text-center">
                {error}
              </p>
            )}
          </form>
          <div className="text-center mt-4 text-sm ">
            <a
              href="/recuperar-senha"
              className="text-center text-petzzy-blue hover:underline hover:text-petzzy-blue2 font-medium"
            >
              Esqueceu a senha?
            </a>
          </div>
        </div>
        <div className="text-center mt-4 text-sm text-gray-500">
          Novo na Petzzy?{" "}
          <a
            href="/cadastro"
            className="text-petzzy-blue hover:underline hover:text-petzzy-blue2 font-medium"
          >
            Cadastre-se
          </a>
        </div>
        <ToastContainer position="top-right" autoClose={1500} />
      </motion.div>
      <br></br>
    </div>
  );
}
