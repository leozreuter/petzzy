export default function Logo({
  type = "text",
  variant = "primary",
  size = "medium", // default
}) {
  // Map de tamanhos para arquivos de imagem
  const sizeMap = {
    small: "30",
    medium: "96",
    large: "150",
    xlarge: "200",
  };

  const sizeSuffix = sizeMap[size] || sizeMap["xlarge"];

  const src_defined =
    type === "text"
      ? `/logo_${sizeSuffix}.png`
      : `/logo_${type}_${sizeSuffix}.png`;
  return (
    <img className={`img ${variant}`} src={src_defined} alt="Petzzy Logo" />
  );
}
