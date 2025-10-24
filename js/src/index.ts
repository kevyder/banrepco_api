import { env } from "cloudflare:workers";
import { Container, getRandom } from "@cloudflare/containers";
import { fetchLatestTRM } from './services/trm';
import { DbService } from './services/db';

export interface Env {
  BANREPCO_API_CACHE: KVNamespace;
  API_CONTAINER: DurableObjectNamespace<Container>;
  BANREP_WEB_SERVICE_URL: string;
  INSTANCE_COUNT?: string;
  CACHE_EXPIRATION_TTL?: string;
  ENVIRONMENT?: string;
  DATABASE_URL: string;
  DATABASE_AUTH_TOKEN: string;
}

const INSTANCE_COUNT = parseInt(env.INSTANCE_COUNT || "10");
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

  async scheduled(
    controller: ScheduledController,
    env: Env,
    ctx: ExecutionContext,
  ) {
    try {
      const banrepWebServiceUrl = env.BANREP_WEB_SERVICE_URL
      const trmValue = await fetchLatestTRM(banrepWebServiceUrl);
      console.log("TRM Value:", trmValue);

      if (env.DATABASE_URL && env.DATABASE_AUTH_TOKEN) {
        const dbService = new DbService({
          url: env.DATABASE_URL,
          authToken: env.DATABASE_AUTH_TOKEN
        });

        await dbService.insertTRM(trmValue);
        console.log("TRM value stored in database successfully");
      } else {
        console.error('Database configuration not found in environment variables');
      }
    } catch (error) {
      console.error('Failed to fetch and store TRM:', error);
    }
  },


  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/v1")) {
      const cacheKey = url.toString();
      // Check cache first
      let cacheData = await env.BANREPCO_API_CACHE.get(cacheKey, { type: "json" });
      if (!cacheData) {
        const containerInstance = await getRandom(env.API_CONTAINER, INSTANCE_COUNT);
        const response = await containerInstance.fetch(request);
        const responseData = await response.clone().text();
        await env.BANREPCO_API_CACHE.put(cacheKey, responseData, { expirationTtl: CACHE_EXPIRATION_TTL });
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
