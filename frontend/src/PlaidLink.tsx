interface Props {
  fetchLinkToken: Function;
}

export default function PlaidLink({fetchLinkToken }: Props) {
  return (
    <button onClick={() => fetchLinkToken()}>
      <strong>Link account</strong>
    </button>
  );
}
