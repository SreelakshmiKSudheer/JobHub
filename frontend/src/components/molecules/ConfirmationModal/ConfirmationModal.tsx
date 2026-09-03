import Button from '../../atoms/Button/Button';
import { AlertTriangle, HelpCircle } from 'lucide-react';
import type { ConfirmationModalProps } from '../../../types/confirmationModal.types';

const ConfirmationModal: React.FC<ConfirmationModalProps> = ({
  isOpen,
  title,
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'primary',
  loading = false,
  onConfirm,
  onCancel,
}) => {
  if (!isOpen) return null;

  const isDanger = variant === 'danger';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4 animate-fadeIn">
      <div className="w-full max-w-md bg-bg-alt rounded-3xl p-6 border border-text/10 shadow-2xl flex flex-col gap-5 animate-scaleUp">
        {/* Header */}
        <div className="flex items-center gap-3.5">
          <div
            className={`p-3 rounded-2xl border shrink-0 ${
              isDanger
                ? 'bg-red-500/10 text-red-600 border-red-500/20'
                : 'bg-primary/10 text-primary border-primary/20'
            }`}
          >
            {isDanger ? <AlertTriangle size={24} /> : <HelpCircle size={24} />}
          </div>
          <div>
            <h3 className="text-lg font-bold text-text">{title}</h3>
            <p className="text-xs text-text-alt mt-0.5">Please confirm your action to proceed.</p>
          </div>
        </div>

        {/* Message */}
        <p className="text-sm text-text-alt leading-relaxed bg-bg/50 p-4 rounded-xl border border-text/5">
          {message}
        </p>

        {/* Footer buttons */}
        <div className="flex items-center justify-end gap-3 pt-2">
          <Button
            text={cancelText}
            variant="outline"
            color="secondary"
            size="sm"
            onClick={onCancel}
            disabled={loading}
            className="rounded-xl px-5"
          />
          <Button
            text={confirmText}
            variant="filled"
            color={isDanger ? 'secondary' : 'primary'}
            size="sm"
            loading={loading}
            onClick={onConfirm}
            className={`rounded-xl px-6 font-semibold ${isDanger ? 'bg-red-600 hover:bg-red-700 text-white border-none' : ''}`}
          />
        </div>
      </div>
    </div>
  );
};

export default ConfirmationModal;
