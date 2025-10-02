import { createClient } from '@libsql/client';

export interface DbConfig {
  url: string;
  authToken: string;
}

export class DbService {
  private client;

  constructor(config: DbConfig) {
    this.client = createClient({
      url: config.url,
      authToken: config.authToken
    });
  }

  async trmExistsForDate(date: string): Promise<boolean> {
    try {
      const result = await this.client.execute({
        sql: 'SELECT COUNT(*) as count FROM trm WHERE DATE(date) = DATE(?)',
        args: [date]
      });

      return (result.rows[0].count as number) > 0;
    } catch (error) {
      console.error('Error checking TRM existence:', error);
      throw error;
    }
  }

  async insertTRM(value: number): Promise<void> {
    try {
      const date = new Date().toISOString().split('T')[0]; // Get only the date part
      const exists = await this.trmExistsForDate(date);

      if (exists) {
        console.log('TRM record already exists for today');
        return;
      }

      const id = crypto.randomUUID();

      await this.client.execute({
        sql: 'INSERT INTO trm (id, value, date) VALUES (?, ?, ?)',
        args: [id, value, date]
      });
    } catch (error) {
      console.error('Error inserting TRM value:', error);
      throw error;
    }
  }
}
