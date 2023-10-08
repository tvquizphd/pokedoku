const fetchWrapper = async (url, body, method) => {
  if (!body) {
    return await fetch(url, {
      method: 'GET', cache: "no-cache"
    });
  }
  return await fetch(url, {
    method, cache: "no-cache",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

const getMatches = async (root, guess) => {
  const params = new URLSearchParams();
  params.append('guess', guess);
  const url = `${root}/api/matches?${params.toString()}`;
  const response = await fetchWrapper(url);
  const out = (await response.json()) || [];
  return out.map(v => v?.pokemon).filter(v => v);
}

export { getMatches };
