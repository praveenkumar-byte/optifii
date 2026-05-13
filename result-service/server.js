const express = require('express');
const { Pool } = require('pg');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const PORT = process.env.PORT || 4000;
const POLL_INTERVAL = parseInt(process.env.POLL_INTERVAL || '1000');

// PostgreSQL connection pool
const pool = new Pool({
  host:     process.env.DB_HOST     || 'db',
  port:     parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME     || 'votes',
  user:     process.env.DB_USER     || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
  max: 5,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'result' });
});

app.get('/api/results', async (req, res) => {
  try {
    const result = await queryResults();
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

async function queryResults() {
  const client = await pool.connect();
  try {
    const { rows } = await client.query(`
      SELECT vote, COUNT(id) AS count
      FROM votes
      GROUP BY vote
    `);
    const totals = { a: 0, b: 0, total: 0 };
    rows.forEach(row => {
      totals[row.vote] = parseInt(row.count);
      totals.total += parseInt(row.count);
    });
    return {
      a: totals.a,
      b: totals.b,
      total: totals.total,
      pct_a: totals.total > 0 ? ((totals.a / totals.total) * 100).toFixed(1) : 0,
      pct_b: totals.total > 0 ? ((totals.b / totals.total) * 100).toFixed(1) : 0,
    };
  } finally {
    client.release();
  }
}

// Push live results to all connected clients via WebSocket
async function broadcastResults() {
  try {
    const data = await queryResults();
    io.emit('scores', data);
  } catch (err) {
    console.error('DB query failed:', err.message);
  }
}

io.on('connection', (socket) => {
  console.log(`Client connected: ${socket.id}`);
  broadcastResults(); // send immediately on connect
});

setInterval(broadcastResults, POLL_INTERVAL);

server.listen(PORT, () => {
  console.log(`result-service listening on :${PORT}`);
});
