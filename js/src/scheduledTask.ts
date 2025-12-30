import { fetchLatestTRM } from './services/trm';
import { fetchLatestInflation } from './services/inflation';
import { DbService } from './services/db';

export async function getDailyTRM(env: Env) {
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
}


export async function getMonthlyInflation(env: Env) {
  const inflationWebServiceUrl = env.INFLATION_WEB_SERVICE_URL
  const inflationData = await fetchLatestInflation(inflationWebServiceUrl);
  console.log("Inflation Data:", inflationData);

  if (env.DATABASE_URL && env.DATABASE_AUTH_TOKEN) {
    const dbService = new DbService({
      url: env.DATABASE_URL,
      authToken: env.DATABASE_AUTH_TOKEN
    });

    await dbService.insertInflation(
      inflationData.year,
      inflationData.month,
      inflationData.inflation,
      inflationData.target
    );

    console.log("Inflation data stored in database successfully");
  } else {
    console.error('Database configuration not found in environment variables');
  }
}
