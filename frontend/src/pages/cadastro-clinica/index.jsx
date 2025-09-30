import React, { useState } from "react";

const InputField = ({
  label,
  id,
  type = "text",
  value,
  onChange,
  placeholder,
  required = true,
  className = "",
  isSelect = false,
  children,
  maxLength,
}) => (
  <div className="mb-4">
    <label
      htmlFor={id}
      className="block text-sm font-medium text-gray-700 mb-1"
    >
      {label}
      {required && <span className="text-red-500 ml-1">*</span>}
    </label>

    {isSelect ? (
      <select
        id={id}
        name={id}
        value={value}
        onChange={onChange}
        required={required}
        className={`w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white
                   focus:outline-none focus:ring-sky-500 focus:border-sky-500 transition duration-150 ease-in-out ${className}`}
      >
        {children}
      </select>
    ) : (
      <input
        type={type}
        id={id}
        name={id}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className={`w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 
                   focus:outline-none focus:ring-sky-500 focus:border-sky-500 transition duration-150 ease-in-out ${className}`}
        maxLength={maxLength} // Aplicando maxLength
      />
    )}
  </div>
);

const CadastroClinica = () => {
  const [nomeFantasia, setNomeFantasia] = useState("");
  const [cnpj, setCnpj] = useState("");
  const [telefone, setTelefone] = useState("");

  const [cep, setCep] = useState("");
  const [rua, setRua] = useState("");
  const [numero, setNumero] = useState("");
  const [complemento, setComplemento] = useState("");
  const [bairro, setBairro] = useState("");
  const [cidade, setCidade] = useState("");
  const [estado, setEstado] = useState("");

  // Função auxiliar para calcular e restaurar a posição do cursor após a aplicação da máscara
  const applyMaskAndFixCursor = (e, setter, maskLogic) => {
    const input = e.target;
    const originalValue = input.value;
    const originalCursor = input.selectionStart;

    const maskedValue = maskLogic(originalValue);

    setter(maskedValue);

    const diff = maskedValue.length - originalValue.length;
    let newCursor = originalCursor + diff;

    if (newCursor > maskedValue.length) {
      newCursor = maskedValue.length;
    }

    setTimeout(() => {
      if (document.activeElement === input) {
        input.setSelectionRange(newCursor, newCursor);
      }
    }, 0);
  };

  // Lógica CEP (5 dígitos + traço + 3 dígitos)
  const cepMaskLogic = (value) => {
    let cleanValue = value.replace(/\D/g, "").substring(0, 8);
    if (cleanValue.length > 5) {
      cleanValue = cleanValue.replace(/^(\d{5})(\d)/, "$1-$2");
    }
    return cleanValue;
  };
  const handleCepChange = (e) => {
    applyMaskAndFixCursor(e, setCep, cepMaskLogic);
  };

  // Lógica CNPJ (XX.XXX.XXX/XXXX-XX)
  const cnpjMaskLogic = (value) => {
    let rawValue = value.replace(/\D/g, "").substring(0, 14);

    // Aplicação progressiva da máscara
    if (rawValue.length > 2)
      rawValue = rawValue.replace(/^(\d{2})(\d)/, "$1.$2");
    if (rawValue.length > 6)
      rawValue = rawValue.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
    if (rawValue.length > 10)
      rawValue = rawValue.replace(
        /^(\d{2})\.(\d{3})\.(\d{3})(\d)/,
        "$1.$2.$3/$4"
      );
    if (rawValue.length > 14)
      rawValue = rawValue.replace(
        /^(\d{2})\.(\d{3})\.(\d{3})\/(\d{4})(\d)/,
        "$1.$2.$3/$4-$5"
      );

    return rawValue.substring(0, 18); // Limite de caracteres de exibição
  };
  const handleCnpjChange = (e) => {
    applyMaskAndFixCursor(e, setCnpj, cnpjMaskLogic);
  };

  // Lógica Telefone (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
  const telefoneMaskLogic = (value) => {
    let rawValue = value.replace(/\D/g, "").substring(0, 11);

    if (rawValue.length > 0) rawValue = `(${rawValue}`;
    if (rawValue.length > 3)
      rawValue = rawValue.replace(/^(\(\d{2})(\d)/, "$1) $2");

    // Formato com 9 dígitos (celular)
    if (rawValue.length > 10 && rawValue.length <= 11)
      rawValue = rawValue.replace(/^(\(\d{2}\))\s(\d{5})(\d)/, "$1 $2-$3");
    // Formato com 8 dígitos (fixo)
    else if (rawValue.length > 9)
      rawValue = rawValue.replace(/^(\(\d{2}\))\s(\d{4})(\d)/, "$1 $2-$3");

    return rawValue.substring(0, 15);
  };
  const handleTelefoneChange = (e) => {
    applyMaskAndFixCursor(e, setTelefone, telefoneMaskLogic);
  };

  // Função para lidar com o envio do formulário
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Objeto com os dados para envio
    const dadosClinica = {
      nome_fantasia: nomeFantasia,
      cnpj: cnpj.replace(/\D/g, ""),
      telefone_contato: telefone.replace(/\D/g, ""),
      cep: cep.replace(/\D/g, ""),
      logradouro: rua,
      numero,
      complemento,
      bairro,
      cidade,
      estado,
    };

    const respose = await fetch(
      process.env.REACT_APP_BACKEND_SERVER + "/api/v1/clinica",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
        body: JSON.stringify(dadosClinica),
      }
    );

    if (respose.status === 201) {
      window.location.href = "/home";
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white p-8 rounded-xl shadow-2xl border border-gray-200">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">
          🏥 Cadastro de Clínica Veterinária
        </h1>
        <p className="text-sm text-gray-500 mb-8 text-center">
          Preencha os dados básicos e o endereço detalhado para prosseguir.
        </p>

        <form onSubmit={handleSubmit}>
          {/* GRUPO: Dados Básicos */}
          <div className="mb-8 border-b border-gray-200 pb-6">
            <h2 className="text-xl font-semibold text-sky-700 mb-4 border-l-4 border-sky-500 pl-2">
              Informações da Clínica
            </h2>

            <InputField
              label="Nome Fantasia"
              id="nomeFantasia"
              value={nomeFantasia}
              onChange={(e) => setNomeFantasia(e.target.value)}
              placeholder="Ex: 4 Patinhas"
            />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InputField
                label="CNPJ"
                id="cnpj"
                value={cnpj}
                onChange={handleCnpjChange} // Máscara CNPJ com correção de foco
                placeholder="00.000.000/0000-00"
                type="text"
                maxLength={18}
              />
              <InputField
                label="Telefone"
                id="telefone"
                type="text"
                value={telefone}
                onChange={handleTelefoneChange} // Máscara Telefone com correção de foco
                placeholder="(XX) XXXXX-XXXX"
                maxLength={15}
              />
            </div>
          </div>

          {/* GRUPO: Endereço Detalhado */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-sky-700 mb-4 border-l-4 border-sky-500 pl-2">
              Endereço
            </h2>

            {/* Linha 1: CEP */}
            <div className="mb-4 w-full md:w-1/3">
              <InputField
                label="CEP"
                id="cep"
                value={cep}
                onChange={handleCepChange} // Máscara CEP com correção de foco
                placeholder="00000-000"
                type="text"
                maxLength={9}
              />
            </div>

            {/* Linha 2: Rua e Número */}
            <div className="grid grid-cols-3 gap-4">
              <div className="col-span-2">
                <InputField
                  label="Rua"
                  id="rua"
                  value={rua}
                  onChange={(e) => setRua(e.target.value)}
                  placeholder="Rua das Patas"
                />
              </div>
              <div>
                <InputField
                  label="Número"
                  id="numero"
                  value={numero}
                  onChange={(e) => setNumero(e.target.value)}
                  placeholder="123"
                  type="text"
                />
              </div>
            </div>

            {/* Linha 3: Complemento e Bairro */}
            <div className="grid grid-cols-2 gap-4">
              <InputField
                label="Complemento (Opcional)"
                id="complemento"
                value={complemento}
                onChange={(e) => setComplemento(e.target.value)}
                placeholder="Apto, Sala, Bloco"
                required={false}
              />
              <InputField
                label="Bairro"
                id="bairro"
                value={bairro}
                onChange={(e) => setBairro(e.target.value)}
                placeholder="Centro"
              />
            </div>

            {/* Linha 4: Cidade e Estado */}
            <div className="grid grid-cols-3 gap-4">
              <div className="col-span-2">
                <InputField
                  label="Cidade"
                  id="cidade"
                  value={cidade}
                  onChange={(e) => setCidade(e.target.value)}
                  placeholder="Porto Alegre"
                />
              </div>
              <div className="col-span-1">
                {/* Campo de Seleção para UF usando o InputField com prop isSelect */}
                <InputField
                  label="Estado (UF)"
                  id="estado"
                  value={estado}
                  onChange={(e) => setEstado(e.target.value)}
                  isSelect={true}
                >
                  <option value="" disabled>
                    Selecione
                  </option>
                  <option value="AC">AC</option>
                  <option value="AL">AL</option>
                  <option value="AP">AP</option>
                  <option value="AM">AM</option>
                  <option value="BA">BA</option>
                  <option value="CE">CE</option>
                  <option value="DF">DF</option>
                  <option value="ES">ES</option>
                  <option value="GO">GO</option>
                  <option value="MA">MA</option>
                  <option value="MT">MT</option>
                  <option value="MS">MS</option>
                  <option value="MG">MG</option>
                  <option value="PA">PA</option>
                  <option value="PB">PB</option>
                  <option value="PR">PR</option>
                  <option value="PE">PE</option>
                  <option value="PI">PI</option>
                  <option value="RJ">RJ</option>
                  <option value="RN">RN</option>
                  <option value="RS">RS</option>
                  <option value="RO">RO</option>
                  <option value="RR">RR</option>
                  <option value="SC">SC</option>
                  <option value="SP">SP</option>
                  <option value="SE">SE</option>
                  <option value="TO">TO</option>
                </InputField>
              </div>
            </div>
          </div>

          {/* Botão de Envio */}
          <button
            type="submit"
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-lg text-lg font-medium text-white bg-sky-600 
                       hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 transition duration-150 ease-in-out"
          >
            Cadastrar Clínica
          </button>
        </form>
      </div>
    </div>
  );
};

export default CadastroClinica;
