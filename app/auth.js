import dotenv from "dotenv";
dotenv.config()

const API_TOKEN = process.env.API_TOKEN;

export function verifyAuth(req, reply) {
    const auth = req.headers.authorization || "";
    if (!auth.startsWith("Bearer ")) {
        reply.code(401).send({ error: "Unauthorized" });
        return;
    }

    const token = auth.split(" ")[1];
    if (token !== API_TOKEN) {
        reply.code(403).send({ error: "Forbidden" });
    }
}
