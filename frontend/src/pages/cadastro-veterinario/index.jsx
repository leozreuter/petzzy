import React, { useState, useEffect } from "react";
// Importação simulada de ícones Lucide
import {
  Mail,
  User,
  Lock,
  Phone,
  Stethoscope,
  Layers,
  Hospital,
  ArrowRight,
} from "lucide-react";

async function fetchApi(key, data, type) {
  if (!key) {
    return [];
  }
  const response = await fetch(process.env.REACT_APP_BACKEND_SERVER + key, {
    method: type || "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
    },
    body: JSON.stringify(data),
  });
  const responseBody = await response.json();
  return Array.isArray(responseBody) ? responseBody : [];
}

// Componente Input Customizado (Definido fora de App para reuso e limpeza)
const InputField = ({
  icon: Icon,
  id,
  label,
  type = "text",
  name,
  value,
  onChange,
  placeholder,
  error,
  maxLength = 256,
  className = "",
  isRequired = true,
  options = [],
}) => (
  <div className={`space-y-1 ${className}`}>
    <label
      htmlFor={id}
      className="text-sm font-medium text-gray-700 block select-none"
    >
      {label} {isRequired && <span className="text-red-500">*</span>}
    </label>
    <div
      className={`flex items-center rounded-lg border transition-all duration-200 ${
        error
          ? "border-red-500 ring-2 ring-red-500"
          : "border-gray-300 focus-within:border-indigo-500 focus-within:ring-1 focus-within:ring-indigo-500"
      } bg-white shadow-sm`}
    >
      <div className="p-3 text-gray-400">
        <Icon size={20} />
      </div>
      {type === "select" ? (
        <select
          id={id}
          name={name}
          value={value}
          onChange={onChange}
          required={isRequired}
          className="w-full px-2 py-3 bg-transparent text-gray-800 focus:outline-none appearance-none cursor-pointer"
        >
          {/* Mapeia as opções passadas via prop (options) */}
          {options.map((option) => (
            <option
              key={option.value || "loading"}
              value={option.value}
              disabled={option.disabled} // Adicionado suporte para desabilitar opções
            >
              {option.label}
            </option>
          ))}
        </select>
      ) : (
        <input
          id={id}
          type={type}
          name={name}
          value={value}
          maxLength={maxLength}
          onChange={onChange}
          placeholder={placeholder}
          required={isRequired}
          className="w-full px-2 py-3 bg-transparent text-gray-800 placeholder-gray-400 focus:outline-none"
        />
      )}
    </div>
    {error && <p className="mt-1 text-xs text-red-600 font-medium">{error}</p>}
  </div>
);

/**
 * Componente de Formulário de Cadastro para Profissionais Veterinários (CRMV).
 * Utiliza Tailwind CSS para um design responsivo e moderno.
 */
const CadastroVeterinario = () => {
  // Estado para dados dinâmicos da clínica
  const [clinics, setClinics] = useState([]);
  const [isLoadingClinics, setIsLoadingClinics] = useState(true);
  const [clinicError, setClinicError] = useState(null);

  // Estado para armazenar os dados do formulário
  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    senha: "",
    confirmSenha: "",
    telefone: "",
    crmv: "",
    id_clinica: "", // Começa vazio e será preenchido após o fetch
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState({});

  // Efeito para simular a busca de clínicas na API /api/v1/clinicas
  useEffect(() => {
    const fetchClinics = async () => {
      setIsLoadingClinics(true);
      setClinicError(null);

      const fetchedData = await fetchApi("/api/v1/clinica");

      try {
        // Formatação dos dados para o componente Select
        const formattedClinics = fetchedData.map((c) => ({
          value: c.id,
          label: c.nome_fantasia,
        }));

        setClinics(formattedClinics);

        // Define o valor padrão da clínica no formulário, se houver dados
        if (formattedClinics.length > 0) {
          setFormData((prev) => ({
            ...prev,
            id_clinica: formattedClinics[0].value,
          }));
        }
      } catch (error) {
        console.error("Erro ao buscar clínicas:", error);
        setClinicError("Não foi possível carregar a lista de clínicas.");
      } finally {
        setIsLoadingClinics(false);
      }
    };

    fetchClinics();
  }, []); // Executa apenas na montagem do componente

  // Função genérica para atualizar o estado dos inputs
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Remove o erro ao começar a digitar
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  // Prepara as opções para o campo de seleção de clínicas, incluindo estados de carregamento/erro
  let clinicSelectOptions = [];
  if (isLoadingClinics) {
    clinicSelectOptions = [
      { value: "", label: "Carregando clínicas...", disabled: true },
    ];
  } else if (clinicError) {
    clinicSelectOptions = [
      { value: "", label: `Erro: ${clinicError}`, disabled: true },
    ];
  } else if (clinics.length === 0) {
    clinicSelectOptions = [
      { value: "", label: "Nenhuma clínica encontrada", disabled: true },
    ];
  } else {
    clinicSelectOptions = clinics;
  }

  // Função para lidar com a submissão do formulário
  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrors({});

    // Reseta a mensagem de feedback
    document.getElementById("feedback-message").innerText = "";

    // Validação
    let validationErrors = {};
    if (!formData.nome.trim()) validationErrors.nome = "O nome é obrigatório.";
    if (!formData.email.includes("@"))
      validationErrors.email = "E-mail inválido.";

    if (formData.senha.length < 6) {
      validationErrors.senha = "A senha deve ter pelo menos 6 caracteres.";
    } else if (formData.senha !== formData.confirmSenha) {
      // Validação de confirmação de senha
      validationErrors.confirmSenha = "As senhas não coincidem.";
    }
    if (!formData.confirmSenha.trim())
      validationErrors.confirmSenha = "Confirmação de senha é obrigatória.";

    if (!formData.crmv.trim())
      validationErrors.crmv = "O CRMV é obrigatório para veterinários.";

    // Validação da clínica (apenas se não estiver carregando e não houver erro)
    if (
      !isLoadingClinics &&
      !clinicError &&
      clinics.length > 0 &&
      !formData.id_clinica
    ) {
      validationErrors.id_clinica = "A clínica é obrigatória.";
    }

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      setIsSubmitting(false);
      console.error("Erros de validação:", validationErrors);
      // Usar um modal customizado em vez de alert()
      const feedbackEl = document.getElementById("feedback-message");
      feedbackEl.innerText = "Por favor, corrija os erros no formulário.";
      feedbackEl.classList.add("text-red-600");
      feedbackEl.classList.remove("text-green-600");
      return;
    }

    // Simulação de envio de dados
    setTimeout(async () => {
      console.log("Dados a serem enviados:", formData);

      const feedbackEl = document.getElementById("feedback-message");
      feedbackEl.innerText =
        "Cadastro Enviado com Sucesso! (Verifique o console)";
      feedbackEl.classList.remove("text-red-600");
      feedbackEl.classList.add("text-green-600");

      setIsSubmitting(false);
      await fetchApi("/api/v1/user", formData, "POST");
      window.location.href = "/";
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4 sm:p-6">
      <div className="w-full max-w-2xl bg-white p-6 sm:p-10 rounded-xl shadow-2xl border border-gray-100 animate-fadeIn">
        {/* Cabeçalho */}
        <header className="text-center mb-8 sm:mb-10">
          <Stethoscope className="w-12 h-12 text-indigo-600 mx-auto mb-3" />
          <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">
            Cadastro de Profissional Veterinário
          </h1>
          <p className="mt-2 text-md text-gray-500">
            Preencha seus dados para criar sua conta na plataforma e associar-se
            a uma clínica.
          </p>
        </header>

        {/* Formulário */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* GRUPO 1-A: Dados Pessoais (Nome e Email) */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <InputField
              icon={User}
              id="nome"
              label="Nome Completo"
              name="nome"
              value={formData.nome}
              onChange={handleChange}
              placeholder="Seu nome"
              error={errors.nome}
            />
            <InputField
              icon={Mail}
              id="email"
              label="E-mail"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="seu.email@exemplo.com"
              error={errors.email}
            />
          </div>

          {/* GRUPO 1-B: Senhas */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <InputField
              icon={Lock}
              id="senha"
              label="Senha"
              type="password"
              name="senha"
              value={formData.senha}
              onChange={handleChange}
              placeholder="Mínimo 6 caracteres"
              error={errors.senha}
            />
            <InputField
              icon={Lock}
              id="confirmSenha"
              label="Confirmar Senha"
              type="password"
              name="confirmSenha"
              value={formData.confirmSenha}
              onChange={handleChange}
              placeholder="Repita a senha"
              error={errors.confirmSenha}
            />
          </div>

          {/* GRUPO 1-C: Telefone (Opcional) */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <InputField
              icon={Phone}
              id="telefone"
              label="Telefone (Opcional)"
              type="tel"
              name="telefone"
              maxLength={13}
              value={formData.telefone}
              onChange={handleChange}
              placeholder="(99) 99999-9999"
              isRequired={false}
            />
            <InputField
              icon={Stethoscope}
              id="crmv"
              label="CRMV (Registro Veterinário)"
              name="crmv"
              value={formData.crmv}
              onChange={handleChange}
              placeholder="Ex: 12345 SP"
              error={errors.crmv}
            />
            {/* Espaçador para alinhamento em desktops */}
            <div className="hidden md:block"></div>
          </div>

          {/* GRUPO 2: Dados Profissionais e Associações */}
          <div className="flex flex-col tablet:flex-row justify-around gap-6 pt-6 border-t border-gray-200">
            {/* Campo de Clínica: agora usa as opções dinâmicas */}
            <InputField
              icon={Hospital}
              id="id_clinica"
              label="Clínica Associada"
              type="select"
              name="id_clinica"
              value={formData.id_clinica}
              onChange={handleChange}
              className="w-[50%] text-center"
              options={clinicSelectOptions} // Usando as opções carregadas
              error={errors.id_clinica || clinicError} // Mostra erro de validação ou de carregamento
            />
          </div>

          {/* Área de Feedback (em vez de alert) */}
          <div className="text-center pt-2">
            <p id="feedback-message" className="text-sm font-semibold"></p>
          </div>

          {/* Botão de Submissão */}
          <div className="pt-2">
            <button
              type="submit"
              disabled={isSubmitting || isLoadingClinics || clinicError} // Desabilita se estiver enviando, carregando clínicas ou com erro
              className={`w-full flex justify-center items-center py-3 px-4 border border-transparent text-base font-semibold rounded-lg shadow-lg transition duration-300 ease-in-out transform hover:-translate-y-0.5
                ${
                  isSubmitting || isLoadingClinics || clinicError
                    ? "bg-indigo-400 cursor-not-allowed"
                    : "bg-indigo-600 text-white hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-500 focus:ring-opacity-50"
                }`}
            >
              {isSubmitting || isLoadingClinics ? (
                <svg
                  className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
              ) : (
                <>
                  Criar Conta
                  <ArrowRight className="ml-2 h-5 w-5" />
                </>
              )}
            </button>
          </div>
        </form>

        {/* Link de Ajuda/Login */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500">
            Já tem uma conta?{" "}
            <a
              href="#"
              className="font-medium text-indigo-600 hover:text-indigo-500"
            >
              Fazer Login
            </a>
          </p>
        </div>
      </div>

      {/* Estilos para Animações */}
      <style>{`
        /* Animação para o card principal */
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out;
        }

        /* Estilo para garantir que o select não tenha a seta padrão se o ícone estiver visível */
        /* E ajuste de fonte */
        :root {
            font-family: 'Inter', sans-serif;
        }

        /* O select tem a classe appearance-none no Tailwind para remover a seta padrão */
        select {
          background-position: right 0.75rem center;
        }
      `}</style>
    </div>
  );
};

export default CadastroVeterinario;
