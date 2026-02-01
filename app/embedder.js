import { pipeline } from "@huggingface/transformers";

let extractorPromise = null;

async function loadModel() {
    if (!extractorPromise) {
        extractorPromise = pipeline(
            "feature-extraction",
            "Xenova/bge-small-en-v1.5"
        );
    }
    return extractorPromise;
}

export async function embedTexts(texts, normalize = true) {
    const extractor = await loadModel();
    const embeddings = [];

    // ONE BY ONE embedding (your requirement)
    for (const text of texts) {
        const output = await extractor(text, {
            pooling: "mean",
            normalize
        });

        embeddings.push(output.tolist()[0]);
    }

    return embeddings;
}
