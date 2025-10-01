import React from "react";

// Componente para exibir uma página 404 (Página Não Encontrada) com tema Pet
const NotFound = () => {
  return (
    <div className="min-h-screen bg-sky-50 flex items-center justify-center p-4 font-sans">
      <div className="text-center p-10 bg-white rounded-xl shadow-2xl border border-gray-200 w-full max-w-md">
        {/* Ícone Temático */}
        <p className="text-6xl mb-4">🐾</p>

        {/* Código de Erro Grande - Cor mais suave */}
        <h1 className="text-8xl md:text-9xl font-extrabold text-gray-400 mb-2 tracking-tight">
          404
        </h1>

        {/* Mensagem de Título */}
        <h2 className="text-3xl font-bold text-gray-800 mb-4">
          Ops! Não encontramos este cantinho. 🐶
        </h2>

        {/* Descrição Temática */}
        <p className="text-lg text-gray-600 mb-8">
          Parece que esta coleira digital se perdeu! A página que você tentou
          acessar não existe mais ou o endereço foi digitado incorretamente.
          Vamos voltar para onde estão os petiscos?
        </p>

        {/* Ação (Botão) */}
        <button
          // Simula a navegação de volta para a página inicial
          onClick={() => {
            window.location.href = "/";
          }}
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-md text-lg font-medium text-white bg-sky-600 
                       hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 transition duration-150 ease-in-out"
        >
          Voltar para a Área Principal
        </button>

        <p className="mt-6 text-sm text-gray-500">
          Se o problema persistir, entre em contato com o suporte da clínica.
        </p>
      </div>
    </div>
  );
};

export default NotFound;
