interface Props {
  open: Function;
  ready: boolean
}

export default function PlaidLink({open, ready }: Props) {
  return (
    <button onClick={() => open()} disabled={!ready}>
      <strong>Link account</strong>
    </button>
  );
}
