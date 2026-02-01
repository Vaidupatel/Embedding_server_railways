import dotenv from "dotenv";
import Fastify from "fastify";
import { verifyAuth } from "./auth.js";
import { embedTexts } from "./embedder.js";
import { validatePayload } from "./validate.js";

dotenv.config()
const app = Fastify({ logger: false });

app.get("/health", async () => {
    return { status: "ok" };
});

app.post("/embed", { preHandler: verifyAuth }, async (req, reply) => {
    const error = validatePayload(req.body);
    if (error) {
        return reply.code(400).send({ error });
    }

    const { texts, normalize = true } = req.body;

    const embeddings = await embedTexts(texts, normalize);

    return {
        model: "bge-small-en-v1.5",
        dimensions: embeddings[0].length,
        count: embeddings.length,
        embeddings
    };
});

const port = process.env.PORT || 3000;
app.listen({ port, host: "0.0.0.0" });
