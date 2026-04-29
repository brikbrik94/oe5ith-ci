/**
 * OE5ITH CI — Toast
 * Kurze Status-Meldungen, auto-dismiss, stapelbar.
 *
 * CSS: css/toast.css (muss eingebunden sein)
 *
 * Verwendung:
 *   import { toast } from './toast';
 *
 *   toast.success('Gespeichert');
 *   toast.danger('Fehler beim Laden');
 *   toast.info('Update verfügbar', { body: 'Version 2.1.0 ist bereit.' });
 *   const dismiss = toast.warning('Verbindung instabil', { duration: 0 });
 *   dismiss(); // manuell schließen
 */

export type ToastType = 'success' | 'warning' | 'danger' | 'info';

export interface ToastAction {
  label: string;
  onClick: () => void;
}

export interface ToastOptions {
  /** Variante — bestimmt Farbe und Icon. Default: 'info' */
  type?: ToastType;
  /** Pflichtfeld: kurze Hauptmeldung */
  text: string;
  /** Nur .toast--rich: ausführlicherer Beschreibungstext */
  body?: string;
  /** Nur .toast--rich: optionaler Action-Button */
  action?: ToastAction;
  /** Auto-dismiss Dauer in ms. 0 = kein Auto-dismiss. Default: 4000 */
  duration?: number;
}

/** Rückgabewert von show() — rufe auf um den Toast manuell zu schließen */
export type DismissFn = () => void;

const ICONS: Record<ToastType, string> = {
  success: '✔',
  warning: '⚠',
  danger:  '✖',
  info:    'ℹ',
};

export class ToastManager {
  private container: HTMLElement | null = null;

  private getContainer(): HTMLElement {
    if (!this.container || !this.container.isConnected) {
      this.container = document.createElement('div');
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    }
    return this.container;
  }

  show(options: ToastOptions): DismissFn {
    const { type = 'info', text, body, action, duration = 4000 } = options;
    const isRich = !!(body || action);

    const toast = document.createElement('div');
    toast.className = `toast toast--${type}${isRich ? ' toast--rich' : ''}`;
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.setAttribute('aria-atomic', 'true');

    // ── Hauptzeile ──
    const main = document.createElement('div');
    main.className = 'toast-main';

    const icon = document.createElement('span');
    icon.className = 'toast-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = ICONS[type];

    const textEl = document.createElement('span');
    textEl.className = 'toast-text';
    textEl.textContent = text;

    const closeBtn = document.createElement('button');
    closeBtn.className = 'toast-close';
    closeBtn.setAttribute('aria-label', 'Schließen');
    closeBtn.textContent = '✕';
    closeBtn.type = 'button';

    main.append(icon, textEl, closeBtn);
    toast.appendChild(main);

    // ── Rich: Body-Text ──
    if (body) {
      const bodyEl = document.createElement('p');
      bodyEl.className = 'toast-body';
      bodyEl.textContent = body;
      toast.appendChild(bodyEl);
    }

    // ── Rich: Action-Button ──
    if (action) {
      const actionBtn = document.createElement('button');
      actionBtn.className = 'toast-action';
      actionBtn.textContent = action.label;
      actionBtn.type = 'button';
      actionBtn.addEventListener('click', () => {
        action.onClick();
        dismiss();
      });
      toast.appendChild(actionBtn);
    }

    // ── Einfügen (neueste oben) ──
    const container = this.getContainer();
    container.prepend(toast);

    // ── Eintritts-Animation (doppeltes rAF erzwingt reflow) ──
    requestAnimationFrame(() => {
      requestAnimationFrame(() => toast.classList.add('toast--visible'));
    });

    // ── Dismiss ──
    let timer: ReturnType<typeof setTimeout> | null = null;

    const dismiss: DismissFn = () => {
      if (timer !== null) {
        clearTimeout(timer);
        timer = null;
      }
      toast.classList.remove('toast--visible');
      toast.classList.add('toast--hiding');
      toast.addEventListener(
        'transitionend',
        (e) => { if (e.propertyName === 'opacity') toast.remove(); },
        { once: true }
      );
    };

    closeBtn.addEventListener('click', dismiss);

    if (duration > 0) {
      timer = setTimeout(dismiss, duration);
    }

    return dismiss;
  }

  success(text: string, options?: Omit<ToastOptions, 'type' | 'text'>): DismissFn {
    return this.show({ ...options, type: 'success', text });
  }

  warning(text: string, options?: Omit<ToastOptions, 'type' | 'text'>): DismissFn {
    return this.show({ ...options, type: 'warning', text });
  }

  danger(text: string, options?: Omit<ToastOptions, 'type' | 'text'>): DismissFn {
    return this.show({ ...options, type: 'danger', text });
  }

  info(text: string, options?: Omit<ToastOptions, 'type' | 'text'>): DismissFn {
    return this.show({ ...options, type: 'info', text });
  }
}

/** Singleton — direkt importieren und verwenden */
export const toast = new ToastManager();
export default toast;
