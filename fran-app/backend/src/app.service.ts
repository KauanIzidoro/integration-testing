import { Injectable } from '@nestjs/common';
import { ok } from 'assert';
import { query } from 'express';

@Injectable()
export class AppService {
  getStatus(): string {
    return 'STATUS: OK';
  }

  postDataFetch(dataFromDesktop): Record<string,unknown> {
    return dataFromDesktop;
  }

  getDataFetch(): string {
    return 'Data fetched successfully';
  }
}
