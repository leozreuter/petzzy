import useSWR from "swr";
import { useState } from "react";
import Logo from "../../components/logo/Logo";
import Icone from "../../components/Icone";

import Modal from "./modal"; // Importa o componente Modal
import AddPetForm from "./addPetForm"; // Importa o formulário de adicionar pet
import AddAtendimentoForm from "./addAtendimentoForm"; // Importa o formulário de adicionar pet

async function fetchMyPets(key) {
  const response = await fetch(process.env.REACT_APP_BACKEND_SERVER + key, {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
    },
  });
  const responseBody = await response.json();
  return responseBody;
}

const logout = async () => {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("nomeCliente");
  await new Promise((r) => setTimeout(r, 1000)); // pausa 1s
  window.location.href = "/login";
};

export default function Dashboard() {
  let {
    data: myPets,
    error,
    isLoading,
    mutate: mutatePets,
  } = useSWR("/api/v1/pet", fetchMyPets, {
    refreshInterval: 30000,
  });
  let {
    data: myAtendimentos,
    error: errorAtendimentos,
    isLoading: isLoadingAtendimentos,
    mutate: mutateAtendimentos,
  } = useSWR("/api/v1/atendimento", fetchMyPets, {
    refreshInterval: 30000,
  });

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalType, setModalType] = useState("");
  const openModal = () => setIsModalOpen(true);

  const closeModal = async () => {
    setIsModalOpen(false);
    await mutatePets();
    await mutateAtendimentos();
  };

  const addPet = async () => {
    setModalType("pet");
    openModal();
  };

  const addAtendimento = async () => {
    setModalType("atendimento");
    openModal();
  };

  function dt_atentimento_formatado(dthr) {
    const date = new Date(dthr);

    const diaSemana = new Intl.DateTimeFormat("pt-BR", {
      weekday: "long",
    }).format(date);
    const dia = date.getDate();
    const mes = new Intl.DateTimeFormat("pt-BR", { month: "long" }).format(
      date
    );
    const ano = date.getFullYear();

    // primeira letra maiúscula no dia da semana e mês
    const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);

    return `${capitalize(diaSemana)}, ${dia} de ${capitalize(mes)} de ${ano}`;
  }

  function hr_atentimento_formatado(dthr) {
    const date = new Date(dthr);
    const horas = String(date.getHours()).padStart(2, "0");
    const minutos = String(date.getMinutes()).padStart(2, "0");

    return `${horas}:${minutos}`;
  }

  const sexoColors = {
    M: "bg-blue-300",
    F: "bg-pink-300",
    null: "bg-gray-400/80",
  };

  return (
    (document.title = "Dashboard | Petzzy"),
    (
      <div className="h-[100dvh] bg-gradient-to-br from-blue-100 to-blue-200 p-[10px] font-baloo">
        <header className="mt-5 mb-10 ml-20 mr-20 h-[12dvh] tablet:h-[12dvh] min-h-min flex flex-col items-center">
          <div className="max-h-full md:h-full flex-shrink-0 cursor-pointer">
            <Logo size="xlarge" className="w-auto h-full" />
          </div>
        </header>
        <div className="w-[99dvw] pl-64 pr-64 flex justify-between">
          <h1 className="font-semibold text-4xl text-petzzy-blue ">
            Seja bem-vindo(a), {localStorage.getItem("nomeCliente")}!
          </h1>
          <div
            onClick={logout}
            className="bg-sky-500 hover:bg-sky-600 text-white w-20 h-8 rounded-xl flex items-center justify-center font-semibold text-lg cursor-pointer"
          >
            Sair
          </div>
        </div>
        <div className="w-[99dvw] pt-6 self-center flex flex-row justify-center gap-10">
          <div className="flex flex-col w-[40dvw] h-[60dvh] self-center bg-white p-5 rounded-lg shadow-xl">
            {/* Header MEUS PETS */}
            <div className="flex w-[100%] pb-1 justify-between items-center gap-5 relative">
              <h1 className="text-3xl font-bold text-gray-700">Meus Pets</h1>
              <div
                onClick={addPet}
                className="bg-green-500 rounded-2xl max-w-40 min-w-32 h-10 text-center flex justify-center items-center cursor-pointer hover:bg-green-600 transition-all duration-200"
              >
                <h3 className="font-semibold text-white mr-5 ml-5">
                  + Adicionar Pet
                </h3>
              </div>
              <div class="absolute -bottom-7 left-0 w-full h-8 bg-gradient-to-b from-white to-transparent"></div>
            </div>
            <div className="flex flex-wrap w-[100%] pb-2 h-[100%] bg-transparent flex-row justify-center gap-5 overflow-y-scroll">
              {isLoading ? (
                <p>Carregando pets...</p>
              ) : error ? (
                <p>Erro ao carregar pets</p>
              ) : (
                myPets.map((pet, index) => (
                  <div
                    key={index}
                    className="flex flex-col mt-2 items-center border-[1px] w-[30%] h-min bg-gray-100 rounded-xl p-3 hover:bg-gray-200 transition-all duration-1"
                    style={{ boxShadow: "-6px 6px 10px rgba(0, 0, 0, 0.15)" }}
                  >
                    <div
                      className={`rounded-full h-28 w-28 flex items-center justify-center p-6 ${
                        sexoColors[pet.sexo] || "bg-gray-400/80"
                      }`}
                    >
                      <Icone
                        className="self-center"
                        icon={`${pet.especie.toLowerCase()}`}
                      />
                    </div>
                    <div className="h-12 flex flex-col items-center">
                      <h2 className="font-semibold">{pet.nome}</h2>
                      <span>
                        {pet.raca} {pet.especie}
                      </span>
                      <br />
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
          <div className="flex flex-col w-[40dvw] h-[60dvh] self-center bg-white p-5 rounded-lg shadow-xl ">
            {/* Header PROX LEMBRETES */}
            <div className="flex w-[100%] justify-between items-center gap-5 relative">
              <h1 className="text-3xl font-bold text-gray-700">
                Próximos lembretes
              </h1>
              <div
                onClick={addAtendimento}
                className="bg-yellow-500 rounded-2xl max-w-40 min-w-32 h-10 text-center flex justify-center items-center cursor-pointer hover:bg-yellow-600 transition-all duration-200"
              >
                <h3 className="font-semibold text-white mr-4 ml-4">
                  + Novo Lembrete
                </h3>
              </div>
              <div class="absolute -bottom-10 left-0 w-full h-10 bg-gradient-to-b from-white to-transparent"></div>
            </div>
            <div className="flex flex-wrap w-[100%] pb-2 bg-transparent justify-center flex-row overflow-y-scroll">
              {isLoadingAtendimentos ? (
                <p>Carregando lembretes...</p>
              ) : errorAtendimentos ? (
                <p>Erro ao carregar atendimentos</p>
              ) : (
                myAtendimentos.map((atendimento, index) => (
                  <div
                    key={index}
                    className="flex flex-col gap-2 w-[90%] h-24 h-min mt-5 bg-gray-100 rounded-xl p-3 hover:bg-gray-200 transition-all duration-1 border-l-8 border-violet-500"
                    style={{ boxShadow: "-6px 6px 15px rgba(0, 0, 0, 0.15)" }}
                  >
                    <div className="flex flex-col">
                      <h2 className="font-medium text-xl text-gray-900">
                        {"Tipo de consulta"} - {atendimento.nome_fantasia}
                      </h2>
                      <span className="font-medium text-md text-gray-700">
                        {dt_atentimento_formatado(atendimento.dthr_atendimento)}
                      </span>
                      <span className="text-sm text-gray-600">
                        {hr_atentimento_formatado(atendimento.dthr_atendimento)}{" "}
                        - {atendimento.clinica.toUpperCase()}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
        <Modal isOpen={isModalOpen} onClose={closeModal}>
          {modalType === "pet" && <AddPetForm onClose={closeModal} />}
          {modalType === "atendimento" && (
            <AddAtendimentoForm onClose={closeModal} />
          )}
        </Modal>
      </div>
    )
  );
}
