import { NestFactory } from '@nestjs/core';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Setup para documentação de endpoints com Swagger
  const config = new DocumentBuilder()
    .setTitle('Integration Service')
    .setDescription(
      'Serviço para integrar as aplicações desktop ao Banco de dados unificado e ao dashboard de métricas.',
    )
    .setVersion('0.0.1')
    .build();
  const documentFactory = () => SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, documentFactory);

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
