interface FormInputProps {
  id: string;
  name: string;
  type: string;
  label: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  required?: boolean;
  error?: string;
}

export default function FormInput({
  id,
  name,
  type,
  label,
  value,
  onChange,
  placeholder,
  required = false,
  error
}: FormInputProps) {
  return (
    <div className="form-field">
      <label 
        htmlFor={id} 
        className={`form-label ${required ? 'form-label-required' : ''}`}
      >
        {label}
      </label>
      <input
        type={type}
        id={id}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="form-input"
      />
      {error && <span className="form-error">{error}</span>}
    </div>
  );
}

