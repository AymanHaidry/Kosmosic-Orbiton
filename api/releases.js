// api/releases.js
export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const githubRes = await fetch(
      'https://api.github.com/repos/AymanHaidry/Kosmosic-Orbiton/releases/latest',
      {
        headers: {
          'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github+json',
          'X-GitHub-Api-Version': '2022-11-28',
          'User-Agent': 'Orbiton-Website'
        }
      }
    );

    if (!githubRes.ok) {
      const error = await githubRes.text();
      return res.status(githubRes.status).json({ error, status: githubRes.status });
    }

    const data = await githubRes.json();
    res.status(200).json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
