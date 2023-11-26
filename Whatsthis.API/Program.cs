using System.Reflection;
using Microsoft.OpenApi.Models;
using WhatsthisAPI.Service;
using WhatsthisAPI.Models;

string version = "0.3.0";

IConfigurationRoot configuration = new ConfigurationBuilder()
	.AddJsonFile("appsettings.json", optional: true)
	.AddJsonFile($"appsettings.{Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production"}.json", optional: true)
	.AddEnvironmentVariables()
	.Build();

WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(config =>
{
	config.SwaggerDoc("v1", new OpenApiInfo
	{
		Title = "What's This? API",
		Description = "Inspection application that detects web technologies and informs the user of them.",
		Version = version,
		Contact = new OpenApiContact
		{
			Name = "soup-bowl",
			Url = new Uri("https://soupbowl.io")
		},
		License = new OpenApiLicense
		{
			Name = "MIT",
			Url = new Uri("https://github.com/whatsth-is/api.whatsth.is/blob/main/LICENSE")
		}
	});

	string xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
	string xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
	config.IncludeXmlComments(xmlPath);
});

builder.Services.AddSingleton<IConfigurationService, ConfigurationService>();

builder.Services.AddCors(options =>
{
	options.AddPolicy("AllowAllOrigins",
		builder =>
		{
			builder.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod();
		});
});

string? redisURL = configuration.GetValue<string>("REDIS_URL");
if (!string.IsNullOrEmpty(redisURL))
{
	builder.Services.AddStackExchangeRedisCache(options =>
	{
		options.Configuration = redisURL;
		options.InstanceName = $"wapi{version.Replace(".", string.Empty)}:";
	});
}
else
{
	builder.Services.AddDistributedMemoryCache();
}

WebApplication app = builder.Build();

app.UseCors("AllowAllOrigins");

app.UseSwagger();
app.UseSwaggerUI(options =>
{
	options.SwaggerEndpoint("/swagger/v1/swagger.json", "v1");
	options.RoutePrefix = string.Empty;
});

app.Use(async (context, next) =>
{
	InspectionSetup inDef = app.Services.GetService<IConfigurationService>()!.InspectionDefinitions;
	context.Items["InspectionDefinitions"] = inDef;
	await next();
});

//app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
