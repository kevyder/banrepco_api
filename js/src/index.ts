import { env } from "cloudflare:workers";
import { Container, getRandom } from "@cloudflare/containers";

export interface Env {
  BANREPCO_API_CACHE: KVNamespace;
}

const INSTANCE_COUNT = 3;
const CACHE_EXPIRATION_TTL = parseInt(env.CACHE_EXPIRATION_TTL || "60"); // Default to 1 hour

export class APIContainer extends Container {
  defaultPort = 3000;
  sleepAfter = "5m";
  envVars = {
    ENVIRONMENT: env.ENVIRONMENT,
    DATABASE_URL: env.DATABASE_URL,
    DATABASE_AUTH_TOKEN: env.DATABASE_AUTH_TOKEN,
  };

  onError(error: unknown) {
    console.error(error);
  }

  onStart() {
    console.log("Container started");
  }

  onStop() {
    console.log("Container stopped");
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/v1")) {
      // Check cache first
      let cacheData = await env.BANREPCO_API_CACHE.get(url, { type: "json" });
      if (!cacheData) {
        const containerInstance = await getRandom(env.API_CONTAINER, INSTANCE_COUNT);
        const response = await containerInstance.fetch(request);
        const responseData = await response.clone().text();
        await env.BANREPCO_API_CACHE.put(url, responseData, { expirationTtl: CACHE_EXPIRATION_TTL });
        return response;
      } else {
        return new Response(JSON.stringify(cacheData), {
          headers: { "Content-Type": "application/json" },
        });
      }
    }

    return new Response("Not found", { status: 404 });
  },
};