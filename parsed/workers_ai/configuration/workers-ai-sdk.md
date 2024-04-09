# Workers AI SDK
The Workers AI SDK provides an interface between a [Worker](/workers/) or [Pages Function](/pages/functions/) and Workers AI.
The Workers AI SDK makes Workers AI APIs available for use in your code. To import the Workers AI SDK, run:
```sh
$ npm install --save-dev @cloudflare/ai
```
```sh
$ yarn add --dev @cloudflare/ai
```
Import the library in your code:
```javascript
import { Ai } from "@cloudflare/ai";
```
Workers AI is iterating rapidly. Ensure you're using the latest version of `@cloudflare/ai` in your Workers' scripts to take advantage of our latest models and features. Type `npm update @cloudflare/ai --save-dev` to update the package.
## Constructor
### new `Ai()`
`new Ai()` creates a new `Ai` instance:
```javascripthiglight: [1, 11]import { Ai } from "@cloudflare/ai";
export interface Env {
  // If you set another name in wrangler.toml as the value for 'binding',
  // replace "AI" with the variable name you defined.
  AI: any;
}
export default {
  async fetch(request: Request, env: Env) {
    const ai = new Ai(env.AI);
    const response = await ai.run('@cf/meta/llama-2-7b-chat-int8', {
        prompt: "What is the origin of the phrase Hello, World"
      }
    );
    return new Response(JSON.stringify(response));
  },
};
```
**env.AI** is the [AI binding](/workers-ai/configuration/bindings/) defined in your `wrangler.toml` configuration.
## Methods
### async ai.run()
`async ai.run()` is a method of the class instance created by `new Ai()`.
`async ai.run()` runs a model. Takes a model as the first parameter, and an object as the second parameter.
```javascript
import { Ai } from '@cloudflare/ai'
// sessionOptions are optional
const ai = new Ai(env.AI, { sessionOptions: { ctx }});
const answer = ai.run('@cf/meta/llama-2-7b-chat-int8', {
    prompt: "What is the origin of the phrase 'Hello, World'"
});
```
**Parameters**
- `model` string required
  - The model to run.
- `options` object depends on the model
  - Depends on the model type.
  **Supported options**
  - `stream` boolean optional
    - Returns a stream of results as they are available.
Optionally, you can pass a `stream` property to the `options` object. This will return a stream of results as they are available.
```javascript
import { Ai } from '@cloudflare/ai'
// sessionOptions are optional
const ai = new Ai(env.AI, { sessionOptions: { ctx }});
const answer = await ai.run('@cf/meta/llama-2-7b-chat-int8', {
    prompt: "What is the origin of the phrase 'Hello, World'",
    stream: true
});
return new Response(answer, {
    headers: { "content-type": "text/event-stream" }
});
```