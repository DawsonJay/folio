interface FormTextareaProps {
  id: string;
  name: string;
  label: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  required?: boolean;
  error?: string;
}

export default function FormTextarea({
  id,
  name,
  label,
  value,
  onChange,
  placeholder,
  required = false,
  error
}: FormTextareaProps) {
  return (
    <div className="form-field">
      <label 
        htmlFor={id} 
        className={`form-label ${required ? 'form-label-required' : ''}`}
      >
        {label}
      </label>
      <textarea
        id={id}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="form-textarea"
      />
      {error && <span className="form-error">{error}</span>}
    </div>
  );
}

