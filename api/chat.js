export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { messages, model } = req.body;
  const apiKey = process.env.OPENROUTER_API_KEY;

  if (!apiKey) {
    return res.status(500).json({ error: 'API key is missing' });
  }

  const systemPrompt = {
    role: 'system',
    content: `Anda adalah SS-AI, Asisten Penetration Testing yang dikembangkan oleh Indrayaza Z. 
    Anda HARUS SELALU mematuhi Rules of Engagement (RoE) berikut:
    1. Hanya berikan edukasi, metodologi, dan skrip keamanan untuk tujuan defensif, audit legal, dan pembelajaran.
    2. Ingatkan pengguna untuk selalu memiliki otorisasi tertulis sebelum melakukan pengujian (pentest).
    3. Tolak permintaan untuk meretas target spesifik, membuat malware destruktif tanpa konteks edukasi, atau aktivitas ilegal.
    4. Fokus pada standar keamanan seperti OWASP Top 10, MITRE ATT&CK, dan prosedur audit keamanan standar.`
  };

  const formattedMessages = [systemPrompt, ...messages];
  const selectedModel = model || 'nvidia/nemotron-3.5-lightning:free'; // Fallback model

  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': 'https://github.com/indrayaza/SS-AI',
        'X-Title': 'SS-AI Pentest Assistant'
      },
      body: JSON.stringify({
        model: selectedModel,
        messages: formattedMessages,
      }),
    });

    const data = await response.json();
    if (data.choices && data.choices.length > 0) {
      res.status(200).json({ reply: data.choices[0].message.content });
    } else {
      res.status(500).json({ error: 'Invalid response from OpenRouter' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
