import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
// Ícones adaptados para o tema: KeyRound, User, Mail, Phone, Stethoscope, Hospital
import {
  KeyRound,
  User,
  Mail,
  Phone,
  Stethoscope,
  Hospital,
} from "lucide-react";
import Logo from "../../components/logo/Logo";
import InputIcon from "../../components/input/InputIcon"; // Seu componente customizado

import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

// ----------------------------------------------------
// DADOS DE EXEMPLO (Simulando o carregamento da API de Clínicas)
// ----------------------------------------------------
const mockClinicas = [
  { id: 1, nome: "Clínica Vet. Central - Dr. Cão" },
  { id: 2, nome: "Pet Care 24 Horas" },
  { id: 3, nome: "Hospital Veterinário São Francisco" },
  { id: 4, nome: "Consultório Animal Feliz" },
];

// ----------------------------------------------------
// FUNÇÃO DE CADASTRO (Substitua pela sua)
// ----------------------------------------------------
async function ApiCadastroVeterinario(data) {
  // Simulação da chamada API com novos dados
  console.log("Chamando API com:", data);

  // Simula resposta de sucesso
  // Mude o status para 400 para testar o erro
  const status = 201;

  return {
    status: status,
    json: async () => ({
      message: "Veterinário criado com sucesso!",
      action: status === 201 ? "Sucesso!" : "E-mail já cadastrado.",
    }),
  };

  // CÓDIGO REAL DA SUA API (Remova a simulação acima para usar este)
  /*
    const response = await fetch("http://localhost:5001/api/v1/veterinario", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return response;
    */
}

// ----------------------------------------------------
// COMPONENTE PRINCIPAL
// ----------------------------------------------------
export default function CadastroVeterinario() {
  const navigate = useNavigate();

  // NOVO ESTADO COM TODOS OS CAMPOS DE VETERINÁRIO
  const [form, setForm] = useState({
    nome: "",
    email: "",
    senha: "",
    confirmaSenha: "",
    telefone: "",
    crmv: "",
    id_clinica: "", // Campo para o SELECT
  });

  const [clinicas, setClinicas] = useState([]);
  const [loadingClinicas, setLoadingClinicas] = useState(true);
  const [error, setError] = useState("");

  // Carrega a lista de clínicas ao montar o componente
  useEffect(() => {
    setTimeout(() => {
      setClinicas(mockClinicas);
      setLoadingClinicas(false);
    }, 800);
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); // Limpa erro anterior

    if (form.senha !== form.confirmaSenha) {
      setError("As senhas não coincidem!");
      toast.error("Verifique a confirmação de senha.");
      return;
    }

    // Prepara os dados (remove a confirmação de senha antes de enviar)
    const { confirmaSenha, ...dataToSubmit } = form;

    const response = await ApiCadastroVeterinario(dataToSubmit); // Usa a nova API
    const responseBody = await response.json();

    if (response.status === 201) {
      toast.success("Veterinário criado com sucesso!");

      setTimeout(() => {
        navigate("/login", {});
      }, 1000);
    } else if (response.status >= 400 && response.status < 500) {
      setError(responseBody.message || "Erro no cadastro. Verifique os dados.");
      toast.error(responseBody.action || "Falha na requisição.");
      setForm((prev) => ({
        ...prev,
        confirmaSenha: "",
        senha: "",
      }));
    } else {
      setError("Erro no servidor. Tente novamente mais tarde.");
      toast.error(responseBody.action || "Erro interno.");
    }
  };

  return (
    (document.title = "Cadastro Veterinário | Petzzy"),
    (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4 sm:p-8">
        {/* O grid foi simplificado, pois o formulário agora é maior */}
        <div className="w-full max-w-4xl grid md:grid-cols-2 gap-8 items-center">
          {/* Coluna da Logo/Ilustração */}
          <div className="hidden md:flex items-center justify-center">
            <motion.div
              initial={{ opacity: 0, x: -150 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 1 }}
              className="text-center p-8"
            >
              <Logo size="xlarge" type="bg" className="mx-auto"></Logo>
              <h2 className="mt-6 text-xl font-bold text-blue-700">
                Seu cadastro é o primeiro passo para o cuidado animal.
              </h2>
              <p className="text-gray-500 mt-2">
                Preencha todos os campos, incluindo seu CRMV e a clínica de
                atuação.
              </p>
            </motion.div>
          </div>

          {/* Coluna do Formulário */}
          <motion.div
            initial={{ opacity: 0.5, x: 150 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 1 }}
            className="w-full"
          >
            <div className="bg-white shadow-2xl rounded-2xl p-6 sm:p-10">
              <h1 className="text-3xl font-extrabold text-center text-blue-700 mb-6">
                Cadastro de Veterinário
              </h1>

              <form onSubmit={handleSubmit} className="space-y-4">
                {error && (
                  <p className="text-red-500 font-medium text-sm mt-1 text-center bg-red-50 p-2 rounded-lg border border-red-200">
                    ⚠️ {error}
                  </p>
                )}

                {/* ----------------------- LINHA 1: NOME E EMAIL ----------------------- */}
                <div className="grid sm:grid-cols-2 gap-4">
                  {/* Nome */}
                  <InputBlock
                    label="Nome completo"
                    name="nome"
                    type="text"
                    form={form}
                    handleChange={handleChange}
                    icon={User}
                    placeholder="Seu nome profissional"
                  />
                  {/* E-mail */}
                  <InputBlock
                    label="E-mail"
                    name="email"
                    type="email"
                    form={form}
                    handleChange={handleChange}
                    icon={Mail}
                    placeholder="email@clinica.com"
                  />
                </div>

                {/* ----------------------- LINHA 2: SENHA E CONFIRMAÇÃO ----------------------- */}
                <div className="grid sm:grid-cols-2 gap-4">
                  {/* Senha */}
                  <InputBlock
                    label="Senha"
                    name="senha"
                    type="password"
                    form={form}
                    handleChange={handleChange}
                    icon={KeyRound}
                    placeholder="Mínimo 6 caracteres"
                  />
                  {/* Confirmar senha */}
                  <InputBlock
                    label="Confirmar Senha"
                    name="confirmaSenha"
                    type="password"
                    form={form}
                    handleChange={handleChange}
                    icon={KeyRound}
                    placeholder="Confirme a senha"
                  />
                </div>

                {/* ----------------------- LINHA 3: TELEFONE E CRMV ----------------------- */}
                <div className="grid sm:grid-cols-2 gap-4">
                  {/* Telefone */}
                  <InputBlock
                    label="Telefone"
                    name="telefone"
                    type="tel"
                    form={form}
                    handleChange={handleChange}
                    icon={Phone}
                    placeholder="(XX) XXXXX-XXXX"
                  />
                  {/* CRMV */}
                  <InputBlock
                    label="CRMV"
                    name="crmv"
                    type="text"
                    form={form}
                    handleChange={handleChange}
                    icon={Stethoscope}
                    placeholder="CRMV/UF 12345"
                    required={true}
                  />
                </div>

                {/* ----------------------- LINHA 4: CLÍNICA (SELECT) ----------------------- */}
                <div>
                  <label
                    htmlFor="id_clinica"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Clínica de Atuação
                  </label>
                  <div className="relative">
                    <select
                      id="id_clinica"
                      name="id_clinica"
                      value={form.id_clinica}
                      onChange={handleChange}
                      required
                      disabled={loadingClinicas}
                      className={`w-full appearance-none pr-10 pl-12 py-3 border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition cursor-pointer ${
                        loadingClinicas
                          ? "bg-gray-100 text-gray-500"
                          : "bg-white"
                      }`}
                    >
                      <option value="" disabled>
                        {loadingClinicas
                          ? "Carregando clínicas..."
                          : "Selecione a clínica..."}
                      </option>
                      {!loadingClinicas &&
                        clinicas.map((clinica) => (
                          <option key={clinica.id} value={clinica.id}>
                            {clinica.nome}
                          </option>
                        ))}
                    </select>
                    <Hospital className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none" />
                  </div>
                </div>

                {/* Botão */}
                <button
                  type="submit"
                  className="w-full bg-green-600 text-white font-bold py-3 rounded-lg hover:bg-green-700 transition shadow-lg mt-6"
                >
                  Cadastrar Veterinário
                </button>
              </form>

              {/* Link login */}
              <p className="text-center text-gray-600 text-sm mt-6">
                Já tem conta?{" "}
                <a
                  onClick={() => navigate("/login")}
                  className="text-blue-600 font-semibold cursor-pointer hover:underline hover:text-blue-800 transition"
                >
                  Fazer Login
                </a>
              </p>
            </div>
          </motion.div>
        </div>
        <ToastContainer position="top-right" autoClose={1500} />
      </div>
    )
  );
}

// Componente auxiliar para Input Block (melhora a legibilidade)
const InputBlock = ({
  label,
  name,
  type,
  form,
  handleChange,
  icon,
  placeholder,
  required = false,
}) => (
  <div>
    <label
      htmlFor={name}
      className="block text-sm font-medium text-gray-700 mb-1"
    >
      {label} {required && <span className="text-red-500">*</span>}
    </label>
    <InputIcon
      type={type}
      name={name}
      placeholder={placeholder}
      value={form[name]}
      onChange={handleChange}
      required={required}
      icon={icon}
    />
  </div>
);
