import { Body, Controller, Get, Post } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('/status')
  getStatus(): string {
    return this.appService.getStatus();
  }

  @Post('/postdata')
  postDataFetch(@Body() dataFromDesktop: Record<string, unknown>): Record<string, unknown> {
    return this.appService.postDataFetch(dataFromDesktop);
  }

  @Get('/data')
  getDataFetch(): string {
    return this.appService.getDataFetch();
  }
}
