export function KeystoneMark({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <path d="M4 26V14L16 6L28 14V26H22V18H10V26H4Z" stroke="#1c1915" strokeWidth="1.6" />
      <path d="M13 18V12.5L16 10.5L19 12.5V18H13Z" fill="#c45c26" />
    </svg>
  );
}
