// Stand-in for the chrome.* APIs so the real popup.html renders outside Chrome.
// Used only to produce store screenshots; not part of the extension package.
(() => {
  const view = (location.hash || '').slice(1);
  const reply = (msg) => {
    if (Array.isArray(msg)) {
      if (msg[1] === 'reports::getState') return [msg[0], { config: { enabled: false, key: '' }, state: {} }];
      return [msg[0], {}];
    }
    if (msg && msg.type === 'get_enabled') return { type: 'ok', enabled: false };
    return undefined;
  };
  window.chrome = {
    runtime: {
      lastError: undefined,
      getURL: (p) => p,
      sendMessage: (msg, cb) => { if (typeof cb === 'function') setTimeout(() => cb(reply(msg)), 0); }
    },
    storage: { local: { get: async () => ({}), set: async () => ({}) } }
  };
  // no CSS transitions, so a capture never catches a switch mid-animation
  document.addEventListener('DOMContentLoaded', () => {
    const s = document.createElement('style');
    s.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}';
    document.head.appendChild(s);
  });
  document.addEventListener('DOMContentLoaded', () => setTimeout(() => {
    const id = view === 'reports' ? 'open_reports' : view === 'timeouts' ? 'open_timeouts' : null;
    if (id) document.getElementById(id)?.click();
  }, 80));
})();
