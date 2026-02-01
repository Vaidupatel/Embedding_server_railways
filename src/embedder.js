import { pipeline } from '@huggingface/transformers';
import { CONFIG } from './config.js';

let extractorPromise = null;

/**
 * Singleton model loader
 */
async function getExtractor() {
    if (!extractorPromise) {
        extractorPromise = pipeline(
            'feature-extraction',
            CONFIG.MODEL_ID
        );
    }
    return extractorPromise;
}

/**
 * Embed texts ONE BY ONE, return ALL
 */
export async function embedTexts(texts, normalize = true) {
    const extractor = await getExtractor();
    const embeddings = [];

    for (const text of texts) {
        const output = await extractor(text, {
            pooling: 'mean',
            normalize
        });

        // output is a Tensor
        embeddings.push(output.tolist()[0]);
    }

    return embeddings;
}
