import { CONFIG } from './config.js';

export function requireAuth(req, res, next) {
    const auth = req.headers.authorization || '';
    const token = auth.startsWith('Bearer ') ? auth.split(" ")[1] : null;

    if (token !== CONFIG.AUTH_TOKEN) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    next();
}
