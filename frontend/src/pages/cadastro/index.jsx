import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { KeyRound, User, Mail } from "lucide-react";
import Logo from "../../components/logo/Logo";
import InputIcon from "../../components/input/InputIcon";

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function Cadastro() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    nome: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Login com:", form);
    try {
      await fakeApiLogin();
      toast.success("Cadastro realizado com sucesso!");
      setTimeout(() => {
        navigate("/login", {});
      }, 1000);
    } catch {
      setError("Verifique as credenciais digitadas!");
      setForm({
        nome: form.nome,
        email: form.email,
        confirmPassword: "",
        password: "",
      });
      toast.error("Informações inválidas!");
    }
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  function fakeApiLogin() {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        Math.random() > 0.5 ? resolve() : reject();
      }, 1000);
    });
  }

  return (
    (document.title = "Cadastre-se | Petzzy"),
    (
      <div className="h-screen grid md:grid-cols-2 md:grid-rows-1 items-center justify-items-center bg-gradient-to-br from-blue-100 to-blue-200 p-8">
        {/* Logo */}
        <div className="flex items-center justify-center m-3 md:m-7">
          <motion.div
            initial={{ opacity: 0, x: -150 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 1 }}
            className="w-full max-w-md"
          >
            <Logo size="xlarge" type="bg" className="w-15 h-15"></Logo>
          </motion.div>
        </div>

        {/* Formulário */}
        <motion.div
          initial={{ opacity: 0.5, x: 150 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 1 }}
          className="w-full max-w-md m-3 md:m-7"
        >
          <div className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-md">
            <h1 className="text-3xl font-bold text-center text-blue-700 mb-6">
              Criar Conta
            </h1>

            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <p className="text-red-500 font-medium text-sm mt-1 text-center">
                  {error}
                </p>
              )}
              {/* Nome */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nome completo
                </label>
                <InputIcon
                  type="text"
                  name="nome"
                  placeholder="Digite seu nome"
                  value={form.nome}
                  onChange={handleChange}
                  required
                  icon={User}
                />
              </div>

              {/* E-mail */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  E-mail
                </label>
                <InputIcon
                  type="email"
                  name="email"
                  placeholder="Digite seu e-mail"
                  value={form.email}
                  onChange={handleChange}
                  required
                  icon={Mail}
                />
              </div>

              {/* Senha */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Senha
                </label>
                <InputIcon
                  type="password"
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  required
                  icon={KeyRound}
                  placeholder="Digite sua senha"
                />
              </div>

              {/* Confirmar senha */}

              <InputIcon
                type="password"
                name="confirmPassword"
                value={form.confirmPassword}
                onChange={handleChange}
                required
                icon={KeyRound}
                placeholder="Confirme a senha"
              />

              {/* Botão */}
              <button
                type="submit"
                className="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-petzzy-blue2 transition"
              >
                Cadastrar
              </button>
            </form>

            {/* Link login */}
            <p className="text-center text-gray-600 text-sm mt-6">
              Já tem conta?{" "}
              <a
                href="/login"
                className="text-blue-600 font-semibold hover:underline hover:text-petzzy-blue2"
              >
                Entrar
              </a>
            </p>
          </div>
        </motion.div>
        <ToastContainer position="top-right" autoClose={1500} />
      </div>
    )
  );
}
