export default function Icone({ className = "", icon = "pet" }) {
  const src_defined = `/${icon}Icon.png`;

  return (
    <img
      className={`img ${className}`}
      src={src_defined}
      onError={(e) => (e.currentTarget.src = "/petIcon.png")}
      alt="icone"
    />
  );
}
