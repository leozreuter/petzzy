export default function InputIcon({
  icon: Icon,
  placeholder,
  type = "text",
  error,
  ...rest
}) {
  return (
    <div
      className={`flex items-center w-full px-4 py-2 border rounded-lg focus-within:ring-1 ${
        error
          ? "border-red-500 focus-within:ring-red-400 bg-red-200"
          : "border-gray-300 "
      }`}
    >
      <Icon className="w-5 h-5 mr-2 text-gray-400" />
      <input
        type={type}
        placeholder={placeholder}
        className="bg-transparent outline-none w-full text-sm"
        {...rest}
      />
    </div>
  );
}
