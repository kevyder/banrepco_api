import { env } from "cloudflare:workers";
import { Container, getRandom } from "@cloudflare/containers";


const INSTANCE_COUNT = 3;

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
      // note: "getRandom" to be replaced with latency-aware routing in the near future
      const containerInstance = await getRandom(env.API_CONTAINER, INSTANCE_COUNT);
      return containerInstance.fetch(request);
    }

    return new Response("Not found", { status: 404 });
  },
};