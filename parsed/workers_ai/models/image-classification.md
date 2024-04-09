# Image Classification
Image classification models take an image input and assigns it labels or classes.
* Task type: **image-classification**
* TypeScript class: **AiImageClassification**
Workers AI is iterating rapidly. Ensure you're using the latest version of `@cloudflare/ai` in your Workers' scripts to take advantage of our latest models and features. Type `npm update @cloudflare/ai --save-dev` to update the package.
## Available models
List of available Image Classification models:
| Model ID                        | Description                   |
| ------------------------------- | ----------------------------- |
| `@cf/microsoft/resnet-50`                   | 50 layers deep image classification CNN trained on more than 1M images from ImageNet<br/>[More information](https://www.microsoft.com/en-us/research/blog/microsoft-vision-model-resnet-50-combines-web-scale-data-and-multi-task-learning-to-achieve-state-of-the-art/)<br/>  |
## Examples
```ts
import { Ai } from '@cloudflare/ai'
export interface Env {
  AI: any;
}
export default {
  async fetch(request: Request, env: Env) {
    const res: any = await fetch("https://cataas.com/cat");
    const blob = await res.arrayBuffer();
    const ai = new Ai(env.AI);
    const inputs = {
        image: [...new Uint8Array(blob)],
    };
    const response = await ai.run("@cf/microsoft/resnet-50", inputs);
    return new Response(JSON.stringify({ inputs: { image: [] }, response }));
  }
}
```
```sh
$ curl https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/microsoft/resnet-50 \
    -X POST \
    -H "Authorization: Bearer {API_TOKEN}" \
    --data-binary @orange-llama.png
```
**Example Workers AI response**
```json
[
  { "label":"PERSIAN CAT" ,"score":0.4071170687675476 },
  { "label":"PEKINESE", "score":0.23444877564907074 },
  { "label":"FEATHER BOA", "score":0.22562485933303833 },
  { "label":"POMERANIAN", "score":0.033316344022750854 },
  { "label":"JAPANESE SPANIEL", "score":0.024184171110391617 }
]
```
## API schema
The following schema is based on [JSON Schema](https://json-schema.org/)
### Input
```json
{
  "oneOf": [
    {
      "type": "string",
      "format": "binary"
    },
    {
      "type": "object",
      "properties": {
        "image": {
          "type": "array",
          "items": {
            "type": "number"
          }
        }
      }
    }
  ]
}
```
TypeScript class: **AiImageClassificationInput**
### Output
```json
{
  "type": "array",
  "contentType": "application/json",
  "items": {
    "type": "object",
    "properties": {
      "score": {
        "type": "number"
      },
      "label": {
        "type": "string"
      }
    }
  }
}
```
TypeScript class: **AiImageClassificationOutput**