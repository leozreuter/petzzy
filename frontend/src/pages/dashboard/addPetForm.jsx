import React, { useState } from "react";
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

const AddPetForm = ({ onClose }) => {
  const [sexoSelecionado, setSexoSelecionado] = useState(null);
  const [especieSelecionada, setEspecieSelecionada] = useState(null);

  const handleSelect = (sexo) => {
    setSexoSelecionado(sexo);
  };
  const handleEspecieChange = (e) => {
    setEspecieSelecionada(e.target.value);
  };

  const {
    data: dataEspecies,
    error: errorEspecies,
    isLoading: isLoadingEspecies,
  } = useSWR("/api/v1/especie", fetchApi);

  const {
    data: dataRacas,
    error: errorRacas,
    isLoading: isLoadingRacas,
  } = useSWR(
    especieSelecionada ? `/api/v1/raca?especie=${especieSelecionada}` : [],
    fetchApi
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    let values = Object.fromEntries(data.entries());
    values = { sexo: sexoSelecionado, ...values };
    await fetchApi("/api/v1/pet", values, "POST");
    onClose();
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Adicionar Novo Pet</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <label htmlFor="nome" className="text-gray-700 flex text-sm">
            <div>Nome do Pet</div>
            <div className="text-red-700 font-medium">*</div>
          </label>
          <input
            type="text"
            id="nome"
            name="nome"
            required={true}
            className="w-full p-2 border rounded-md"
          />
        </div>
        <div>
          <label htmlFor="especie" className="block text-gray-700 text-sm">
            Espécie
          </label>
          <div className="grid w-full border rounded-md text-sm">
            <select
              id="especie"
              name="especie"
              required={true}
              onChange={handleEspecieChange}
              className="w-full h-full p-2 col-start-1 row-start-1 appearance-none bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-sky-500 rounded-md"
            >
              {isLoadingEspecies ? (
                <option value="" disabled selected>
                  Carregando espécies
                </option>
              ) : errorEspecies ? (
                <option value="" disabled selected>
                  Erro ao carregar espécies
                </option>
              ) : (
                <>
                  <option value="" disabled selected>
                    Selecione a Espécie
                  </option>
                  {dataEspecies.map((especie) => (
                    <option value={especie.id}>{especie.nome}</option>
                  ))}
                </>
              )}
            </select>
            <div className="flex items-center justify-end pr-4 col-start-1 row-start-1 pointer-events-none">
              <ChevronDown className="h-4 w-4 text-gray-400" />
            </div>
          </div>
        </div>
        {especieSelecionada && (
          <div>
            <label htmlFor="raca" className="block text-gray-700 text-sm">
              Raça
            </label>
            <div className="grid w-full border rounded-md text-sm">
              <select
                id="raca"
                name="id_raca"
                required={true}
                className="w-full h-full p-2 col-start-1 row-start-1 appearance-none bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-sky-500 rounded-md"
              >
                {isLoadingRacas ? (
                  <option value="" disabled>
                    Carregando raças...
                  </option>
                ) : errorRacas ? (
                  <option value="" disabled>
                    Erro ao carregar raças
                  </option>
                ) : (
                  <>
                    <option value="" disabled>
                      Selecione a Raça
                    </option>
                    {dataRacas &&
                      dataRacas.length > 0 &&
                      dataRacas.map((raca) => (
                        <option key={raca.id} value={raca.id}>
                          {raca.nome}
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
        )}
        <div className="flex flex-row w-full justify-between gap-[5%]">
          <div className="w-[100%]">
            <label htmlFor="cor" className="block text-gray-700 text-sm">
              Cor/Pelagem
            </label>
            <input
              type="text"
              id="cor"
              name="cor"
              className="w-full p-2 border rounded-md"
            />
          </div>
          <div className="w-[100%]">
            <label className="block text-gray-700 text-sm">Sexo</label>
            <div className="w-[100%] p-2 flex gap-3">
              <input
                type="button"
                id="sexo"
                onClick={() => handleSelect("M")}
                value="Masculino"
                name="sexo"
                className={`w-1/2 border rounded-full transition-colors duration-200 ease-in-out
            ${
              sexoSelecionado === "M"
                ? "bg-sky-500 text-white"
                : "bg-white text-gray-700 hover:bg-sky-300"
            }
          `}
              />
              <input
                type="button"
                id="sexo"
                onClick={() => handleSelect("F")}
                value="Feminino"
                name="sexo"
                className={`w-1/2 border rounded-full transition-colors duration-200 ease-in-out
            ${
              sexoSelecionado === "F"
                ? "bg-pink-500 text-white"
                : "bg-white text-gray-700 hover:bg-pink-300"
            }
          `}
              />
            </div>
          </div>
        </div>
        <div>
          <label htmlFor="obs" className="block text-gray-700 text-sm">
            Observação
          </label>
          <textarea
            type="text"
            id="obs"
            name="obs"
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

export default AddPetForm;
