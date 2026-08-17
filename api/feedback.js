// Vercel Serverless Function - Feedback & Bug Report Collector
module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const data = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    console.log('[LAPTOP-REPORT-VN REPORT RECEIVED]', JSON.stringify(data, null, 2));

    // Optional: Forward to Discord / Telegram webhook if env var exists
    if (process.env.DISCORD_WEBHOOK_URL) {
      try {
        await fetch(process.env.DISCORD_WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            content: `🚨 **Báo cáo mới [${data.code || 'LRVN'}]**\n- **Loại:** ${data.type} (${data.topic})\n- **Người gửi:** ${data.name}\n- **Máy:** ${data.deviceName || 'N/A'}\n- **Shop:** ${data.shop || 'N/A'}\n- **Giá:** ${data.price || 'N/A'}\n- **Link:** ${data.url || 'N/A'}\n- **Mô tả:** ${data.desc}\n- **Thời gian:** ${data.time}`
          })
        });
      } catch (e) {
        console.error('Webhook relay note:', e);
      }
    }

    return res.status(200).json({
      status: 'success',
      message: 'Báo cáo đã được ghi nhận thành công!',
      code: data.code
    });
  } catch (error) {
    console.error('Error handling report:', error);
    return res.status(500).json({ error: 'Internal Server Error', details: error.message });
  }
};
