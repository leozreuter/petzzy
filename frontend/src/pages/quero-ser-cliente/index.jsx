function DivBtn({ href, children, icon }) {
  return (
    <div
      onClick={() => (window.location.href = href)}
      className="flex flex-col items-center justify-center w-[250px] h-[250px] bg-petzzy-blue/40 hover:bg-petzzy-blue text-white p-6 rounded-2xl shadow-lg cursor-pointer transform transition duration-300 hover:scale-105 hover:shadow-xl"
    >
      {icon && <div className="text-6xl mb-4">{icon}</div>}
      <span className="text-xl font-semibold text-center">{children}</span>
    </div>
  );
}

const QueroSerCliente = () => {
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center px-4 overflow-hidden">
      {/* Fundo degradê desfocado */}
      <div className="absolute inset-0 bg-gradient-to-r from-violet-500 via-pink-400 to-red-700 filter blur-xl opacity-80 -z-10"></div>
      <div className="absolute inset-0 bg-gradient-to-tr from-sky-400 via-green-400 to-yellow-200 filter blur-2xl opacity-50 -z-10"></div>

      {/* Conteúdo */}
      <h1 className="text-3xl font-bold text-white mb-12 text-center drop-shadow-lg">
        Selecione o que deseja cadastrar:
      </h1>

      <div className="flex flex-col tablet:flex-row gap-8 items-center justify-center z-10">
        <DivBtn href="/cadastro-veterinario" icon="👤">
          Quero ser veterinário assoiado
        </DivBtn>
        <DivBtn href="/cadastro-clinica" icon="🏥">
          Clínica
        </DivBtn>
      </div>
    </div>
  );
};

export default QueroSerCliente;
