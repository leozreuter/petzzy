import React, { useState, useEffect } from "react";
import useSWR from "swr";
import { ChevronDown } from "lucide-react";

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

const AddAtendimentoForm = ({ onClose }) => {
  const [clinicaSelecionada, setClinicaSelecionada] = useState(null);
  const [minDateTime, setMinDateTime] = useState("");

  useEffect(() => {
    const now = new Date();

    // arredonda para o próximo intervalo de 30min
    const minutes = now.getMinutes();
    const remainder = 30 - (minutes % 30);
    now.setMinutes(minutes + remainder);
    now.setSeconds(0);
    now.setMilliseconds(0);

    // formata para datetime-local
    const offset = now.getTimezoneOffset();
    const isoString = new Date(
      now.getTime() - offset * 60 * 1000
    ).toISOString();
    const splitedDate = isoString.slice(0, 16).split("T");

    setMinDateTime(`${splitedDate[0]} ${splitedDate[1]}`); // YYYY-MM-DDT HH:mm
  }, []);

  const handleDatetimeChange = (e) => {
    let dt = new Date(e.target.value);
    let minutes = dt.getMinutes();

    // arredonda para o próximo múltiplo de 30
    if (minutes % 30 !== 0) {
      dt.setMinutes(minutes + (30 - (minutes % 30)));
      dt.setSeconds(0);
      dt.setMilliseconds(0);

      const offset = dt.getTimezoneOffset();
      const local = new Date(dt.getTime() - offset * 60 * 1000)
        .toISOString()
        .slice(0, 16);

      e.target.value = local;
    }
  };

  const handleClinicaChange = (e) => {
    setClinicaSelecionada(e.target.value);
  };

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

    return rawValue.substring(0, 18);
  };

  const {
    data: dataClinicas,
    error: errorClinicas,
    isLoading: isLoadingClinicas,
  } = useSWR("/api/v1/clinica", fetchApi);

  const {
    data: dataVeterinarios,
    error: errorVeterinarios,
    isLoading: isLoadingVeterinarios,
  } = useSWR("/api/v1/user?perfil=Veterinario", fetchApi);

  const {
    data: dataPets,
    error: errorPets,
    isLoading: isLoadingPets,
  } = useSWR("/api/v1/pet", fetchApi);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    let values = Object.fromEntries(data.entries());

    console.log(values);
    await fetchApi("/api/v1/atendimento", values, "POST");
    onClose();
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Adicionar Novo Atendimento</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label htmlFor="id_pet" className="text-gray-700 flex text-sm">
            <div>Nome do Pet</div>
            <div className="text-red-700 font-medium">*</div>
          </label>
          <div className="grid w-full border rounded-md text-sm">
            <select
              id="id_pet"
              name="id_pet"
              required={true}
              className="w-full h-full p-2 col-start-1 row-start-1 appearance-none bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-sky-500 rounded-md"
            >
              {isLoadingPets ? (
                <option value="" disabled selected>
                  Carregando seus pets
                </option>
              ) : errorPets ? (
                <option value="" disabled selected>
                  Erro ao carregar seus pets
                </option>
              ) : (
                <>
                  <option value="" disabled selected>
                    Selecione seu Pet
                  </option>
                  {dataPets.map((pet) => (
                    <option value={pet.id}>{pet.nome}</option>
                  ))}
                </>
              )}
            </select>
          </div>
        </div>
        <div>
          <label htmlFor="id_clinica" className="block text-gray-700 text-sm">
            Clinicas
          </label>
          <div className="grid w-full border rounded-md text-sm">
            <select
              id="id_clinica"
              name="id_clinica"
              required={true}
              onChange={handleClinicaChange}
              className="w-full h-full p-2 col-start-1 row-start-1 appearance-none bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-sky-500 rounded-md"
            >
              {isLoadingClinicas ? (
                <option value="" disabled selected>
                  Carregando clinicas
                </option>
              ) : errorClinicas ? (
                <option value="" disabled selected>
                  Erro ao carregar clinicas
                </option>
              ) : (
                <>
                  <option value="" disabled selected>
                    Selecione a Clinica
                  </option>
                  {dataClinicas.map((clinica) => (
                    <option value={clinica.id}>
                      {clinica.nome_fantasia} -{" "}
                      {cnpjMaskLogic(clinica.cnpj, "")}
                    </option>
                  ))}
                </>
              )}
            </select>
            <div className="flex items-center justify-end pr-4 col-start-1 row-start-1 pointer-events-none">
              <ChevronDown className="h-4 w-4 text-gray-400" />
            </div>
          </div>
        </div>
        <div>
          <label
            htmlFor="id_veterinario"
            className="text-gray-700 flex text-sm"
          >
            <div>Veterinario</div>
            <div className="text-red-700 font-medium">*</div>
          </label>
          <div className="grid w-full border rounded-md text-sm">
            <select
              id="id_veterinario"
              name="id_veterinario"
              required={true}
              className="w-full h-full p-2 col-start-1 row-start-1 appearance-none bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-sky-500 rounded-md"
            >
              {isLoadingVeterinarios ? (
                <option value="" disabled selected>
                  Carregando veterinários
                </option>
              ) : errorVeterinarios ? (
                <option value="" disabled selected>
                  Erro ao carregar veterinários
                </option>
              ) : (
                <>
                  <option value="" disabled selected>
                    Selecione o veterinario
                  </option>
                  {dataVeterinarios.map((veterinario) => (
                    <option value={veterinario.id}>{veterinario.nome}</option>
                  ))}
                </>
              )}
            </select>
          </div>
        </div>
        <div className="flex flex-row w-full justify-between gap-[5%]">
          <div className="w-[100%]">
            <label
              htmlFor="dthr_atendimento"
              className="block text-gray-700 text-sm"
            >
              Horário (30 em 30 minutos)
            </label>
            <input
              type="datetime-local"
              min={minDateTime}
              onBlur={handleDatetimeChange}
              id="dthr_atendimento"
              name="dthr_atendimento"
              className="w-full p-2 border rounded-md"
            />
          </div>
        </div>
        <div>
          <label htmlFor="motivo" className="block text-gray-700 text-sm">
            Motivo
          </label>
          <textarea
            type="text"
            id="motivo"
            name="motivo"
            maxlength="255"
            required={true}
            placeholder="Digite até 255 caracteres..."
            className="w-[100%] p-2 border rounded-md min-h-40"
          ></textarea>
        </div>

        <button
          type="submit"
          className="bg-green-500 text-white p-2 rounded-md hover:bg-green-600"
        >
          Salvar Pet
        </button>
      </form>
    </div>
  );
};

export default AddAtendimentoForm;
