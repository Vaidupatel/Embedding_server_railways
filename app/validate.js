export function validatePayload(body) {
    if (!body || !Array.isArray(body.texts)) {
        return "texts must be an array";
    }

    if (body.texts.length === 0) {
        return "texts cannot be empty";
    }

    if (body.texts.length > 40) {
        return "Max 40 chunks allowed per request";
    }

    for (const t of body.texts) {
        if (typeof t !== "string" || !t.trim()) {
            return "All texts must be non-empty strings";
        }
    }

    return null;
}
