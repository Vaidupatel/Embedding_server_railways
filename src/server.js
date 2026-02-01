import express from 'express';
import { embedTexts } from './embedder.js';
import { requireAuth } from './auth.js';
import { CONFIG } from './config.js';

const app = express();
app.use(express.json({ limit: '1mb' }));

/**
 * Health check
 */
app.get('/health', (_req, res) => {
    res.json({ status: 'ok' });
});

/**
 * Embedding endpoint
 */
app.post('/embed', requireAuth, async (req, res) => {
    try {
        const { texts, normalize = true } = req.body;

        if (!Array.isArray(texts)) {
            return res.status(400).json({ error: '`texts` must be an array' });
        }

        if (texts.length === 0) {
            return res.status(400).json({ error: '`texts` cannot be empty' });
        }

        if (texts.length > CONFIG.MAX_CHUNKS) {
            return res.status(400).json({
                error: `Max ${CONFIG.MAX_CHUNKS} chunks allowed`
            });
        }

        for (const t of texts) {
            if (typeof t !== 'string') {
                return res.status(400).json({
                    error: 'All chunks must be strings'
                });
            }
        }

        const embeddings = await embedTexts(texts, normalize);

        res.json({
            model: CONFIG.MODEL_ID,
            dimensions: CONFIG.EMBEDDING_DIM,
            count: embeddings.length,
            embeddings
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Embedding failed' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Embedding service running on port ${PORT}`);
});
