import { env } from "cloudflare:workers";
import { Container, getContainer } from "@cloudflare/containers";
import { getDailyTRM, getMonthlyInflation } from "./scheduledTask";


export interface Env {
  BANREPCO_API_CACHE: KVNamespace;
  API_CONTAINER: DurableObjectNamespace<Container>;
  BANREP_WEB_SERVICE_URL: string;
  INFLATION_WEB_SERVICE_URL: string;
  CACHE_EXPIRATION_TTL?: string;
  ENVIRONMENT?: string;
  DATABASE_URL: string;
  DATABASE_AUTH_TOKEN: string;
}

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
    switch (controller.cron) {
      case "0 5 * * *": // Every day at 5 AM
        await getDailyTRM(env);
        break;
      case "0 5 15 * *": // On the 15th of every month at 5 AM
        await getMonthlyInflation(env);
        break;
    }

  },


  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/v1")) {
      const cacheKey = url.toString();
      // Check cache first
      let cacheData = await env.BANREPCO_API_CACHE.get(cacheKey, { type: "json" });
      if (!cacheData) {
        const { "session-id": sessionId } = await request.json();
        const containerInstance = getContainer(env.MY_CONTAINER, sessionId);
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
