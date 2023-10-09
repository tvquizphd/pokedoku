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

const getRegions = async (root, guess) => {
  const url = `${root}/api/regions`;
  const response = await fetchWrapper(url);
  const out = (await response.json()) || [];
  return out.map(v => v?.region).filter(v => v);
}

const getForms = async (root, guess) => {
  const params = new URLSearchParams();
  params.append('dexn', guess);
  const url = `${root}/api/forms?${params.toString()}`;
  const response = await fetchWrapper(url);
  const out = (await response.json()) || [];
  return out.map(v => v?.form).filter(v => v);
}

const getMatches = async (root, guess) => {
  const params = new URLSearchParams();
  params.append('guess', guess);
  const url = `${root}/api/matches?${params.toString()}`;
  const response = await fetchWrapper(url);
  const out = (await response.json()) || [];
  return out.map(v => v?.pokemon).filter(v => v);
}

const testGuess = async (root, identifier, conditions) => {
  const params = new URLSearchParams();
  params.append('identifier', identifier);
  params.append('conditions', conditions.join(','));
  const url = `${root}/api/test?${params.toString()}`;
  const response = await fetchWrapper(url);
  const out = (await response.json()) || {};
  return out?.ok || false;
}

export { testGuess, getMatches, getForms, getRegions };
