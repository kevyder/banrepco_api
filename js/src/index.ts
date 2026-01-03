import { getDailyTRM, getMonthlyInflation } from "./scheduledTask";


export interface Env {
  BANREP_WEB_SERVICE_URL: string;
  INFLATION_WEB_SERVICE_URL: string;
  ENVIRONMENT?: string;
  DATABASE_URL: string;
  DATABASE_AUTH_TOKEN: string;
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
    return new Response("Not found", { status: 404 });
  },
};
