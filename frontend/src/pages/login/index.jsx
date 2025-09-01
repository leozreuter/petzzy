import { useState } from "react";
import { motion } from "framer-motion";

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import Logo from "../../components/logo/Logo";
import InputIcon from "../../components/input/InputIcon";

import { KeyRound, Mail } from "lucide-react";

export default function LoginPage() {
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
    (document.title = "Faça Login | Petzzy</title>"),
    (
      <div className="min-h-screen flex items-center flex-col justify-center bg-gradient-to-br from-blue-100 to-blue-200 p-4">
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
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  E-mail
                </label>
                <InputIcon
                  type="email"
                  name="email"
                  placeholder="email@exemplo.com"
                  value={form.email}
                  onChange={handleChange}
                  required
                  icon={Mail}
                  error={error}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Senha
                </label>
                <InputIcon
                  type="password"
                  name="password"
                  placeholder="********"
                  value={form.password}
                  onChange={handleChange}
                  required
                  icon={KeyRound}
                  error={error}
                />
              </div>

              <button
                type="submit"
                className="w-full rounded-xl bg-blue-600 hover:bg-petzzy-blue2 text-white font-medium py-2 transition"
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
                className="text-center text-blue-600 hover:underline hover:text-petzzy-blue2 font-medium"
              >
                Esqueceu a senha?
              </a>
            </div>
          </div>
          <div className="text-center mt-4 text-sm text-gray-500">
            Novo na Petzzy?{" "}
            <a
              href="/cadastro"
              className="text-blue-600 hover:underline hover:text-petzzy-blue2 font-medium"
            >
              Cadastre-se
            </a>
          </div>
          <ToastContainer position="top-right" autoClose={1500} />
        </motion.div>
        <br></br>
      </div>
    )
  );
}
