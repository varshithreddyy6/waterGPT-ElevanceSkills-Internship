export function nowTime() {
  return new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function percentage(part, total) {
  if (!total) return 0;
  return Math.round((part / total) * 100);
}

export function languageLabel(code) {
  return code.toUpperCase().slice(0, 2);
}