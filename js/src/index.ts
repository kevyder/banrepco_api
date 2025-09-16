import { env } from "cloudflare:workers";
import { Container, getRandom } from "@cloudflare/containers";
import { Hono } from "hono";


export class MyContainer extends Container {
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

const app = new Hono<{
  Bindings: { MY_CONTAINER: DurableObjectNamespace<MyContainer> };
}>();

// Load balance all requests across multiple containers
app.get("*", async (c) => {
  const container = await getRandom(c.env.MY_CONTAINER, 3);
  return await container.fetch(c.req.raw);
});

export default app;