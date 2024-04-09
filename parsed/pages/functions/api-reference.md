# API reference
The following methods can be used to configure your Pages Function.
## Methods
### `onRequests`
- onRequest(context[EventContext](#eventcontext)) Response | Promise&lt;Response&gt;
  - This function will be invoked on all requests no matter the request method.
- onRequestGet(context[EventContext](#eventcontext)) Response | Promise&lt;Response&gt;
  - This function will be invoked on all `GET` requests.
- onRequestPost(context[EventContext](#eventcontext)) Response | Promise&lt;Response&gt;
  - This function will be invoked on all `POST` requests.
- onRequestPatch(context[EventContext](#eventcontext)) Response | Promise&lt;Response&gt;
  - This function will be invoked on all `PATCH` requests.
- onRequestPut(context[EventContext](#eventcontext)) Response | Promise&lt;Response&gt;
  - This function will be invoked on all `PUT` requests.
- onRequestDelete(context[EventContext](#eventcontext)) Response | Promise&lt;Response&gt;
  - This function will be invoked on all `DELETE` requests.
- onRequestHead(context[EventContext](#eventcontext)) Response | Promise&lt;Response&gt;
  - This function will be invoked on all `HEAD` requests.
- onRequestOptions(context[EventContext](#eventcontext)) Response | Promise&lt;Response&gt;
  - This function will be invoked on all `OPTIONS` requests.
### `env.ASSETS.fetch()`
The `env.ASSETS.fetch()` function allows you to fetch a static asset from your Pages project.
You can pass a [Request object](/workers/runtime-apis/request/), URL string, or URL object to `env.ASSETS.fetch()` function. The URL must be to the pretty path, not directly to the asset. For example, if you had the path `/users/index.html`, you will request `/users/` instead of `/users/index.html`. This method call will run the header and redirect rules, modifying the response that is returned.
## Types
### `EventContext`
The following are the properties on the `context` object which are passed through on the `onRequest` methods:
  - `request` [Request](/workers/runtime-apis/request/)
 
      This is the incoming [Request](/workers/runtime-apis/request/).
  
  - `functionPath` string
  
      This is the path of the request. 
    
  - waitUntil(promisePromise&lt;any&gt;) void
  
      Refer to [`waitUntil` documentation](/workers/runtime-apis/handlers/fetch/#contextwaituntil) for more information.
  
  - passThroughOnException() void
  
      Refer to [`passThroughOnException` documentation](/workers/runtime-apis/handlers/fetch/#contextpassthroughonexception) for more information. Note that this will not work on an [advanced mode project](/pages/functions/advanced-mode/).
  
  - next(input?Request | string, init?RequestInit) Promise&lt;Response&gt;
  
      Passes the request through to the next Function or to the asset server if no other Function is available. 
  
  - `env` [EnvWithFetch](#envwithfetch)
  - `params` Params&lt;P&gt;
      Holds the values from [dynamic routing](/pages/functions/routing/#dynamic-routes).
      In the following example, you have a dynamic path that is `/users/[user].js`. When you visit the site on `/users/nevi` the `params` object would look like:
      ```js
      {
        user: "nevi"
      }
      ```
      This allows you fetch the dynamic value from the path:
      ```js
      export function onRequest(context) {
        return new Response(`Hello ${context.params.user}`);
      }
      ```
      Which would return `"Hello nevi"`.
  - `data` Data
  
### `EnvWithFetch`
Holds the environment variables, secrets, and bindings for a Function. This also holds the `ASSETS` binding which is how you can fallback to the asset-serving behavior.