import Logo from "../../components/logo/Logo";
import { ClipboardList, MapPinCheck, CalendarCheck } from "lucide-react";

export default function Home() {
  return (
    (document.title = "Faça Login | Petzzy"),
    (
      <div className="h-[100dvh] bg-gradient-to-br from-white to-blue-100">
        <header className="pt-5 mb-5 ml-20 mr-20 h-[18dvh] tablet:h-[15dvh] min-h-min flex flex-col items-center gap-1 tablet:gap-1 tablet:flex-row tablet:justify-between">
          <div className="max-h-full md:h-full flex-shrink-0">
            <Logo size="xlarge" className="w-auto h-full" />
          </div>

          <div class="h-min flex gap-[5dvw]">
            <a
              href="#"
              className="text-lg/8 font-semibold text-petzzy-blue hover:text-blue-800 hover:border-b-2 hover:border-petzzy-blue transition-all"
            >
              Quem somos?
            </a>
            <a
              href="#"
              className="text-lg/8 font-semibold text-petzzy-blue hover:text-blue-800 hover:border-b-2 hover:border-petzzy-blue transition-all"
            >
              Seja um cliente
            </a>
            <a
              href="#"
              className="text-lg/8 font-semibold text-petzzy-blue hover:text-blue-800 hover:border-b-2 hover:border-petzzy-blue transition-all"
            >
              Cadastre-se
            </a>
            <a
              href="login"
              class="text-lg/8 font-semibold text-petzzy-blue hover:text-blue-800 hover:border-b-2 hover:border-petzzy-blue transition-all"
            >
              Login <span aria-hidden="true">&rarr;</span>
            </a>
          </div>
        </header>

        <div className="pt-5 pb-5 h-[80dvh] w-[95dvw] flex-shrink-0 flex justify-self-center">
          <div className=" w-[70%]">
            <div className="ml-6 w-full h-[50%] flex flex-col gap-2 font-baloo">
              <h1 className="text-petzzy-blue text-7xl font-bold w-[70%]">
                Agendamentos veterinários Online
              </h1>
              <p className="text-petzzy-blue text-3xl">
                Marque consultas com veterinários de confiança perto de você!
              </p>
              <button className="bg-blue-500 w-80 h-12 mt-2 text-white text-xl font-semibold flex items-center justify-center rounded-lg hover:bg-petzzy-blue2 transition-all duration-1">
                <p>Agendar uma consulta</p>
              </button>
            </div>
            <div className="mt-8 w-[90%] h-[50%] flex justify-around aling-center font-baloo text-petzzy-blue">
              <div className="flex flex-col gap-4 align-center items-center">
                <div className="bg-blue-400/30 text-center rounded-full h-24 w-24 flex justify-center">
                  <ClipboardList className="self-center justify-self-center size-12 text-blue-600" />
                </div>
                <h1 className="font-semibold text-lg">Agende online</h1>
                <p className="w-48 text-center">
                  Agende sem precisar se preocupar em sair de sua casa
                </p>
              </div>
              <div className="flex flex-col gap-4 align-center items-center">
                <div className="bg-blue-400/30 text-center rounded-full h-24 w-24 flex justify-center">
                  <MapPinCheck className="self-center justify-self-center size-12 text-blue-600" />
                </div>
                <h1 className="font-semibold text-lg">Encontre veterinários</h1>
                <p className="w-48 text-center">
                  Ache diversos profissionais em sua região{" "}
                </p>
              </div>
              <div className="flex flex-col gap-4 align-center items-center">
                <div className="bg-blue-400/30 text-center rounded-full h-24 w-24 flex justify-center">
                  <CalendarCheck className="self-center justify-self-center size-12 text-blue-600" />
                </div>
                <h1 className="font-semibold text-lg">Confirme o horário</h1>
                <p className="w-48 text-center">
                  Marque o melhor hoário para você e seu pet
                </p>
              </div>
            </div>
          </div>
          <img
            src="home.png"
            alt="Veterinária"
            className="absolute bottom-8 right-20 size-[30%] h-auto"
          />
        </div>
      </div>
    )
  );
}
