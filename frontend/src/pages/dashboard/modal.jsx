// Modal.jsx
import React, { useRef } from "react";
import { CSSTransition } from "react-transition-group";

const Modal = ({ isOpen, onClose, children }) => {
  const nodeRef = useRef(null);

  return (
    <CSSTransition
      in={isOpen}
      timeout={300}
      classNames={{
        enter: "opacity-0 scale-100",
        enterActive:
          "transition-all duration-500 ease-out opacity-100 scale-100",
        exit: "transition-all duration-300 ease-out opacity-0 scale-100",
      }}
      unmountOnExit
      nodeRef={nodeRef}
    >
      <div
        ref={nodeRef}
        className="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50"
        onClick={onClose}
      >
        <div
          className="bg-white p-6 rounded-lg shadow-xl relative max-w-lg w-full mx-4"
          onClick={(e) => e.stopPropagation()}
        >
          <button
            className="absolute top-2 right-4 text-gray-400 hover:text-gray-600 text-3xl font-light"
            onClick={onClose}
          >
            &times;
          </button>
          {children}
        </div>
      </div>
    </CSSTransition>
  );
};

export default Modal;
