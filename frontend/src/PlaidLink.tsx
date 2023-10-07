interface Props {
  open: Function;
  ready: boolean;
  fetchLinkToken: Function;
}

export default function PlaidLink({ open, ready, fetchLinkToken }: Props) {
  return (
    <button onClick={() => fetchLinkToken()}>
      <strong>Link account</strong>
    </button>
  );
}
