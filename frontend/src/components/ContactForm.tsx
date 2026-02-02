import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import emailjs from '@emailjs/browser';
import FormInput from './FormInput';
import FormTextarea from './FormTextarea';

const CONTACT_EMAIL = 'dawsonjames027@gmail.com';
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

interface FormData {
  name: string;
  email: string;
  company: string;
  message: string;
}

interface FormErrors {
  name?: string;
  email?: string;
  message?: string;
}

export default function ContactForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    company: '',
    message: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const validateEmail = (email: string): boolean => {
    return EMAIL_REGEX.test(email);
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.message.trim()) {
      newErrors.message = 'Message is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    
    if (errors[name as keyof FormErrors]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name as keyof FormErrors];
        return newErrors;
      });
    }
    setSubmitError(null);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSubmitError(null);

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const serviceId = import.meta.env.VITE_EMAILJS_SERVICE_ID;
      const templateId = import.meta.env.VITE_EMAILJS_TEMPLATE_ID;
      const publicKey = import.meta.env.VITE_EMAILJS_PUBLIC_KEY;

      if (!serviceId || !templateId || !publicKey) {
        throw new Error('EmailJS configuration missing');
      }

      emailjs.init(publicKey);

      await emailjs.send(serviceId, templateId, {
        from_name: formData.name,
        from_email: formData.email,
        company: formData.company || 'Not provided',
        message: formData.message,
      });
      
      setFormData({ name: '', email: '', company: '', message: '' });
      navigate('/get-in-touch/sent');
    } catch (error) {
      console.error('EmailJS error:', error);
      setSubmitError(
        `Something went wrong with the form. Please email me directly at ${CONTACT_EMAIL}`
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const isFormValid = (): boolean => {
    return (
      formData.name.trim() !== '' &&
      formData.email.trim() !== '' &&
      validateEmail(formData.email) &&
      formData.message.trim() !== ''
    );
  };

  const renderErrorMessage = () => {
    if (!submitError) return null;
    
    const parts = submitError.split(CONTACT_EMAIL);
    return (
      <div className="form-submit-error">
        {parts[0]}
        <a href={`mailto:${CONTACT_EMAIL}`} className="form-error-email">
          {CONTACT_EMAIL}
        </a>
        {parts[1]}
      </div>
    );
  };

  return (
    <div className="contact-form-container">
      {renderErrorMessage()}

      <form className="contact-form" onSubmit={handleSubmit}>
        <FormInput
          id="name"
          name="name"
          type="text"
          label="Name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Your name"
          required
          error={errors.name}
        />

        <FormInput
          id="email"
          name="email"
          type="email"
          label="Email"
          value={formData.email}
          onChange={handleChange}
          placeholder="your.email@example.com"
          required
          error={errors.email}
        />

        <FormInput
          id="company"
          name="company"
          type="text"
          label="Company"
          value={formData.company}
          onChange={handleChange}
          placeholder="Your company (optional)"
        />

        <FormTextarea
          id="message"
          name="message"
          label="Message"
          value={formData.message}
          onChange={handleChange}
          placeholder="Tell me about the opportunity..."
          required
          error={errors.message}
        />

        <button type="submit" className="form-submit-button" disabled={isSubmitting || !isFormValid()}>
          {isSubmitting ? 'Sending...' : 'Get in Touch'}
        </button>
      </form>

      <p className="contact-form-response-text">
        Send me a message and I'll get back to you within <span className="contact-form-highlight">12 hours</span>.
      </p>
    </div>
  );
}

